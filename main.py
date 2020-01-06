from tkinter import *
from tkinter import messagebox
from decimal import *
from functions import *


def process_functions():
    try:
        file_input = open("functions.calc", 'r')
        data = file_input.readlines()
        file_input.close()
        funcs = []
        for idx in range(0, len(data)):
            funcs.append(data[idx][0:len(data[idx]) - 1])
        return funcs
    except FileNotFoundError:
        return []


def save_func(code):
    global funcs
    code = code.get("1.0", END)
    print(code)
    if code:
        try:
            tree = compile(code, "<string>", "exec")
            def_idx = code.find("def")
            newline_idx = code.find("\n")
            definition = code[def_idx + 3:newline_idx]
            definition.replace(" ", "")
            if '(' in definition and ")" in definition and ":" in definition:
                left_bracket_idx = definition.find("(")
                right_bracket_idx = definition.find(")")
                if left_bracket_idx > right_bracket_idx:
                    messagebox.showerror("code error", "code must be a function")
                else:
                    func_name = definition[0: left_bracket_idx]
                    functions_name_output_file = open("functions.calc", 'a')
                    functions_output_file = open("functions.py", 'a')
                    functions_name_output_file.write(func_name + '\n')
                    functions_output_file.write(code + '\n')
            else:
                messagebox.showerror("code error", "code must be a function")
        except Exception as e:
            messagebox.showerror("code error", e)


root = Tk()
root.title('Calculator')

buttons = (('(', ')', '←', 'CE'),
           ('7', '8', '9', '/', '4'),
           ('4', '5', '6', '*', '4'),
           ('1', '2', '3', '-', '4'),
           ('0', '.', '=', '+', '4'),
           ('(', ')', ',', '_', '4')
           )

activeStr = ''
funcs = process_functions()
menu = Menu(root)
root.config(menu=menu)
menu.add_command(label='Функций', command=lambda _root=root: functions_window(_root))
label = Label(root, text='0', width=35, bg="white")
label.grid(row=0, column=0, columnspan=4, sticky="nsew")


def functions_window(main_window):
    window = Toplevel(main_window)
    window.geometry("200x200")
    funcs = process_functions()
    lines = int((len(funcs) / 5) % 1 + 1)
    idx_i, idx_j = 0, 0
    for i in range(lines):
        for j in range(5):
            if 5 * i + j < len(funcs):
                button = Button(window, text=funcs[i * 5 + j], command=lambda text=funcs[5 * i + j]: click(text))
                button.grid(row=i, column=j, sticky="nsew")
            elif (idx_i, idx_j) == (0, 0):
                idx_i, idx_j = i, j
    button = Button(window, text="+", command=lambda _root=window: add_function_window(_root))
    button.grid(row=idx_i, column=idx_j, sticky="nsew")
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)


def add_function_window(root):
    window = Toplevel(root)
    window.geometry("500x700")
    code = Text(window, state=NORMAL, height=43)
    code.place(x=0, y=3)
    ok_button = Button(window, text="ok", command=lambda _code=code: save_func(_code))
    ok_button.place(x=0, y=675, width=500)


def calculate():
    global activeStr
    result = activeStr
    activeStr = activeStr.replace('^', '**')
    if 'inf' in activeStr:
        return 'inf'
    try:
        result = eval(activeStr)
    except ZeroDivisionError:
        result = 'inf'
    except Exception as e:
        messagebox.showerror("runtime error", e)
    return result


def click(text):
    global activeStr
    if activeStr == '0':
        activeStr = ''
    if text in funcs:
        text += "()"
    if text == 'CE':
        activeStr = ''
    elif '0' <= text <= '9':
        activeStr += text
    elif text == '.':
        if '.' not in activeStr and activeStr:
            activeStr += text
    elif text == '←':
        if activeStr:
            activeStr = activeStr[0:len(activeStr) - 1]
    elif text == '=':
        activeStr = str(calculate())
    else:
        activeStr += text
    label.configure(text=activeStr)


for row in range(6):
    for col in range(4):
        button = Button(root, text=buttons[row][col],
                        command=lambda row=row, col=col: click(buttons[row][col]))
        button.grid(row=row + 1, column=col, sticky="nsew")

root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(5, weight=1)

root.mainloop()
