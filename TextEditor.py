from tkinter import *
from tkinter import messagebox,filedialog, colorchooser, font
import os
import sys

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
window_title = "Untitled"
savedContent = "\n"
fileOpenPath = ""

def checkContent(event):
    global window_title
    global savedContent
    if textArea.get(1.0, END) != savedContent:
        window_title = "*" + window_title
        window.title(window_title)
        window_title = window_title.replace("*","")
    else:
        window.title(window_title)
    print(savedContent + " and " + textArea.get(1.0, END))

def newFile():
    global window_title, savedContent
    answer = messagebox.askyesnocancel(title="SonText", message="Do you want save change of {} ?".format(window_title))
    if answer == True:
        saveFile("")
        window_title = "Untitled"
        window.title(window_title)
    elif answer == False:
        window_title = "Untitled"
        window.title(window_title)
    textArea.delete(1.0, END)
    savedContent = "\n"

def openFile():
    global window_title
    global savedContent
    global fileOpenPath
    try:
        filePath = filedialog.askopenfilename(initialdir = "C:\\Users\\nguye\\PycharmProjects\\PythonBasic\\venv",
                                              filetypes = (("Text File", "*.txt"), ("All File", "*.*"), ("Python File", "*.py")),
                                              title = "Open File")
        file = open(filePath, "r")
        window_title = os.path.basename(filePath)
        window.title(window_title)
        textArea.delete(1.0, END)
        data = file.read()
        textArea.insert(1.0, data)
        savedContent = data + "\n"
        fileOpenPath = filePath
        file.close()
    except Exception:
        print("Can't open the file")

def saveFile(event):
    global window_title, savedContent
    print(event)
    if fileOpenPath == "":
        return saveAsFile()
    else:
        try:
            file = open(fileOpenPath, "w")
            file.write(textArea.get(1.0, END))
            window_title = os.path.basename(fileOpenPath)
            window.title(window_title)
            savedContent = textArea.get(1.0, END)
            file.close()
        except Exception:
            print("Can't open file")

def saveAsFile():
    global window_title, savedContent
    try:
        filePath = filedialog.asksaveasfilename(defaultextension = ".txt",
                                        initialdir = "C:\\Users\\nguye\\PycharmProjects\\PythonBasic\\venv",
                                        filetypes = [("Text File", ".txt"), ("HTML File", ".html"), ("All File", ".*")],
                                        title = "Save As")
        file = open(filePath, "w")
        file.write(textArea.get(1.0, END))
        window_title = os.path.basename(filePath)
        window.title(window_title)
        file.close()
        savedContent = textArea.get(1.0, END)
    except Exception:
        return False

def exitFile():
    global window_title
    if textArea.get(1.0, END) == savedContent:
        sys.exit(0)
    else:
        answer = messagebox.askyesnocancel(title="SonText",
                                           message="Do you want save change of {} ?".format(window_title))
        if answer is None:
            return
        if answer == True:
            check = saveFile("")
            print(check)
            if check == False:
                return
            else:
                sys.exit(0)
        else:
            sys.exit(0)

def cut():
    textArea.event_generate("<<Cut>>")

def copy():
    textArea.event_generate("<<Copy>>")

def paste():
    textArea.event_generate("<<Paste>>")

def changeColor():
    color = colorchooser.askcolor()
    textArea.config(fg = color[1])

def changeFont(*args):
    textArea.config(font = (font_families.get(), int(font_size.get())))

def about():
    messagebox.showinfo(title = "About", message="The text editor of Sơn")

if __name__ == "__main__":
    window = Tk()
    font_size = StringVar()
    font_size.set("15")
    font_families = StringVar()
    font_families.set("Arial")
    window.title(window_title)
    window.bind("<Key>", checkContent)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_x = int(screen_width / 2 - WINDOW_WIDTH / 2)
    window_y = int(screen_height / 2 - WINDOW_HEIGHT / 2)
    window.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, window_x, window_y))
    textArea = Text(window, font = (font_families.get(), int(font_size.get())))
    scollBar = Scrollbar(window, command = textArea.yview)
    scollBar.pack(side=RIGHT, fill=Y)
    frame = Frame(window)
    font_box = OptionMenu(frame, font_families, *font.families(), command=changeFont).grid(row = 0, column = 0)
    size_box = Spinbox(frame, from_ = 0, to = 100, textvariable = font_size, command = changeFont).grid(row = 0, column = 1)
    colorButton = Button(frame, text = "Color", command = changeColor).grid(row = 0, column = 2)
    frame.pack(side = BOTTOM)
    textArea.pack(side = LEFT, expand = True, fill = "both")
    textArea.config(yscrollcommand = scollBar.set)
    menuBar = Menu(window)
    window.config(menu = menuBar)
    fileMenu = Menu(menuBar, tearoff = False)
    editMenu = Menu(menuBar, tearoff = False)
    formatMenu = Menu(menuBar, tearoff = False)
    helpMenu = Menu(menuBar, tearoff = False)
    menuBar.add_cascade(menu = fileMenu, label = "File")
    fileMenu.add_command(label = "New", command = newFile)
    fileMenu.add_command(label = "Open", command = openFile)
    fileMenu.add_command(label = "Save", command = lambda : saveFile(""))
    fileMenu.add_command(label = "Save As", command = saveAsFile)
    fileMenu.add_separator()
    fileMenu.add_command(label = "Exit", command = exitFile)
    menuBar.add_cascade(menu = editMenu, label = "Edit")
    editMenu.add_command(label = "Cut", command = cut)
    editMenu.add_command(label = "Copy", command = copy)
    editMenu.add_separator()
    editMenu.add_command(label = "Paste", command = paste)
    menuBar.add_cascade(label = "Help", menu = helpMenu)
    helpMenu.add_command(label = "About", command = about)
    window.bind("<Control-KeyPress-s>", saveFile)
    window.bind("<Control-KeyPress-S>", saveFile)
    window.protocol("WM_DELETE_WINDOW", exitFile)
    window.mainloop()