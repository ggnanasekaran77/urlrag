import csv
import requests

with open('sample.csv', 'r') as file:
    reader = csv.reader(file)
    name = ""
    url = ""
    count = 0
    for row in reader:
        name = row[0]
        url = row[1]
        x = requests.get(url)
        count += 1
        print(f'count: {count} name: {name} url: {url} http_code: {x.status_code}')