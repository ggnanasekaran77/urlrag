import csv
import requests
import threading
from datetime import datetime

from influxdb import InfluxDBClient
from datetime import datetime


def insert_influxdb(domain_name, domain_url, http_status_code):
    client = InfluxDBClient('localhost', 8086, 'admin', 'admin123', 'mydb')
    client.create_database('mydb')
    client.get_list_database()
    client.switch_database('mydb')

    # Setup Payload
    json_payload = []
    data = {
        "measurement": "http_status_code",
        "tags": {
            "monitor_type": "http_status_code"
        },
        "time": datetime.now(),
        "fields": {
            'domain_name': domain_name,
            'domain_url': domain_url,
            'http_status_code': http_status_code
        }
    }
    json_payload.append(data)

    # Send our payload
    client.write_points(json_payload)


def http_code(domain_name, domain_url):
    global count
    http_status_code = requests.head(domain_url, timeout=2).status_code
    print(f"domain_name: {domain_name}, domain_url: {domain_url}, http_status_code: {http_status_code}")
    try:
        insert_influxdb(domain_name, domain_url, http_status_code)
    except:
        print(f"WARN: http_code Unable to insert http_status_code to influxdb for domain_name: {domain_name}, url: {domain_url}")


def csv_parse(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            url = row[1]
            try:
                threading.Thread(http_code(name, url)).start()
            except:
                print(f"WARN: csv_parse Unable to get http_status_code for name: {name}, url: {url}")
