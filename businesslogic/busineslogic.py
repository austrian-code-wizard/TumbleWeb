from model.data_access_objects import Tumbleweed, TumbleBase, Run, Command, CommandType, SubSystem, DataSource, FloatData, LongData, IntData, StringData, ByteData, ImageData
from util.utils import internal_server_error_message, get_config_parser
from repositories.repositories import TumbleweedRepository, TumbleBaseRepository, RunRepository, CommandRepository, CommandTypeRepository, SubSystemRepository, DataSourceRepository, LongDataRepository, IntDataRepository, FloatDataRepository, StringDataRepository, ByteDataRepository, ImageDataRepository
from exception.custom_exceptions import TumbleWebException, InternalServerError
from model.data_transfer_objects import Tumbleweed as TumbleweedDTO, TumbleBase as TumbleBaseDTO, Run as RunDTO, Command as CommandDTO, CommandType as CommandTypeDTO, SubSystem as SubSystemDTO, DataSource as DataSourceDTO, LongData as LongDataDTO, IntData as IntDataDTO, FloatData as FloatDataDTO, StringData as StringDataDTO, ByteData as ByteDataDTO, ImageData as ImageDataDTO
from database.database import DatabaseConnector
from logger.logger import LoggerFactory
from abc import abstractmethod
from functools import wraps
from util.mode import Mode


def execute_in_session(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            business_logic = args[0]
            session = business_logic._database_connector.session
            kwargs["session"] = session

            # execute the method which needs the session
            result = func(*args, **kwargs)

            session.commit()
            return result
        except TumbleWebException as e:
            session.rollback()
            raise e
        except Exception as e:
            business_logic._logger.error(business_logic.__class__.__name__ + "." + func.__name__ + "(): " + str(e))
            session.rollback()
            raise InternalServerError(internal_server_error_message)
        finally:
            session.close()
    return wrapper


class BusinessLogic:

    def __init__(self, database_connector, logger, mode):
        self._database_connector = database_connector
        self._logger = logger
        self._mode = mode

    @staticmethod
    @abstractmethod
    def get_business_logic():
        raise NotImplementedError("You called an abstract method!")


# TODO: Restructuring business logic. Methods have to be moved into separate classes.
class TumbleWebLogic(BusinessLogic):

    def __init__(self, database_connector, logger, mode):
        super().__init__(database_connector, logger, mode)
        self._tumbleBase_repository = None
        self._tumbleweed_repository = None
        self._run_repository = None
        self._command_repository = None
        self._commandType_repository = None
        self._subSystem_repository = None
        self._dataSource_repository = None
        self._longData_repository = None
        self._intData_repository = None
        self._floatData_repository = None
        self._stringData_repository = None
        self._byteData_repository = None
        self._imageData_repository = None
        self._secret_key = None

    @property
    def tumbleweed_repository(self):
        if self._tumbleweed_repository is None:
            self._tumbleweed_repository = TumbleweedRepository.get_repository(self._mode)
        return self._tumbleweed_repository

    @property
    def tumbleBase_repository(self):
        if self._tumbleBase_repository is None:
            self._tumbleBase_repository = TumbleBaseRepository.get_repository(self._mode)
        return self._tumbleBase_repository

    @property
    def run_repository(self):
        if self._run_repository is None:
            self._run_repository = RunRepository.get_repository(self._mode)
        return self._run_repository

    @property
    def command_repository(self):
        if self._command_repository is None:
            self._command_repository = CommandRepository.get_repository(self._mode)
        return self._command_repository

    @property
    def commandType_repository(self):
        if self._commandType_repository is None:
            self._commandType_repository = CommandTypeRepository.get_repository(self._mode)
        return self._commandType_repository

    @property
    def subSystem_repository(self):
        if self._subSystem_repository is None:
            self._subSystem_repository = SubSystemRepository.get_repository(self._mode)
        return self._subSystem_repository

    @property
    def dataSource_repository(self):
        if self._dataSource_repository is None:
            self._dataSource_repository = DataSourceRepository.get_repository(self._mode)
        return self._dataSource_repository

    @property
    def longData_repository(self):
        if self._longData_repository is None:
            self._longData_repository = LongDataRepository.get_repository(self._mode)
        return self._longData_repository

    @property
    def intData_repository(self):
        if self._intData_repository is None:
            self._intData_repository = IntDataRepository.get_repository(self._mode)
        return self._intData_repository

    @property
    def floatData_repository(self):
        if self._floatData_repository is None:
            self._floatData_repository = FloatDataRepository.get_repository(self._mode)
        return self._floatData_repository

    @property
    def stringData_repository(self):
        if self._stringData_repository is None:
            self._stringData_repository = StringDataRepository.get_repository(self._mode)
        return self._stringData_repository

    @property
    def byteData_repository(self):
        if self._byteData_repository is None:
            self._byteData_repository = ByteDataRepository.get_repository(self._mode)
        return self._byteData_repository

    @property
    def imageData_repository(self):
        if self._imageData_repository is None:
            self._imageData_repository = ImageDataRepository.get_repository(self._mode)
        return self._imageData_repository

    @property
    def secret_key(self):
        if self._secret_key is None:
            environment_parser = get_config_parser("environment.ini")
            self._secret_key = environment_parser["environment"]["secret_key"]
        return self._secret_key

    @staticmethod
    def get_business_logic(mode=Mode.productive):
        database_connector = DatabaseConnector()
        database_connector.connection_string = DatabaseConnector.get_connection_string(mode=mode)
        if mode == Mode.productive:
            logger_name = "tumbleweb-business-logic-logger"
        elif mode == Mode.test:
            logger_name = "tumbleweb-business-logic-test-logger"
        logger = LoggerFactory.create_logger(logger_name)
        return TumbleWebLogic(database_connector, logger, mode)


    @execute_in_session
    def save_tumbleweed(self, tumbleweed_dto, session=None):
        tumbleweed_dao = Tumbleweed.create_from_dto(tumbleweed_dto)
        tumbleweed_id = self.tumbleweed_repository.save_entity(tumbleweed_dao, session)
        return tumbleweed_id

    @execute_in_session
    def save_tumblebase(self, tumblebase_dto, session=None):
        tumblebase_dao = TumbleBase.create_from_dto(tumblebase_dto)
        tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
        return tumblebase_id

    @execute_in_session
    def save_subSystem(self, subSystem_dto, session=None):
        subSystem_dao = SubSystem.create_from_dto(subSystem_dto)
        subSystem_id = self.subSystem_repository.save_entity(subSystem_dao, session)
        return subSystem_id

    @execute_in_session
    def save_dataSource(self, dataSource_dto, session=None):
        dataSource_dao = DataSource.create_from_dto(dataSource_dto)
        dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
        return dataSource_id

    @execute_in_session
    def save_commandType(self, commandType_dto, session=None):
        commandType_dao = CommandType.create_from_dto(commandType_dto)
        commandType_id = self.commandType_repository.save_entity(commandType_dao, session)
        return commandType_id

    @execute_in_session
    def add_subSystem_to_tumbleweed(self, subSystem_id, tumbleweed_id, session=None):
        subSystem_dao = self.subSystem_repository.get_entity(subSystem_id, session)
        tumbleweed_dao = self.tumbleweed_repository.get_entity(tumbleweed_id, session)
        if subSystem_dao is not None and tumbleweed_dao is not None:
            tumbleweed_dao.subsystems.append(subSystem_dao)
            tumbleweed_id = self.tumbleweed_repository.save_entity(tumbleweed_dao, session)
            return tumbleweed_id
        else:
            return None

    @execute_in_session
    def get_tumbleweeds(self, session=None):
        tumbleweeds_dao = self.tumbleweed_repository.get_entities(session)
        if tumbleweeds_dao is not None:
            tumbleweeds_dto = TumbleweedDTO.create_from_dao_list(tumbleweeds_dao)
            return tumbleweeds_dto
        else:
            return None
