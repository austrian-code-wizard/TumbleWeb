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

    """ Methods to save resources """

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
    def save_command(self, command_dto, session=None):
        command_dao = Command.create_from_dto(command_dto)
        command_id = self.command_repository.save_entity(command_dao, session)
        return command_id

    @execute_in_session
    def save_LongData(self, dataPoint_dto, session=None):
        dataPoint_dao = LongData.create_from_dto(dataPoint_dto)
        dataPoint_id = self.longData_repository.save_entity(dataPoint_dao, session)
        return dataPoint_id

    @execute_in_session
    def save_FloatData(self, dataPoint_dto, session=None):
        dataPoint_dao = FloatData.create_from_dto(dataPoint_dto)
        dataPoint_id = self.floatData_repository.save_entity(dataPoint_dao, session)
        return dataPoint_id

    @execute_in_session
    def save_IntData(self, dataPoint_dto, session=None):
        dataPoint_dao = IntData.create_from_dto(dataPoint_dto)
        dataPoint_id = self.intData_repository.save_entity(dataPoint_dao, session)
        return dataPoint_id

    @execute_in_session
    def save_StringData(self, dataPoint_dto, session=None):
        dataPoint_dao = StringData.create_from_dto(dataPoint_dto)
        dataPoint_id = self.stringData_repository.save_entity(dataPoint_dao, session)
        return dataPoint_id

    @execute_in_session
    def save_ByteData(self, dataPoint_dto, session=None):
        dataPoint_dao = ByteData.create_from_dto(dataPoint_dto)
        dataPoint_id = self.byteData_repository.save_entity(dataPoint_dao, session)
        return dataPoint_id

    @execute_in_session
    def save_ImageData(self, dataPoint_dto, session=None):
        dataPoint_dao = ImageData.create_from_dto(dataPoint_dto)
        dataPoint_id = self.imageData_repository.save_entity(dataPoint_dao, session)
        return dataPoint_id

    @execute_in_session
    def start_run(self, run_dto, tumbleweed_id, session=None):
        run_dao = Run.create_from_dto(run_dto)
        tumbleweed_dao = self.tumbleweed_repository.get_entity(tumbleweed_id, session)
        tumbleweed_dao.runs.append(run_dao)
        tumbleweed_id = self.tumbleweed_repository.save_entity(tumbleweed_dao, session)
        run_id = self.run_repository.save_entity(run_dao, session)
        return run_id

    """ Methods to link resources """

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
    def add_dataSource_to_subSystem(self, dataSource_id, subSystem_id, session=None):
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        subSystem_dao = self.subSystem_repository.get_entity(subSystem_id, session)
        if dataSource_dao is not None and subSystem_dao is not None:
            subSystem_dao.data_sources.append(dataSource_dao)
            subSystem_id = self.subSystem_repository.save_entity(subSystem_dao, session)
            return subSystem_id
        else:
            return None

    @execute_in_session
    def add_dataSource_to_tumbleweed(self, dataSource_id, tumbleweed_id, session=None):
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        tumbleweed_dao = self.tumbleweed_repository.get_entity(tumbleweed_id, session)
        if dataSource_dao is not None and tumbleweed_dao is not None:
            tumbleweed_dao.data_sources.append(dataSource_dao)
            tumbleweed_id = self.tumbleweed_repository.save_entity(tumbleweed_dao, session)
            return tumbleweed_id
        else:
            return None

    @execute_in_session
    def add_command_to_tumbleweed(self, command_id, tumbleweed_id, session=None):
        command_dao = self.command_repository.get_entity(command_id, session)
        tumbleweed_dao = self.tumbleweed_repository.get_entity(tumbleweed_id, session)
        if command_dao is not None and tumbleweed_dao is not None:
            tumbleweed_dao.commands.append(command_dao)
            tumbleweed_id = self.tumbleweed_repository.save_entity(tumbleweed_dao, session)
            return tumbleweed_id
        else:
            return None

    @execute_in_session
    def add_command_to_tumblebase(self, command_id, tumblebase_id, session=None):
        command_dao = self.command_repository.get_entity(command_id, session)
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if command_dao is not None and tumblebase_dao is not None:
            tumblebase_dao.sent_commands.append(command_dao)
            tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
            return tumblebase_id
        else:
            return None

    @execute_in_session
    def add_command_to_commandType(self, command_id, commandType_id, session=None):
        command_dao = self.command_repository.get_entity(command_id, session)
        commandType_dao = self.commandType_repository.get_entity(commandType_id, session)
        if command_dao is not None and commandType_dao is not None:
            commandType_dao.commands.append(command_dao)
            commandType_id = self.commandType_repository.save_entity(commandType_dao, session)
            return commandType_id
        else:
            return None

    @execute_in_session
    def add_command_to_run(self, command_id, run_id, session=None):
        command_dao = self.command_repository.get_entity(command_id, session)
        run_dao = self.run_repository.get_entity(run_id, session)
        if command_dao is not None and run_id is not None:
            run_dao.commands.append(command_dao)
            run_id = self.run_repository.save_entity(run_dao, session)
            return run_id
        else:
            return None

    @execute_in_session
    def add_LongData_to_dataSource(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.longData_repository.get_entity(datapoint_id, session)
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and dataSource_dao is not None:
            dataSource_dao.long_data_points.append(datapoint_dao)
            dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
            return dataSource_id
        else:
            return None

    @execute_in_session
    def add_IntData_to_dataSource(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.intData_repository.get_entity(datapoint_id, session)
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and dataSource_dao is not None:
            dataSource_dao.int_data_points.append(datapoint_dao)
            dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
            return dataSource_id
        else:
            return None

    @execute_in_session
    def add_FloatData_to_dataSource(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.floatData_repository.get_entity(datapoint_id, session)
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and dataSource_dao is not None:
            dataSource_dao.float_data_points.append(datapoint_dao)
            dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
            return dataSource_id
        else:
            return None

    @execute_in_session
    def add_StringData_to_dataSource(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.stringData_repository.get_entity(datapoint_id, session)
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and dataSource_dao is not None:
            dataSource_dao.string_data_points.append(datapoint_dao)
            dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
            return dataSource_id
        else:
            return None

    @execute_in_session
    def add_ByteData_to_dataSource(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.byteData_repository.get_entity(datapoint_id, session)
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and dataSource_dao is not None:
            dataSource_dao.byte_data_points.append(datapoint_dao)
            dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
            return dataSource_id
        else:
            return None

    @execute_in_session
    def add_ImageData_to_dataSource(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.imageData_repository.get_entity(datapoint_id, session)
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and dataSource_dao is not None:
            dataSource_dao.image_data_points.append(datapoint_dao)
            dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
            return dataSource_id
        else:
            return None

    @execute_in_session
    def add_IntData_to_run(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.intData_repository.get_entity(datapoint_id, session)
        run_dao = self.run_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and run_dao is not None:
            run_dao.int_data_points.append(datapoint_dao)
            run_id = self.run_repository.save_entity(run_dao, session)
            return run_id
        else:
            return None

    @execute_in_session
    def add_FloatData_to_run(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.floatData_repository.get_entity(datapoint_id, session)
        run_dao = self.run_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and run_dao is not None:
            run_dao.float_data_points.append(datapoint_dao)
            run_id = self.run_repository.save_entity(run_dao, session)
            return run_id
        else:
            return None

    @execute_in_session
    def add_StringData_to_run(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.stringData_repository.get_entity(datapoint_id, session)
        run_dao = self.run_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and run_dao is not None:
            run_dao.string_data_points.append(datapoint_dao)
            run_id = self.run_repository.save_entity(run_dao, session)
            return run_id
        else:
            return None

    @execute_in_session
    def add_ByteData_to_run(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.byteData_repository.get_entity(datapoint_id, session)
        run_dao = self.run_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and run_dao is not None:
            run_dao.byte_data_points.append(datapoint_dao)
            run_id = self.run_repository.save_entity(run_dao, session)
            return run_id
        else:
            return None

    @execute_in_session
    def add_ImageData_to_run(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.imageData_repository.get_entity(datapoint_id, session)
        run_dao = self.run_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and run_dao is not None:
            run_dao.image_data_points.append(datapoint_dao)
            run_id = self.run_repository.save_entity(run_dao, session)
            return run_id
        else:
            return None

    @execute_in_session
    def add_LongData_to_run(self, datapoint_id, dataSource_id, session=None):
        datapoint_dao = self.longData_repository.get_entity(datapoint_id, session)
        run_dao = self.run_repository.get_entity(dataSource_id, session)
        if datapoint_dao is not None and run_dao is not None:
            run_dao.long_data_points.append(datapoint_dao)
            run_id = self.run_repository.save_entity(run_dao, session)
            return run_id
        else:
            return None

    @execute_in_session
    def add_LongData_to_tumblebase(self, datapoint_id, tumblebase_id, session=None):
        datapoint_dao = self.longData_repository.get_entity(datapoint_id, session)
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if datapoint_dao is not None and tumblebase_dao is not None:
            tumblebase_dao.long_data_points.append(datapoint_dao)
            tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
            return tumblebase_id
        else:
            return None

    @execute_in_session
    def add_IntData_to_tumblebase(self, datapoint_id, tumblebase_id, session=None):
        datapoint_dao = self.intData_repository.get_entity(datapoint_id, session)
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if datapoint_dao is not None and tumblebase_dao is not None:
            tumblebase_dao.int_data_points.append(datapoint_dao)
            tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
            return tumblebase_id
        else:
            return None

    @execute_in_session
    def add_FloatData_to_tumblebase(self, datapoint_id, tumblebase_id, session=None):
        datapoint_dao = self.floatData_repository.get_entity(datapoint_id, session)
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if datapoint_dao is not None and tumblebase_dao is not None:
            tumblebase_dao.float_data_points.append(datapoint_dao)
            tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
            return tumblebase_id
        else:
            return None

    @execute_in_session
    def add_StringData_to_tumblebase(self, datapoint_id, tumblebase_id, session=None):
        datapoint_dao = self.stringData_repository.get_entity(datapoint_id, session)
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if datapoint_dao is not None and tumblebase_dao is not None:
            tumblebase_dao.string_data_points.append(datapoint_dao)
            tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
            return tumblebase_id
        else:
            return None

    @execute_in_session
    def add_ByteData_to_tumblebase(self, datapoint_id, tumblebase_id, session=None):
        datapoint_dao = self.byteData_repository.get_entity(datapoint_id, session)
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if datapoint_dao is not None and tumblebase_dao is not None:
            tumblebase_dao.byte_data_points.append(datapoint_dao)
            tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
            return tumblebase_id
        else:
            return None

    @execute_in_session
    def add_ImageData_to_tumblebase(self, datapoint_id, tumblebase_id, session=None):
        datapoint_dao = self.imageData_repository.get_entity(datapoint_id, session)
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if datapoint_dao is not None and tumblebase_dao is not None:
            tumblebase_dao.image_data_points.append(datapoint_dao)
            tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
            return tumblebase_id
        else:
            return None

    """ Methods to get resources"""

    @execute_in_session
    def get_active_run(self, tumbleweed_id, session=None):
        tumbleweed_dao = self.tumbleweed_repository.get_entity(tumbleweed_id, session)
        if len(tumbleweed_dao.runs) == 0:
            return None
        runs = tumbleweed_dao.runs.copy()
        runs.sort(key=lambda run: run.created_at, reverse=True)
        most_recent_run = runs[0]
        if most_recent_run.ended_at is None:
            return RunDTO.create_from_dao(most_recent_run)
        else:
            return None

    @execute_in_session
    def get_tumbleweed(self, tumbleweed_id, session=None):
        tumbleweed_dao = self.tumbleweed_repository.get_entity(tumbleweed_id, session)
        if tumbleweed_dao is not None:
            tumbleweed_dto = TumbleweedDTO.create_from_dao(tumbleweed_dao)
            return tumbleweed_dto
        else:
            return None

    @execute_in_session
    def get_tumblebase(self, tumblebase_id, session=None):
        tumblebase_dao = self.tumbleBase_repository.get_entity(tumblebase_id, session)
        if tumblebase_dao is not None:
            tumblebase_dto = TumbleBaseDTO.create_from_dao(tumblebase_dao)
            return tumblebase_dto
        else:
            return None

    @execute_in_session
    def get_subSystem(self, subSystem_id, session=None):
        subSystem_dao = self.subSystem_repository.get_entity(subSystem_id, session)
        if subSystem_dao is not None:
            subSystem_dto = SubSystemDTO.create_from_dao(subSystem_dao)
            return subSystem_dto
        else:
            return None

    @execute_in_session
    def get_command(self, command_id, session=None):
        command_dao = self.command_repository.get_entity(command_id, session)
        if command_dao is not None:
            command_dto = CommandDTO.create_from_dao(command_dao)
            return command_dto
        else:
            return None

    @execute_in_session
    def get_commandType(self, commandType_id, session=None):
        commandType_dao = self.commandType_repository.get_entity(commandType_id, session)
        if commandType_dao is not None:
            commandType_dto = CommandTypeDTO.create_from_dao(commandType_dao)
            return commandType_dto
        else:
            return None

    @execute_in_session
    def get_dataSource(self, dataSource_id, session=None):
        dataSource_dao = self.dataSource_repository.get_entity(dataSource_id, session)
        if dataSource_dao is not None:
            dataSource_dto = DataSourceDTO.create_from_dao(dataSource_dao)
            return dataSource_dto
        else:
            return None

    @execute_in_session
    def get_run(self, run_id, session=None):
        run_dao = self.run_repository.get_entity(run_id, session)
        if run_dao is not None:
            run_dto = RunDTO.create_from_dao(run_dao)
            return run_dto
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

    @execute_in_session
    def get_tumblebases(self, session=None):
        tumblebases_dao = self.tumbleBase_repository.get_entities(session)
        if tumblebases_dao is not None:
            tumblebases_dto = TumbleBaseDTO.create_from_dao_list(tumblebases_dao)
            return tumblebases_dto
        else:
            return None

    @execute_in_session
    def get_commandTypes(self, session=None):
        commandTypes_dao = self.commandType_repository.get_entities(session)
        if commandTypes_dao is not None:
            commandTypes_dto = CommandDTO.create_from_dao_list(commandTypes_dao)
            return commandTypes_dto
        else:
            return None

    @execute_in_session
    def get_subSystems_by_tumbleweed_id(self, tumbleweed_id, session=None):
        subSystems_dao = self.subSystem_repository.get_by_tumbleweed_id(tumbleweed_id, session)
        if subSystems_dao is not None:
            subSystems_dto = SubSystemDTO.create_from_dao_list(subSystems_dao)
            return subSystems_dto
        else:
            return None

    @execute_in_session
    def get_dataSources_by_subSystem_id(self, subSystem_id, session=None):
        dataSources_dao = self.dataSource_repository.get_by_subSystem_id(subSystem_id, session)
        if dataSources_dao is not None:
            dataSources_dto = DataSourceDTO.create_from_dao_list(dataSources_dao)
            return dataSources_dto
        else:
            return None

    @execute_in_session
    def get_dataSources_by_tumbleweed_id(self, tumbleweed_id, session=None):
        #dataSources_dao = self.dataSource_repository.get_dataSources_by_tumbleweed_id(tumbleweed_id, session)
        dataSources_dao = self.dataSource_repository.get_entities(session)
        if dataSources_dao is not None:
            dataSources_dto = DataSourceDTO.create_from_dao_list(dataSources_dao)
            return dataSources_dto
        else:
            return None

    @execute_in_session
    def get_tumbleweed_by_address(self, tumbleweed_address, session=None):
        tumbleweed_dao = self.tumbleweed_repository.get_by_address(tumbleweed_address, session)
        if tumbleweed_dao is not None:
            tumbleweed_dto = TumbleweedDTO.create_from_dao(tumbleweed_dao)
            return tumbleweed_dto
        else:
            return None

    @execute_in_session
    def get_tumblebase_by_address(self, tumblebase_address, session=None):
        tumblebase_dao = self.tumbleBase_repository.get_by_address(tumblebase_address, session)
        if tumblebase_dao is not None:
            tumblebase_dto = TumbleBaseDTO.create_from_dao(tumblebase_dao)
            return tumblebase_dto
        else:
            return None

    @execute_in_session
    def get_dataSource_by_tumbleweed_id_and_short_key(self, tumbleweed_id, short_key, session=None):
        dataSource_dao = self.dataSource_repository.get_dataSource_by_tumbleweed_id_and_short_key(tumbleweed_id, short_key, session)
        if dataSource_dao is not None:
            dataSource_dto = DataSourceDTO.create_from_dao(dataSource_dao)
            return dataSource_dto
        else:
            return None

    @execute_in_session
    def get_commands_by_commandType_id(self, commmandType_id, session=None):
        commands_dao = self.command_repository.get_by_commandType_id(commmandType_id, session)
        if commands_dao is not None:
            commands_dto = CommandDTO.create_from_dao_list(commands_dao)
            return commands_dto
        else:
            return None

    @execute_in_session
    def get_commands_by_tumbleweed_id_and_run_id(self, tumbleweed_id, run_id, session=None):
        commands_dao = self.command_repository.get_by_tumbleweed_id_and_run_id(tumbleweed_id, run_id, session)
        if commands_dao is not None:
            commands_dto = CommandDTO.create_from_dao_list(commands_dao)
            return commands_dto
        else:
            return None

    @execute_in_session
    def get_unanswered_commands_by_tumbleweed_id_and_run_id(self, tumbleweed_id, run_id, session=None):
        commands_dao = self.command_repository.get_unanswered_by_tumbleweed_id_and_run_id(tumbleweed_id, run_id, session)
        if commands_dao is not None:
            commands_dto = CommandDTO.create_from_dao_list(commands_dao)
            return commands_dto
        else:
            return None

    @execute_in_session
    def get_longdatapoints_by_dataSource_and_run(self, dataSource_id, run_id, session=None):
        longdata_dao = self.longData_repository.get_by_dataSource_id_and_run_id(dataSource_id, run_id, session)
        if longdata_dao is not None:
            longdata_dto = LongDataDTO.create_from_dao_list(longdata_dao)
            return longdata_dto
        else:
            return None

    @execute_in_session
    def get_intdatapoints_by_dataSource_and_run(self, dataSource_id, run_id, session=None):
        intdata_dao = self.intData_repository.get_by_dataSource_id_and_run_id(dataSource_id, run_id, session)
        if intdata_dao is not None:
            intdata_dto = IntDataDTO.create_from_dao_list(intdata_dao)
            return intdata_dto
        else:
            return None

    @execute_in_session
    def get_floatdatapoints_by_dataSource_and_run(self, dataSource_id, run_id, session=None):
        floatdata_dao = self.floatData_repository.get_by_dataSource_id_and_run_id(dataSource_id, run_id, session)
        if floatdata_dao is not None:
            floatdata_dto = FloatDataDTO.create_from_dao_list(floatdata_dao)
            return floatdata_dto
        else:
            return None

    @execute_in_session
    def get_stringdatapoints_by_dataSource_and_run(self, dataSource_id, run_id, session=None):
        stringdata_dao = self.stringData_repository.get_by_dataSource_id_and_run_id(dataSource_id, run_id, session)
        if stringdata_dao is not None:
            stringdata_dto = StringDataDTO.create_from_dao_list(stringdata_dao)
            return stringdata_dto
        else:
            return None

    @execute_in_session
    def get_bytedatapoints_by_dataSource_and_run(self, dataSource_id, run_id, session=None):
        bytedata_dao = self.byteData_repository.get_by_dataSource_id_and_run_id(dataSource_id, run_id, session)
        if bytedata_dao is not None:
            bytedata_dto = ByteDataDTO.create_from_dao_list(bytedata_dao)
            return bytedata_dto
        else:
            return None

    @execute_in_session
    def get_imagedatapoints_by_dataSource_and_run(self, dataSource_id, run_id, session=None):
        imagedata_dao = self.imageData_repository.get_by_dataSource_id_and_run_id(dataSource_id, run_id, session)
        if imagedata_dao is not None:
            imagedata_dto = ImageDataDTO.create_from_dao_list(imagedata_dao)
            return imagedata_dto
        else:
            return None

    """ Methods to update resources"""

    @execute_in_session
    def update_tumbleweed(self, tumbleweed_id, tumbleweed_dto, session=None):
        tumbleweed_dao = Tumbleweed.create_from_dto_update(tumbleweed_dto)
        tumbleweed_dao.id = tumbleweed_id
        tumbleweed_id = self.tumbleweed_repository.save_entity(tumbleweed_dao, session)
        return tumbleweed_id

    @execute_in_session
    def update_tumblebase(self, tumblebase_id, tumblebase_dto, session=None):
        tumblebase_dao = TumbleBase.create_from_dto_update(tumblebase_dto)
        tumblebase_dao.id = tumblebase_id
        tumblebase_id = self.tumbleBase_repository.save_entity(tumblebase_dao, session)
        return tumblebase_id

    @execute_in_session
    def update_subSystem(self, subSystem_id, subSystem_dto, session=None):
        subSystem_dao = SubSystem.create_from_dto_update(subSystem_dto)
        subSystem_dao.id = subSystem_id
        subSystem_id = self.subSystem_repository.save_entity(subSystem_dao, session)
        return subSystem_id

    @execute_in_session
    def update_dataSource(self, dataSource_id, dataSource_dto, session=None):
        dataSource_dao = DataSource.create_from_dto_update(dataSource_dto)
        dataSource_dao.id = dataSource_id
        dataSource_id = self.dataSource_repository.save_entity(dataSource_dao, session)
        return dataSource_id

    @execute_in_session
    def update_commandType(self, commandType_id, commandType_dto, session=None):
        commandType_dao = CommandType.create_from_dto_update(commandType_dto)
        commandType_dao.id = commandType_id
        commandType_id = self.commandType_repository.save_entity(commandType_dao, session)
        return commandType_id

    @execute_in_session
    def update_run(self, run_id, run_dto, session=None):
        run_dao = Run.create_from_dto_update(run_dto)
        run_dao.id = run_id
        run_id = self.run_repository.save_entity(run_dao, session)
        return run_id

    @execute_in_session
    def update_command(self, command_id, command_dto, session=None):
        command_dao = Command.create_from_dto_update(command_dto)
        command_dao.id = command_id
        command_id = self.command_repository.save_entity(command_dao, session)
        return command_id

    """ Methods to delete resources """

    @execute_in_session
    def delete_dataSource(self, dataSource_id, session=None):
        dataSource_id = self.dataSource_repository.delete_entity(dataSource_id, session)
        if dataSource_id is None:
            return None
        else:
            return dataSource_id

    @execute_in_session
    def delete_subSystem(self, subSystem_id, session=None):
        subSystem_id = self.subSystem_repository.delete_entity(subSystem_id, session)
        if subSystem_id is None:
            return None
        else:
            return subSystem_id

    @execute_in_session
    def delete_tumbleweed(self, tumbleweed_id, session=None):
        tumbleweed_id = self.tumbleweed_repository.delete_entity(tumbleweed_id, session)
        if tumbleweed_id is None:
            return None
        else:
            return tumbleweed_id
