import json
import bittensor
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import ValidationError

from core.config import settings
from core.logger import _m, get_logger
from payloads.miner import MinerAuthPayload
logger = get_logger(__name__)


class MinerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            body_bytes = await request.body()
            miner_ip = request.client.host
            print(miner_ip)
            # Parse the original payload
            payload_dict = json.loads(body_bytes)
            # Add the miner_ip
            payload_dict['miner_ip'] = miner_ip
            
            # Store both original body and modified payload
            request.state.raw_body = json.dumps(payload_dict).encode()
            request.state.miner_ip = miner_ip
            
            
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Middleware error: {str(e)}")
            return JSONResponse(status_code=500, content=str(e))
