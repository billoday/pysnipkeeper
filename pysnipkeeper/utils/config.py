import os
import yaml
import logging
from pathlib import Path

logger = logging.getLogger()


class Config:
    user_config_final = f'{Path.home()}/.config/pysnipkeeper/config.yaml'
    user_config_alt = f'{Path.home()}/.pysnipkeeper.yaml'
    default = 'config.yaml'

    def __init__(self):
        self.config = {}
        self.datafile = 'snips.yaml'
        self.parse_configs()

    def get_default_category(self):
        return self.config.get('default_category')

    def get_schemas(self):
        return self.config.get('schemas', {})

    def get_category_schema(self, category):
        schemas = self.config.get('schemas', {})
        return schemas.get(category, schemas.get('default'))

    def get_category_format(self, category):
        formats = self.config.get('format', {})
        return formats.get(category, formats.get('default'))

    def parse_configs(self):
        crash = False
        working_config = self.load_file(self.default)
        if len(working_config) == 0:
            logger.critical('Default config missing - if no user config is found, crashing')
            crash = True
        user_config = self.load_file(self.user_config_alt)
        if len(user_config) > 0:
            self.datafile = f'{Path.home()}/.snips.yaml'
            working_config = self.merge_config(working_config, user_config)
        user_config = self.load_file(self.user_config_final)
        if len(user_config) > 0:
            self.datafile = f'{Path.home()}/.config/pysnipkeeper/data.yaml'  # TODO move to config
            working_config = self.merge_config(working_config, user_config)
        if crash is True and len(working_config) == 0:
            raise RuntimeError('No valid config and default config is missing.')
        logger.info('Default category - %s', working_config.get('default_category'))
        self.config = dict(working_config)

    @staticmethod
    def load_file(config_file):
        try:
            with open(config_file, 'r') as f:
                temp_dict = yaml.load(f, Loader=yaml.Loader)
        except Exception as e:
            logger.warning(str(e))
            temp_dict = {}
        return temp_dict

    @classmethod
    def merge_config(cls, original: dict, overriding: dict):
        merged_config = {}
        for node, value in original.items():
            if node in overriding:
                if isinstance(value, dict):
                    if isinstance(overriding.get(node), dict):
                        merged_config[node] = cls.merge_config(value, overriding.get(node))
                    else:
                        merged_config[node] = overriding.get(node)
                else:
                    logger.info('Key %s does exist in override - value %s', node, overriding.get(node))
                    merged_config[node] = overriding.get(node)
            else:
                logger.info('Key %s does not exist in override', node)
                merged_config[node] = value
        return merged_config
