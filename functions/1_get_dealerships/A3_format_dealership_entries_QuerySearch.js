/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const md5 = require('spark-md5');

function main(params) {

return {
    entries: params.docs.map((row) => { return {
        id: row.id,
        city: row.city,
        state: row.state,
        st: row.st,
        address:row.address,
        zip: row.zip,
        lat: row.lat,
        long: row.long,
        short_name: row.short_name,
        full_name: row.full_name,
    }})
  };
}
