"""
Get the last 1hour data from influxdb and return sorted output based http_response_code
"""
from . import config

from influxdb_client import InfluxDBClient
from jinja2 import Template


def main():
    influx_config = config.InfluxConfig.get_config()
    bucket = influx_config['bucket_name']
    conf_file = influx_config['conf_file']
    client = InfluxDBClient.from_config_file(conf_file)

    query = '''from(bucket: "{{bucket}}") 
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "http_response_code") 
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            |> sort(columns:["http_response_code", "_value"], desc: true)
            |> limit(n:11000)
    '''

    tm = Template(query)
    influx_query = tm.render(bucket=bucket)
    result = client.query_api().query(query=influx_query)

    try:
        if len(result) <= 0:
            result = False
    except:
        print("Result is not empty table")

    return result

