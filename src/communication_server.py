#!/usr/bin/env python3

import logging
import threading
import time
import zmq

logger = logging.getLogger(__name__)


class CommunicationServer():

    def __init__(self, commands_provider, host="127.0.0.1", port=5555):
        self.commands_provider = commands_provider
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.listen_thread = None
        self.listen = False

    def start(self):
        logger.debug(f"Starting communication server ('{self.host}:{self.port}')")
        self.socket.bind(f"tcp://{self.host}:{self.port}")
        self.listen = True
        self.listen_thread = threading.Thread(target=self.__listen)
        self.listen_thread.start()

    def stop(self):
        logger.debug("Stopping communication server")
        self.listen = False
        if self.listen_thread:
            self.listen_thread.join()
            self.listen_thread = None
        self.socket.close()
        self.context.term()

    def __listen(self):
        while self.listen:
            try:
                message = self.socket.recv_json(flags=zmq.NOBLOCK)
            except zmq.Again:
                time.sleep(0.3)
                continue

            req_command = message.get("command")
            req_params = message.get("params")
            logger.debug(f"Command '{req_command}' has been requested")

            try:
                command_function = getattr(self.commands_provider, req_command)
            except AttributeError:
                logger.error(f"Non existing command '{req_command}' has been requested")
                self.socket.send_json(None)
                continue

            if command_function:
                if req_params:
                    resp = command_function(req_params)
                else:
                    resp = command_function()
            else:
                resp = {}

            self.socket.send_json(resp)
        logger.debug("Stopping listen thread")


