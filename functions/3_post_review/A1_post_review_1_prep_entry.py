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
    fields = ["id", "name", "dealership", "review", "purchase",
              "purchase_date", "car_make", "car_model", "car_year"]
              
    list_int_fields = ["id", "dealership", "car_year"]          
    doc = {}
    for field in fields:
        if field in list(dict["review"].keys()):
            input = dict["review"][field]
            doc[field] = input

    return {"doc": doc}