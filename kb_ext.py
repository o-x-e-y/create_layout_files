from keyboards import Keyboard, AnsiKeyboard, IsoKeyboard


def keyboard_to_kb(keyboard: Keyboard, directory="kb_files"):
    assert type(keyboard) == Keyboard or type(keyboard) == AnsiKeyboard or type(keyboard) == IsoKeyboard, "keyboard should be a Keyboard object"
    with open(f"{directory}/{keyboard.name}.kb", 'w', encoding='utf-8') as kb_file:
        kb_file.write(f"{keyboard.name.capitalize()}\n{' '.join(keyboard.layout[0])}\n"
                      f"{' '.join(keyboard.layout[1])}\n{' '.join(keyboard.layout[2])}")


def kb_to_keyboard(file_name: str, kb_type=IsoKeyboard, directory="kb_files"):
    with open(f"{directory}/{file_name.split('.')[0]}.kb", 'r', encoding='utf-8') as kb_file:
        kb = kb_file.read()
        name, top_row, homerow, bot_row = tuple(kb.split('\n')[0:4])
        return kb_type(''.join(top_row.split(' ')), ''.join(homerow.split(' ')), ''.join(bot_row.split(' ')), name)
