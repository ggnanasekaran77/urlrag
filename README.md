[![Build Status - GitHub](https://github.com/ggnanasekaran77/monitor-service/workflows/pytesting/badge.svg)](https://github.com/ggnanasekaran77/monitor-service/actions?query=workflow%3Apytesting)
# URLRAG 
URL Red Amber Green status

## Requirements 
* docker 20.10+ (20.10.5)
* docker-compose 1.28+ (1.28.5)
* docker with 6CPU 8GB, refer this screenshot [docker settings](#docker-settings)

## INPUT
* CSV file
* Data Format, header should be similar
* Sample data 
```csv
name,url
google,https://www.google.com
credit-suisse,https://www.credit-suisse.com/sg/en.html
gnanam,https://ggnanasekaran.com
```

## To RUN this App on MacOS
```shell
unzip urlrag.zip
cd urlrag
# URL_CSV_FILE=<<File Path>> docker-compose up
# Example below
URL_CSV_FILE=/tmp/urls.csv docker-compose up
# or
URL_CSV_FILE=./urls.csv docker-compose up
```

## Docker Settings
![Docker Settings](./images/docker_settings.png)
