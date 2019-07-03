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
    address: str = None
    name: str = None
    created_at: datetime = None


@dataclass
class TumbleBase(BaseClass):

    # attributes
    created_at: datetime = None
    address: str = None
    name: str = None
    host: str = None
    port: int = None
    command_route: str = None


@dataclass
class Run(BaseClass):

    # attributes
    created_at: datetime = None
    ended_at: datetime = None
    name: str = None
    description: str = None
    tumbleweed_id: int = None


@dataclass
class SubSystem(BaseClass):

    # attributes
    tumbleweed_id: int = None
    created_at: datetime = None
    name: str = None
    description: str = None


@dataclass
class CommandType(BaseClass):

    # attributes
    tumbleweed_id: int = None
    created_at: datetime = None
    type: str = None
    description: str = None


@dataclass
class Command(BaseClass):

    # attributes
    created_at: datetime = None
    run_id: int = None
    sender_base_id: int = None
    command_type_id: int = None
    args: str = None
    transmitted: bool = None
    response: str = None
    received_response_at: datetime = None
    response_message_id: int = None


@dataclass
class DataSource(BaseClass):

    # attributes
    subsystem_id: int = None
    created_at: datetime = None
    short_key: str = None
    dtype: str = None
    name: str = None
    type: str = None
    description: str = None


@dataclass
class LongData(BaseClass):

    # attributes
    data_source_id: int = None
    run_id: int = None
    receiving_start: datetime = None
    receiving_done: datetime = None
    data: int = None
    packets: int = None
    packets_received: int = None
    message_id: int = None
    size: int = None


@dataclass
class IntData(BaseClass):

    # attributes
    data_source_id: int = None
    run_id: int = None
    receiving_start: datetime = None
    receiving_done: datetime = None
    data: int = None
    packets: int = None
    packets_received: int = None
    message_id: int = None
    size: int = None


@dataclass
class FloatData(BaseClass):

    # attributes
    data_source_id: int = None
    run_id: int = None
    receiving_start: datetime = None
    receiving_done: datetime = None
    data: float = None
    packets: int = None
    packets_received: int = None
    message_id: int = None
    size: int = None


@dataclass
class StringData(BaseClass):

    # attributes
    data_source_id: int = None
    run_id: int = None
    receiving_start: datetime = None
    receiving_done: datetime = None
    data: str = None
    packets: int = None
    packets_received: int = None
    message_id: int = None
    size: int = None


@dataclass
class ByteData(BaseClass):

    # attributes
    data_source_id: int = None
    run_id: int = None
    receiving_start: datetime = None
    receiving_done: datetime = None
    data: bytes = None
    packets: int = None
    packets_received: int = None
    message_id: int = None
    size: int = None



