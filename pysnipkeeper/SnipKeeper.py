import logging
from string import Template
from pysnipkeeper.Models.Snips import Snips
from pysnipkeeper.utils.config import Config
from pysnipkeeper.utils.FileHandler import load as file_load
from pysnipkeeper.utils.FileHandler import save as file_save

logger = logging.getLogger()


class SnipKeeper:
    def __init__(self):
        self.in_context = False
        self.config = Config()
        self.snips = None

    def __enter__(self):
        logger.info('Default Category: %s', self.config.get_default_category())
        self.snips = Snips(
            self.config.get_schemas(),
            self.config.get_default_category(),
            file_load(self.config.datafile)
        )
        self.in_context = True
        return self

    def __exit__(self, *args):
        file_save(
            self.config.datafile,
            self.snips.get_all_data()
        )
        self.in_context = False

    def add_item(self, category=None, **kwargs):
        if self.in_context is False:
            raise RuntimeError('Attempting to modify snip data out of context.')
        self.snips.add(kwargs, category)

    def _format_item(self, item: dict, category: str):
        format_order = [
            'title',
            'quote',
            'author',
            'source',
            'notes'
        ]  # TODO add to config for overrides
        divider = '\n'
        fmt_str_dict = {}
        format_dict = self.config.get_category_format(category)
        logger.info('Category Format: %s', str(format_dict))
        fmt_str = ''
        for k, v in item.items():
            if k in format_dict:
                try:
                    fmt_str_dict[k] = Template(format_dict.get(k)).substitute(**{k:v})
                except TypeError:
                    logger.error('TypeError')
                    logger.error('Template: %s', format_dict.get(k))
                    logger.error('Key: %s', k)
                    logger.error('Value: %s', v)
                except KeyError:
                    logger.error('KeyError')
                    logger.error('Template: %s', format_dict.get(k))
                    logger.error('Key: %s', k)
                    logger.error('Value: %s', v)
        for key in format_order:
            if key in fmt_str_dict:
                fmt_str += f'{fmt_str_dict.get(key)}{divider}'
        fmt_str += divider
        return fmt_str

    def get_random_item(self, category: str = None):
        if self.in_context is False:
            raise RuntimeError('Attempting to modify snip data out of context.')
        if category is None:
            category = self.config.get_default_category()

        item = self.snips.get_random_entry(category=category)
        if item is not None:
            return self._format_item(item, category)
        else:
            return 'There are no entries.'

    def get_all(self, category: str = None):
        if self.in_context is False:
            raise RuntimeError('Attempting to modify snip data out of context.')

        items = self.snips.get_all_entries(category=category)
        return ''.join(
            [self._format_item(item) for item in items]
        )
