import json
import os

from click import prompt

from templates.Template import Template

from constants.constants import TEMPLATES_JSON


def save_to_file(data):
    # Write JSON file
    with open(TEMPLATES_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=lambda x: x.__dict__)
    return "Done"


def read_from_file():
    # Read JSON file
    parsed_array = []
    if os.path.exists(TEMPLATES_JSON):
        with open(TEMPLATES_JSON) as data_file:
            data_loaded = json.load(data_file)
        for x in data_loaded:
            parsed_array.append(Template(**x))
    return parsed_array


def name_validation(templates_array, new_template):
    ask = False
    for old_template in templates_array:
        if new_template.name == old_template.name:
            print(f"{new_template.name} already exists, please change it")
            ask = True
            break
    if ask:
        new_template.name = prompt('Enter template name', type=str)
        name_validation(templates_array, new_template)
    else:
        return new_template
