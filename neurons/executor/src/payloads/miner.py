from pydantic import BaseModel
from typing import Optional



class MinerAuthPayload(BaseModel):
    public_key: str
    signature: str
    miner_ip: str ="dummy"
