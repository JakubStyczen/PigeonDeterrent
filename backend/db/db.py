from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
from pymongo.database import Database, Collection
from datetime import datetime

from bson.objectid import ObjectId

DeterrentInfo = Dict[str, bool | datetime]


class IDataBaseRecord(ABC):
    @abstractmethod
    def to_db_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def to_modify(self) -> Dict[str, Any]:
        raise NotImplementedError


class DeterrentDataBaseRecord(IDataBaseRecord):
    def __init__(
        self,
        timestamp: datetime = datetime.now(),
        sensors_interrupts: Dict[str, bool] = {},
    ) -> None:
        self.timestamp = timestamp
        self.sensors_interrupts = sensors_interrupts

    def to_db_dict(self) -> DeterrentInfo:
        return {"Time": self.timestamp, **self.sensors_interrupts}

    def to_modify(self) -> Dict[str, DeterrentInfo]:
        return {"$set": self.to_db_dict()}


class IDB(ABC):
    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> IDataBaseRecord | None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError


class MongoDBColletion(IDB):
    def __init__(self, db: Database) -> None:
        self._db = db
        self._collection: Collection = db.interrupts_collection

    def create(self, data: IDataBaseRecord) -> None:
        self._collection.insert_one(data.to_db_dict())

    def read(self, id: str | None = None) -> list[IDataBaseRecord] | None:
        if id is None:
            data = self._collection.find()
        else:
            data = self._collection.find({"_id": ObjectId(id)})
        return list(data) if data is not None else None

    def delete(self, id: str) -> None:
        self._collection.delete_one({"_id": ObjectId(id)})

    def update(self, id: str, data: Dict[str, DeterrentInfo]) -> None:
        self._collection.update_one({"_id": ObjectId(id)}, data)
