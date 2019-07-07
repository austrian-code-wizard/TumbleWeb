from database.database import DatabaseConnector, DatabaseTools
from model.schema import TumbleweedSchema, TumbleBaseSchema, SubSystemSchema, DataSourceSchema, CommandTypeSchema, \
    CommandSchema, RunSchema, LongDataSchema, IntDataSchema, FloatDataSchema, StringDataSchema, ByteDataSchema, \
    ImageDataSchema
from test.templates import tumbleweed_json, tumblebase_json, subSystem_json, dataSource_json, run_json, \
    longdatapoint_json, intdatapoint_json, floatdatapoint_json, stringdatapoint_json, bytedatapoint_json, \
    commandType_json, command_json, imagedatapoint_json
from businesslogic.busineslogic import TumbleWebLogic
from datetime import datetime
from logger.logger import LoggerFactory
from tumbleweb_api import app
from util.mode import Mode
import unittest
import base64


class RestApiTest(unittest.TestCase):
    def setUp(self):
        self.database_connector = DatabaseConnector()
        self.database_connector.connection_string = DatabaseConnector.get_connection_string(mode=Mode.test)
        self.database_connector.pool_size = DatabaseConnector.get_pool_size(mode=Mode.test)
        self.database_tools = DatabaseTools(self.database_connector)
        self.database_tools.drop_database()
        self.database_tools.create_database()

        self.app = app.test_client()
        self.app.testing = True

        self.app.application.config["TUMBLEWEB_LOGGER"] = LoggerFactory.create_logger("rest-api-test-logger")
        self.app.application.config["TUMBLEWEB_BUSINESS_LOGIC"] = TumbleWebLogic.get_business_logic(Mode.test)
        self.app.application.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"] = TumbleweedSchema()
        self.app.application.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"] = TumbleBaseSchema()
        self.app.application.config["TUMBLEWEB_RUN_SCHEMA"] = RunSchema()
        self.app.application.config["TUMBLEWEB_COMMAND_SCHEMA"] = CommandSchema()
        self.app.application.config["TUMBLEWEB_COMMANDTYPE_SCHEMA"] = CommandTypeSchema()
        self.app.application.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"] = SubSystemSchema()
        self.app.application.config["TUMBLEWEB_DATASOURCE_SCHEMA"] = DataSourceSchema()
        self.app.application.config["TUMBLEWEB_LONGDATA_SCHEMA"] = LongDataSchema()
        self.app.application.config["TUMBlEWEB_INTDATA_SCHEMA"] = IntDataSchema()
        self.app.application.config["TUMBLEWEB_FLOATDATA_SCHEMA"] = FloatDataSchema()
        self.app.application.config["TUMBLEWEB_STRINGDATA_SCHEMA"] = StringDataSchema()
        self.app.application.config["TUMBLEWEB_BYTEDATA_SCHEMA"] = ByteDataSchema()

    def test_add_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_tumblebase(self):
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_subSystem(self):
        self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_commandType(self):
        response = self.app.post("/add-commandType", json=commandType_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_start_run(self):
        self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/start-run/1", json=run_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.post("/start-run/1", json=run_json)
        self.assertEqual(response.status, "400 BAD REQUEST")

    def test_send_command(self):
        self.app.post("/add-tumbleweed", json=tumbleweed_json)
        self.app.post("/add-tumblebase", json=tumblebase_json)
        self.app.post("/add-commandType", json=commandType_json)
        self.app.post("/start-run/1", json=run_json)
        response = self.app.post("/send-command/1/1/1", json=command_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_long(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "L"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=longdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_int(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "I"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=intdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_float(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "F"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=floatdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_string(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "S"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=stringdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_byte(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_image(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "M"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=imagedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_get_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-tumbleweed/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["address"], tumbleweed_json["address"])
        self.assertEqual(response.json["name"], tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def tearDown(self):
        self.database_tools.drop_database()
        self.database_connector.engine.dispose()


if __name__ == "__main__":
    unittest.test()
