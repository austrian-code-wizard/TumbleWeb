from model.data_access_objects import Tumbleweed, TumbleBase, Run, SubSystem, Command, CommandType, DataSource, LongData, IntData, FloatData, StringData, ByteData, ImageData
from logger.logger import LoggerFactory
from abc import abstractmethod
from util.mode import Mode
from re import findall


class Repository:
    """
    There exists repositories and daos. The difference between these two is a dao builds sql commands and executes them
    on the database like the sqlalchemy orm does for us. A repository uses a dao to store and load data. The better way
    to explain it is with anemic and rich models. Rich models include also data access to the database. Anemic models
    only describe the structure of data in the database. A repository uses a rich model to query and insert data into
    the database. A dao uses a anemic model to create sql commands and communicate with the database. So in this case
    it is a repository with a rich sqlalchemy model.
    """
    def __init__(self, logger, entity_model):
        self._logger = logger
        self.entity_model = entity_model

    def save_entity(self, entity, session):
        entity = session.merge(entity)
        session.commit()
        return entity.id

    def get_entity(self, entity_id, session):
        return session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()

    def get_entities(self, session):
        return session.query(self.entity_model).order_by(self.entity_model.id).all()

    @abstractmethod
    def delete_entity(self, entity_id, session):
        raise NotImplementedError("You called an abstract method!")

    @classmethod
    def get_repository(cls, mode=Mode.productive):
        """
        Instantiate a logger named after the given class. The name of the logger is derived
        from the class name by adding "-" signs between all parts of the camelcased name.
        See https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
        for the respective regular expression. Create and return the instantiated class.
        :param mode: Describes if the application is run in productive or test mode.
        :return: A newly instantiated class that is connected to the logger.
        """
        parts = findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', cls.__name__)
        name = "-".join([s.lower() for s in parts])
        if mode == Mode.productive:
            logger_name = f"{name}-logger"
        if mode == Mode.test:
            logger_name = f"{name}-test-logger"
        logger = LoggerFactory.create_logger(logger_name)
        return cls(logger)


class TumbleweedRepository(Repository):
    """
    A repository for Tumbleweeds.
    """

    def __init__(self, logger):
        super().__init__(logger, Tumbleweed)

    def delete_entity(self, entity_id, session):
        tumbleweed = session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()
        if len(tumbleweed.subsystems) > 0 or len(tumbleweed.data_sources) > 0:
            return None
        for run in tumbleweed.runs:
            for datapoint in run.long_data_points:
                datapoint.run = None
                datapoint.run_id = None
                datapoint.data_source = None
                datapoint.data_source_id = None
                datapoint.tumblebases = []
                session.delete(datapoint)
            for datapoint in run.int_data_points:
                datapoint.run = None
                datapoint.run_id = None
                datapoint.data_source = None
                datapoint.data_source_id = None
                datapoint.tumblebases = []
                session.delete(datapoint)
            for datapoint in run.float_data_points:
                datapoint.run = None
                datapoint.run_id = None
                datapoint.data_source = None
                datapoint.data_source_id = None
                datapoint.tumblebases = []
                session.delete(datapoint)
            for datapoint in run.string_data_points:
                datapoint.run = None
                datapoint.run_id = None
                datapoint.data_source = None
                datapoint.data_source_id = None
                datapoint.tumblebases = []
                session.delete(datapoint)
            for datapoint in run.byte_data_points:
                datapoint.run = None
                datapoint.run_id = None
                datapoint.data_source = None
                datapoint.data_source_id = None
                datapoint.tumblebases = []
                session.delete(datapoint)
            for datapoint in run.image_data_points:
                datapoint.run = None
                datapoint.run_id = None
                datapoint.data_source = None
                datapoint.data_source_id = None
                datapoint.tumblebases = []
                session.delete(datapoint)
            for command in run.commands:
                command.tumbleweed = None
                command.tumbleweed_id = None
                command.run_id = None
                command.run = None
                command.command_type_id = None
                command.command_type = None
                command.sender_base = None
                command.sender_base_id = None
                command.received_from_bases = []
                session.delete(command)
            run.tumbleweed = None
            run.tumbleweed_id = None
            session.delete(run)
        tumbleweed.tumblebases = []
        tumbleweed.data_sources = []
        tumbleweed.subsystems = []
        for command in tumbleweed.commands:
            command.tumbleweed = None
            command.tumbleweed_id = None
            command.run_id = None
            command.run = None
            command.command_type_id = None
            command.command_type = None
            command.sender_base = None
            command.sender_base_id = None
            command.received_from_bases = []
            session.delete(command)
        session.delete(tumbleweed)
        return entity_id

    def get_by_address(self, address, session):
        return session.query(self.entity_model).filter(self.entity_model.address == address).all()


class TumbleBaseRepository(Repository):
    """
    A repository for TumbleBases.
    """

    def __init__(self, logger):
        super().__init__(logger, TumbleBase)

    def delete_entity(self, entity_id, session):
        tumblebase = session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()
        if len(tumblebase.long_data_points) > 0 or len(tumblebase.int_data_points) > 0 or len(
                tumblebase.float_data_points) > 0 or len(tumblebase.string_data_points) > 0 or len(
                tumblebase.byte_data_points) > 0 or len(tumblebase.image_data_points) > 0 or len(
                tumblebase.sent_commands) > 0 or len(tumblebase.received_commands) > 0:
            return None
        tumblebase.tumbleweeds = []
        session.delete(tumblebase)
        return entity_id

    def get_by_address(self, address, session):
        return session.query(self.entity_model).filter(self.entity_model.address == address).first()


class RunRepository(Repository):
    """
    A repository for Runs.
    """

    def __init__(self, logger):
        super().__init__(logger, Run)

    def delete_entity(self, entity_id, session):
        run = session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()
        if run is None:
            return None
        for datapoint in run.long_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in run.int_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in run.float_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in run.string_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in run.byte_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in run.image_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for command in run.commands:
            command.tumbleweed = None
            command.tumbleweed_id = None
            command.run_id = None
            command.run = None
            command.command_type_id = None
            command.command_type = None
            command.sender_base = None
            command.sender_base_id = None
            command.received_from_bases = []
            session.delete(command)
        run.tumbleweed = None
        run.tumbleweed_id = None
        session.delete(run)
        return entity_id


class SubSystemRepository(Repository):
    """
    A repository for SubSystems.
    """

    def __init__(self, logger):
        super().__init__(logger, SubSystem)

    def delete_entity(self, entity_id, session):
        subSystem = session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()
        if len(subSystem.data_sources) > 0:
            return None
        else:
            subSystem.tumbleweed_id = None
            subSystem.tumbleweed = None
            session.delete(subSystem)
            return entity_id

    def get_by_tumbleweed_id(self, tumbleweed_id, session):
        return session.query(self.entity_model).filter(self.entity_model.tumbleweed_id == tumbleweed_id).all()


class CommandTypeRepository(Repository):
    """
    A repository for Command Types.
    """

    def __init__(self, logger):
        super().__init__(logger, CommandType)

    def delete_entity(self, entity_id, session):
        commandType = session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()
        if commandType is None:
            return None
        for command in commandType.commands:
            command.tumbleweed = None
            command.tumbleweed_id = None
            command.run_id = None
            command.run = None
            command.command_type_id = None
            command.command_type = None
            command.sender_base = None
            command.sender_base_id = None
            command.received_from_bases = []
            session.delete(command)
        session.delete(commandType)
        return entity_id


class CommandRepository(Repository):
    """
    A repository for Commands.
    """

    def __init__(self, logger):
        super().__init__(logger, Command)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

    def get_by_commandType_id(self, commandType_id, session):
        return session.query(self.entity_model).filter(self.entity_model.command_type_id == commandType_id).all()

    def get_by_tumbleweed_id_and_run_id(self, tumbleweed_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.tumbleweed_id == tumbleweed_id).filter(self.entity_model.run_id == run_id).all()

    def get_unanswered_by_tumbleweed_id_and_run_id(self, tumbleweed_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.tumbleweed_id == tumbleweed_id).filter(
            self.entity_model.run_id == run_id).filter(self.entity_model.response == None).filter(
            self.entity_model.received_response_at == None).filter(self.entity_model.response_message_id == None).all()


class DataSourceRepository(Repository):
    """
    A repository for byte data sources.
    """

    def __init__(self, logger):
        super().__init__(logger, DataSource)

    def delete_entity(self, entity_id, session):
        dataSource = session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()
        for datapoint in dataSource.long_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in dataSource.int_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in dataSource.float_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in dataSource.string_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in dataSource.byte_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        for datapoint in dataSource.image_data_points:
            datapoint.run = None
            datapoint.run_id = None
            datapoint.data_source = None
            datapoint.data_source_id = None
            datapoint.tumblebases = []
            session.delete(datapoint)
        dataSource.subsystem_id = None
        dataSource.subsystem = None
        dataSource.tumbleweed_id = None
        dataSource.tumbleweed = None
        session.delete(dataSource)
        return entity_id

    def get_dataSources_by_tumbleweed_id(self, tumbleweed_id, session):
        return session.query(self.entity_model).filter(self.entity_model.tumbleweed_id == tumbleweed_id).all()

    def get_dataSource_by_tumbleweed_id_and_short_key(self, tumbleweed_id, short_key, session):
        return session.query(self.entity_model).filter(self.entity_model.tumbleweed_id == tumbleweed_id).filter(
            self.entity_model.short_key == short_key).first()

    def get_by_subSystem_id(self, subSystem_id, session):
        return session.query(self.entity_model).filter(self.entity_model.subsystem_id == subSystem_id).all()


class LongDataRepository(Repository):
    """
    A repository for Long data.
    """

    def __init__(self, logger):
        super().__init__(logger, LongData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

    def get_by_dataSource_id_and_run_id(self, dataSource_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.data_source_id == dataSource_id).filter(self.entity_model.run_id == run_id).all()


class IntDataRepository(Repository):
    """
    A repository for Int data.
    """

    def __init__(self, logger):
        super().__init__(logger, IntData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

    def get_by_dataSource_id_and_run_id(self, dataSource_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.data_source_id == dataSource_id).filter(self.entity_model.run_id == run_id).all()


class FloatDataRepository(Repository):
    """
    A repository for Float data.
    """

    def __init__(self, logger):
        super().__init__(logger, FloatData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

    def get_by_dataSource_id_and_run_id(self, dataSource_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.data_source_id == dataSource_id).filter(self.entity_model.run_id == run_id).all()


class StringDataRepository(Repository):
    """
    A repository for String data.
    """

    def __init__(self, logger):
        super().__init__(logger, StringData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

    def get_by_dataSource_id_and_run_id(self, dataSource_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.data_source_id == dataSource_id).filter(self.entity_model.run_id == run_id).all()


class ByteDataRepository(Repository):
    """
    A repository for Byte data.
    """

    def __init__(self, logger):
        super().__init__(logger, ByteData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

    def get_by_dataSource_id_and_run_id(self, dataSource_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.data_source_id == dataSource_id).filter(self.entity_model.run_id == run_id).all()


class ImageDataRepository(Repository):
    """
    A repository for Byte data.
    """

    def __init__(self, logger):
        super().__init__(logger, ImageData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

    def get_by_dataSource_id_and_run_id(self, dataSource_id, run_id, session):
        return session.query(self.entity_model).filter(self.entity_model.data_source_id == dataSource_id).filter(self.entity_model.run_id == run_id).all()
