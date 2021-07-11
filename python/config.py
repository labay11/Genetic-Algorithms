import os
import json
import yaml


def load_config_file(file_name):
    filename, file_extension = os.path.splitext(file_name)
    file_extension = file_extension.lower()[1:]
    if file_extension == 'json':
        return json.load(file_name)
    elif file_extension in ['yaml', 'yml']:
        return yaml.load(file_name)

    raise ValueError('Extension {} is not supported as a valid config file'.format(file_extension))
