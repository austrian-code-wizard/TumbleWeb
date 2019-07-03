from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseClass:

    # primary key
    id: int = None

    # override to_string method
    def __str__(self):
        model_as_string = self.__class__.__name__ + ": "
        first_line = True
        for field_name in self.__dataclass_fields__.keys():
            column_value = str(getattr(self, field_name))
            if first_line:
                model_as_string += field_name + "=" + column_value
                first_line = False
            else:
                model_as_string += ", " + field_name + "=" + column_value
        model_as_string += ";"
        return model_as_string

    @classmethod
    def create_from_dao(cls, dao):
        dto = cls()
        for column_name in dao.__table__.columns.keys():
            setattr(dto, column_name, getattr(dao, column_name))
        return dto

    @classmethod
    def create_from_dao_list(cls, dao_list):
        dto_list = list()
        for dao in dao_list:
            dto_list.append(cls.create_from_dao(dao))
        return dto_list


@dataclass
class Tumbleweed(BaseClass):

    # attributes
    id: int
    address: str
    name: str
    created_at: datetime


@dataclass
class TumbleBase(BaseClass):

    # attributes
    id: int
    created_at: datetime
    address: str
    name: str
    host: str
    port: int
    command_route: str


@dataclass
class Run(BaseClass):

    # attributes
    id: int
    created_at: datetime
    ended_at: datetime
    name: str
    description: str
    tumbleweed_id: int


@dataclass
class SubSystem(BaseClass):

    # attributes
    id: int
    tumbleweed_id: int
    created_at: datetime
    name: str
    description: str


@dataclass
class CommandType(BaseClass):

    # attributes
    id: int
    tumbleweed_id: int
    created_at: datetime
    type: str
    description: str


@dataclass
class Command(BaseClass):

    # attributes
    id: int
    created_at: datetime
    run_id: int
    sender_base_id: int
    command_type_id: int
    args: str
    transmitted: bool
    response: str
    received_response_at: datetime
    response_message_id: int


@dataclass
class DataSource(BaseClass):

    # attributes
    id: int
    subsystem_id: int
    created_at: datetime
    short_key: str
    dtype: str
    name: str
    type: str
    description: str


@dataclass
class LongData(BaseClass):

    # attributes
    id: int
    data_source_id: int
    run_id: int
    receiving_start: datetime
    receiving_done: datetime
    data: int
    packets: int
    packets_received: int
    message_id: int
    size: int


@dataclass
class IntData(BaseClass):

    # attributes
    id: int
    data_source_id: int
    run_id: int
    receiving_start: datetime
    receiving_done: datetime
    data: int
    packets: int
    packets_received: int
    message_id: int
    size: int


@dataclass
class FloatData(BaseClass):

    # attributes
    id: int
    data_source_id: int
    run_id: int
    receiving_start: datetime
    receiving_done: datetime
    data: float
    packets: int
    packets_received: int
    message_id: int
    size: int


@dataclass
class StringData(BaseClass):

    # attributes
    id: int
    data_source_id: int
    run_id: int
    receiving_start: datetime
    receiving_done: datetime
    data: str
    packets: int
    packets_received: int
    message_id: int
    size: int


@dataclass
class ByteData(BaseClass):

    # attributes
    id: int
    data_source_id: int
    run_id: int
    receiving_start: datetime
    receiving_done: datetime
    data: bytes
    packets: int
    packets_received: int
    message_id: int
    size: int


