import configparser
from os import environ


# MS stand for Monitor Service
class InfluxConfig:

    @staticmethod
    def get_config():

        if environ.get('MS_CONF_FILE') is None:
            conf_file = "config.ini"
        else:
            conf_file = environ.get('MS_CONF_FILE')

        config_parse = configparser.ConfigParser()
        config_parse.read(conf_file)
        config = dict()
        config['conf_file'] = conf_file
        config['bucket_name'] = config_parse['bucket']['name']
        config['influx2_org'] = config_parse['influx2']['org']

        return config
