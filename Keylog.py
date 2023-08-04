# '-' функции
import keyboard
import ctypes
from ctypes import wintypes
import time
import pyperclip
def load_keyboard_layout(layout):
    user32 = ctypes.WinDLL('user32')
    KLF_ACTIVATE = 1  # Activate layout
    WM_INPUTLANGCHANGEREQUEST = 0x0050  # Message for changing layout
    HWND_BROADCAST = 0xFFFF  # Send message to all windows
    # Load keyboard layout if not loaded yet
    if layout not in LAYOUT_HANDLES:
        LAYOUT_HANDLES[layout] = user32.LoadKeyboardLayoutW(layout, KLF_ACTIVATE)
    layout_handle = LAYOUT_HANDLES[layout]
    # Get the active window
    hwnd = user32.GetForegroundWindow()

    # Get the window name
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)

    # If the active window is not MS Word, send the message
    if "Microsoft Word" not in buff.value:
        user32.PostMessageW(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, layout_handle)
def print_pressed_keys(e):
    global pred  # памятка о предыдущем событии
    global rdy  # счетчик нажатий
    print(e, e.event_type, e.name)  # KeyboardEvent(right alt down) down right altаhhаараf
    if rdy == 2 and e.name in d:
        if str(d.get(e.name))[0] == "-":  # проверка вызова доп опций вместо ввода
            if str(d.get(e.name)) == "-англ":  # раскладки
                keyboard.press_and_release('backspace')
                load_keyboard_layout(ENGLISH_LAYOUT)
            if str(d.get(e.name)) == "-рус":
                keyboard.press_and_release('backspace')
                load_keyboard_layout(RUSSIAN_LAYOUT)
            if str(d.get(e.name)) == "-замена":
                keyboard.press_and_release('backspace')
                m = pyperclip.paste()
                m = m.translate(trans_table)
                pyperclip.copy(m)
        else:  # просто ввод
            keyboard.press_and_release('backspace')
            keyboard.write(d.get(e.name))
        rdy = 0
    if e.event_type == "up" and (e.name == knopnadopt1 or e.name == knopnadopt2) and rdy == 1:  # контроль нажатия команды
        rdy = 2
    else:
        rdy = 0
    if e.event_type == "down" and (e.name == knopnadopt1 or e.name == knopnadopt2):
        rdy = 1
    if e.event_type == "up" and pred.name == "right ctrl":#and e.name == "insert"
        keyboard.send('ctrl+c')
        print("found")
    pred = e
rdy = 0
# словарь функций и спец
d = {'1': "'", '2': '"', '3': "#", '4': ";", '5': "$", '6': ":", '7': "&", "р": "-рус", "h": "-рус", "f": "-англ",
     "а": "-англ", 'э': "'", "'": "'", 'ю': ">", '.': ">", 'б': "<", ',': "<", '/': ",", 'х': "[]", '[': "[]", 'ъ': "]",
     '`': "-замена", 'ё': "-замена"}
# словарь неправильного алфавита
alf = {'q': "й", 'w': "ц", 'e': "у", 'r': "к", 't': "е", 'y': "н", 'u': "г", 'i': "ш", 'o': "щ", 'p': "з", '[': "х",
       ']': "ъ", 'a': "ф", 's': "ы", 'd': "в", 'f': "а", 'g': "п", 'h': "р", 'j': "о", 'k': "л", 'l': "д", ';': "ж",
       "'": "э", 'z': "я", 'x': "ч", 'c': "с", 'v': "м", 'b': "и", 'n': "т", 'm': "ь", ',': "б", '.': "ю", '/': ".",
       'й': "q", 'ц': "w", 'у': "e", 'к': "r", 'е': "t", 'н': "y", 'г': "u", 'ш': "i", 'щ': "o", 'з': "p", 'х': "[",
       'ъ': "]", 'ф': "a", 'ы': "s", 'в': "d", 'а': "f", 'п': "g", 'р': "h", 'о': "j", 'л': "k", 'д': "l", 'ж': ";",
       'э': "'", 'я': "z", 'ч': "x", 'с': "c", 'м': "v", 'и': "b", 'т': "n", 'ь': "m", 'б': ",", 'ю': ".", '&': "?"}
trans_table = str.maketrans(alf)  # Создание таблицы перевода с помощью функции maketrans().
RUSSIAN_LAYOUT = '00000419'
ENGLISH_LAYOUT = '00000409'
LAYOUT_HANDLES = {}
knopnadopt1 = "right shift"  # right alt
knopnadopt2 = "right shift"  # alt gr
keyboard.hook(print_pressed_keys)  # KeyboardEvent(down up) up down
keyboard.wait()
