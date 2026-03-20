from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from log_parser import parse_logs, to_feature_matrix
from detector import AnomalyDetector

app = FastAPI(title="Log Anomaly Detector", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogRequest(BaseModel):
    logs: str
    contamination: float = 0.1  # expected % of anomalies, 0.05–0.5

class LogResult(BaseModel):
    raw: str
    ip: str
    method: str
    path: str
    status_code: int
    response_time: float
    is_anomaly: bool
    anomaly_score: float
    reasons: list[str]

def explain(parsed: dict, result: dict) -> list[str]:
    """Generate human-readable reasons why a log was flagged."""
    reasons = []
    if parsed["response_time"] > 5.0:
        reasons.append(f"High response time: {parsed['response_time']}s")
    if parsed["is_server_error"]:
        reasons.append(f"Server error: HTTP {parsed['status_code']}")
    if parsed["status_code"] == 401:
        reasons.append("Unauthorized access attempt")
    if parsed["status_code"] == 403:
        reasons.append("Forbidden request")
    if parsed["bytes"] == 0:
        reasons.append("Zero bytes returned")
    if result["anomaly_score"] > 0.75 and not reasons:
        reasons.append("Unusual pattern detected by model")
    return reasons

@app.get("/")
def root():
    return {"status": "ok", "message": "Log Anomaly Detector API"}

@app.post("/analyze", response_model=list[LogResult])
def analyze_logs(request: LogRequest):
    if not request.logs.strip():
        raise HTTPException(status_code=400, detail="No logs provided")

    if not (0.01 <= request.contamination <= 0.5):
        raise HTTPException(status_code=400, detail="contamination must be between 0.01 and 0.5")

    parsed = parse_logs(request.logs)
    if len(parsed) < 5:
        raise HTTPException(status_code=400, detail="Need at least 5 valid log lines to detect anomalies")

    df = to_feature_matrix(parsed)
    detector = AnomalyDetector(contamination=request.contamination)
    results = detector.fit_predict(df)

    return [
        LogResult(
            raw=parsed[i]["raw"],
            ip=parsed[i]["ip"],
            method=parsed[i]["method"],
            path=parsed[i]["path"],
            status_code=parsed[i]["status_code"],
            response_time=parsed[i]["response_time"],
            is_anomaly=results[i]["is_anomaly"],
            anomaly_score=results[i]["anomaly_score"],
            reasons=explain(parsed[i], results[i])
        )
        for i in range(len(parsed))
    ]

@app.get("/health")
def health():
    return {"status": "healthy"}