import configparser

from influxdb_client import InfluxDBClient
from jinja2 import Template


def http_status_code():
    client = InfluxDBClient.from_config_file("config.ini")

    config = configparser.ConfigParser()
    config.read('config.ini')
    bucket = config['bucket']['name']

    query = '''from(bucket: "{{bucket}}") 
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "http_status_code") 
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") 
    '''

    tm = Template(query)
    influx_query = tm.render(bucket=bucket)
    result = client.query_api().query(query=influx_query)

    return result
