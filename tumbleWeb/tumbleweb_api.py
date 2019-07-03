from tumbleWeb.util.utils import internal_server_error_message, invalid_format_message, endpoint_not_found_message, \
    method_not_allowed_message, could_not_verify_message, invalid_token_message, no_admin_message
from tumbleWeb.exception.custom_exceptions import TumbleWebException, InternalServerError
from tumbleWeb.model.schema import TumbleweedSchema, TumbleBaseSchema, RunSchema, CommandSchema, CommandTypeSchema, DataSourceSchema, SubSystemSchema, LongDataSchema, IntDataSchema, FloatDataSchema, StringDataSchema, ByteDataSchema
from tumbleWeb.businesslogic.busineslogic import TumbleWebLogic
from flask import Flask, request, jsonify
from tumbleWeb.logger.logger import LoggerFactory
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
def add_message():
    tumbleweed_json = request.get_json()
    tumbleweed_to_insert = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].load(tumbleweed_json)
    tumbleweed_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_tumbleweed(tumbleweed_to_insert)
    if tumbleweed_id is None:
        return jsonify({"info": f"The tumbleweed cannot be added."}), 400
    else:
        return jsonify({"info": tumbleweed_id})


@app.route("/get-tumbleweeds", methods=["GET"])
@handle_exception
def get_image():
    found_tumbleweeds = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_tumbleweeds()
    if found_tumbleweeds is None:
        return jsonify({"info": f"No Tumbleweeds exist."}), 400
    else:
        result = app.config["TUMBLEWEB_TUMBLEWEED_SCHEMA"].dump(found_tumbleweeds, many=True)
        return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8006")
