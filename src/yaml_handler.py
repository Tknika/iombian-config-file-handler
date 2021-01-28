#!/usr/bin/env python3

import logging
import yaml

logger = logging.getLogger(__name__)


class YAMLHandler(object):

    def __init__(self, yaml_file_path):
        self.yaml_file_path = yaml_file_path
        self.config = None

    def load_file(self):
        with open(self.yaml_file_path, 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
                import json
            except yaml.YAMLError as ex:
                logger.error(f"Error loading yaml configuration: {ex}")

    def get_config(self):
        return self.config

    def save_config(self, config):
        with open(self.yaml_file_path, 'w') as stream:
            try:
                yaml.dump(config, stream)
                logger.debug("New configuration has been saved")
            except Exception as ex:
                logger.error(f"Error saving yaml configuration: {ex}")

        self.load_file()