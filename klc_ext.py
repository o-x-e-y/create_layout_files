from keyboards import Keyboard, AnsiKeyboard, IsoKeyboard
from keyboards import layout_symbols
from static import locale_ids, SC, VK, sym_upper, static_text, SC_REVERSE
from locale import windows_locale
import re


# KC MEANS 'KEY CODE' just for yall's info


def _get_locale_id(language="english", region=None):
    """If the locale id exists, gives it back. If it doesn't, raises a KeyError"""
    if region:
        try:
            return locale_ids[f"{language.lower()} - {region.lower()}"]
        except KeyError:
            print(f"{language} - {region} is not a valid identifier")
    else:
        try:
            return locale_ids[language]
        except KeyError:
            print(f"{language} unfortunately does not exist")


def _make_rows_scs(keyboard, has_symbols: bool):
    """Depending on the keyboard type, creates rows of scs and
    keys with or without custom numbers, an iso key or symbols"""
    if type(keyboard) == Keyboard:
        try:
            symbols = layout_symbols[keyboard.name]
        except KeyError:
            symbols = layout_symbols["dvorak"]
        if has_symbols:
            rows = ["1234567890", keyboard.top_row, keyboard.homerow, keyboard.bot_row, symbols]
            scs = [SC["nums"], SC["top_row"], SC["homerow"], SC["bot_row"], SC["symbols"]]
            return rows, scs
        else:
            rows = ["1234567890", keyboard.top_row, keyboard.homerow, keyboard.bot_row]
            scs = [SC["nums"], SC["top_row"], SC["homerow"], SC["bot_row"]]
            return rows, scs
    else:
        rows = [keyboard.nums, keyboard.top_row, keyboard.homerow, keyboard.bot_row,
                keyboard.symbols if keyboard.symbols != "*******" else layout_symbols["dvorak"]]
        scs = [SC["nums"], SC["top_row"], SC["homerow"], SC["bot_row"], SC["symbols"]]
        return rows, scs


def _get_kc_line(key: str, sc: str):
    """create a line containing sc, vk and key information. The format is as follows:
    <SC> - <VK code> - <has_capital> - <default ascii code> - <capital ascii code> - <ctrl ascii code>.
    Note that the ctrl ascii code is set to be -1 (doesn't exist)."""
    no_cap = key != key.upper()
    hex_def = hex(ord(key))[2:]
    hex_upper = hex(ord(sym_upper[key]))[2:] if not no_cap else hex(ord(key.upper()))[2:]
    if sc != "iso_key":
        return f"{sc}\t{VK[key]}\t{int(no_cap)}\t00{hex_def}\t00{hex_upper}\t-1"
    else:
        return f"{SC[sc]}\t{VK['iso_key']}\t{int(no_cap)}\t00{hex_def}\t00{hex_upper}\t-1"


def keyboard_to_klc(keyboard, language="english", region=None, has_symbols=True, directory="klc_files"):
    """Takes a Keyboard, AnsiKeyboard or IsoKeyboard object and generates a .klc file corresponding to its name.
    If no symbols, numbers or iso keys are present, uses dvorak symbols, 1234567890 numbers and \\\\ by default."""
    assert type(keyboard) == Keyboard or type(keyboard) == AnsiKeyboard or type(keyboard) == IsoKeyboard,\
        "keyboard should be a Keyboard object"
    locale_id = _get_locale_id(language, region)
    locale_name = windows_locale[int(locale_id, 16)]
    description = f"keyboardD\t{keyboard.name}\t\"{keyboard.description}\"\n\nCOPYRIGHT\t\"(c) 2021 OEM\"\n\nCOMPANY\t\"OEM\"\n\n"\
                  f"LOCALENAME\t\"{'-'.join(locale_name.split('_'))}\"\n\nLOCALEID\t\"0000{locale_id}\"\n\nVERSION\t"\
                  f"1.0\n\nSHIFTSTATE\n\n0\t//Column 4\n1\t//Column 5 : Shft\n2\t//Column 6 :       Ctrl\n\nLAYOUT\t\t"\
                  f";an extra \'@\' at the end is a dead key\n\n//SC\tVK_\t\tCap\t0\t1\t2\n//--\t----\t\t----\t----" \
                  f"\t----\t----\n\n"

    kc_lines = []
    for row, sc_row in zip(*_make_rows_scs(keyboard, has_symbols)):
        for key, sc in zip(row, sc_row):
            kc_lines.append(_get_kc_line(key, sc))

    if type(keyboard) == IsoKeyboard:
        kc_lines.append(_get_kc_line(keyboard.iso_key, sc="iso_key"))

    kc_lines.append("39\tSPACE\t0\t0020\t0020\t0020")
    kc_lines.append("53\tDECIMAL\t0\t002e\t002e\t-1")
    key_lines = '\n'.join(kc_lines)

    desc_2 = f"DESCRIPTIONS\n\n{locale_id}\t{region}-{keyboard.description}" \
             f"\nLANGUAGENAMES\n\n{locale_id}\t{language}\nENDKBD\n"
    with open(f"{directory}/{keyboard.name}.klc", "w", encoding='utf-16') as new_klc_file:
        new_klc_file.write(description + key_lines + static_text + desc_2)


def kc_to_char(kc: str):
    if len(kc) == 1:
        return kc
    else:
        return chr(int(kc[0:4], 16))


def klc_to_keyboard(file_name: str, keyboard_type=Keyboard, directory="klc_files"):
    assert keyboard_type == Keyboard or keyboard_type == AnsiKeyboard or keyboard_type == IsoKeyboard,\
        "keyboard_type should be a Keyboard object"
    with open(f"{directory}/{file_name.split('.')[0]}.klc", 'r', encoding='utf-16') as klc_file:
        klc = klc_file.read()
        kc_pattern = re.compile(r'(\d.)\t.+\t\d\t(.{4,5}|.)\t')
        keyboard_data = {"nums":    ['*'] * 10,
                         "top_row": ['*'] * 10,
                         "homerow": ['*'] * 10,
                         "bot_row": ['*'] * 10,
                         "symbols": ['*'] * 7,
                         "iso_key": '*'}
        for kc_data in re.findall(kc_pattern, klc):
            sc, key = kc_data
            try:
                row_destination, key_nr_destination = SC_REVERSE[sc]
                keyboard_data[row_destination][key_nr_destination] = kc_to_char(key)
            except ValueError:
                keyboard_data["iso_key"] = kc_to_char(key)
            except KeyError:
                pass

        name, description = re.compile(r'KBD\t(.+)\t"(.+)"').findall(klc)[0]

        if keyboard_type == Keyboard:
            return Keyboard(keyboard_data['top_row'], keyboard_data['homerow'],
                            keyboard_data['bot_row'], name, description)
        elif keyboard_type == AnsiKeyboard:
            return AnsiKeyboard(keyboard_data['top_row'], keyboard_data['homerow'], keyboard_data['bot_row'],
                                name, description, keyboard_data['symbols'], keyboard_data['nums'])
        else:
            return IsoKeyboard(keyboard_data['top_row'], keyboard_data['homerow'], keyboard_data['bot_row'], name,
                               description, keyboard_data['symbols'], keyboard_data['nums'], keyboard_data['iso_key'])
