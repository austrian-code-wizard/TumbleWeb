from model.data_access_objects import Tumbleweed, TumbleBase, Run, Command, CommandType, SubSystem, LongDataSource, IntDataSource, FloatDataSource, StringDataSource, ByteDataSource, FloatData, LongData, IntData, StringData, ByteData
from util.utils import internal_server_error_message, get_config_parser
from repositories.repositories import TumbleweedRepository, TumbleBaseRepository, RunRepository, CommandRepository, CommandTypeRepository, SubSystemRepository, LongDataSourceRepository, IntDataSourceRepository, FloatDataSourceRepository, StringDataSourceRepository, ByteDataSourceRepository, LongDataRepository, IntDataRepository, FloatDataRepository, StringDataRepository, ByteDataRepository
from exception.custom_exceptions import TumbleWebException, InternalServerError
from model.data_transfer_objects import Tumbleweed as TumbleweedDTO, TumbleBase as TumbleBaseDTO, Run as RunDTO, Command as CommandDTO, CommandType as CommandTypeDTO, SubSystem as SubSystemDTO, DataSource as DataSourceDTO, LongData as LongDataDTO, IntData as IntDataDTO, FloatData as FloatDataDTO, StringData as StringDataDTO, ByteData as ByteDataDTO
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
        self._longDataSource_repository = None
        self._intDataSource_repository = None 
        self._floatDataSource_repository = None
        self._stringDataSource_repository = None
        self._byteDataSource_repository = None
        self._longData_repository = None
        self._intData_repository = None
        self._floatData_repository = None
        self._stringData_repository = None
        self._byteData_repository = None
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
    def longDataSource_repository(self):
        if self._longDataSource_repository is None:
            self._longDataSource_repository = LongDataSourceRepository.get_repository(self._mode)
        return self._longDataSource_repository

    @property
    def intDataSource_repository(self):
        if self._intDataSource_repository is None:
            self._intDataSource_repository = IntDataSourceRepository.get_repository(self._mode)
        return self._intDataSource_repository

    @property
    def floatDataSource_repository(self):
        if self._floatDataSource_repository is None:
            self._floatDataSource_repository = FloatDataSourceRepository.get_repository(self._mode)
        return self._floatDataSource_repository

    @property
    def stringDataSource_repository(self):
        if self._stringDataSource_repository is None:
            self._stringDataSource_repository = StringDataSourceRepository.get_repository(self._mode)
        return self._stringDataSource_repository

    @property
    def byteDataSource_repository(self):
        if self._byteDataSource_repository is None:
            self._byteDataSource_repository = ByteDataSourceRepository.get_repository(self._mode)
        return self._byteDataSource_repository

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
    def get_tumbleweeds(self, session=None):
        tumbleweeds_dao = self.tumbleweed_repository.get_entities(session)
        if tumbleweeds_dao is not None:
            tumbleweeds_dto = TumbleweedDTO.create_from_dao_list(tumbleweeds_dao)
            return tumbleweeds_dto
        else:
            return None
