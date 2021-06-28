from kb_ext import kb_to_keyboard, keyboard_to_kb
from json_ext import json_to_keyboard, keyboard_to_json
from klc_ext import klc_to_keyboard, keyboard_to_klc
import keyboards
from keyboards import Keyboard, AnsiKeyboard, IsoKeyboard


if __name__ == "__main__":
    keyboard = IsoKeyboard(*keyboards.layouts["halmak"], keyboards.layout_symbols["halmak"])
    keyboard_to_kb(keyboard)
