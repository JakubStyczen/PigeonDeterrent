from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

from db.db import IDB, MongoDBColletion, IDataBaseRecord, DeterrentDataBaseRecord

logger = logging.getLogger(__name__)


class IDBHandler(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_record(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read_record(self, id: str | None) -> list[IDataBaseRecord] | None:
        raise NotImplementedError

    @abstractmethod
    def update_record(self, id: str, data: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_record(self, id: str) -> None:
        raise NotImplementedError


class MongoDBHandler(IDBHandler):
    def __init__(
        self, ip: str = "localhost", port: int = 27017, uri: Optional[str] = None
    ) -> None:
        self.ip = ip
        self.port = port
        self.uri = uri
        self._db_client: Optional[MongoClient] = None
        self._db: IDB = None
        self.connect()

    def connect(self) -> None:
        if self._db_client is not None:
            logger.warning("MongoDB already connected!")
            return None
        credentials: str = self.uri if self.uri else f"mongodb://{self.ip}:{self.port}"
        self._db_client = MongoClient(credentials)
        self._db_client.admin.command("ping")
        logger.info("Connecting to db!")

    def disconnect(self) -> None:
        if self._db_client is None:
            logger.warning("MongoDB already disconnected!")
            return
        self._db_client = None
        logger.info("Disconnected from db!")

    def create_db_collection(self) -> None:
        if self._db_client is None:
            logger.warning("MongoDB connection has not been established yet!")
            return
        db = self._db_client.flask_database
        self._db = MongoDBColletion(db)
        logger.debug("Created new MongoDB collection")

    def create_record(
        self, timestamp: datetime, sensors_interrupts: Dict[str, bool]
    ) -> None:
        data = DeterrentDataBaseRecord(timestamp, sensors_interrupts)
        self._db.create(data)

    def read_record(self, id: str | None) -> list[IDataBaseRecord] | None:
        return self._db.read(id)

    def read_all_records(self) -> list[IDataBaseRecord] | None:
        return self._db.read()

    def update_record(
        self, id: str, timestamp: datetime, sensors_interrupts: Dict[str, bool]
    ) -> None:
        data = DeterrentDataBaseRecord(timestamp, sensors_interrupts)
        self._db.update(id, data.to_modify())

    def delete_record(self, id: str) -> None:
        self._db.delete(id)
