# '-' функции
import keyboard
import ctypes
def load_keyboard_layout(layout):
    user32 = ctypes.WinDLL('user32')
    KLF_ACTIVATE = 1  # Activate layout
    WM_INPUTLANGCHANGEREQUEST = 0x0050  # Message for changing layout
    HWND_BROADCAST = 0xFFFF  # Send message to all windows

    # Load keyboard layout if not loaded yet
    if layout not in LAYOUT_HANDLES:
        LAYOUT_HANDLES[layout] = user32.LoadKeyboardLayoutW(layout, KLF_ACTIVATE)
        print("14")

    layout_handle = LAYOUT_HANDLES[layout]
    print("17")

    # Switch layout
    user32.PostMessageW(HWND_BROADCAST, WM_INPUTLANGCHANGEREQUEST, 0, layout_handle)


def print_pressed_keys(e):
    global rdy  # счетчик нажатий
    print(e, e.event_type, e.name) #KeyboardEvent(right alt down) down right altаhhаараf
    if rdy == 2 and e.name in d:
        if str(d.get(e.name))[0] == "-":  # проверка вызова доп опций вместо символьных операций
            if str(d.get(e.name)) == "-англ":
                print(e.name)
                load_keyboard_layout(ENGLISH_LAYOUT)
            if str(d.get(e.name)) == "-рус":
                print(e.name)
                load_keyboard_layout(RUSSIAN_LAYOUT)
        else:
            keyboard.press_and_release('backspace')
            keyboard.write(d.get(e.name))
        rdy = 0
    if e.event_type == "up" and (e.name == "right alt" or e.name == "alt gr") and rdy == 1:
        rdy = 2
    else:
        rdy = 0
    if e.event_type == "down" and (e.name == "right alt" or e.name == "alt gr"):
        rdy = 1
rdy = 0
d = {'1': "\'", '2': "\"", '3': "#", '4': ";", '5': "$", '6': ":", '7': "&", "р": "-рус", "h": "-рус", "f": "-англ", "а": "-англ", 'э': "\'", 'ю': ">", 'б': "<", '/': ",", 'х': "[]"}
RUSSIAN_LAYOUT = '00000419'
ENGLISH_LAYOUT = '00000409'
LAYOUT_HANDLES = {}

keyboard.hook(print_pressed_keys)#KeyboardEvent(down up) up downsрааhhhhhhhрааааааа[]
keyboard.wait()