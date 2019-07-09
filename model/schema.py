from model.data_transfer_objects import Tumbleweed, TumbleBase, Run, SubSystem, DataSource, IntData, LongData, FloatData, StringData, ByteData, Command, CommandType, ImageData
from marshmallow import Schema, fields, post_load, post_dump, pre_dump, pre_load
from marshmallow_enum import EnumField
from datetime import datetime, timezone
from model.enums import DType, ImageFormat
import base64


class TumbleweedSchema(Schema):

    id = fields.Int(dump_only=True)

    address = fields.String(allow_none=False, required=True)
    name = fields.String(allow_none=True, required=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def init_model(self, data):
        data["created_at"] = datetime.now(timezone.utc)
        return Tumbleweed(**data)


class TumbleBaseSchema(Schema):

    id = fields.Int(dump_only=True)

    address = fields.String(allow_none=True, required=True)
    name = fields.String(allow_none=False, required=True)
    created_at = fields.DateTime(dump_only=True)
    host = fields.String(allow_none=False, required=True)
    port = fields.Int(allow_none=True, required=True)
    command_route = fields.String(allow_none=True, required=True)

    @post_load
    def init_model(self, data):
        data["created_at"] = datetime.now(timezone.utc)
        return TumbleBase(**data)


class RunSchema(Schema):

    id = fields.Int(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    ended_at = fields.DateTime(dump_only=True)
    name = fields.String(allow_none=True, required=True)
    description = fields.String(allow_none=True, required=True)
    tumbleweed_id = fields.Int(dump_only=True)

    @post_load
    def init_model(self, data):
        data["created_at"] = datetime.now(timezone.utc)
        return Run(**data)


class SubSystemSchema(Schema):

    id = fields.Int(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    name = fields.String(allow_none=False, required=True)
    description = fields.String(allow_none=True, required=True)
    tumbleweed_id = fields.Int(dump_only=True)

    @post_load
    def init_model(self, data):
        data["created_at"] = datetime.now(timezone.utc)
        return SubSystem(**data)


class CommandTypeSchema(Schema):

    id = fields.Int(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    type = fields.String(allow_none=False, required=True)
    description = fields.String(allow_none=True, required=True)

    @post_load
    def init_model(self, data):
        data["created_at"] = datetime.now(timezone.utc)
        return CommandType(**data)


class CommandSchema(Schema):

    id = fields.Int(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    run_id = fields.Int(dump_only=True)
    sender_base_id = fields.Int(dump_only=True)
    command_type_id = fields.Int(dump_only=True)
    args = fields.String(allow_none=True, required=True)
    transmitted = fields.Bool(dump_only=True)
    response = fields.String(allow_none=True, required=True)
    received_response_at = fields.DateTime(allow_none=True, required=True)
    response_message_id = fields.Int(allow_none=True, required=True)

    @post_load
    def init_model(self, data):
        data["created_at"] = datetime.now(timezone.utc)
        return Command(**data)


class DataSourceSchema(Schema):

    id = fields.Int(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    name = fields.String(allow_none=False, required=True)
    description = fields.String(allow_none=True, required=True)
    subsystem_id = fields.Int(dump_only=True, required=True)
    short_key = fields.String(allow_none=False, required=True)
    dtype = EnumField(DType, by_value=True, allow_none=False, required=True)
    type = fields.String(allow_none=True, required=True)

    @post_load
    def init_model(self, data):
        data["created_at"] = datetime.now(timezone.utc)
        return DataSource(**data)


class LongDataSchema(Schema):

    id = fields.Int(dump_only=True)

    data_source_id = fields.Int(dump_only=True)
    run_id = fields.Int(dump_only=True)
    receiving_start = fields.DateTime(allow_none=False, required=True)
    receiving_done = fields.DateTime(allow_none=True, required=True)
    data = fields.Int(allow_none=True, required=True)
    packets = fields.Int(allow_none=False, required=True)
    packets_received = fields.Int(allow_none=False, required=True)
    message_id = fields.Int(allow_none=False, required=True)
    size = fields.Int(dump_only=True)

    @post_dump
    def convert_long_to_str(self, data):
        """javascript cannot handle large integers, so we must convert to a string"""
        if data["data"] is not None:
            data["data"] = str(data["data"])
        return data

    @post_load
    def init_model(self, data):
        return LongData(**data)


class IntDataSchema(Schema):

    id = fields.Int(dump_only=True)

    data_source_id = fields.Int(dump_only=True)
    run_id = fields.Int(dump_only=True)
    receiving_start = fields.DateTime(allow_none=False, required=True)
    receiving_done = fields.DateTime(allow_none=True, required=True)
    data = fields.Int(allow_none=True, required=True)
    packets = fields.Int(allow_none=False, required=True)
    packets_received = fields.Int(allow_none=False, required=True)
    message_id = fields.Int(allow_none=False, required=True)
    size = fields.Int(dump_only=True)

    @post_load
    def init_model(self, data):
        return IntData(**data)


class FloatDataSchema(Schema):

    id = fields.Int(dump_only=True)

    data_source_id = fields.Int(dump_only=True)
    run_id = fields.Int(dump_only=True)
    receiving_start = fields.DateTime(allow_none=False, required=True)
    receiving_done = fields.DateTime(allow_none=True, required=True)
    data = fields.Decimal(allow_none=True, required=True)
    packets = fields.Int(allow_none=False, required=True)
    packets_received = fields.Int(allow_none=False, required=True)
    message_id = fields.Int(allow_none=False, required=True)
    size = fields.Int(dump_only=True)

    @post_load
    def init_model(self, data):
        return FloatData(**data)

    @post_dump
    def convert_from_decimal(self, data):
        if data["data"] is not None:
            data["data"] = float(data["data"])
        return data


class StringDataSchema(Schema):

    id = fields.Int(dump_only=True)

    data_source_id = fields.Int(dump_only=True)
    run_id = fields.Int(dump_only=True)
    receiving_start = fields.DateTime(allow_none=False, required=True)
    receiving_done = fields.DateTime(allow_none=True, required=True)
    data = fields.String(allow_none=True, required=True)
    packets = fields.Int(allow_none=False, required=True)
    packets_received = fields.Int(allow_none=False, required=True)
    message_id = fields.Int(allow_none=False, required=True)
    size = fields.Int(dump_only=True)

    @post_load
    def init_model(self, data):
        return StringData(**data)


class ByteDataSchema(Schema):

    id = fields.Int(dump_only=True)

    data_source_id = fields.Int(dump_only=True)
    run_id = fields.Int(dump_only=True)
    receiving_start = fields.DateTime(allow_none=False, required=True)
    receiving_done = fields.DateTime(allow_none=True, required=True)
    data = fields.String(allow_none=True, required=True)
    packets = fields.Int(allow_none=False, required=True)
    packets_received = fields.Int(allow_none=False, required=True)
    message_id = fields.Int(allow_none=False, required=True)
    size = fields.Int(dump_only=True)

    @post_load
    def convert_base_64(self, data):
        """we cannot send bytestrings via http post requests, so we must convert to a base 64 string and back"""
        if data["data"] is not None:
            to_bytes = data["data"].encode()
            to_bytes = base64.b64decode(to_bytes)
            data["data"] = to_bytes
        return ByteData(**data)

    @pre_dump
    def convert_to_str(self, data):
        if data.data is not None:
            to_string = base64.b64encode(data.data)
            to_string = to_string.decode()
            data.data = to_string
        return data


class ImageDataSchema(Schema):

    id = fields.Int(dump_only=True)

    data_source_id = fields.Int(dump_only=True)
    run_id = fields.Int(dump_only=True)
    receiving_start = fields.DateTime(allow_none=False, required=True)
    receiving_done = fields.DateTime(allow_none=True, required=True)
    data = fields.String(allow_none=True, required=True)
    packets = fields.Int(allow_none=False, required=True)
    packets_received = fields.Int(allow_none=False, required=True)
    message_id = fields.Int(allow_none=False, required=True)
    size = fields.Int(dump_only=True)

    @post_load
    def convert_base_64(self, data):
        """we cannot send bytestrings via http post requests, so we must convert to a base 64 string and back"""
        if data["data"] is not None:
            to_bytes = data["data"].encode()
            to_bytes = base64.b64decode(to_bytes)
            data["data"] = to_bytes
        return ImageData(**data)

    @pre_dump
    def convert_to_str(self, data):
        if data.data is not None:
            to_string = base64.b64encode(data.data)
            to_string = to_string.decode()
            data.data = to_string
        return data
