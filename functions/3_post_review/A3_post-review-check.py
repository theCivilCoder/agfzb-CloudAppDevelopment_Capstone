#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

def main(dict):

    if dict["ok"] != True:
        result = {"error": {"status": 500,
                            "msg": "Something went wrong on the server"}}
    else:
        result = {"result": dict}

    return result
