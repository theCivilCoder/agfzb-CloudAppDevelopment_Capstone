/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */


function main(params) {
  let result = {};
  //if param state is provided, create query to match the state
  if (params.state) {
    result["query"] = {
      "selector": {
        "st": params.state
      },
      "use_index": "state_index"
    }
  }
  //otherwise, select all dealerships
  else {
    result["query"] = {
      "selector": {
        "id": {
          "$exists": true
        }
      }
    }
  }
  return result;
}