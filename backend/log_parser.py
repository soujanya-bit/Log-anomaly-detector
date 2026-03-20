import re
import pandas as pd
from datetime import datetime

LOG_PATTERN=re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\]'
    r' "(?P<method>\S+) (?P<path>\S+) \S+"'
    r' (?P<status>\d{3}) (?P<bytes>\d+) (?P<response_time>[\d.]+)'
)

METHOD_MAP={"GET": 0, "POST": 1, "PUT": 2, "DELETE": 3, "PATCH": 4}

def parse_line(line:str)->dict |None:
    line=line.strip()
    if not line:
        return None
    match=LOG_PATTERN.match(line)
    if not match:
        return None
    
    d=match.groupdict()
    try:
        dt=datetime.strptime(d['timestamp'], '%d/%b/%Y:%H:%M:%S')
        hour=dt.hour
    except:
        hour=0

    status=int(d['status'])
    return {
        "raw": line,
        "ip": d['ip'],
        "method": d['method'],
        "path": d['path'],
        "status_code": status,
        "bytes": int(d['bytes']),
        "response_time": float(d['response_time']),
        "hour": hour,

        "is_error": 1 if status >= 400 else 0,
        "is_server_error": 1 if status >= 500 else 0,
        "method_code": METHOD_MAP.get(d['method'], 5),
        "path_depth": d['path'].count('/'),
    }

def parse_logs(raw_text: str) -> list[dict]:
    lines = raw_text.strip().splitlines()
    parsed = [parse_line(l) for l in lines]
    return [p for p in parsed if p is not None]

def to_feature_matrix(parsed: list[dict]) -> pd.DataFrame:
    return pd.DataFrame([{
        "response_time": p["response_time"],
        "status_code": p["status_code"],
        "bytes": p["bytes"],
        "hour": p["hour"],
        "is_error": p["is_error"],
        "is_server_error": p["is_server_error"],
        "method_code": p["method_code"],
        "path_depth": p["path_depth"],
    } for p in parsed])