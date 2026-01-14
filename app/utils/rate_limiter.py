import time
from collections import defaultdict
from fastapi import HTTPException,status


request_log = defaultdict(list)

def rate_limit(
        key : str,
        limit : int,
        window_seconds : int,
):
    

    now = time.time()
    window_start = now - window_seconds

    request_log[key] = [
        t for t in request_log[key]
        if t > window_start
    ]

    if len(request_log[key]) >= limit:
        raise HTTPException(
            status_code= status.HTTP_429_TOO_MANY_REQUESTS,
            detail= "too many requests, slow down."
        )
    
    request_log[key].append(now)