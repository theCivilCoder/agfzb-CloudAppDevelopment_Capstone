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
    # Check for errors
    try:
        error = dict["error"]
        return {"error": {"status": 500, "msg": "Something went wrong on the server", "params": dict}}
        
    except Exception as e:
        if dict["docs"] == []:
            return {"error": {"status": 404, "msg": "DealerId does not exist so nothing is returned."}}
        # No error present
        docs = [entry(doc) for doc in dict["docs"]]
        return {"entries": docs}


#remove the unecessary tags
def entry(doc):
    doc.pop("_id")
    doc.pop("_rev")
    return doc