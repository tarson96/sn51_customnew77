import sys
import logging
from pathlib import Path
from typing import Annotated
from fastapi import Depends
from core.config import settings
from services.ssh_service import SSHService
from payloads.miner import MinerAuthPayload

logger = logging.getLogger(__name__)


class MinerService:
    def __init__(
        self,
        ssh_service: Annotated[SSHService, Depends(SSHService)],
    ):
        self.ssh_service = ssh_service

    async def upload_ssh_key(self, payload: MinerAuthPayload):
        logger.info(f"Service received payload: {payload}")
        self.ssh_service.add_pubkey_to_host(payload.public_key)
        
        ssh_ports = {
        }
        
        port_mappings = {
            # "103.180.163.187": "[[9006, 60019], [9007, 60023]]"
        }
          
        port_ranges = {
            "185.141.218.121": "9000,9001",
            "185.141.218.3": "9002,9003",
            "185.141.218.179": "9004,9005",
            "185.141.218.181": "9006,9007",
            "185.141.218.198": "9033,9044",
        }

        print("Custom code.....")

        return {
            "ssh_username": self.ssh_service.get_current_os_user(),
            "ssh_port": ssh_ports.get(payload.miner_ip, settings.SSH_PORT),
            "python_path": sys.executable,
            "root_dir": str(Path(__file__).resolve().parents[2]),
            "port_range": port_ranges.get(payload.miner_ip, settings.RENTING_PORT_RANGE),
            "port_mappings": port_mappings.get(payload.miner_ip,settings.RENTING_PORT_MAPPINGS)  # Return the mappings instead
        }

    async def remove_ssh_key(self, paylod: MinerAuthPayload):
        return self.ssh_service.remove_pubkey_from_host(paylod.public_key)
