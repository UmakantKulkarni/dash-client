#!/usr/bin/env python3
import logging
import config_dash
import sys
from time import strftime
import json


def configure_log_file(playback_type="", log_file=""):
    """ Module to configure the log file and the log parameters.
    Logs are streamed to the log file as well as the screen.
    Log Levels: CRITICAL:50, ERROR:40, WARNING:30, INFO:20, DEBUG:10, NOTSET	0
    """
    if log_file == "":
        log_file = config_dash.LOG_FILENAME
    config_dash.LOG = logging.getLogger(config_dash.LOG_NAME)
    config_dash.LOG_LEVEL = logging.INFO
    config_dash.LOG.setLevel(config_dash.LOG_LEVEL)
    log_formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
    # Add the handler to print to the screen
    handler1 = logging.StreamHandler(sys.stdout)
    handler1.setFormatter(log_formatter)
    config_dash.LOG.addHandler(handler1)
    # Add the handler to for the file if present
    if log_file:
        #log_filename = "_".join(
        #    (log_file, playback_type, strftime('%Y-%m-%d.%H_%M_%S.log')))
        print(("Configuring log file: {}".format(log_file)))
        handler2 = logging.FileHandler(filename=log_file)
        handler2.setFormatter(log_formatter)
        config_dash.LOG.addHandler(handler2)
        print(("Started logging in the log file:{}".format(log_file)))


def write_json(json_data="", json_file=""):
    """
    :param json_data: dict
    :param json_file: json file
    :return: None
    """
    if json_data == "":
        json_data = config_dash.JSON_HANDLE
    if json_file == "":
        json_file = config_dash.JSON_LOG
    with open(json_file, 'wb') as json_file_handle:
        json_file_handle.write(json.dumps(json_data).encode())
