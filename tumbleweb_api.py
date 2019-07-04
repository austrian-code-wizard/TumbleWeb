from util.utils import internal_server_error_message, invalid_format_message, endpoint_not_found_message, \
    method_not_allowed_message, could_not_verify_message, invalid_token_message, no_admin_message
from exception.custom_exceptions import TumbleWebException, InternalServerError
from model.schema import TumbleweedSchema, TumbleBaseSchema, RunSchema, CommandSchema, CommandTypeSchema, DataSourceSchema, SubSystemSchema, LongDataSchema, IntDataSchema, FloatDataSchema, StringDataSchema, ByteDataSchema
from businesslogic.busineslogic import TumbleWebLogic
from flask import Flask, request, jsonify
from logger.logger import LoggerFactory
from marshmallow import ValidationError
from functools import wraps


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

@app.route("/add-subSystem", methods=["POST"])
@handle_exception
def add_subSystem():
    subSystem_json = request.get_json()
    subSystem_to_insert = app.config["TUMBLEWEB_SUBSYSTEM_SCHEMA"].load(subSystem_json)
    subSystem_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_subSystem(subSystem_to_insert)
    if subSystem_id is None:
        return jsonify({"info": f"The SubSystem cannot be added."}), 400
    else:
        return jsonify({"info": subSystem_id})

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

@app.route("/add-dataSource", methods=["POST"])
@handle_exception
def add_dataSource():
    dataSource_json = request.get_json()
    dataSource_to_insert = app.config["TUMBLEWEB_DATASOURCE_SCHEMA"].load(dataSource_json)
    dataSource_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_dataSource(dataSource_to_insert)
    if dataSource_id is None:
        return jsonify({"info": f"The DataSource cannot be added."}), 400
    else:
        return jsonify({"info": dataSource_id})

@app.route("/add-subSystem-to-tumbleweed/<int:subSystem_id>/<int:tumbleweed_id>", methods=["POST"])
@handle_exception
def add_subSystem_to_tumbleweed(subSystem_id, tumbleweed_id):
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_subSystem_to_tumbleweed(subSystem_id, tumbleweed_id)
    if tumbleweed_id is None:
        return jsonify({"info": f"The SubSystem {subSystem_id} cannot be added to Tumbleweed {tumbleweed_id}"})
    else:
        return jsonify({"info": tumbleweed_id})

@app.route("/add-dataSource-to-subSystem/<int:dataSource_id>/<int:subSystem_id>", methods=["POST"])
@handle_exception
def add_dataSource_to_subSystem(dataSource_id, subSystem_id):
    subSystem_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].add_dataSource_to_subSystem(dataSource_id, subSystem_id)
    if subSystem_id is None:
        return jsonify({"info": f"The DataSource {dataSource_id} cannot be added to SubSystem {subSystem_id}"})
    else:
        return jsonify({"info": subSystem_id})

@app.route("/get-tumbleweeds", methods=["GET"])
@handle_exception
def get_tumbleweeds():
    found_tumbleweeds = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweeds()
    if found_tumbleweeds is None:
        return jsonify({"info": f"No Tumbleweeds exist."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].dump(found_tumbleweeds, many=True)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8006")
