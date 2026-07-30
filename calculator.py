from customtkinter import*
from collections import deque
from decimal import Decimal

def setup():
    global window, bg
    window = CTk()
    window.geometry('364x555')
    window._set_appearance_mode('dark')
    window.title('Calculator')
    window.resizable(False, False)
    bg = '#242424'

def frames():
    global frame_1, frame_2, frame_3, frame_4

    global buttons_frame_1, buttons_frame_2, buttons_frame_3
    buttons_frame_1 = ['7','8','9',
                    '4','5','6',
                    '1','2','3',
                    '∓','0','.']
    buttons_frame_2 = ['÷', 'x','-','+','=']
    buttons_frame_3 = ['CE','C','◄']

    frame_border_width = 2

    app_frame = CTkFrame(window, width=364, height=550,
                    fg_color=bg, bg_color=bg,
                    corner_radius=14)
    app_frame.place(relx=0.5, rely=0.5, anchor='center')

    frame_1 = CTkFrame(app_frame, width=240, height=319, 
                    border_color='#82B8FF', bg_color=bg,
                    border_width=frame_border_width, fg_color= bg,
                    corner_radius=14)
    frame_1.place(x=17, y=215)

    frame_2 = CTkFrame(app_frame, width=84, height=413, 
                    border_color="#ED5555", bg_color=bg,
                    border_width= frame_border_width, fg_color= bg,
                    corner_radius=14)
    frame_2.place(x=265, y=128)

    frame_3 = CTkFrame(app_frame
                       , width=240, height=87, 
                    border_color="#66FF8C", bg_color=bg,
                    border_width=frame_border_width, fg_color= bg,
                    corner_radius=14)
    frame_3.place(x=17, y=128)

    frame_4 = CTkFrame(app_frame, width=330, height=100, 
                    fg_color="#292929", bg_color=bg,
                    corner_radius=14, border_width=frame_border_width, 
                    border_color="#EAE9E9")
    frame_4.place(x=17,y=19)

number_1 = ''
number_2 = ''
result = 0
operation_io = 0
operations = deque(maxlen=2)

def clicked(num): # frame 1 buttons
    global number_1, number_2, operation_io, number_show

    #number_1 = ''
    #number_2 = ''

    print(f'Op: {operation_io}')

    if num == '.' and operation_io == 0 and '.' in number_1: # copilot
        return

    if num == '∓':
        if operation_io == 0 and number_1 != '':
            number_1 = str(Decimal(number_1) * -1) #GPT helped with debugging
            number_show.configure(text = number_1)

        if operation_io == 1 and number_2 != '':
            number_2 = str(Decimal(number_2) * -1)
            number_show.configure(text = number_2)
    else:
        if operation_io == 0:
            if len(number_1) >= 17:
                return
            number_1 = str(number_1) + str(num)
            number_show.configure(text = number_1)

        if operation_io == 1:
            if len(number_2) >= 17:
                return
            number_2 = str(number_2) + str(num)
            number_show.configure(text = number_2)

def clicked_math(operation): #frame 2 buttons
    global operation_io, number_1, number_2, result, operations

    if operation_io == 1 and operation != '=' and (operations[0] != operations[len(operations)-1] and len(operations) > 0): 
        operation_io = 0
    else:
        operation_io = 1    
    
    operations.append(operation)

    #inefficient code, but it works for now :) I will refactor later...
    def calculate():
        global operation_io, number_1, number_2, result, operations
        if operations[len(operations)-1] == '=' and len(operations) > 1 and operations[-2] != '=' and (number_1 != '' and number_2 != ''): #index error fix - Copilot
            operation_io = 0
            if operations[-2] == 'x':
                result = str(Decimal(number_1) * Decimal(number_2))
            if operations[-2] == '-':
                result = str(Decimal(number_1) - Decimal(number_2))
            if operations[-2] == '+':
                result = str(Decimal(number_1) + Decimal(number_2))
            if operations[-2] == '÷':
                if Decimal(number_2) == 0:
                    result = ' '
                    print('Error')
                else:
                    result = str(Decimal(number_1) / Decimal(number_2))

            if result == ' ':
                number_1 = ''
                number_show.configure(text = 'Error')
            else:
                number_1 = result
                number_show.configure(text = result)

            number_2 = ''

        elif operation in ['÷', 'x', '-', '+'] and number_2 != '': 
            operation_io = 0
            if operation == 'x':
                result = str(Decimal(number_1) * Decimal(number_2))
            if operation == '-':
                result = str(Decimal(number_1) - Decimal(number_2))
            if operation == '+':
                result = str(Decimal(number_1) + Decimal(number_2))
            if operation == '÷':
                if Decimal(number_2) == 0:
                    result = ' '
                    print('Error')
                else:
                    result = str(Decimal(number_1) / Decimal(number_2))

            if result == ' ':
                number_1 = ''
                number_show.configure(text = 'Error')
            else:
                number_1 = result
                number_show.configure(text = result)

            number_2 = ''    

        if len(str(result)) >= 17:
            result = result[:14]
            number_1 = result
            number_show.configure(text = result + '...')

    calculate()

    print(f"Num1: {number_1}, Num2: {number_2}, op: {operation_io}, result: {result}, operations: {operations}") # debugging

def clicked_clear(text): #frame 3 buttons
    print(f'Clear button, {text} was clicked!!!') # debugging

    global number_1, number_2, result, operation_io, operations

    if text == 'CE':
        number_1 = ''
        number_2 = ''
        result = 0
        operation_io = 0
        operations = deque(maxlen=2)
        number_show.configure(text = '0')

    if text == 'C':
        if operation_io == 0:
            number_1 = ''
        else:
            number_2 = ''
        operation_io = 1
        number_show.configure(text = '0')
        print(f"Num1: {number_1}, Num2: {number_2}") # checking if the numbers are cleared properly

    if text == '◄':

        if operation_io == 0:
            if len(number_1) <= 1:
                number_1 = ''
                number_show.configure(text = '0')
                return
            else:
                number_1 = number_1[:-1]
                number_show.configure(text = number_1)

            #number_show.configure(text = number_1)
            print(f"Num1: {number_1}, Num2: {number_2}") # debugging

        if operation_io == 1:
            if len(number_2) <= 1:
                number_2 = ''
                number_show.configure(text = '0')
                return
            else:
                number_2 = number_2[:-1]
                number_show.configure(text = number_2)

            print(number_2) # debugging

def buttons():
    global number_show, buttons_library

    number_show = CTkLabel(frame_4, width=304, height=44,
                           text= '0', text_color="#fefefe",
                           font=('arial',32), anchor='e')
    number_show.place(x=13, y =26)

    buttons_library = {} # GPT helped with this idea of storing buttons in a dictionary for easy access later in the animation function

    size = 67

    for i in range(len(buttons_frame_1)):
        button_text = buttons_frame_1[i]

        button_1 = CTkButton(frame_1, width=size, height=size, corner_radius=9,
                            fg_color='#82B8FF', bg_color=bg, text=button_text,
                            hover_color="#90C0FD", font=('arial',24),
                            text_color="#43426E",
                            command= lambda text=button_text: clicked(text))
        
        button_1.grid(row=int(i/3), column=i%3, padx=6, pady=6) # row = i // 3 also works
        buttons_library[button_text] = button_1

    for i in range(len(buttons_frame_2)): #red
            button_text = buttons_frame_2[i]
    
            button_1 = CTkButton(frame_2, width=size, height=size, corner_radius=9,
                                fg_color='#FF8585', bg_color=bg, text=button_text,
                                hover_color="#FC8E8E", font=('arial',24),
                                text_color="#9D3939",
                                command= lambda text=button_text: clicked_math(operation=text))
            
            button_1.grid(row=i, column=0, padx=7.2, pady=7)
            buttons_library[button_text] = button_1 

    for i in range(len(buttons_frame_3)): # green frame
            button_text = buttons_frame_3[i]
    
            button_1 = CTkButton(frame_3, width=size, height=size, corner_radius=9,
                                fg_color="#59F17F", bg_color=bg, text=button_text,
                                hover_color="#87FFA5", font=('arial',24),
                                text_color="#318036",
                                command= lambda text=button_text: clicked_clear(text))
            
            button_1.grid(row=0, column=i, padx=6, pady=6)
            buttons_library[button_text] = button_1

def animation(bt): #button / hover color / normal color
    nc = ''
    hc = ''

    if bt in buttons_frame_1:
        nc = '#82B8FF'
        hc = "#A0C7FB"

    if bt in buttons_frame_2:
        nc = '#FF8585'
        hc = "#F7A5A5"

    if bt in buttons_frame_3:
        nc = '#59F17F'
        hc = "#96FFB1"

    buttons_library[bt].configure(fg_color = hc)
    window.after(75, 
                 lambda: buttons_library[str(bt)].configure(fg_color = nc))


def keyboard_input(event): # Learned from ChatGPT
    key = event.char
    s_key = event.keysym

    if s_key == 'Shift_L' or s_key == 'Shift_R':
        return

    if key in '0123456789':
        clicked(key)

    if key == '/':
        clicked_math('÷')
        animation('÷')

    if key == '*' or key == 'x':
        clicked_math('x')
        animation('x')

    if key in ['+', '-','=']:
        clicked_math(key)

    if s_key == 'Return':
        clicked_math('=')
        animation('=')

    if s_key == 'BackSpace':
        clicked_clear('◄')
        animation('◄')

    if key == '.':
        clicked('.')

    if s_key == 'Escape':
        clicked('∓')
        animation('∓')

    if s_key == 'Delete':
        clicked_clear('C')
        animation('C')  

    if key in buttons_library:
        animation(key)  

    if s_key.upper() in buttons_library:
        animation(s_key.upper()) 

setup()
frames()
buttons()

window.bind('<Key>', keyboard_input)
window.mainloop()