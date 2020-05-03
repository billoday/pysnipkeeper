import yaml
import logging

logger = logging.getLogger()


def load(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.load(f, Loader=yaml.Loader)
    except Exception as e:
        logger.warning(str(e))
        return {}


def save(filename, snips_data):
    with open(filename, 'w') as f:
        f.write(yaml.dump(snips_data, Dumper=yaml.Dumper))
