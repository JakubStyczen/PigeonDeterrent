import os
import logging
from environs import Env
from typing import Optional

class Config:
    def __init__(self) -> None:
        self.env = Env()
        self.env.read_env()
        self.logging_level: Optional[int] = None
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        self.logging_level: int = logging.getLevelName(self.env.str("LOGGING_LEVEL", "INFO"))
        logging.basicConfig(level=self.logging_level, format="[%(levelname)s]:  %(message)s")
        self.logger = logging.getLogger(__name__)
        
    def read_server_variables(self) -> None:
        self.port: int = self.env.int("PORT", 5000)
        self.host: str = self.env.str("HOST_IP", "127.0.0.1")
        self.debug: bool = self.env.bool("DEBUG", False)
        
    def read_mongodb_variables(self) -> None:
        self.db_port: int = self.env.int("DB_PORT", 27017)
        self.db_host: str = self.env.str("DB_HOST_IP", "127.0.0.1")
        self.db_password: str = self.env.bool("MONGODB_PASSWORD", "")
