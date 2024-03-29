from util.utils import internal_server_error_message, invalid_format_message, endpoint_not_found_message, \
    method_not_allowed_message, could_not_verify_message, invalid_token_message, no_admin_message
from exception.custom_exceptions import TumbleWebException, InternalServerError
from model.schema import TumbleweedSchema, TumbleBaseSchema, RunSchema, CommandSchema, CommandTypeSchema, DataSourceSchema, SubSystemSchema, LongDataSchema, IntDataSchema, FloatDataSchema, StringDataSchema, ByteDataSchema, ImageDataSchema
from businesslogic.busineslogic import TumbleWebLogic
from flask import Flask, request, jsonify
from logger.logger import LoggerFactory
from marshmallow import ValidationError
from functools import wraps
from model.enums import DType
from flask_cors import CORS
from datetime import datetime, timezone
import requests


"""
Flask is built for extensions. Use the config to add new keywords and new resources which can be used in the
endpoint definitions. This is needed for example for testing. Now it is possible to connect a business logic
which is connected to a test database and everything runs over the app config.
"""

app = Flask(__name__)
CORS(app)
app.config["TUMBLEWEB_LOGGER"] = LoggerFactory.create_logger("rest-api-logger")
app.config["TUMBLEWEB_BUSINESS_LOGIC"] = TumbleWebLogic.get_business_logic()
app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"] = TumbleweedSchema()
app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"] = TumbleBaseSchema()
app.config["TUMBLEWEB_RUN_SCHEMA"] = RunSchema()
app.config["TUMBLEWEB_COMMAND_SCHEMA"] = CommandSchema()
app.config["TUMBLEWEB_COMMANDTYPE_SCHEMA"] = CommandTypeSchema()
app.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"] = SubSystemSchema()
app.config["TUMBLEWEB_DATASOURCE_SCHEMA"] = DataSourceSchema()
app.config["TUMBLEWEB_LONGDATA_SCHEMA"] = LongDataSchema()
app.config["TUMBlEWEB_INTDATA_SCHEMA"] = IntDataSchema()
app.config["TUMBLEWEB_FLOATDATA_SCHEMA"] = FloatDataSchema()
app.config["TUMBLEWEB_STRINGDATA_SCHEMA"] = StringDataSchema()
app.config["TUMBLEWEB_BYTEDATA_SCHEMA"] = ByteDataSchema()
app.config["TUMBLEWEB_IMAGEDATA_SCHEMA"] = ImageDataSchema()


@app.errorhandler(404)
def page_not_found(_):
    return jsonify({"info": endpoint_not_found_message}), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({"info": method_not_allowed_message}), 405


def handle_exception(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValidationError:
            return jsonify({"info": invalid_format_message}), 400
        except TumbleWebException as e:
            return jsonify({"info": str(e)}), 400
        except InternalServerError as e:
            return jsonify({"info": str(e)}), 500
        except Exception as e:
            app.config["TUMBLEWEB_LOGGER"].error("TumbleWebApi.handle_exception(): " + str(e))
            return jsonify({"info": internal_server_error_message}), 500
    return wrapper

#
#   Routes to add resources
#


@app.route("/add-tumbleweed", methods=["POST"])
@handle_exception
def add_tumbleweed():
    tumbleweed_json = request.get_json()
    tumbleweed_to_insert = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].load(tumbleweed_json)
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_tumbleweed(tumbleweed_to_insert)
    if tumbleweed_id is None:
        return jsonify({"info": f"The tumbleweed cannot be added."}), 400
    else:
        return jsonify({"info": tumbleweed_id})


@app.route("/add-tumblebase", methods=["POST"])
@handle_exception
def add_tumblebase():
    tumblebase_json = request.get_json()
    tumblebase_to_insert = app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"].load(tumblebase_json)
    tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_tumblebase(tumblebase_to_insert)
    if tumblebase_id is None:
        return jsonify({"info": f"The tumblebase cannot be added."}), 400
    else:
        return jsonify({"info": tumblebase_id})


@app.route("/add-subSystem/<int:tumbleweed_id>", methods=["POST"])
@handle_exception
def add_subSystem(tumbleweed_id):
    subSystem_json = request.get_json()
    subSystem_to_insert = app.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"].load(subSystem_json)
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"The Tumbleweed with id {tumbleweed_id} does not exist."}), 400
    subSystem_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_subSystem(subSystem_to_insert)
    if subSystem_id is None:
        return jsonify({"info": f"The SubSystem cannot be added."}), 400
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_subSystem_to_tumbleweed(subSystem_id, tumbleweed_id)
    if tumbleweed_id is None:
        return jsonify({"info": f"The SubSystem cannot be added to the Tumbleweed with id {tumbleweed_id}"}), 400
    else:
        return jsonify({"info": subSystem_id})


@app.route("/add-dataSource/<int:subSystem_id>", methods=["POST"])
@handle_exception
def add_dataSource_to_subSystem(subSystem_id):
    dataSource_json = request.get_json()
    dataSource_to_insert = app.config["TUMBLEWEB_DATASOURCE_SCHEMA"].load(dataSource_json)
    subSystem = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_subSystem(subSystem_id)
    if subSystem is None:
        return jsonify({"info": f"The SubSystem with id {subSystem_id} does not exist."}), 400
    dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_dataSource(dataSource_to_insert)
    if dataSource_id is None:
        return jsonify({"info": f"The Data Source cannot be added."}), 400
    subSystem_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_dataSource_to_subSystem(dataSource_id, subSystem_id)
    if subSystem_id is None:
        return jsonify({"info": f"The DataSource cannot be added to the SubSystem with id {subSystem_id}"}), 400
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_dataSource_to_tumbleweed(dataSource_id, subSystem.tumbleweed_id)
    if tumbleweed_id is None:
        return jsonify({"info": f"The DataSource cannot be added to the Tumbleweed with id {tumbleweed_id}"}), 400
    else:
        return jsonify({"info": dataSource_id})


@app.route("/add-commandType", methods=["POST"])
@handle_exception
def add_commandType():
    commandType_json = request.get_json()
    commandType_to_insert = app.config["TUMBLEWEB_COMMANDTYPE_SCHEMA"].load(commandType_json)
    commandType_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_commandType(commandType_to_insert)
    if commandType_id is None:
        return jsonify({"info": f"The CommandType cannot be added."}), 400
    else:
        return jsonify({"info": commandType_id})


@app.route("/start-run/<int:tumbleweed_id>", methods=["POST"])
@handle_exception
def start_run(tumbleweed_id):
    run_json = request.get_json()
    run_to_insert = app.config["TUMBLEWEB_RUN_SCHEMA"].load(run_json)
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"The Tumbleweed with id {tumbleweed_id} does not exist."}), 400
    is_running = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_active_run(tumbleweed_id)
    if is_running is not None:
        return jsonify({"info": f"Tumbleweed {tumbleweed_id} is already active"}), 400
    tumbleweeds_same_address = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed_by_address(tumbleweed.address)
    for tumbleweed_same_address in tumbleweeds_same_address:
        if app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_active_run(tumbleweed_same_address.id) is not None:
            return jsonify({"info": f"A tumbleweed with the same address and id {tumbleweed_same_address.id} is already active"})
    run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].start_run(run_to_insert, tumbleweed_id)
    if run_id is None:
        return jsonify({"info": f"The Run cannot be added."}), 400
    else:
        return jsonify({"info": run_id})


@app.route("/stop-run/<int:tumbleweed_id>", methods=["POST"])
@handle_exception
def stop_run(tumbleweed_id):
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"The Tumbleweed with id {tumbleweed_id} does not exist."}), 400
    is_running = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_active_run(tumbleweed_id)
    if is_running is None:
        return jsonify({"info": f"Tumbleweed {tumbleweed_id} is not active"}), 400
    is_running.ended_at = datetime.utcnow()
    run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_run(is_running.id, is_running)
    if run_id is None:
        return jsonify({"info": f"The Run cannot be stopped."}), 400
    else:
        return jsonify({"info": run_id})


@app.route("/send-command/<int:tumbleweed_id>/<int:tumblebase_id>/<int:commandType_id>", methods=["POST"])
@handle_exception
def send_command(tumbleweed_id, tumblebase_id, commandType_id):
    command_json = request.get_json()
    command_to_insert = app.config["TUMBLEWEB_COMMAND_SCHEMA"].load(command_json)
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"The Tumbleweed with id {tumbleweed_id} does not exist."}), 400
    if tumbleweed.address is None:
        return jsonify({"info": f"The Tumbleweed with id {tumbleweed_id} has no address configured."}), 400
    active_run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_active_run(tumbleweed_id)
    if active_run is None:
        return jsonify({"info": f"The Tumbleweed {tumbleweed_id} is currently not active"}), 400
    tumblebase = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumblebase(tumblebase_id)
    if tumblebase is None:
        return jsonify({"info": f"The TumbleBase with id {tumblebase_id} does not exist."}), 400
    commandType = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_commandType(commandType_id)
    if commandType is None:
        return jsonify({"info": f"The CommandType with id {commandType_id} does not exist."}), 400
    command_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_command(command_to_insert)
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_command_to_tumbleweed(command_id, tumbleweed_id)
    tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_command_to_tumblebase(command_id, tumblebase_id)
    commandType_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_command_to_commandType(command_id, commandType_id)
    active_run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_command_to_run(command_id, active_run.id)
    data = commandType.type
    if command_to_insert.args is not None:
        data += f"+{command_to_insert.args}"
    json_request = {
        "address": tumbleweed.address,
        "data": f"{data}"
    }
    response = requests.post(f"http://{tumblebase.host}:{tumblebase.port}/{tumblebase.command_route}", json=json_request)
    if response.status_code == 200:
        command = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_command(command_id)
        command.transmitted = True
        command_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_command(command)
        return jsonify({"info": command_id})
    else:
        return jsonify({"info": f"Unable to send command {command_id} from tumblebase {tumblebase_id} to tumbleweed"
        f" {tumbleweed_id}: {(response.json())['info']}"})


@app.route("/add-datapoint/<string:tumbleweed_address>/<string:tumblebase_address>/<string:short_key>", methods=["POST"])
@handle_exception
def add_datapoint(tumbleweed_address, tumblebase_address, short_key):
    data_json = request.get_json()
    tumbleweeds = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed_by_address(tumbleweed_address)
    tumbleweed = None
    run_id = None
    for tw in tumbleweeds:
        active_run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_active_run(tw.id)
        if active_run is not None:
            if tumbleweed is not None:
                return jsonify({"info": f"More than one tumbleweed with ID {tumbleweed_address} is active"}), 400
            tumbleweed = tw
            run_id = active_run.id
    if tumbleweed is None:
        return jsonify({"info": f"No Tumbleweed with address {tumbleweed_address} is active."}), 400
    dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource_by_tumbleweed_id_and_short_key(tumbleweed.id, short_key)
    if dataSource is None:
        return jsonify({"info": f"The DataSource with short key {short_key} does not exist for tumbleweed with address {tumbleweed_address}."}), 400
    tumblebase = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumblebase_by_address(tumblebase_address)
    if tumblebase is None:
        tumblebase_json = {
            "address": tumblebase_address,
            "host": request.headers.environ["REMOTE_ADDR"],
            "name": "Default TumbleBase",
            "port": None,
            "command_route": None
        }
        tumblebase_to_insert = app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"].load(tumblebase_json)
        tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_tumblebase(tumblebase_to_insert)
    else:
        tumblebase_id = tumblebase.id
    if dataSource.dtype == DType.Long:
        data_to_insert = app.config["TUMBLEWEB_LONGDATA_SCHEMA"].load(data_json)
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_LongData(data_to_insert)
        if datapoint_id is None:
            return jsonify({"info": f"The Run cannot be added."}), 400
        dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_LongData_to_dataSource(datapoint_id, dataSource.id)
        run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_LongData_to_run(datapoint_id, run_id)
        tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_LongData_to_tumblebase(datapoint_id, tumblebase_id)
        return jsonify({"info": datapoint_id})
    elif dataSource.dtype == DType.Int:
        data_to_insert = app.config["TUMBlEWEB_INTDATA_SCHEMA"].load(data_json)
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_IntData(data_to_insert)
        if datapoint_id is None:
            return jsonify({"info": f"The Run cannot be added."}), 400
        dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_IntData_to_dataSource(datapoint_id, dataSource.id)
        run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_IntData_to_run(datapoint_id, run_id)
        tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_IntData_to_tumblebase(datapoint_id, tumblebase_id)
        return jsonify({"info": datapoint_id})
    elif dataSource.dtype == DType.Float:
        data_to_insert = app.config["TUMBLEWEB_FLOATDATA_SCHEMA"].load(data_json)
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_FloatData(data_to_insert)
        if datapoint_id is None:
            return jsonify({"info": f"The Run cannot be added."}), 400
        dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_FloatData_to_dataSource(datapoint_id, dataSource.id)
        run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_FloatData_to_run(datapoint_id, run_id)
        tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_FloatData_to_tumblebase(datapoint_id, tumblebase_id)
        return jsonify({"info": datapoint_id})
    elif dataSource.dtype == DType.String:
        data_to_insert = app.config["TUMBLEWEB_STRINGDATA_SCHEMA"].load(data_json)
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_StringData(data_to_insert)
        if datapoint_id is None:
            return jsonify({"info": f"The Run cannot be added."}), 400
        dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_StringData_to_dataSource(datapoint_id, dataSource.id)
        run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_StringData_to_run(datapoint_id, run_id)
        tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_StringData_to_tumblebase(datapoint_id, tumblebase_id)
        return jsonify({"info": datapoint_id})
    elif dataSource.dtype == DType.Byte:
        data_to_insert = app.config["TUMBLEWEB_BYTEDATA_SCHEMA"].load(data_json)
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_ByteData(data_to_insert)
        if datapoint_id is None:
            return jsonify({"info": f"The Run cannot be added."}), 400
        dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_ByteData_to_dataSource(datapoint_id, dataSource.id)
        run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_ByteData_to_run(datapoint_id, run_id)
        tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_ByteData_to_tumblebase(datapoint_id, tumblebase_id)
        return jsonify({"info": datapoint_id})
    elif dataSource.dtype == DType.Image:
        data_to_insert = app.config["TUMBLEWEB_IMAGEDATA_SCHEMA"].load(data_json)
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_ImageData(data_to_insert)
        if datapoint_id is None:
            return jsonify({"info": f"The Run cannot be added."}), 400
        dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_ImageData_to_dataSource(datapoint_id, dataSource.id)
        run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_ImageData_to_run(datapoint_id, run_id)
        tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_ImageData_to_tumblebase(datapoint_id, tumblebase_id)
        return jsonify({"info": datapoint_id})
    else:
        return jsonify({"info": f"No data source found for tumbleweed {tumbleweed.id} with short key {short_key}."}), 400

#
#   Routes to get resources
#


@app.route("/get-tumbleweed/<int:tumbleweed_id>", methods=["GET"])
@handle_exception
def get_tumbleweed(tumbleweed_id):
    found_tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if found_tumbleweed is None:
        return jsonify({"info": f"No tumbleweed with id {tumbleweed_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].dump(found_tumbleweed)
        return jsonify(result)


@app.route("/get-tumblebase/<int:tumblebase_id>", methods=["GET"])
@handle_exception
def get_tumblebase(tumblebase_id):
    found_tumblebase = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumblebase(tumblebase_id)
    if found_tumblebase is None:
        return jsonify({"info": f"No tumblebase with id {tumblebase_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"].dump(found_tumblebase)
        return jsonify(result)


@app.route("/get-subSystem/<int:subSystem_id>", methods=["GET"])
@handle_exception
def get_subSystem(subSystem_id):
    found_subSystem = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_subSystem(subSystem_id)
    if found_subSystem is None:
        return jsonify({"info": f"No subSystem with id {subSystem_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"].dump(found_subSystem)
        return jsonify(result)


@app.route("/get-dataSource/<int:dataSource_id>", methods=["GET"])
@handle_exception
def get_dataSource(dataSource_id):
    found_dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource(dataSource_id)
    if found_dataSource is None:
        return jsonify({"info": f"No data source with id {dataSource_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_DATASOURCE_SCHEMA"].dump(found_dataSource)
        return jsonify(result)


@app.route("/get-commandType/<int:commandType_id>", methods=["GET"])
@handle_exception
def get_commandType(commandType_id):
    found_commandType = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_commandType(commandType_id)
    if found_commandType is None:
        return jsonify({"info": f"No command type with id {commandType_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_COMMANDTYPE_SCHEMA"].dump(found_commandType)
        return jsonify(result)


@app.route("/get-run/<int:run_id>", methods=["GET"])
@handle_exception
def get_run(run_id):
    found_run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_run(run_id)
    if found_run is None:
        return jsonify({"info": f"No run with id {run_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_RUN_SCHEMA"].dump(found_run)
        return jsonify(result)


@app.route("/get-command/<int:command_id>", methods=["GET"])
@handle_exception
def get_command(command_id):
    found_command = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_command(command_id)
    if found_command is None:
        return jsonify({"info": f"No command with id {command_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_COMMAND_SCHEMA"].dump(found_command)
        return jsonify(result)


@app.route("/get-commands-by-commandType-id/<int:commandType_id>", methods=["GET"])
@handle_exception
def get_commands_by_commandType_id(commandType_id):
    found_commands = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_commands_by_commandType_id(commandType_id)
    if found_commands is None:
        return jsonify({"info": f"No commands for commandType with ID {commandType_id} exist."}), 400
    else:
        result = app.config["TUMBLEWEB_COMMAND_SCHEMA"].dump(found_commands, many=True)
        return jsonify(result)


@app.route("/get-commands-by-tumbleweed-id-and-run-id/<int:tumbleweed_id>/<int:run_id>", methods=["GET"])
@handle_exception
def get_commands_by_tumbleweed_id_and_run_id(tumbleweed_id, run_id):
    found_commands = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_commands_by_tumbleweed_id_and_run_id(tumbleweed_id, run_id)
    if found_commands is None:
        return jsonify({"info": f"No commands for Tumbleweed with ID {tumbleweed_id} and run with id {run_id} exist."}), 400
    else:
        result = app.config["TUMBLEWEB_COMMAND_SCHEMA"].dump(found_commands, many=True)
        return jsonify(result)


@app.route("/get-unanswered-commands-by-tumbleweed-id-and-run-id/<int:tumbleweed_id>/<int:run_id>", methods=["GET"])
@handle_exception
def get_unanswered_commands_by_tumbleweed_id_and_run_id(tumbleweed_id, run_id):
    found_commands = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_unanswered_commands_by_tumbleweed_id_and_run_id(tumbleweed_id, run_id)
    if found_commands is None:
        return jsonify({"info": f"No commands for Tumbleweed with ID {tumbleweed_id} and run with id {run_id} exist."}), 400
    else:
        result = app.config["TUMBLEWEB_COMMAND_SCHEMA"].dump(found_commands, many=True)
        return jsonify(result)


@app.route("/get-tumbleweed-by-address/<string:tumbleweed_address>", methods=["GET"])
@handle_exception
def get_tumbleweed_by_address(tumbleweed_address):
    found_tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed_by_address(tumbleweed_address)
    if found_tumbleweed is None:
        return jsonify({"info": f"No tumbleweed with id {tumbleweed_address} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].dump(found_tumbleweed, many=True)
        return jsonify(result)


@app.route("/get-tumblebase-by-address/<string:tumblebase_address>", methods=["GET"])
@handle_exception
def get_tumblebase_by_address(tumblebase_address):
    found_tumblebase = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumblebase_by_address(tumblebase_address)
    if found_tumblebase is None:
        return jsonify({"info": f"No tumblebase with id {tumblebase_address} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"].dump(found_tumblebase)
        return jsonify(result)


@app.route("/get-subSystems-by-tumbleweed-id/<int:tumbleweed_id>", methods=["GET"])
@handle_exception
def get_subSystems_by_tumbleweed_id(tumbleweed_id):
    found_subSystems = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_subSystems_by_tumbleweed_id(tumbleweed_id)
    if found_subSystems is None:
        return jsonify({"info": f"No sub systems for tumbleweed with id {tumbleweed_id} exist."}), 400
    else:
        result = app.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"].dump(found_subSystems, many=True)
        return jsonify(result)


@app.route("/get-active-run/<int:tumbleweed_id>")
@handle_exception
def get_active_run(tumbleweed_id):
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"No tumbleweed with id {tumbleweed_id} exists."}), 400
    active_run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_active_run(tumbleweed_id)
    if active_run is None:
        return jsonify({"info": f"The tumbleweed with id {tumbleweed_id} is not active."}), 400
    else:
        result = app.config["TUMBLEWEB_RUN_SCHEMA"].dump(active_run)
        return jsonify(result)


@app.route("/get-runs-by-tumbleweed-id/<int:tumbleweed_id>", methods=["GET"])
@handle_exception
def get_runs_by_tumbleweed_id(tumbleweed_id):
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"No tumbleweed with id {tumbleweed_id} exists."}), 400
    found_runs = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_runs_by_tumbleweed_id(tumbleweed_id)
    if found_runs is None:
        return jsonify({"info": f"No runs for tumbleweed with id {tumbleweed_id} exist."}), 400
    else:
        result = app.config["TUMBLEWEB_RUN_SCHEMA"].dump(found_runs, many=True)
        return jsonify(result)


@app.route("/get-dataSources-by-subSystem-id/<int:subSystem_id>", methods=["GET"])
@handle_exception
def get_dataSources_by_subSystem_id(subSystem_id):
    found_dataSources = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSources_by_subSystem_id(subSystem_id)
    if found_dataSources is None:
        return jsonify({"info": f"No data sources for sub system with id {subSystem_id} exist."}), 400
    else:
        result = app.config["TUMBLEWEB_DATASOURCE_SCHEMA"].dump(found_dataSources, many=True)
        return jsonify(result)


@app.route("/get-dataSource-by-short-key-and-tumbleweed-address/<string:short_key>/<string:address>")
@handle_exception
def get_dataSource_by_short_key_and_tumbleweed_address(short_key, address):
    tumbleweed_dto = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed_by_address(address)
    tumbleweed_dto = tumbleweed_dto[0] #TODO: find a better fix for tws with same id
    if tumbleweed_dto is None:
        return jsonify({"info": f"No Tumbleweed with address {address.id} exists."}), 400
    found_dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource_by_tumbleweed_id_and_short_key(tumbleweed_dto.id, short_key)
    if found_dataSource is None:
        return jsonify({"info": f"No data sources for Tumbleweed {tumbleweed_dto.id} and short key {short_key} exist."}), 400
    else:
        result = app.config["TUMBLEWEB_DATASOURCE_SCHEMA"].dump(found_dataSource)
        return jsonify(result)


@app.route("/get-datapoint-by-dataSource-id-and-datapoint-id/<int:dataSource_id>/<int:datapoint_id>", methods=["GET"])
@handle_exception
def get_datapoint_by_dataSource_id_and_datapoint_id(dataSource_id, datapoint_id):
    dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource(dataSource_id)
    if dataSource is None:
        return jsonify({"info": f"No Data Source with id {dataSource_id} exists."}), 400
    if dataSource.dtype == DType.Long:
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_longdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No Data Point with id {datapoint_id} exists for data source {dataSource_id}."}), 400
        result = app.config["TUMBLEWEB_LONGDATA_SCHEMA"].dump(datapoint)
        return jsonify(result)
    elif dataSource.dtype == DType.Int:
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_intdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No Data Point with id {datapoint_id} exists for data source {dataSource_id}."}), 400
        result = app.config["TUMBlEWEB_INTDATA_SCHEMA"].dump(datapoint)
        return jsonify(result)
    elif dataSource.dtype == DType.Float:
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_floatdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No Data Point with id {datapoint_id} exists for data source {dataSource_id}."}), 400
        result = app.config["TUMBLEWEB_FLOATDATA_SCHEMA"].dump(datapoint)
        return jsonify(result)
    elif dataSource.dtype == DType.String:
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_stringdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No Data Point with id {datapoint_id} exists for data source {dataSource_id}."}), 400
        result = app.config["TUMBLEWEB_STRINGDATA_SCHEMA"].dump(datapoint)
        return jsonify(result)
    elif dataSource.dtype == DType.Byte:
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_bytedatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No Data Point with id {datapoint_id} exists for data source {dataSource_id}."}), 400
        result = app.config["TUMBLEWEB_BYTEDATA_SCHEMA"].dump(datapoint)
        return jsonify(result)
    elif dataSource.dtype == DType.Image:
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_imagedatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No Data Point with id {datapoint_id} exists for data source {dataSource_id}."}), 400
        result = app.config["TUMBLEWEB_IMAGEDATA_SCHEMA"].dump(datapoint)
        return jsonify(result)
    else:
        return jsonify({"info": f"Data source {dataSource_id} has an invalid dtype."}), 400


@app.route("/get-datapoints-by-dataSource-and-run/<int:dataSource_id>/<int:run_id>", methods=["GET"])
@handle_exception
def get_datapoints_by_dataSource_and_run(dataSource_id, run_id):
    dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource(dataSource_id)
    if dataSource is None:
        return jsonify({"info": f"No dataSource with id {dataSource_id} exists."}), 400
    run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_run(run_id)
    if run is None:
        return jsonify({"info": f"No run with id {run_id} exists."}), 400
    if dataSource.dtype == DType.Long:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_longdatapoints_by_dataSource_and_run(dataSource_id, run_id)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_LONGDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Int:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_intdatapoints_by_dataSource_and_run(dataSource_id, run_id)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBlEWEB_INTDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Float:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_floatdatapoints_by_dataSource_and_run(dataSource_id, run_id)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_FLOATDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.String:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_stringdatapoints_by_dataSource_and_run(dataSource_id, run_id)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_STRINGDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Byte:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_bytedatapoints_by_dataSource_and_run(dataSource_id, run_id)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_BYTEDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Image:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_imagedatapoints_by_dataSource_and_run(dataSource_id, run_id)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_IMAGEDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    else:
        return jsonify({"info": f"Data source {dataSource_id} has an invalid dtype."}), 400


@app.route("/get-datapoints-by-dataSource-and-run-interval/<int:dataSource_id>/<int:run_id>/<string:start>/<string:end>", methods=["GET"])
@handle_exception
def get_datapoints_by_dataSource_and_run_interval(dataSource_id, run_id, start, end):
    if start != "null":
        start = datetime.fromisoformat(start)
    else:
        start = datetime.fromisoformat('1970-01-01T00:00:00+00:00')
    if end != "null":
        end = datetime.fromisoformat(end)
    else:
        end = datetime.now(timezone.utc)
    dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource(dataSource_id)
    if dataSource is None:
        return jsonify({"info": f"No dataSource with id {dataSource_id} exists."}), 400
    run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_run(run_id)
    if run is None:
        return jsonify({"info": f"No run with id {run_id} exists."}), 400
    if dataSource.dtype == DType.Long:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_longdatapoints_by_dataSource_and_run_interval(dataSource_id, run_id, start, end)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_LONGDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Int:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_intdatapoints_by_dataSource_and_run_interval(dataSource_id, run_id, start, end)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBlEWEB_INTDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Float:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_floatdatapoints_by_dataSource_and_run_interval(dataSource_id, run_id, start, end)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_FLOATDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.String:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_stringdatapoints_by_dataSource_and_run_interval(dataSource_id, run_id, start, end)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_STRINGDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Byte:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_bytedatapoints_by_dataSource_and_run_interval(dataSource_id, run_id, start, end)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_BYTEDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    elif dataSource.dtype == DType.Image:
        datapoints = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_imagedatapoints_by_dataSource_and_run_interval(dataSource_id, run_id, start, end)
        if datapoints is None:
            return jsonify({"info": f"No datapoints for data source {dataSource_id} and run {run_id} exist."}), 400
        result = app.config["TUMBLEWEB_IMAGEDATA_SCHEMA"].dump(datapoints, many=True)
        return jsonify(result)
    else:
        return jsonify({"info": f"Data source {dataSource_id} has an invalid dtype."}), 400


@app.route("/get-tumbleweeds", methods=["GET"])
@handle_exception
def get_tumbleweeds():
    found_tumbleweeds = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweeds()
    if found_tumbleweeds is None:
        return jsonify({"info": f"No Tumbleweeds exist."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].dump(found_tumbleweeds, many=True)
        return jsonify(result)


@app.route("/get-tumblebases", methods=["GET"])
@handle_exception
def get_tumbleBases():
    found_tumbleBases = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumblebases()
    if found_tumbleBases is None:
        return jsonify({"info": f"No TumbleBases exist."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"].dump(found_tumbleBases, many=True)
        return jsonify(result)


@app.route("/get-commandTypes", methods=["GET"])
@handle_exception
def get_commandTypes():
    found_commandTypes = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_commandTypes()
    if found_commandTypes is None:
        return jsonify({"info": f"No Command Types exist."}), 400
    else:
        result = app.config["TUMBLEWEB_COMMANDTYPE_SCHEMA"].dump(found_commandTypes, many=True)
        return jsonify(result)
#
#   Routes to update resources
#


@app.route("/update-tumbleweed/<int:tumbleweed_id>", methods=["PATCH"])
@handle_exception
def update_tumbleweed(tumbleweed_id):
    tumbleweed_json = request.get_json()
    tumbleweed_to_update = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].load(tumbleweed_json)
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"The Tumbleweed with ID {tumbleweed_id} was not found."}), 400
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_tumbleweed(tumbleweed_id, tumbleweed_to_update)
    return jsonify({"info": tumbleweed_id})


@app.route("/update-tumblebase/<int:tumblebase_id>", methods=["PATCH"])
@handle_exception
def update_tumblebase(tumblebase_id):
    tumblebase_json = request.get_json()
    tumblebase_to_update = app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"].load(tumblebase_json)
    tumblebase = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumblebase(tumblebase_id)
    if tumblebase is None:
        return jsonify({"info": f"The Tumblebase with ID {tumblebase_id} was not found."}), 400
    tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_tumblebase(tumblebase_id, tumblebase_to_update)
    return jsonify({"info": tumblebase_id})


@app.route("/update-subSystem/<int:subSystem_id>", methods=["PATCH"])
@handle_exception
def update_subSystem(subSystem_id):
    subSystem_json = request.get_json()
    subSystem_to_update = app.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"].load(subSystem_json)
    subSystem = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_subSystem(subSystem_id)
    if subSystem is None:
        return jsonify({"info": f"The SubSystem with ID {subSystem_id} was not found."}), 400
    subSystem_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_subSystem(subSystem_id, subSystem_to_update)
    return jsonify({"info": subSystem_id})


@app.route("/update-dataSource/<int:dataSource_id>", methods=["PATCH"])
@handle_exception
def update_dataSource(dataSource_id):
    dataSource_json = request.get_json()
    dataSource_to_update = app.config["TUMBLEWEB_DATASOURCE_SCHEMA"].load(dataSource_json)
    dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource(dataSource_id)
    if dataSource is None:
        return jsonify({"info": f"The Data Source with ID {dataSource_id} was not found."}), 400
    dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_dataSource(dataSource_id, dataSource_to_update)
    return jsonify({"info": dataSource_id})


@app.route("/update-commandType/<int:commandType_id>", methods=["PATCH"])
@handle_exception
def update_commandType(commandType_id):
    commandType_json = request.get_json()
    commandType_to_update = app.config["TUMBLEWEB_COMMANDTYPE_SCHEMA"].load(commandType_json)
    commandType = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_commandType(commandType_id)
    if commandType is None:
        return jsonify({"info": f"The Command Type with ID {commandType_id} was not found."}), 400
    commandType_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_commandType(commandType_id, commandType_to_update)
    return jsonify({"info": commandType_id})


@app.route("/update-run/<int:run_id>", methods=["PATCH"])
@handle_exception
def update_run(run_id):
    run_json = request.get_json()
    run_to_update = app.config["TUMBLEWEB_RUN_SCHEMA"].load(run_json)
    run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_run(run_id)
    if run is None:
        return jsonify({"info": f"The run with ID {run_id} was not found."}), 400
    run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_run(run_id, run_to_update)
    return jsonify({"info": run_id})


@app.route("/update-command/<int:command_id>", methods=["PATCH"])
@handle_exception
def update_command(command_id):
    command_json = request.get_json()
    command_to_update = app.config["TUMBLEWEB_COMMAND_SCHEMA"].load(command_json)
    command = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_command(command_id)
    if command is None:
        return jsonify({"info": f"The command with ID {command_id} was not found."}), 400
    command_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_command(command_id, command_to_update)
    return jsonify({"info": command_id})


@app.route("/update-datapoint/<string:dtype>/<int:datapoint_id>", methods=["PATCH"])
@handle_exception
def update_datapoint(dtype, datapoint_id):
    datapoint_json = request.get_json()
    if dtype == DType.Long.value:
        datapoint_to_update = app.config["TUMBLEWEB_LONGDATA_SCHEMA"].load(datapoint_json)
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_longdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No long datapoint with ID {datapoint_id} was found."}), 400
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_longdatapoint(datapoint_id, datapoint_to_update)
        return jsonify({"info": datapoint_id})
    elif dtype == DType.Int.value:
        datapoint_to_update = app.config["TUMBlEWEB_INTDATA_SCHEMA"].load(datapoint_json)
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_intdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No int datapoint with ID {datapoint_id} was found."}), 400
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_intdatapoint(datapoint_id, datapoint_to_update)
        return jsonify({"info": datapoint_id})
    elif dtype == DType.Float.value:
        datapoint_to_update = app.config["TUMBLEWEB_FLOATDATA_SCHEMA"].load(datapoint_json)
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_floatdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No float datapoint with ID {datapoint_id} was found."}), 400
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_floatdatapoint(datapoint_id, datapoint_to_update)
        return jsonify({"info": datapoint_id})
    elif dtype == DType.String.value:
        datapoint_to_update = app.config["TUMBLEWEB_STRINGDATA_SCHEMA"].load(datapoint_json)
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_stringdatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No string datapoint with ID {datapoint_id} was found."}), 400
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_stringdatapoint(datapoint_id, datapoint_to_update)
        return jsonify({"info": datapoint_id})
    elif dtype == DType.Byte.value:
        datapoint_to_update = app.config["TUMBLEWEB_BYTEDATA_SCHEMA"].load(datapoint_json)
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_bytedatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No byte datapoint with ID {datapoint_id} was found."}), 400
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_bytedatapoint(datapoint_id, datapoint_to_update)
        return jsonify({"info": datapoint_id})
    elif dtype == DType.Image.value:
        datapoint_to_update = app.config["TUMBLEWEB_IMAGEDATA_SCHEMA"].load(datapoint_json)
        datapoint = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_imagedatapoint(datapoint_id)
        if datapoint is None:
            return jsonify({"info": f"No image datapoint with ID {datapoint_id} was found."}), 400
        datapoint_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].update_imagedatapoint(datapoint_id, datapoint_to_update)
        return jsonify({"info": datapoint_id})
    else:
        return jsonify({"info": f"Invalid data type {dtype}."}), 400



#
#   Routes to delete resources
#


@app.route("/delete-dataSource/<int:dataSource_id>", methods=["DELETE"])
@handle_exception
def delete_dataSource(dataSource_id):
    dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource(dataSource_id)
    if dataSource is None:
        return jsonify({"info": f"The DataSource with ID {dataSource_id} was not found."}), 400
    dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].delete_dataSource(dataSource_id)
    if dataSource_id is None:
        return jsonify({"info": f"The DataSource with ID {dataSource_id} cannot be deleted."}), 400
    return jsonify({"info": dataSource_id})


@app.route("/delete-subSystem/<int:subSystem_id>", methods=["DELETE"])
@handle_exception
def delete_subSystem(subSystem_id):
    subSystem = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_subSystem(subSystem_id)
    if subSystem is None:
        return jsonify({"info": f"The Sub System with ID {subSystem_id} was not found."}), 400
    subSystem_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].delete_subSystem(subSystem_id)
    if subSystem_id is None:
        return jsonify({"info": f"The Sub System with ID {subSystem_id} cannot be deleted."}), 400
    return jsonify({"info": subSystem_id})


@app.route("/delete-tumbleweed/<int:tumbleweed_id>", methods=["DELETE"])
@handle_exception
def delete_tumbleweed(tumbleweed_id):
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed(tumbleweed_id)
    if tumbleweed is None:
        return jsonify({"info": f"The Tumbleweed with ID {tumbleweed_id} was not found."}), 400
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].delete_tumbleweed(tumbleweed_id)
    if tumbleweed_id is None:
        return jsonify({"info": f"The Tumbleweed with ID {tumbleweed_id} cannot be deleted."}), 400
    return jsonify({"info": tumbleweed_id})


@app.route("/delete-commandType/<int:commandType_id>", methods=["DELETE"])
@handle_exception
def delete_commandType(commandType_id):
    commandType = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_commandType(commandType_id)
    if commandType is None:
        return jsonify({"info": f"The Command Type with ID {commandType_id} was not found."}), 400
    commandType_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].delete_commandType(commandType_id)
    if commandType_id is None:
        return jsonify({"info": f"The Command Type with ID {commandType_id} cannot be deleted."}), 400
    return jsonify({"info": commandType_id})


@app.route("/delete-run/<int:run_id>", methods=["DELETE"])
@handle_exception
def delete_run(run_id):
    run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_run(run_id)
    if run.ended_at is None:
        return jsonify({"info": f"The Run with ID {run_id} is still active."}), 400
    if run is None:
        return jsonify({"info": f"The Run with ID {run_id} was not found."}), 400
    run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].delete_run(run_id)
    if run_id is None:
        return jsonify({"info": f"The Run with ID {run_id} cannot be deleted."}), 400
    return jsonify({"info": run_id})


@app.route("/delete-tumblebase/<int:tumblebase_id>", methods=["DELETE"])
@handle_exception
def delete_tumblebase(tumblebase_id):
    tumblebase = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumblebase(tumblebase_id)
    if tumblebase is None:
        return jsonify({"info": f"The Tumblebase with ID {tumblebase_id} was not found."}), 400
    tumblebase_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].delete_tumblebase(tumblebase_id)
    if tumblebase_id is None:
        return jsonify({"info": f"The Tumblebase with ID {tumblebase_id} cannot be deleted."}), 400
    return jsonify({"info": tumblebase_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8006")
