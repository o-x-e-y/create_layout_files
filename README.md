# Create layout files more easily.
 
 To interface it, there are 3 keyboard classes: Keyboard, AnsiKeyboard and IsoKeyboard.
 
 Put these into any of the keyboard_to_xxx functions, and the function will generate a file of corresponding type. You can also
do the reverse and generate a Keyboard object from a xxx_to_keyboard function.
 
 When I say Keyboard object, I mean either Keyboard, AnsiKeyboard or IsoKeyboard.
 
 ### Keyboard class:
 Represents a numberless 3\*10 matrix. Takes 5 arguments: top_row, homerow and bot_row are strings of length 10, they represent the first 10 keys counted from the left side of a keyboard, on qwerty this is from q to p, from a to ; and from z to /. Then there is name which will also be the name of the keyboard file. If not given, defaults to the first 4 keys on the home row, which is completely arbitrary and might cause naming conflics so giving a name is advisable. The description defaults to the name if not given.
 ### AnsiKeyboard class:
 Represents a US Ansi keyboard. Besides taking the above arguments, numbers is a string of 10 characters that correspond to what on qwerty are all numbers, default to 1234567890. symbols is a string of length 7 that correspond to all other symbol keys on the keyboard, and default to "\*\*\*\*\*\*\*".

(UNFINISHED) It also provides a function that in place makes the keyboard wide modded.
 ### IsoKeyboard class:
 Represents an Iso keyboard. Besides taking all of AnsiKeyboard's arguments, also takes an iso_key argument representing the key in the bottom left typical to iso keyboards. Defaults to "\*".
 
 (UNFINISHED) Besides having a wide mod function, also provides an angle mod function that angle mods the keyboard in place.
 
 Within the keyboards.py file there are also present arguments for a couple of layouts, see main.py for an example of how to use those.
 
 ## File types:
 KLC is the Microsoft Layout Creator file type, json is a Keyboard class type representation that might not have all parameters for all 3 classes and instead includes a type, and kb represents the bare minimum of a keyboard being the name and the 3\*10 matrix.
 
 ## How to interface the functions:
 All 3 file types provide an xxx_to_keyboard and keyboard_to_xxx function that take slightly different arguments.
 
 klc_to_keyboard and kb_to_keyboard: takes a file name (both with and without extension works), and a Keyboard type. Also takes an optional directory though modifying this should not be necessary. NOTE: kb_to_keyboard does not consider mods, only klc does.
 
 json_to_keyboard: besides the other 2 arguments takse a boolean fill_unknowns, which determines what type to return if not all fields in the json file are filled. Defaults to True. If True, returns the type given, if False, returns the biggest between either what the json parameters can fill, or the type given. NOTE: does not consider mods.
 
 keyboard_to_klc: takes a Keyboard object, a language (like English, german, french), and optionally a region (default None), a has_symbols (default True, if false, defaults to "\`[]/=-\\" and an optional directory. Changing this shouldn't be necessary. Writes to a file corresponding to <Keyboard.name>.klc in the directory.
 
 keyboard_to_kb: simply takes a Keyboard object and an optional directory, writes to a file corresponding to <Keyboard.name>.kb in the directory.
 
 keyboard_to_json: simply takes a Keyboard object and an optional directory, writes to a file corresponding to <Keyboard.name>.json in the directory.
