import json
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from services.miner_service import MinerService
from payloads.miner import MinerAuthPayload
apis_router = APIRouter()


@apis_router.post("/upload_ssh_key")
async def upload_ssh_key(
    request: Request,
    miner_service: Annotated[MinerService, Depends(MinerService)]
):
    # Get the modified body from state
    body = json.loads(request.state.raw_body)
    payload = MinerAuthPayload(**body)
    return await miner_service.upload_ssh_key(payload)

@apis_router.post("/remove_ssh_key")
async def remove_ssh_key(
    request: Request,
    miner_service: Annotated[MinerService, Depends(MinerService)]
):
    body = json.loads(request.state.raw_body)
    payload = MinerAuthPayload(**body)
    return await miner_service.remove_ssh_key(payload)