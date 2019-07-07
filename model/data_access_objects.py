from sqlalchemy import Column, ForeignKey, Table, Integer, String, Enum, DateTime, Boolean, UniqueConstraint, BigInteger, Float, LargeBinary, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from util.utils import get_config_parser
from sqlalchemy.orm import relationship
from sqlalchemy import func
import fleep
import os
from model.enums import DType, ImageFormat
import uuid


Base = declarative_base()


# Abstract classes 


class BaseWithConverter(Base):
    __abstract__ = True

    # override to_string method
    def __str__(self):
        model_as_string = self.__tablename__ + ": "
        first_line = True
        for column_name in self.__table__.columns.keys():
            column_value = str(getattr(self, column_name))
            if first_line:
                model_as_string += column_name + "=" + column_value
                first_line = False
            else:
                model_as_string += ", " + column_name + "=" + column_value
        model_as_string += ";"
        return model_as_string

    @classmethod
    def create_from_dto(cls, dto):
        dao = cls()
        for key in dto.__dataclass_fields__.keys():
            setattr(dao, key, getattr(dto, key))
        return dao

    @classmethod
    def create_from_dto_list(cls, dto_list):
        dao_list = list()
        for dto in dto_list:
            dao_list.append(cls.create_from_dto(dto))
        return dao_list

class DataPoint(BaseWithConverter):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


# Association tables


tumbleweed_tumblebase = Table('tumbleweed_tumblebase', Base.metadata,
    Column('tumbleweed_id', Integer, ForeignKey('tumbleweed.id')),
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id'))
)

tumblebase_intdata = Table('tumblebase_intdata', Base.metadata,
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id')),
    Column('intdata_id', Integer, ForeignKey('intdata.id'))
)

tumblebase_longdata = Table('tumblebase_longdata', Base.metadata,
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id')),
    Column('longdata_id', Integer, ForeignKey('longdata.id'))
)

tumblebase_floatdata = Table('tumblebase_floatdata', Base.metadata,
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id')),
    Column('floatdata_id', Integer, ForeignKey('floatdata.id'))
)

tumblebase_stringdata = Table('tumblebase_stringdata', Base.metadata,
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id')),
    Column('stringdata_id', Integer, ForeignKey('stringdata.id'))
)

tumblebase_bytedata = Table('tumblebase_bytedata', Base.metadata,
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id')),
    Column('bytedata_id', Integer, ForeignKey('bytedata.id'))
)

tumblebase_imagedata = Table('tumblebase_imagedata', Base.metadata,
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id')),
    Column('imagedata_id', Integer, ForeignKey('imagedata.id'))
)

tumblebase_command = Table('tumblebase_command', Base.metadata,
    Column('tumblebase_id', Integer, ForeignKey('tumblebase.id')),
    Column('command_id', Integer, ForeignKey('command.id'))
) 



# Model classes


class Tumbleweed(BaseWithConverter):
    __tablename__ = "tumbleweed"
    
    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relationships
    tumblebases = relationship("TumbleBase", uselist=True, secondary=tumbleweed_tumblebase, back_populates="tumbleweeds")
    subsystems = relationship("SubSystem", uselist=True, back_populates="tumbleweed")
    data_sources = relationship("DataSource", uselist=True, back_populates="tumbleweed")
    runs = relationship("Run", uselist=True, back_populates="tumbleweed")
    commands = relationship("Command", uselist=True, back_populates="tumbleweed")

    # fields
    address = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    name = Column(String)


class TumbleBase(BaseWithConverter):
    __tablename__ = "tumblebase"

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relationships
    tumbleweeds = relationship("Tumbleweed", uselist=True, secondary=tumbleweed_tumblebase, back_populates="tumblebases")
    int_data_points = relationship("IntData", uselist=True, secondary=tumblebase_intdata, back_populates="tumblebases")
    float_data_points = relationship("FloatData", uselist=True, secondary=tumblebase_floatdata, back_populates="tumblebases")
    long_data_points = relationship("LongData", uselist=True, secondary=tumblebase_longdata, back_populates="tumblebases")
    string_data_points = relationship("StringData", uselist=True, secondary=tumblebase_stringdata, back_populates="tumblebases")
    byte_data_points = relationship("ByteData", uselist=True, secondary=tumblebase_bytedata, back_populates="tumblebases")
    image_data_points = relationship("ImageData", uselist=True, secondary=tumblebase_imagedata, back_populates="tumblebases")
    sent_commands = relationship("Command", uselist=True, back_populates="sender_base")
    received_commands = relationship("Command", uselist=True, secondary=tumblebase_command, back_populates="received_from_bases")

    # fields
    created_at = Column(DateTime(timezone=True), nullable=False)
    address = Column(String, unique=True)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=True)
    command_route = Column(String, nullable=True)


class Run(BaseWithConverter):
    __tablename__ = "run"

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    tumbleweed_id = Column(Integer, ForeignKey('tumbleweed.id'))

    # relationships
    tumbleweed = relationship("Tumbleweed", uselist=False, back_populates="runs")
    commands = relationship("Command", uselist=True, back_populates="run")
    int_data_points = relationship("IntData", uselist=True, back_populates="run")
    long_data_points = relationship("LongData", uselist=True, back_populates="run")
    float_data_points = relationship("FloatData", uselist=True, back_populates="run")
    byte_data_points = relationship("ByteData", uselist=True, back_populates="run")
    string_data_points = relationship("StringData", uselist=True, back_populates="run")
    image_data_points = relationship("ImageData", uselist=True, back_populates="run")

    # fields
    created_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True))
    name = Column(String)
    description = Column(String)


class SubSystem(BaseWithConverter):
    __tablename__ = "subsystem"

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    tumbleweed_id = Column(Integer, ForeignKey('tumbleweed.id'))

    # relationships
    tumbleweed = relationship("Tumbleweed", uselist=False, back_populates="subsystems")
    data_sources = relationship("DataSource", uselist=True, back_populates="subsystem")


    # fields
    created_at = Column(DateTime(timezone=True), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)


class CommandType(BaseWithConverter):
    __tablename__ = "commandtype"

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relationships
    commands = relationship("Command", uselist=True, back_populates="command_type")

    # fields
    created_at = Column(DateTime(timezone=True), nullable=False)
    type = Column(String, nullable=False, unique=True)
    description = Column(String)


class Command(BaseWithConverter):
    __tablename__ = "command"

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign key
    command_type_id = Column(Integer, ForeignKey("commandtype.id"))
    sender_base_id = Column(Integer, ForeignKey("tumblebase.id"))
    tumbleweed_id = Column(Integer, ForeignKey("tumbleweed.id"))
    run_id = Column(Integer, ForeignKey("run.id"))

    # relationships
    command_type = relationship("CommandType", uselist=False, back_populates="commands")
    sender_base = relationship("TumbleBase", uselist=False, back_populates="sent_commands")
    received_from_bases = relationship("TumbleBase", uselist=True, secondary=tumblebase_command, back_populates="received_commands")
    run = relationship("Run", uselist=False, back_populates="commands")
    tumbleweed = relationship("Tumbleweed", uselist=False, back_populates="commands")

    # fields
    created_at = Column(DateTime(timezone=True), nullable=False)
    args = Column(String)
    transmitted = Column(Boolean, nullable=False, default=False)
    response = Column(String)
    received_response_at = Column(DateTime(timezone=True))
    response_message_id = Column(Integer)


class DataSource(BaseWithConverter):
    __tablename__ = "datasource"

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    subsystem_id = Column(Integer, ForeignKey("subsystem.id"))
    tumbleweed_id = Column(Integer, ForeignKey("tumbleweed.id"))

    # relationships
    subsystem = relationship("SubSystem", uselist=False, back_populates="data_sources")
    tumbleweed = relationship("Tumbleweed", uselist=False, back_populates="data_sources")
    long_data_points = relationship("LongData", uselist=True, back_populates="data_source")
    int_data_points = relationship("IntData", uselist=True, back_populates="data_source")
    float_data_points = relationship("FloatData", uselist=True, back_populates="data_source")
    byte_data_points = relationship("ByteData", uselist=True, back_populates="data_source")
    string_data_points = relationship("StringData", uselist=True, back_populates="data_source")
    image_data_points = relationship("ImageData", uselist=True, back_populates="data_source")

    # fields
    created_at = Column(DateTime(timezone=True), nullable=False)
    short_key = Column(String, nullable=False)
    dtype = Column(Enum(DType), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)
    description = Column(String)

    # args
    __table_args__ = (UniqueConstraint('short_key', 'tumbleweed_id', name='_short_key_tumbleweed_id_uc'),)


class LongData(DataPoint):
    __tablename__ = "longdata"

    #primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    data_source_id = Column(Integer, ForeignKey("datasource.id"))
    run_id = Column(Integer, ForeignKey("run.id"))

    # relationships
    tumblebases = relationship("TumbleBase", uselist=True, secondary=tumblebase_longdata, back_populates="long_data_points")
    data_source = relationship("DataSource", uselist=False, back_populates="long_data_points")
    run = relationship("Run", uselist=False, back_populates="long_data_points")

    # fields
    receiving_start = Column(DateTime(timezone=True), nullable=False)
    receiving_done = Column(DateTime(timezone=True))
    data = Column(BigInteger)
    packets = Column(Integer, nullable=False)
    packets_received = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    size = Column(Integer)


class IntData(DataPoint):
    __tablename__ = "intdata"

    #primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    data_source_id = Column(Integer, ForeignKey("datasource.id"))
    run_id = Column(Integer, ForeignKey("run.id"))

    # relationships
    tumblebases = relationship("TumbleBase", uselist=True, secondary=tumblebase_intdata, back_populates="int_data_points")
    data_source = relationship("DataSource", uselist=False, back_populates="int_data_points")
    run = relationship("Run", uselist=False, back_populates="int_data_points")

    # fields
    receiving_start = Column(DateTime(timezone=True), nullable=False)
    receiving_done = Column(DateTime(timezone=True))
    data = Column(Integer)
    packets = Column(Integer, nullable=False)
    packets_received = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    size = Column(Integer)


class FloatData(DataPoint):
    __tablename__ = "floatdata"

    #primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    data_source_id = Column(Integer, ForeignKey("datasource.id"))
    run_id = Column(Integer, ForeignKey("run.id"))

    # relationships
    tumblebases = relationship("TumbleBase", uselist=True, secondary=tumblebase_floatdata, back_populates="float_data_points")
    data_source = relationship("DataSource", uselist=False, back_populates="float_data_points")
    run = relationship("Run", uselist=False, back_populates="float_data_points")

    # fields
    receiving_start = Column(DateTime(timezone=True), nullable=False)
    receiving_done = Column(DateTime(timezone=True))
    data = Column(Float)
    packets = Column(Integer, nullable=False)
    packets_received = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    size = Column(Integer)


class StringData(DataPoint):
    __tablename__ = "stringdata"

    #primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    data_source_id = Column(Integer, ForeignKey("datasource.id"))
    run_id = Column(Integer, ForeignKey("run.id"))

    # relationships
    tumblebases = relationship("TumbleBase", uselist=True, secondary=tumblebase_stringdata, back_populates="string_data_points")
    data_source = relationship("DataSource", uselist=False, back_populates="string_data_points")
    run = relationship("Run", uselist=False, back_populates="string_data_points")

    # fields
    receiving_start = Column(DateTime(timezone=True), nullable=False)
    receiving_done = Column(DateTime(timezone=True))
    data = Column(String)
    packets = Column(Integer, nullable=False)
    packets_received = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    size = Column(Integer)


class ByteData(DataPoint):
    __tablename__ = "bytedata"

    #primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    data_source_id = Column(Integer, ForeignKey("datasource.id"))
    run_id = Column(Integer, ForeignKey("run.id"))

    # relationships
    tumblebases = relationship("TumbleBase", uselist=True, secondary=tumblebase_bytedata, back_populates="byte_data_points")
    data_source = relationship("DataSource", uselist=False, back_populates="byte_data_points")
    run = relationship("Run", uselist=False, back_populates="byte_data_points")

    # fields
    receiving_start = Column(DateTime(timezone=True), nullable=False)
    receiving_done = Column(DateTime(timezone=True))
    data = Column(LargeBinary)
    packets = Column(Integer, nullable=False)
    packets_received = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    size = Column(Integer)


class ImageData(DataPoint):
    __tablename__ = "imagedata"

    #primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # foreign keys
    data_source_id = Column(Integer, ForeignKey("datasource.id"))
    run_id = Column(Integer, ForeignKey("run.id"))

    # relationships
    tumblebases = relationship("TumbleBase", uselist=True, secondary=tumblebase_imagedata, back_populates="image_data_points")
    data_source = relationship("DataSource", uselist=False, back_populates="image_data_points")
    run = relationship("Run", uselist=False, back_populates="image_data_points")

    # fields
    receiving_start = Column(DateTime(timezone=True), nullable=False)
    receiving_done = Column(DateTime(timezone=True))
    data = Column(String)
    packets = Column(Integer, nullable=False)
    packets_received = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    size = Column(Integer)

    def __init__(self):
        super().__init__()
        self.data = None

    @property
    def data(self):
        if self._data is not None:
            return (open(self._data, "rb")).read()
        else:
            return None

    @data.setter
    def data(self, value):
        if isinstance(value, bytes):
            config_parser = get_config_parser("environment.ini")
            path = config_parser["paths"]["images"]
            if not os.path.exists(path):
                os.mkdir(path)
            name = str(uuid.uuid1())
            format = fleep.get(value).extension[0]
            full_path = f"{path}{name}.{format}"
            with open(full_path, "wb+") as f:
                f.write(value)
            self._data = full_path
        elif value is None:
            self._data = None
        else:
            raise TypeError("Must provide bytes as data")




