# '-' функции
import keyboard
import ctypes
from ctypes import wintypes
import time
import pyperclip
import win32gui#pip install pywin32
import win32con
def find_corresponding_char(ky, alf, alf2):  # для переноса символа с известной целью
    # Поиск индекса символа в словаре alf
    index = -1  # Если символ не найден, вернем -1
    for idx, (key, value) in enumerate(alf.items()):
        if key == ky or value == ky:
            index = idx
            break

    # Если индекс найден и он в пределах длины списка alf2, возвращаем соответствующий символ
    if index != -1 and index < len(alf2):
        return alf2[index]
    else:
        return None  # Если индекс не найден или за пределами alf2, возвращаем None
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
    global pred  # памятка о предыдущем событии нажатия
    global rdy  # счетчик нажатий

    global svst  # пул для разбитых вставок работает не стабильно, !!требует переназначения клавиш вставки
    global svst1  # счетчик юза разбитых вставок
    global svval # словарь разб вставок
    global svms  # метка статуса 0 свободен, 5 занят на вставку, 6 занят на шифр
    global prsimb  # номер прошлого символа для молнии

    if not (ctypes.WinDLL('user32').GetKeyState(0x90) & 1):  # намлоковый отбой на случай если он нечаянно включится
        ctypes.WinDLL('user32').keybd_event(0x90, 0, 0, 0)
        ctypes.WinDLL('user32').keybd_event(0x90, 0, 0x0002, 0)

    try:
        _ = svms
    except NameError:
        svms = 0
    #print(e, e.event_type, e.name)  # KeyboardEvent(right alt down) down right altаhhаараf
    if rdy == 2 and e.name in d:
        if str(d.get(e.name))[0] == "-":  # проверка вызова доп опций вместо ввода
            if str(d.get(e.name)) == "-англ":  # раскладки
                keyboard.press_and_release('backspace')
                load_keyboard_layout(ENGLISH_LAYOUT)
            if str(d.get(e.name)) == "-англ2":  # раскладки
                keyboard.press_and_release('backspace')
                load_keyboard_layout(ENGLISH_LAYOUT)
                svms = 8
            if str(d.get(e.name)) == "-рус":
                keyboard.press_and_release('backspace')
                load_keyboard_layout(RUSSIAN_LAYOUT)
            if str(d.get(e.name)) == "-замена":
                keyboard.press_and_release('backspace')
                m = pyperclip.paste()
                m = m.translate(trans_table)
                pyperclip.copy(m)
#!! БИТЫЙ, требует переназначение на незанятую комбинацию вставки
            # if str(d.get(e.name)) == '-каскадвставка':
            #     svst = pyperclip.paste()
            #     if not svst == "":
            #         svst1 = 0
            #         svval = svst.split('\n')
            #         pyperclip.copy(svval[svst1])
            #         if len(svval) > 1:
            #             svms = 5
            #         print("съедено")
            if str(d.get(e.name)) == "-слов2": # съедение на вставку 𝒹 ಽ ᑶ г ᑻ ᚋ 𝞷 𝜕 l i r へ ω N v L I く Ŀ 𝙹 𐌙 ソ ૪ 𐒇 𝞷 ゑ II Ə チ ゃ
                svms = 6
                keyboard.press_and_release('backspace')
        else:  # просто ввод
            keyboard.press_and_release('backspace')
            keyboard.write(d.get(e.name))
        rdy = 0


    if e.name == "insert" and svms == 5 and e.event_type == "down" and pred.name == "right shift":# ловим разб вставку для чередования
        svst1 = svst1+1
        if len(svval) <= svst1-1:
            svst1 = 0
        pyperclip.copy(svval[svst1])
    if e.name == "insert" and e.event_type == "down" and pred.name == "right ctrl":  # ловим разб вставку для чередования
        svms = 0

    if e.event_type == "up" and (e.name == knopnadopt1 or e.name == knopnadopt2) and rdy == 1:  # контроль нажатия команды шифт
        rdy = 2
    else:
        rdy = 0
    if e.event_type == "down" and (e.name == knopnadopt1 or e.name == knopnadopt2):
        rdy = 1
    if (svms == 6 or svms == 7) and e.event_type == "up":# включен контроль замены ш, 6 первичное (сам ш) 7 вторичное𝞷
        print(f"Event: {e.name}, Type: {e.event_type}, State: {svms}")
        if svms == 7:
            rs = find_corresponding_char(e.name, alf, alf2)
            #print(e.name)
            if rs:
                keyboard.press_and_release('backspace')
                keyboard.write(rs)
                prsimb = alf2.find(rs)
            elif e.name == "space":
                keyboard.press_and_release('backspace')
                rs = "中地水風金和"[int(prsimb/6)]
                keyboard.write(rs)#中地水風金和    "⚡"
            else:
                svms = 0  # нет в словаре=сброс
        else:
            svms = 7
    if e.name == "space" and svms==8: # включен контроль разового английского ввода с заменой, пробел - возврат на рус
        svms = 0
        load_keyboard_layout(RUSSIAN_LAYOUT)
    pred = e
rdy = 0
# словарь функций и спец
d = {'1': "«»", '2': '"', '3': "#", '4': ";", '5': "$", '6': ":", '7': "&", "р": "-рус", "h": "-рус", "f": "-англ",
     "а": "-англ", 'э': "'", "'": "'", 'ю': ">", '.': ">", 'б': "<", ',': "<", '/': ",", 'х': "[", '[': "[", 'ъ': "]",
     ']': "]", 'ж': ":", ';': ":", '`': "-замена", 'ё': "-замена", 'right ctrl': '-каскадвставка', 'i': "-слов2",
     'ш': '-слов2', "в": "-англ2", "d": "-англ2"}
# словарь неправильного алфавита
alf = {'q': "й", 'w': "ц", 'e': "у", 'r': "к", 't': "е", 'y': "н", 'u': "г", 'i': "ш", 'o': "щ", 'p': "з", '[': "х",
       ']': "ъ", 'a': "ф", 's': "ы", 'd': "в", 'f': "а", 'g': "п", 'h': "р", 'j': "о", 'k': "л", 'l': "д", ';': "ж",
       "'": "э", 'z': "я", 'x': "ч", 'c': "с", 'v': "м", 'b': "и", 'n': "т", 'm': "ь", ',': "б", '.': "ю", '/': ".",
       'й': "q", 'ц': "w", 'у': "e", 'к': "r", 'е': "t", 'н': "y", 'г': "u", 'ш': "i", 'щ': "o", 'з': "p", 'х': "[",
       'ъ': "]", 'ф': "a", 'ы': "s", 'в': "d", 'а': "f", 'п': "g", 'р': "h", 'о': "j", 'л': "k", 'д': "l", 'ж': ";",
       'э': "'", 'я': "z", 'ч': "x", 'с': "c", 'м': "v", 'и': "b", 'т': "n", 'ь': "m", 'б': ",", 'ю': ".", '&': "?"}
alf2 = "ï૪𝙹rᚋNz𝞷ゑ𝜕ソ'𐌙Ⅱᑶ𝒹LIvへᑻ𝞷Əゃ𐒇くωiĿ'Sチ,"  # Ⅱ не допустим в именах
trans_table = str.maketrans(alf)  # Создание таблицы перевода с помощью функции maketrans().
RUSSIAN_LAYOUT = '00000419'
ENGLISH_LAYOUT = '00000409'
LAYOUT_HANDLES = {}
knopnadopt1 = "right shift"  # right alt Задвоение по случаю разных назывний в разных раскладках
knopnadopt2 = "right shift"  # alt gr

step = "убираем с фона"
def set_window_opacity(hwnd, opacity):
    """ Устанавливает прозрачность окна. """
    # Проверяем, что прозрачность в диапазоне от 0 до 1
    if opacity < 0 or opacity > 1:
        raise ValueError("Прозрачность должна быть в диапазоне от 0 до 1")

    # Преобразуем прозрачность в значение от 0 до 255
    opacity = int(opacity * 255)

    # Устанавливаем прозрачность окна
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, opacity, win32con.LWA_ALPHA)
def hide_window_from_taskbar(hwnd):
    """ Скрывает окно с панели задач. """
    # Скрыть окно
    #win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    # Удалить уведомление о окне с панели задач
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOOLWINDOW)

if __name__ == "__main__":
    # Получаем HWND (дескриптор окна) для приложения
    имяокна = 'keylog – Keylog.py'#"Fallout II  @640x480x1   "
    hwnd = win32gui.FindWindow(None, имяокна)
    if hwnd:
        # Устанавливаем прозрачность
        set_window_opacity(hwnd, 0.3)
        hide_window_from_taskbar(hwnd)
    else:
        print("Окно не найдено")

keyboard.hook(print_pressed_keys)  # KeyboardEvent(down up) up down
keyboard.wait()

