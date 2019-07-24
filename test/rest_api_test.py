from database.database import DatabaseConnector, DatabaseTools
from model.schema import TumbleweedSchema, TumbleBaseSchema, SubSystemSchema, DataSourceSchema, CommandTypeSchema, \
    CommandSchema, RunSchema, LongDataSchema, IntDataSchema, FloatDataSchema, StringDataSchema, ByteDataSchema, \
    ImageDataSchema
from test.templates import tumbleweed_json_template, tumblebase_json_template, subSystem_json_template, \
    dataSource_json_template, run_json_template, longdatapoint_json_template, intdatapoint_json_template, \
    floatdatapoint_json_template, stringdatapoint_json_template, bytedatapoint_json_template, \
    commandType_json_template, command_json_template, imagedatapoint_json_template
from businesslogic.busineslogic import TumbleWebLogic
from datetime import datetime, timezone
from logger.logger import LoggerFactory
from tumbleweb_api import app
from util.mode import Mode
import unittest


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
        self.app.application.config["TUMBLEWEB_IMAGEDATA_SCHEMA"] = ImageDataSchema()

        self.tumbleweed_json = tumbleweed_json_template.copy()
        self.tumblebase_json = tumblebase_json_template.copy()
        self.subSystem_json = subSystem_json_template.copy()
        self.dataSource_json = dataSource_json_template.copy()
        self.command_json = command_json_template.copy()
        self.commandType_json = commandType_json_template.copy()
        self.run_json = run_json_template.copy()
        self.longdatapoint_json = longdatapoint_json_template.copy()
        self.intdatapoint_json = intdatapoint_json_template.copy()
        self.floatdatapoint_json = floatdatapoint_json_template.copy()
        self.stringdatapoint_json = stringdatapoint_json_template.copy()
        self.bytedatapoint_json = bytedatapoint_json_template.copy()
        self.imagedatapoint_json = imagedatapoint_json_template.copy()


    def test_add_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_tumblebase(self):
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_subSystem(self):
        self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_commandType(self):
        response = self.app.post("/add-commandType", json=self.commandType_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_start_run(self):
        self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.assertEqual(response.status, "400 BAD REQUEST")

    def test_stop_run(self):
        self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/stop-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.post("/stop-run/1")
        self.assertEqual(response.status, "400 BAD REQUEST")

    def test_send_command(self):
        self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        self.app.post("/add-tumblebase", json=self.tumblebase_json)
        self.app.post("/add-commandType", json=self.commandType_json)
        self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/send-command/1/1/1", json=self.command_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_long(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "L"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_int(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "I"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_float(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "F"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_string(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "S"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_byte(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_add_datapoint_image(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "M"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_get_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.get(f"/get-tumbleweed/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["address"], self.tumbleweed_json["address"])
        self.assertEqual(response.json["name"], self.tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_get_tumblebase(self):
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.get(f"/get-tumblebase/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.tumblebase_json["name"])
        self.assertEqual(response.json["address"], self.tumblebase_json["address"])
        self.assertEqual(response.json["host"], self.tumblebase_json["host"])
        self.assertEqual(response.json["port"], self.tumblebase_json["port"])
        self.assertEqual(response.json["command_route"], self.tumblebase_json["command_route"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_get_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.get("/get-dataSource/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.dataSource_json["name"])
        self.assertEqual(response.json["description"], self.dataSource_json["description"])
        self.assertEqual(response.json["short_key"], self.dataSource_json["short_key"])
        self.assertEqual(response.json["dtype"], self.dataSource_json["dtype"])
        self.assertEqual(response.json["type"], self.dataSource_json["type"])

    def test_get_subSystem(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.get(f"/get-subSystem/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.subSystem_json["name"])
        self.assertEqual(response.json["description"], self.subSystem_json["description"])
        self.assertIsInstance(datetime.fromisoformat(response.json["created_at"]), datetime)

    def test_get_commandType(self):
        response = self.app.post("/add-commandType", json=self.commandType_json)
        response = self.app.get(f"/get-commandType/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["description"], self.commandType_json["description"])
        self.assertEqual(response.json["type"], self.commandType_json["type"])

    def test_get_command(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/add-commandType", json=self.commandType_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/send-command/1/1/1", json=self.command_json)
        response = self.app.get(f"/get-command/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["args"], self.command_json["args"])
        self.assertEqual(response.json["response"], self.command_json["response"])
        self.assertEqual(response.json["received_response_at"], self.command_json["received_response_at"])
        self.assertEqual(response.json["response_message_id"], self.command_json["response_message_id"])

    def test_get_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.get(f"/get-run/{response.json['info']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["description"], self.run_json["description"])
        self.assertEqual(response.json["name"], self.run_json["name"])

    def test_update_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        self.tumbleweed_json["address"] = "1234567890123456"
        self.tumbleweed_json["name"] = "New Name"
        response = self.app.patch("/update-tumbleweed/1", json=self.tumbleweed_json)
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
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        self.tumblebase_json["address"] = "576435"
        self.tumblebase_json["host"] = "192.168.0.34"
        self.tumblebase_json["port"] = 4000
        self.tumblebase_json["command_route"] = "/new-command"
        self.tumblebase_json["name"] = "New name"
        response = self.app.patch("/update-tumblebase/1", json=self.tumblebase_json)
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
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.subSystem_json["name"] = "new name"
        self.subSystem_json["description"] = "new description"
        response = self.app.patch("/update-subSystem/1", json=self.subSystem_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-subSystem/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.subSystem_json["name"])
        self.assertEqual(response.json["description"], self.subSystem_json["description"])

    def test_update_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        self.dataSource_json["name"] = "new name"
        self.dataSource_json["description"] = "new description"
        self.dataSource_json["short_key"] = "N1"
        self.dataSource_json["dtype"] = "I"
        self.dataSource_json["type"] = "new sensor 8000"
        response = self.app.patch("/update-dataSource/1", json=self.dataSource_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-dataSource/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.dataSource_json["name"])
        self.assertEqual(response.json["description"], self.dataSource_json["description"])
        self.assertEqual(response.json["short_key"], self.dataSource_json["short_key"])
        self.assertEqual(response.json["dtype"], self.dataSource_json["dtype"])
        self.assertEqual(response.json["type"], self.dataSource_json["type"])

    def test_update_commandType(self):
        response = self.app.post("/add-commandType", json=self.commandType_json)
        self.commandType_json["type"] = "other_type"
        self.commandType_json["description"] = "new description"
        response = self.app.patch("/update-commandType/1", json=self.commandType_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-commandType/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["description"], self.commandType_json["description"])
        self.assertEqual(response.json["type"], self.commandType_json["type"])

    def test_update_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.run_json["name"] = "new run name"
        self.run_json["description"] = "new description run"
        response = self.app.patch("/update-run/1", json=self.run_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["description"], self.run_json["description"])
        self.assertEqual(response.json["name"], self.run_json["name"])

    def test_update_command(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/add-commandType", json=self.commandType_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/send-command/1/1/1", json=self.command_json)
        self.command_json["response"] = "True"
        self.command_json["received_response_at"] = datetime.now(timezone.utc).isoformat()
        self.command_json["response_message_id"] = 3
        response = self.app.patch(f"/update-command/{response.json['info']}", json=self.command_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-command/1")
        self.assertEqual(response.json["response"], self.command_json["response"])
        self.assertEqual(response.json["received_response_at"], self.command_json["received_response_at"])
        self.assertEqual(response.json["response_message_id"], self.command_json["response_message_id"])

    def test_update_bytedatapoint(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.bytedatapoint_json["receiving_done"] = None
        self.bytedatapoint_json["packets"] = 2
        self.bytedatapoint_json["data"] = None
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.bytedatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], None)
        self.assertEqual(response.json["packets_received"], self.bytedatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], 2)
        self.assertEqual(response.json["data"], None)
        self.assertEqual(response.json["message_id"], self.bytedatapoint_json["message_id"])
        self.bytedatapoint_json["receiving_done"] = datetime.now(timezone.utc).isoformat()
        self.bytedatapoint_json["data"] = 'RdOPOw=='
        self.bytedatapoint_json["packets_received"] = 2
        response = self.app.patch(f"/update-datapoint/{self.dataSource_json['dtype']}/1", json=self.bytedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.bytedatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.bytedatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.bytedatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.bytedatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.bytedatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.bytedatapoint_json["message_id"])

    def test_update_intdatapoint(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "I"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.intdatapoint_json["receiving_done"] = None
        self.intdatapoint_json["packets"] = 2
        self.intdatapoint_json["data"] = None
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.intdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], None)
        self.assertEqual(response.json["packets_received"], self.intdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], 2)
        self.assertEqual(response.json["data"], None)
        self.assertEqual(response.json["message_id"], self.intdatapoint_json["message_id"])
        self.intdatapoint_json["receiving_done"] = datetime.now(timezone.utc).isoformat()
        self.intdatapoint_json["data"] = 236464
        self.intdatapoint_json["packets_received"] = 2
        response = self.app.patch(f"/update-datapoint/{self.dataSource_json['dtype']}/1", json=self.intdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.intdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.intdatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.intdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.intdatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.intdatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.intdatapoint_json["message_id"])

    def test_update_longdatapoint(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "L"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.longdatapoint_json["receiving_done"] = None
        self.longdatapoint_json["packets"] = 2
        self.longdatapoint_json["data"] = None
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.longdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], None)
        self.assertEqual(response.json["packets_received"], self.longdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], 2)
        self.assertEqual(response.json["data"], None)
        self.assertEqual(response.json["message_id"], self.longdatapoint_json["message_id"])
        self.longdatapoint_json["receiving_done"] = datetime.now(timezone.utc).isoformat()
        self.longdatapoint_json["data"] = 34878673345687543
        self.longdatapoint_json["packets_received"] = 2
        response = self.app.patch(f"/update-datapoint/{self.dataSource_json['dtype']}/1", json=self.longdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.longdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.longdatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.longdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.longdatapoint_json["packets"])
        self.assertEqual(response.json["data"], str(self.longdatapoint_json["data"]))
        self.assertEqual(response.json["message_id"], self.longdatapoint_json["message_id"])

    def test_update_floatdatapoint(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "F"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.floatdatapoint_json["receiving_done"] = None
        self.floatdatapoint_json["packets"] = 2
        self.floatdatapoint_json["data"] = None
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.floatdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], None)
        self.assertEqual(response.json["packets_received"], self.floatdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], 2)
        self.assertEqual(response.json["data"], None)
        self.assertEqual(response.json["message_id"], self.floatdatapoint_json["message_id"])
        self.floatdatapoint_json["receiving_done"] = datetime.now(timezone.utc).isoformat()
        self.floatdatapoint_json["data"] = 348.4635
        self.floatdatapoint_json["packets_received"] = 2
        response = self.app.patch(f"/update-datapoint/{self.dataSource_json['dtype']}/1", json=self.floatdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.floatdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.floatdatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.floatdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.floatdatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.floatdatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.floatdatapoint_json["message_id"])

    def test_update_stringdatapoint(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "S"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.stringdatapoint_json["receiving_done"] = None
        self.stringdatapoint_json["packets"] = 2
        self.stringdatapoint_json["data"] = None
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.stringdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], None)
        self.assertEqual(response.json["packets_received"], self.stringdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], 2)
        self.assertEqual(response.json["data"], None)
        self.assertEqual(response.json["message_id"], self.stringdatapoint_json["message_id"])
        self.stringdatapoint_json["receiving_done"] = datetime.now(timezone.utc).isoformat()
        self.stringdatapoint_json["data"] = "hello"
        self.stringdatapoint_json["packets_received"] = 2
        response = self.app.patch(f"/update-datapoint/{self.dataSource_json['dtype']}/1", json=self.stringdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.stringdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.stringdatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.stringdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.stringdatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.stringdatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.stringdatapoint_json["message_id"])

    def test_update_imagedatapoint(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "M"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        self.imagedatapoint_json["receiving_done"] = None
        self.imagedatapoint_json["packets"] = 2
        image_string = self.imagedatapoint_json["data"]
        self.imagedatapoint_json["data"] = None
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.imagedatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], None)
        self.assertEqual(response.json["packets_received"], self.imagedatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], 2)
        self.assertEqual(response.json["data"], None)
        self.assertEqual(response.json["message_id"], self.imagedatapoint_json["message_id"])
        self.imagedatapoint_json["receiving_done"] = datetime.now(timezone.utc).isoformat()
        self.imagedatapoint_json["data"] = image_string
        self.imagedatapoint_json["packets_received"] = 2
        response = self.app.patch(f"/update-datapoint/{self.dataSource_json['dtype']}/1", json=self.imagedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.imagedatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.imagedatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.imagedatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.imagedatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.imagedatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.imagedatapoint_json["message_id"])

    def test_get_tumbleweed_by_address(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.get(f"/get-tumbleweed-by-address/{self.tumbleweed_json['address']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["address"], self.tumbleweed_json["address"])
        self.assertEqual(response.json[0]["name"], self.tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json[0]["created_at"]), datetime)
        self.assertEqual(response.json[1]["address"], self.tumbleweed_json["address"])
        self.assertEqual(response.json[1]["name"], self.tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json[1]["created_at"]), datetime)

    def test_get_tumblebase_by_address(self):
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.get(f"/get-tumblebase-by-address/{self.tumblebase_json['address']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.tumblebase_json["name"])
        self.assertEqual(response.json["address"], self.tumblebase_json["address"])
        self.assertEqual(response.json["host"], self.tumblebase_json["host"])
        self.assertEqual(response.json["port"], self.tumblebase_json["port"])
        self.assertEqual(response.json["command_route"], self.tumblebase_json["command_route"])

    def test_get_subSystems_by_tumbleweed_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.get("/get-subSystems-by-tumbleweed-id/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["name"], self.subSystem_json["name"])
        self.assertEqual(response.json[0]["description"], self.subSystem_json["description"])
        self.assertIsInstance(datetime.fromisoformat(response.json[0]["created_at"]), datetime)

    def test_get_dataSources_by_subSystem_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.get("/get-dataSources-by-subSystem-id/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["name"], self.dataSource_json["name"])
        self.assertEqual(response.json[0]["description"], self.dataSource_json["description"])
        self.assertEqual(response.json[0]["short_key"], self.dataSource_json["short_key"])
        self.assertEqual(response.json[0]["dtype"], self.dataSource_json["dtype"])
        self.assertEqual(response.json[0]["type"], self.dataSource_json["type"])

    def test_get_dataSource_by_short_key_and_tumbleweed_address(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.get(f"/get-dataSource-by-short-key-and-tumbleweed-address/{self.dataSource_json['short_key']}/{self.tumbleweed_json['address']}")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.dataSource_json["name"])
        self.assertEqual(response.json["description"], self.dataSource_json["description"])
        self.assertEqual(response.json["short_key"], self.dataSource_json["short_key"])
        self.assertEqual(response.json["dtype"], self.dataSource_json["dtype"])
        self.assertEqual(response.json["type"], self.dataSource_json["type"])

    def test_get_commands_by_commandType(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/add-commandType", json=self.commandType_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/send-command/1/1/1", json=self.command_json)
        response = self.app.get(f"/get-commands-by-commandType-id/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["args"], self.command_json["args"])
        self.assertEqual(response.json[0]["response"], self.command_json["response"])
        self.assertEqual(response.json[0]["received_response_at"], self.command_json["received_response_at"])
        self.assertEqual(response.json[0]["response_message_id"], self.command_json["response_message_id"])

    def test_get_commands_by_tumbleweed_id_and_run_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/add-commandType", json=self.commandType_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/send-command/1/1/1", json=self.command_json)
        response = self.app.get(f"/get-commands-by-tumbleweed-id-and-run-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["args"], self.command_json["args"])
        self.assertEqual(response.json[0]["response"], self.command_json["response"])
        self.assertEqual(response.json[0]["received_response_at"], self.command_json["received_response_at"])
        self.assertEqual(response.json[0]["response_message_id"], self.command_json["response_message_id"])

    def test_get_unanswered_commands_by_tumbleweed_id_and_run_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/add-commandType", json=self.commandType_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/send-command/1/1/1", json=self.command_json)
        response = self.app.get(f"/get-unanswered-commands-by-tumbleweed-id-and-run-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["args"], self.command_json["args"])
        self.assertEqual(response.json[0]["response"], self.command_json["response"])
        self.assertEqual(response.json[0]["received_response_at"], self.command_json["received_response_at"])
        self.assertEqual(response.json[0]["response_message_id"], self.command_json["response_message_id"])

    def test_get_floatdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "F"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], self.floatdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], self.floatdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], self.floatdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], self.floatdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], self.floatdatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], self.floatdatapoint_json["message_id"])

    def test_get_intdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "I"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], self.intdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], self.intdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], self.intdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], self.intdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], self.intdatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], self.intdatapoint_json["message_id"])

    def test_get_longdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "L"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.longdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], self.longdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], self.longdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], self.longdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], self.longdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], str(self.longdatapoint_json["data"]))
        self.assertEqual(response.json[0]["message_id"], self.longdatapoint_json["message_id"])

    def test_get_stringdatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "S"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], self.stringdatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], self.stringdatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], self.stringdatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], self.stringdatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], self.stringdatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], self.stringdatapoint_json["message_id"])

    def test_get_bytedatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], self.bytedatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], self.bytedatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], self.bytedatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], self.bytedatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], self.bytedatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], self.bytedatapoint_json["message_id"])

    def test_get_imagedatapoints_by_dataSource_and_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "M"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        self.assertEqual(response.status, "200 OK")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]["receiving_start"], self.imagedatapoint_json["receiving_start"])
        self.assertEqual(response.json[0]["receiving_done"], self.imagedatapoint_json["receiving_done"])
        self.assertEqual(response.json[0]["packets_received"], self.imagedatapoint_json["packets_received"])
        self.assertEqual(response.json[0]["packets"], self.imagedatapoint_json["packets"])
        self.assertEqual(response.json[0]["data"], self.imagedatapoint_json["data"])
        self.assertEqual(response.json[0]["message_id"], self.imagedatapoint_json["message_id"])

    def test_get_imagedatapoint_by_datasource_id_and_datapoint_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "M"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.imagedatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.imagedatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.imagedatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.imagedatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.imagedatapoint_json["packets"])
        self.assertEqual(response.json["data"], str(self.imagedatapoint_json["data"]))
        self.assertEqual(response.json["message_id"], self.imagedatapoint_json["message_id"])

    def test_get_intdatapoint_by_datasource_id_and_datapoint_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "I"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.intdatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.intdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.intdatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.intdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.intdatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.intdatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.intdatapoint_json["message_id"])

    def test_get_floatdatapoint_by_datasource_id_and_datapoint_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "F"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.floatdatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.floatdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.floatdatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.floatdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.floatdatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.floatdatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.floatdatapoint_json["message_id"])

    def test_get_stringdatapoint_by_datasource_id_and_datapoint_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "S"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.stringdatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.stringdatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.stringdatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.stringdatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.stringdatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.stringdatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.stringdatapoint_json["message_id"])

    def test_get_bytedatapoint_by_datasource_id_and_datapoint_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.get("/get-datapoint-by-dataSource-id-and-datapoint-id/1/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["receiving_start"], self.bytedatapoint_json["receiving_start"])
        self.assertEqual(response.json["receiving_done"], self.bytedatapoint_json["receiving_done"])
        self.assertEqual(response.json["packets_received"], self.bytedatapoint_json["packets_received"])
        self.assertEqual(response.json["packets"], self.bytedatapoint_json["packets"])
        self.assertEqual(response.json["data"], self.bytedatapoint_json["data"])
        self.assertEqual(response.json["message_id"], self.bytedatapoint_json["message_id"])

    def test_get_active_run_by_tumbleweed_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.get("/get-active-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], self.run_json["name"])
        self.assertEqual(response.json["description"], self.run_json["description"])

    def test_get_tumbleweeds(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        self.tumbleweed_json2 = self.tumbleweed_json.copy()
        self.tumbleweed_json2["address"] = "9876543456764"
        self.tumbleweed_json2["name"] = "TW2"
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json2)
        response = self.app.get("/get-tumbleweeds")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["address"], self.tumbleweed_json["address"])
        self.assertEqual(response.json[0]["name"], self.tumbleweed_json["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json[0]["created_at"]), datetime)
        self.assertEqual(response.json[1]["address"], self.tumbleweed_json2["address"])
        self.assertEqual(response.json[1]["name"], self.tumbleweed_json2["name"])
        self.assertIsInstance(datetime.fromisoformat(response.json[1]["created_at"]), datetime)

    def test_get_tumblebases(self):
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        self.tumblebase_json2 = self.tumblebase_json.copy()
        self.tumblebase_json2["address"] = "576435"
        self.tumblebase_json2["host"] = "192.168.0.34"
        self.tumblebase_json2["port"] = 4000
        self.tumblebase_json2["command_route"] = "/new-command"
        self.tumblebase_json2["name"] = "New name"
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json2)
        response = self.app.get("/get-tumblebases")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["name"], self.tumblebase_json["name"])
        self.assertEqual(response.json[0]["address"], self.tumblebase_json["address"])
        self.assertEqual(response.json[0]["host"], self.tumblebase_json["host"])
        self.assertEqual(response.json[0]["port"], self.tumblebase_json["port"])
        self.assertEqual(response.json[0]["command_route"], self.tumblebase_json["command_route"])
        self.assertEqual(response.json[1]["id"], 2)
        self.assertEqual(response.json[1]["name"], self.tumblebase_json2["name"])
        self.assertEqual(response.json[1]["address"], self.tumblebase_json2["address"])
        self.assertEqual(response.json[1]["host"], self.tumblebase_json2["host"])
        self.assertEqual(response.json[1]["port"], self.tumblebase_json2["port"])
        self.assertEqual(response.json[1]["command_route"], self.tumblebase_json2["command_route"])

    def test_get_commandTypes(self):
        response = self.app.post("/add-commandType", json=self.commandType_json)
        self.commandType_json2 = self.commandType_json.copy()
        self.commandType_json2["type"] = "second_type"
        self.commandType_json2["description"] = "other desc"
        response = self.app.post("/add-commandType", json=self.commandType_json2)
        response = self.app.get("/get-commandTypes")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["description"], self.commandType_json["description"])
        self.assertEqual(response.json[0]["type"], self.commandType_json["type"])
        self.assertEqual(response.json[1]["id"], 2)
        self.assertEqual(response.json[1]["description"], self.commandType_json2["description"])
        self.assertEqual(response.json[1]["type"], self.commandType_json2["type"])

    def test_get_runs_by_tumbleweed_id(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/stop-run/1")
        run_json2 = self.run_json.copy()
        run_json2["name"] = "run2"
        run_json2["description"] = "desc2"
        response = self.app.post("/start-run/1", json=run_json2)
        response = self.app.post("/stop-run/1")
        run_json3 = self.run_json.copy()
        run_json3["name"] = "run3"
        run_json3["description"] = "desc3"
        response = self.app.post("/start-run/1", json=run_json3)
        response = self.app.get("/get-runs-by-tumbleweed-id/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]["name"], self.run_json["name"])
        self.assertEqual(response.json[0]["description"], self.run_json["description"])
        self.assertEqual(response.json[1]["name"], run_json2["name"])
        self.assertEqual(response.json[1]["description"], run_json2["description"])
        self.assertEqual(response.json[2]["name"], run_json3["name"])
        self.assertEqual(response.json[2]["description"], run_json3["description"])

    def test_delete_dataSource(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
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
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.delete("/delete-subSystem/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.delete("/delete-dataSource/1")
        response = self.app.delete("/delete-subSystem/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_delete_tumbleweed(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        response = self.app.delete("/delete-tumbleweed/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.delete("/delete-subSystem/1")
        response = self.app.delete("/delete-tumbleweed/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)

    def test_delete_commandType(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/add-commandType", json=self.commandType_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post("/send-command/1/1/1", json=self.command_json)
        response = self.app.delete("/delete-commandType/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-command/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.get("/get-tumbleweed/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        response = self.app.get("/get-tumblebase/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        response = self.app.get("/get-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        response = self.app.get("/get-commandType/1")
        self.assertEqual(response.status, "400 BAD REQUEST")

    def test_delete_run(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.delete("/delete-run/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.post("/stop-run/1")
        self.assertEqual(response.status, "200 OK")
        response = self.app.get("/get-run/1")
        self.assertEqual(response.status, "200 OK")
        response = self.app.delete("/delete-run/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-run/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.get(f"/get-datapoints-by-dataSource-and-run/1/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.get("/get-tumbleweed/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        response = self.app.get("/get-tumblebase/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)

    def test_delete_tumblebase(self):
        response = self.app.post("/add-tumbleweed", json=self.tumbleweed_json)
        response = self.app.post("/add-subSystem/1", json=self.subSystem_json)
        self.dataSource_json["dtype"] = "B"
        response = self.app.post("/add-dataSource/1", json=self.dataSource_json)
        response = self.app.post("/add-tumblebase", json=self.tumblebase_json)
        response = self.app.post("/start-run/1", json=self.run_json)
        response = self.app.post(f"/add-datapoint/1234567890123456/123456789123457/T1", json=self.bytedatapoint_json)
        response = self.app.post("/stop-run/1")
        response = self.app.delete("/delete-tumblebase/1")
        self.assertEqual(response.status, "400 BAD REQUEST")
        response = self.app.delete("/delete-run/1")
        response = self.app.delete("/delete-tumblebase/1")
        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["info"], 1)
        response = self.app.get("/get-tumblebase/1")
        self.assertEqual(response.status, "400 BAD REQUEST")

    def tearDown(self):
        self.database_tools.drop_database()
        self.database_connector.engine.dispose()


if __name__ == "__main__":
    unittest.test()
