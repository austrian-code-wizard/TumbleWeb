from model.data_access_objects import Tumbleweed, TumbleBase, Run, SubSystem, Command, CommandType, LongDataSource, IntDataSource, FloatDataSource, StringDataSource, ByteDataSource, LongData, IntData, FloatData, StringData, ByteData
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
        raise NotImplementedError("Not available!")


class TumbleBaseRepository(Repository):
    """
    A repository for TumbleBases.
    """

    def __init__(self, logger):
        super().__init__(logger, TumbleBase)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class RunRepository(Repository):
    """
    A repository for Runs.
    """

    def __init__(self, logger):
        super().__init__(logger, Run)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class SubSystemRepository(Repository):
    """
    A repository for SubSystems.
    """

    def __init__(self, logger):
        super().__init__(logger, SubSystem)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class CommandTypeRepository(Repository):
    """
    A repository for Command Types.
    """

    def __init__(self, logger):
        super().__init__(logger, CommandType)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class CommandRepository(Repository):
    """
    A repository for Commands.
    """

    def __init__(self, logger):
        super().__init__(logger, Command)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class LongDataSourceRepository(Repository):
    """
    A repository for Long data sources.
    """

    def __init__(self, logger):
        super().__init__(logger, LongDataSource)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class IntDataSourceRepository(Repository):
    """
    A repository for Int data sources.
    """

    def __init__(self, logger):
        super().__init__(logger, IntDataSource)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class FloatDataSourceRepository(Repository):
    """
    A repository for Float data sources.
    """

    def __init__(self, logger):
        super().__init__(logger, FloatDataSource)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class StringDataSourceRepository(Repository):
    """
    A repository for String data sources.
    """

    def __init__(self, logger):
        super().__init__(logger, StringDataSource)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class ByteDataSourceRepository(Repository):
    """
    A repository for byte data sources.
    """

    def __init__(self, logger):
        super().__init__(logger, ByteDataSource)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class LongDataRepository(Repository):
    """
    A repository for Long data.
    """

    def __init__(self, logger):
        super().__init__(logger, LongData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class IntDataRepository(Repository):
    """
    A repository for Int data.
    """

    def __init__(self, logger):
        super().__init__(logger, IntData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class FloatDataRepository(Repository):
    """
    A repository for Float data.
    """

    def __init__(self, logger):
        super().__init__(logger, FloatData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class StringDataRepository(Repository):
    """
    A repository for String data.
    """

    def __init__(self, logger):
        super().__init__(logger, StringData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class ByteDataRepository(Repository):
    """
    A repository for Byte data.
    """

    def __init__(self, logger):
        super().__init__(logger, ByteData)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")
