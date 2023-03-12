#!/usr/bin/env python3

import logging
import os
import signal

from iombian_yaml_handler import IoMBianYAMLHandler
from reply_server import ReplyServer
from sub_client import SubClient

logging.basicConfig(format='%(asctime)s %(levelname)-8s - %(name)-16s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

YAML_FILE_PATH = "/boot/config/parameters.yml"
SERVER_PORT = 5555
CLIENT_PORT = 5556
RESET_EVENT = "long_long_click"


def config_update_callback():
    logger.info("Rebooting the system")
    os.system('reboot')


def button_event_callback(event):
    logger.debug(f"'{event}' event received")
    if event == RESET_EVENT:
        logger.info("Resetting 'parameters.yaml' file")
        yaml_handler.reset()


def signal_handler(sig, frame):
    logger.info("Stopping IoMBian Config File Handler")
    if server: server.stop()
    if client: client.stop()


if __name__ == "__main__":
    logger.info("Starting IoMBian Config File Handler")
    
    server, client = None, None

    yaml_handler = IoMBianYAMLHandler(YAML_FILE_PATH)
    yaml_handler.on_config_update(config_update_callback)
    yaml_handler.load_file()

    server = ReplyServer(yaml_handler, port=SERVER_PORT)
    server.start()

    client = SubClient(on_message_callback=button_event_callback, port=CLIENT_PORT)
    client.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()
