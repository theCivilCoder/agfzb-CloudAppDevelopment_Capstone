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
    try:
        dealerId = dict["dealerId"]
    except Exception as e:
        dealerId = "all"
    else:
        # dealerId is present but value is empty
        if dealerId is "":
            dealerId = "all"
    finally:
        # if no dealerId was given or parameter is empty, select all reviews from all dealerships
        if dealerId == "all":
            result = {
                "query": {
                    "selector": {
                        "id": {
                            "$exists": True
                        }
                    }
                }
            }
        # if dealerId is given, retrieve reviews for that delarship only
        else:
            result = {
                "query": {
                    "selector": {
                        "dealership": int(dealerId)
                    },
                    "use_index": "dealer_id"
                }
            }

    return result