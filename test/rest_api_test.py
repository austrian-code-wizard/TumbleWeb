from database.database import DatabaseConnector, DatabaseTools
from model.schema import TumbleweedSchema, TumbleBaseSchema, SubSystemSchema, DataSourceSchema, CommandTypeSchema, \
    CommandSchema, RunSchema, LongDataSchema, IntDataSchema, FloatDataSchema, StringDataSchema, ByteDataSchema, \
    ImageDataSchema
from test.templates import tumbleweed_json, tumblebase_json, subSystem_json, dataSource_json, run_json, \
    longdatapoint_json, intdatapoint_json, floatdatapoint_json, stringdatapoint_json, bytedatapoint_json, \
    commandType_json, command_json, imagedatapoint_json
from businesslogic.busineslogic import TumbleWebLogic
from datetime import datetime, timezone
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

    def test_stop_run(self):
        self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post("/stop-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.post("/stop-run/1")
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
        response = self.app.get(f"/get-tumbleweed/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["address"], tumbleweed_json["address"])
        self.assertEqual(response.json["name"], tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_get_tumblebase(self):
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.get(f"/get-tumblebase/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], tumblebase_json["name"])
        self.assertEqual(response.json["address"], tumblebase_json["address"])
        self.assertEqual(response.json["host"], tumblebase_json["host"])
        self.assertEqual(response.json["port"], tumblebase_json["port"])
        self.assertEqual(response.json["command_route"], tumblebase_json["command_route"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_get_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.get("/get-dataSource/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], dataSource_json["name"])
        self.assertEqual(response.json["description"], dataSource_json["description"])
        self.assertEqual(response.json["short_key"], dataSource_json["short_key"])
        self.assertEqual(response.json["dtype"], dataSource_json["dtype"])
        self.assertEqual(response.json["type"], dataSource_json["type"])

    def test_get_subSystem(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.get(f"/get-subSystem/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], subSystem_json["name"])
        self.assertEqual(response.json["description"], subSystem_json["description"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_get_commandType(self):
        response = self.app.post("/add-commandType", json=commandType_json)
        response = self.app.get(f"/get-commandType/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["description"], commandType_json["description"])
        self.assertEqual(response.json["type"], commandType_json["type"])

    def test_get_command(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/add-commandType", json=commandType_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post("/send-command/1/1/1", json=command_json)
        response = self.app.get(f"/get-command/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["args"], command_json["args"])
        self.assertEqual(response.json["response"], command_json["response"])
        self.assertEqual(response.json["received_response_at"], command_json["received_response_at"])
        self.assertEqual(response.json["response_message_id"], command_json["response_message_id"])

    def test_get_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.get(f"/get-run/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["description"], run_json["description"])
        self.assertEqual(response.json["name"], run_json["name"])

    def test_update_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        tumbleweed_json["address"] = "1234567890123456"
        tumbleweed_json["name"] = "New Name"
        response = self.app.patch("/update-tumbleweed/1", json=tumbleweed_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get(f"/get-tumbleweed/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["address"], "1234567890123456")
        self.assertEqual(response.json["name"], "New Name")
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_update_tumblebase(self):
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        tumblebase_json["address"] = "576435"
        tumblebase_json["host"] = "192.168.0.34"
        tumblebase_json["port"] = 4000
        tumblebase_json["command_route"] = "/new-command"
        tumblebase_json["name"] = "New name"
        response = self.app.patch("/update-tumblebase/1", json=tumblebase_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get(f"/get-tumblebase/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], "New name")
        self.assertEqual(response.json["address"], "576435")
        self.assertEqual(response.json["host"], "192.168.0.34")
        self.assertEqual(response.json["port"], 4000)
        self.assertEqual(response.json["command_route"], "/new-command")

    def test_update_subSystem(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        subSystem_json["name"] = "new name"
        subSystem_json["description"] = "new description"
        response = self.app.patch("/update-subSystem/1", json=subSystem_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-subSystem/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], subSystem_json["name"])
        self.assertEqual(response.json["description"], subSystem_json["description"])

    def test_update_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        dataSource_json["name"] = "new name"
        dataSource_json["description"] = "new description"
        dataSource_json["short_key"] = "N1"
        dataSource_json["dtype"] = "I"
        dataSource_json["type"] = "new sensor 8000"
        response = self.app.patch("/update-dataSource/1", json=dataSource_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-dataSource/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], dataSource_json["name"])
        self.assertEqual(response.json["description"], dataSource_json["description"])
        self.assertEqual(response.json["short_key"], dataSource_json["short_key"])
        self.assertEqual(response.json["dtype"], dataSource_json["dtype"])
        self.assertEqual(response.json["type"], dataSource_json["type"])

    def test_update_commandType(self):
        response = self.app.post("/add-commandType", json=commandType_json)
        commandType_json["type"] = "other_type"
        commandType_json["description"] = "new description"
        response = self.app.patch("/update-commandType/1", json=commandType_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-commandType/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["description"], commandType_json["description"])
        self.assertEqual(response.json["type"], commandType_json["type"])

    def test_update_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/start-run/1", json=run_json)
        run_json["name"] = "new run name"
        run_json["description"] = "new description run"
        response = self.app.patch("/update-run/1", json=run_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["description"], run_json["description"])
        self.assertEqual(response.json["name"], run_json["name"])

    def test_update_command(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/add-commandType", json=commandType_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post("/send-command/1/1/1", json=command_json)
        command_json["response"] = "True"
        command_json["received_response_at"] = datetime.now(timezone.utc).isoformat()
        command_json["response_message_id"] = 3
        response = self.app.patch(f"/update-command/{response.json['info']}", json=command_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-command/1")
        self.assertEqual(response.json["response"], command_json["response"])
        self.assertEqual(response.json["received_response_at"], command_json["received_response_at"])
        self.assertEqual(response.json["response_message_id"], command_json["response_message_id"])


    def test_get_tumbleweed_by_address(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.get(f"/get-tumbleweed-by-address/{tumbleweed_json['address']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["address"], tumbleweed_json["address"])
        self.assertEqual(response.json["name"], tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_get_tumblebase_by_address(self):
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.get(f"/get-tumblebase-by-address/{tumblebase_json['address']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], tumblebase_json["name"])
        self.assertEqual(response.json["address"], tumblebase_json["address"])
        self.assertEqual(response.json["host"], tumblebase_json["host"])
        self.assertEqual(response.json["port"], tumblebase_json["port"])
        self.assertEqual(response.json["command_route"], tumblebase_json["command_route"])

    def test_get_subSystems_by_tumbleweed_id(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.get("/get-subSystems-by-tumbleweed-id/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["name"], subSystem_json["name"])
        self.assertEqual(response.json[0]["description"], subSystem_json["description"])
        self.assertIsInstance(datetime.fromisoformat(response.json[0]["created_at"]), datetime)

    def test_get_dataSources_by_subSystem_id(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.get("/get-dataSources-by-subSystem-id/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["name"], dataSource_json["name"])
        self.assertEqual(response.json[0]["description"], dataSource_json["description"])
        self.assertEqual(response.json[0]["short_key"], dataSource_json["short_key"])
        self.assertEqual(response.json[0]["dtype"], dataSource_json["dtype"])
        self.assertEqual(response.json[0]["type"], dataSource_json["type"])

    def test_get_dataSource_by_short_key_and_tumbleweed_address(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.get(f"/get-dataSource-by-short-key-and-tumbleweed-address/{dataSource_json['short_key']}/{tumbleweed_json['address']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], dataSource_json["name"])
        self.assertEqual(response.json["description"], dataSource_json["description"])
        self.assertEqual(response.json["short_key"], dataSource_json["short_key"])
        self.assertEqual(response.json["dtype"], dataSource_json["dtype"])
        self.assertEqual(response.json["type"], dataSource_json["type"])

    def test_get_commands_by_commandType(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/add-commandType", json=commandType_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post("/send-command/1/1/1", json=command_json)
        response = self.app.get(f"/get-commands-by-commandType-id/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["args"], command_json["args"])
        self.assertEqual(response.json[0]["response"], command_json["response"])
        self.assertEqual(response.json[0]["received_response_at"], command_json["received_response_at"])
        self.assertEqual(response.json[0]["response_message_id"], command_json["response_message_id"])

    def test_get_commands_by_tumbleweed_id_and_run_id(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/add-commandType", json=commandType_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post("/send-command/1/1/1", json=command_json)
        response = self.app.get(f"/get-commands-by-tumbleweed-id-and-run-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["args"], command_json["args"])
        self.assertEqual(response.json[0]["response"], command_json["response"])
        self.assertEqual(response.json[0]["received_response_at"], command_json["received_response_at"])
        self.assertEqual(response.json[0]["response_message_id"], command_json["response_message_id"])

    def test_get_unanswered_commands_by_tumbleweed_id_and_run_id(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/add-commandType", json=commandType_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post("/send-command/1/1/1", json=command_json)
        response = self.app.get(f"/get-unanswered-commands-by-tumbleweed-id-and-run-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["args"], command_json["args"])
        self.assertEqual(response.json[0]["response"], command_json["response"])
        self.assertEqual(response.json[0]["received_response_at"], command_json["received_response_at"])
        self.assertEqual(response.json[0]["response_message_id"], command_json["response_message_id"])

    def test_get_floatdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "F"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=floatdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=floatdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], floatdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], floatdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], floatdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], floatdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], floatdatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], floatdatapoint_json["message_id"])

    def test_get_intdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "I"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=intdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=intdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], intdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], intdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], intdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], intdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], intdatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], intdatapoint_json["message_id"])

    def test_get_longdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "L"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=longdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=longdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], longdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], longdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], longdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], longdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], str(longdatapoint_json["data"]))
        self.assertEqual(response.json[0]["message_id"], longdatapoint_json["message_id"])

    def test_get_stringdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "S"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=stringdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=stringdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], stringdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], stringdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], stringdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], stringdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], stringdatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], stringdatapoint_json["message_id"])

    def test_get_bytedatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], bytedatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], bytedatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], bytedatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], bytedatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], bytedatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], bytedatapoint_json["message_id"])

    def test_get_imagedatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "M"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=imagedatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=imagedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], imagedatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], imagedatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], imagedatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], imagedatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], imagedatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], imagedatapoint_json["message_id"])

    def test_get_active_run_by_tumbleweed_id(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.get("/get-active-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], run_json["name"])
        self.assertEqual(response.json["description"], run_json["description"])

    def test_get_tumbleweeds(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        tumbleweed_json2 = tumbleweed_json.copy()
        tumbleweed_json2["address"] = "9876543456764"
        tumbleweed_json2["name"] = "TW2"
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json2)
        response = self.app.get("/get-tumbleweeds")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["address"], tumbleweed_json["address"])
        self.assertEqual(response.json[0]["name"], tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json[0]["created_at"]), datetime)
        self.assertEqual(response.json[1]["address"], tumbleweed_json2["address"])
        self.assertEqual(response.json[1]["name"], tumbleweed_json2["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json[1]["created_at"]), datetime)

    def test_get_tumblebases(self):
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        tumblebase_json2 = tumblebase_json.copy()
        tumblebase_json2["address"] = "576435"
        tumblebase_json2["host"] = "192.168.0.34"
        tumblebase_json2["port"] = 4000
        tumblebase_json2["command_route"] = "/new-command"
        tumblebase_json2["name"] = "New name"
        response = self.app.post("/add-tumblebase", json=tumblebase_json2)
        response = self.app.get("/get-tumblebases")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["name"], tumblebase_json["name"])
        self.assertEqual(response.json[0]["address"], tumblebase_json["address"])
        self.assertEqual(response.json[0]["host"], tumblebase_json["host"])
        self.assertEqual(response.json[0]["port"], tumblebase_json["port"])
        self.assertEqual(response.json[0]["command_route"], tumblebase_json["command_route"])
        self.assertEqual(response.json[1]["id"], 2)
        self.assertEqual(response.json[1]["name"], tumblebase_json2["name"])
        self.assertEqual(response.json[1]["address"], tumblebase_json2["address"])
        self.assertEqual(response.json[1]["host"], tumblebase_json2["host"])
        self.assertEqual(response.json[1]["port"], tumblebase_json2["port"])
        self.assertEqual(response.json[1]["command_route"], tumblebase_json2["command_route"])

    def test_get_commandTypes(self):
        response = self.app.post("/add-commandType", json=commandType_json)
        commandType_json2 = commandType_json.copy()
        commandType_json2["type"] = "second_type"
        commandType_json2["description"] = "other desc"
        response = self.app.post("/add-commandType", json=commandType_json2)
        response = self.app.get("/get-commandTypes")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["description"], commandType_json["description"])
        self.assertEqual(response.json[0]["type"], commandType_json["type"])
        self.assertEqual(response.json[1]["id"], 2)
        self.assertEqual(response.json[1]["description"], commandType_json2["description"])
        self.assertEqual(response.json[1]["type"], commandType_json2["type"])

    def test_delete_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.post("/add-tumblebase", json=tumblebase_json)
        response = self.app.post("/start-run/1", json=run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=bytedatapoint_json)
        dataPoint_id = response.json["info"]
        response = self.app.delete("/delete-dataSource/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-dataSource/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.get("/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "400 BAD REQUEST")

    def test_delete_subSystem(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=dataSource_json)
        response = self.app.delete("/delete-subSystem/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.delete("/delete-dataSource/1")
        response = self.app.delete("/delete-subSystem/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_delete_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=subSystem_json)
        response = self.app.delete("/delete-tumbleweed/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.delete("/delete-subSystem/1")
        response = self.app.delete("/delete-tumbleweed/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def tearDown(self):
        self.database_tools.drop_database()
        self.database_connector.engine.dispose()


if __name__ == "__main__":
    unittest.test()
