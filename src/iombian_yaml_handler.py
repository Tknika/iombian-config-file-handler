#!/usr/bin/env python3

import logging
import threading
import uuid
from yaml_handler import YAMLHandler

logger = logging.getLogger(__name__)


class IoMBianYAMLHandler(YAMLHandler):

    def __init__(self, yaml_file_path, default_device_id="iombian"):
        super().__init__(yaml_file_path)
        self.default_device_id = default_device_id
        self.random_device_id = "iombian-{}".format(str(uuid.uuid4())[:8])
        self.update_callback = None

    def load_file(self):
        super().load_file()
        # TODO: we need to validate if the file follows the definition schema

    def save_config(self, config):
        # TODO: we need to check if the config fullfils the definition schema
        super().save_config(config)
        if self.update_callback:
            threading.Thread(target=self.update_callback).start()

    def on_config_update(self, callback):
        self.update_callback = callback

    def is_configured(self):
        return self.get_config_date()

    def get_device_id(self):
        if not self.is_configured():
            return self.random_device_id
        device_id = self.config.get("remote_configurator", {}).get("device_id")
        if not device_id:
            logger.debug("'parameters.yml' file does not contain a device identifier")
        return device_id

    def get_refresh_token(self):
        refresh_token = self.config.get("remote_configurator", {}).get("refresh_token")
        if not refresh_token:
            logger.debug("'parameters.yml' file does not contain a refresh token")
        return refresh_token

    def get_api_key(self):
        api_key = self.config.get("remote_configurator", {}).get("api_key")
        if not api_key:
            logger.debug("'parameters.yml' file does not contain the api key")
        return api_key

    def get_project_id(self):
        project_id = self.config.get("remote_configurator", {}).get("project_id")
        if not project_id:
            logger.debug("'parameters.yml' file does not contain the project id")
        return project_id

    def get_config_date(self):
        config_date = self.config.get("config_date", "")
        if not config_date:
            logger.debug("'parameters.yml' file does not contain a config date")
        return config_date

    def reset(self):
        new_config = self.config
        if "remote_configurator" in new_config:
            del new_config["remote_configurator"]
        if "config_date" in new_config:
            new_config["config_date"] = ""
        if "networking" in new_config:
            default_networking = {  "eth0": {
                                        "profile": "dhcp"
                                    },
                                    "wlan0": {
                                        "profile": "dhcp",
                                        "wlan": {
                                            "ssid": "",
                                            "psk": ""
                                        }
                                    }
                                 }
            new_config["networking"] = default_networking
        self.save_config(new_config)
