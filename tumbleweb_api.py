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
import requests


"""
Flask is built for extensions. Use the config to add new keywords and new resources which can be used in the
endpoint definitions. This is needed for example for testing. Now it is possible to connect a business logic
which is connected to a test database and everything runs over the app config.
"""

app = Flask(__name__)
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
    run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].start_run(run_to_insert, tumbleweed_id)
    if run_id is None:
        return jsonify({"info": f"The Run cannot be added."}), 400
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
        return jsonify({"info": f"The Tumbleweed {tumbleweed_id} is currently not active"})
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
    response = requests.post(f"http://{tumblebase.host}:{tumblebase.port}{tumblebase.command_route}", json=json_request)
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
    tumbleweed = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweed_by_address(tumbleweed_address)
    if tumbleweed is None:
        return jsonify({"info": f"The Tumbleweed with address {tumbleweed_address} does not exist."}), 400
    dataSource = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSource_by_tumbleweed_address_and_short_key(tumbleweed.id, short_key)
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
    active_run = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_active_run(tumbleweed.id)
    if active_run is None:
        run_json = {
            "name": "Unnamed run",
            "description": "Default run."
        }
        run_to_insert = app.config["TUMBLEWEB_RUN_SCHEMA"].load(run_json)
        run_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].start_run(run_to_insert, tumbleweed.id)
    else:
        run_id = active_run.id
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


"""
@app.route("/get-subSystem/<int:subSystem_id>", methods=["GET"])
@handle_exception
def get_subSystem(subSystem_id):
    found_subSystem = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_subSystem(subSystem_id)
    if found_subSystem is None:
        return jsonify({"info": f"No subSystem with id {subSystem_id} exists."}), 400
    else:
        result = app.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"].dump(found_subSystem)
        return jsonify(result)

@app.route("/get-tumbleweeds", methods=["GET"])
@handle_exception
def get_tumbleweeds():
    found_tumbleweeds = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweeds()
    if found_tumbleweeds is None:
        return jsonify({"info": f"No Tumbleweeds exist."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].dump(found_tumbleweeds, many=True)
        return jsonify(result)

@app.route("/get-dataSources/<int:tumbleweed_id>", methods=["GET"])
@handle_exception
def get_dataSources(tumbleweed_id):
    found_dataSources = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_dataSources_by_tumbleweed_id(tumbleweed_id)
    if found_dataSources is None:
        return jsonify({"info": f"No DataSources exist for tumbleweed {tumbleweed_id}."}), 400
    else:
        result = app.config["TUMBLEWEB_DATASOURCE_SCHEMA"].dump(found_dataSources, many=True)
        return jsonify(result)

@app.route("/get-tumbleBases", methods=["GET"])
@handle_exception
def get_tumbleBases():
    found_tumbleBases = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleBases()
    if found_tumbleBases is None:
        return jsonify({"info": f"No TumbleBases exist."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEBASE_SCHEMA"].dump(found_tumbleBases, many=True)
        return jsonify(result)
"""

#
#   Routes to update resources
#

@app.route("/edit-tumbleweed/<int:tumbleweed_id>", methods=["POST"])
@handle_exception
def edit_tumbleweed(tumbleweed_id):
    tumbleweed_json = request.get_json()
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8006")
