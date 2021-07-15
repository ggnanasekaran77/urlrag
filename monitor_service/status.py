from influxdb import InfluxDBClient


def http_status_code():
    client = InfluxDBClient('localhost', 8086, 'admin', 'admin123', 'mydb')
    result = list(map(list, client.query('select domain_name, domain_url,http_status_code from http_status_code;')))[0]

    return result
