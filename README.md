[![Build Status - GitHub](https://github.com/ggnanasekaran77/urlrag/workflows/pytesting/badge.svg)](https://github.com/ggnanasekaran77/urlrag/actions?query=workflow%3Apytesting)
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
URL_CSV_FILE=/tmp/urls.csv docker-compose up -d
# or
URL_CSV_FILE=./urls.csv docker-compose up -d
# To shutdown
docker-compose down
```

## To Open this app
* If local in browser open [http://localhost:8000](http://localhost:8000)
* If any server http://server_ip:8000

## Tech stack
* Python 3.9 
* FastApi
* InfluxDB - Time serious database
* Jinja2 Template
* GitHub Actions  
* Html

## Links
* [GitHub Actions CI](#gitHub-actions-ci)
* [10000 URLs with 4CPU Result](#1000-urls)
* [Results Screenshots](#results-screenshots)
* [Sample Demo Video](#demo-video)

## Improvements
* logger integration
* Python documentation
* Input validations
* Test Containers for pytest
* Deployment or CD

## GitHub Actions CI
![gitHub-actions-ci](./images/github_actions_ci.png)

## 10000 URLs
![1000 URLs](./images/10000_urls.png)

## Results Screenshots
![Results Screenshots](./images/results.png)
![Results Screenshots](./images/results1.png)

## Docker Settings
![Docker Settings](./images/docker_settings.png)

## Demo Video
https://user-images.githubusercontent.com/8940344/126400352-f285aa40-1e83-4e2d-a909-912c6c5c0ba2.mp4


