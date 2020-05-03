#!/usr/bin/env python
import logging
import sys
from pysnipkeeper.SnipKeeper import SnipKeeper

LOG_FORMAT = '%(levelname)s - %(message)s'
l_formatter = logging.Formatter(LOG_FORMAT)
l_handler = logging.StreamHandler(stream=sys.stderr)
l_handler.setFormatter(l_formatter)
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.addHandler(l_handler)


# Examples
# pysnipkeeper.py add -c quotes --author Bill --source Life "It is what it is"
# pysnipkeeper.py add --author Bill --source Life "It is what it is"
# pysnipkeeper.py
# pysnipkeeper.py list quotes
def _pop_left(some_list):
    return some_list[0], list(some_list[1:])


def _parse_args():
    single_flags = {
        '-h': 'help',
        '-v': 'verbose'
    }
    category_flags = [
        '-c',
        '--category'
    ]
    arg_dict = {
        'flags': [],
        'command': None,
        'category': None,
        'default_field': None,
        'keywords': {}
    }
    args_to_parse = sys.argv[1:]
    if len(args_to_parse) == 0:
        arg_dict['command'] = 'get'
    while len(args_to_parse) > 0:
        arg, args_to_parse = _pop_left(args_to_parse)
        if arg in single_flags:
            arg_dict['flags'].append(single_flags.get(arg))
        elif arg_dict['command'] is None:
            arg_dict['command'] = arg
        elif arg in category_flags:
            arg, args_to_parse = _pop_left(args_to_parse)
            arg_dict['category'] = arg
        elif '--' in arg:
            keyword = arg.lstrip('--')
            arg, args_to_parse = _pop_left(args_to_parse)
            arg_dict['keywords'][keyword] = arg
        else:  # I should be at the end of the document
            arg_dict['default_field'] = ' '.join(args_to_parse)
    return arg_dict


def main():
    arg_dict = _parse_args()
    flags = arg_dict.get('flags')
    keywords = arg_dict.get('keywords')
    command = arg_dict.get('command')
    category = arg_dict.get('category')
    keywords['default_field'] = arg_dict.get('default_field')
    if 'help' in flags:
        print('USAGE:')
        print(' pysnipkeeper.py - return random entry from default category')
        print(' pysnipkeeper.py [command] [-h] [-v] [-c category] [--keyword value] default_field value')
        return
    if 'verbose' in flags:
        logger.setLevel(logging.INFO)
        if command is None:
            command = 'get'
    logger.info(command)
    logger.info(category)
    logger.info(str(keywords))
    with SnipKeeper() as snip:
        if 'get' in command:
            print(snip.get_random_item(category))
        elif 'list' in command:
            print(snip.get_all(category))
        elif 'add' in command:
            try:
                snip.add_item(category, **keywords)
                print('Item Added.')
            except Exception as e:
                logger.error('Exception raised %s - type %s', str(e), str(type(e)))
        else:
            logger.error('Invalid Command.')
    return


if __name__ == '__main__':
    main()
