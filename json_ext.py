from keyboards import Keyboard, AnsiKeyboard, IsoKeyboard
from json import load, dump
from collections import defaultdict
import re


def keyboard_to_json(keyboard: Keyboard, directory="json_files"):
    json = defaultdict(str)
    type_pattern = re.compile(r'keyboards\.(\w*Keyboard)')
    json["type"]        = re.findall(type_pattern, str(type(keyboard)))[0]
    json["top_row"]     = ''.join(keyboard.layout[0])
    json["homerow"]     = ''.join(keyboard.layout[1])
    json["bot_row"]     = ''.join(keyboard.layout[2])
    json["name"]        = keyboard.name
    json["description"] = keyboard.description

    try:
        json["nums"]    = keyboard.nums
        json["symbols"] = keyboard.symbols
    except AttributeError:
        pass
    try:
        json["iso_key"] = keyboard.iso_key
    except AttributeError:
        pass

    with open(f"{directory}/{keyboard.name}.json", 'w', encoding='utf-8') as json_file:
        dump(dict(json), json_file, indent='\t', separators=(',', ': '))


def _determine_kb_type(json, kb_type, fill_unknowns):
    if fill_unknowns:
        return kb_type
    else:
        if json["type"] == "Keyboard" or kb_type == Keyboard:
            return Keyboard
        if json["type"] == "AnsiKeyboard" or kb_type == AnsiKeyboard:
            return AnsiKeyboard
    return IsoKeyboard


def json_to_keyboard(file_name: str, kb_type=IsoKeyboard, fill_unknowns=True, directory="json_files"):
    with open(f"{directory}/{file_name.split('.')[0]}.json", 'r', encoding='utf-8') as json_file:
        json = load(json_file)
        kb_type = _determine_kb_type(json, kb_type, fill_unknowns)
        print(kb_type)

        top_row     = json["top_row"]
        homerow     = json["homerow"]
        bot_row     = json["bot_row"]
        name        = json["name"]
        description = json["description"]

        if kb_type == Keyboard or fill_unknowns:
            return kb_type(top_row=top_row, homerow=homerow, bot_row=bot_row, name=name, description=description)

        nums        = json["nums"]
        symbols     = json["symbols"]
        if kb_type == AnsiKeyboard or fill_unknowns:
            return kb_type(top_row=top_row, homerow=homerow, bot_row=bot_row, name=name,
                           description=description, nums=nums, symbols=symbols)

        iso_key = json["iso_key"]
        return IsoKeyboard(top_row=top_row, homerow=homerow, bot_row=bot_row, name=name,
                           description=description, nums=nums, symbols=symbols, iso_key=iso_key)
