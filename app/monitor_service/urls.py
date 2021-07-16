import csv
import requests
import threading
from . import config

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def insert_influxdb(domain_name, domain_url, http_status_code):
    influx_config = config.InfluxConfig.get_config()
    bucket = influx_config['bucket_name']
    org = influx_config['influx2_org']
    conf_file = influx_config['conf_file']

    client = InfluxDBClient.from_config_file(conf_file)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = Point("http_status_code") \
        .tag("monitor_type", "http_status_code") \
        .field("domain_name", domain_name) \
        .field("domain_url", domain_url) \
        .field("http_status_code", http_status_code) \
        .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, org, point)


def http_code(domain_name, domain_url):
    http_status_code = requests.head(domain_url, timeout=2).status_code
    print(f"domain_name: {domain_name}, domain_url: {domain_url}, http_status_code: {http_status_code}")
    insert_influxdb(domain_name, domain_url, http_status_code)


def csv_parse(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            url = row[1]
            threading.Thread(http_code(name, url)).start()
