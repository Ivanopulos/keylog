# '-' функции
import keyboard
def print_pressed_keys(e):
    global rdy
    #print(e, e.event_type, e.name) #KeyboardEvent(right alt down) down right alt
    #print(str(d.get(e.name))[0])
    #print(d.get(e.name))
    #print(e.name)
    #print(rdy, e.event_type)
    if rdy == 2 and e.name in d:
        if str(d.get(e.name))[0] == "-":
            pass
        else:
            keyboard.press_and_release('backspace')
            keyboard.write(d.get(e.name))#.press_and_release(d.get(e.name))
        rdy = 0
    if e.event_type == "up" and (e.name == "right alt" or e.name == "alt gr") and rdy == 1:
        rdy = 2
    else:
        rdy = 0
    if e.event_type == "down" and (e.name == "right alt" or e.name == "alt gr"):
        rdy = 1
rdy = 0
d = {'1': "\'", '2': "\"", '3': "#", '4': ";", '7': "&", "р": "-рус", "h": "-рус", "f": "-англ", "а": "-англ"}
keyboard.hook(print_pressed_keys)#KeyboardEvent(down up) up downs
#keyboard.press_and_release('s, space')
keyboard.wait()