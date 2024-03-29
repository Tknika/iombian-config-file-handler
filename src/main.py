#!/usr/bin/env python3

import logging
import os
import signal

from communication_module import CommunicationModule
from iombian_yaml_handler import IoMBianYAMLHandler
from reply_server import ReplyServer
from sub_client import SubClient

CONFIG_PORT = int(os.environ.get("CONFIG_PORT", 5555))
RESET_EVENT = os.environ.get("RESET_EVENT", "long_long_click")
LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.INFO)
BUTTON_EVENTS_HOST = os.environ.get("BUTTON_EVENTS_HOST", "127.0.0.1")
BUTTON_EVENTS_PORT = int(os.environ.get("BUTTON_EVENTS_PORT" , 5556))
YAML_FILE_PATH = os.environ.get("YAML_FILE_PATH", "/app/parameters.yml")
SHUTDOWN_SERVICE_HOST = os.environ.get("SHUTDOWN_SERVICE_HOST", "127.0.0.1")
SHUTDOWN_SERVICE_PORT = int(os.environ.get("SHUTDOWN_SERVICE_PORT", 5558))

CONFIG_HOST = "0.0.0.0"
RESET_COMMAND = "reboot"

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s - %(name)-16s - %(message)s', level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def stop():
    logger.info("Stopping IoMBian Config File Handler")
    if server:
        server.stop()
    if client:
        client.stop()
    if comm_module:
        comm_module.stop()


def signal_handler(sig, frame):
    stop()


def config_update_callback():
    logger.info("Rebooting the system")
    logger.debug(f"Sending {RESET_COMMAND} command to {SHUTDOWN_SERVICE_HOST}:{SHUTDOWN_SERVICE_PORT}")
    comm_module.execute_command(RESET_COMMAND)
    stop()


def button_event_callback(event):
    logger.debug(f"'{event}' event received")
    if event == RESET_EVENT:
        logger.info("Resetting 'parameters.yaml' file")
        yaml_handler.reset()


if __name__ == "__main__":
    logger.info("Starting IoMBian Config File Handler")

    server, client = None, None

    yaml_handler = IoMBianYAMLHandler(YAML_FILE_PATH)
    yaml_handler.on_config_update(config_update_callback)
    yaml_handler.load_file()

    server = ReplyServer(yaml_handler, host=CONFIG_HOST, port=CONFIG_PORT)
    server.start()

    client = SubClient(
        on_message_callback=button_event_callback, host=BUTTON_EVENTS_HOST, port=BUTTON_EVENTS_PORT)
    client.start()

    comm_module = CommunicationModule(host=SHUTDOWN_SERVICE_HOST, port=SHUTDOWN_SERVICE_PORT)
    comm_module.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()
