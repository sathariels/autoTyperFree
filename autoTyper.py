from tkinter import *
from tkinter import font
import pyautogui
import time
def create_gui():
    # Created the main window
    root = Tk()
    root.title("Auto Typer")
    # Creted the text box and the words above it, used pack for formatting
    textLabel = Label(root, text="Enter text to type:")
    textLabel.pack()
    #chagedthe font of the text label
    fontTuple = ("Comic Sans MS", 20, "bold")
    textLabel.configure(font=fontTuple)
    # Created the entry box for the user to enter the text they want to type, and stored it in the variable textBox
    textBox = Entry(root, width=50)
    textBox.pack()
    #Created the label that says WPM, used pack for formatting
    textLabel2 = Label(root, text="Enter WPM")
    textLabel2.pack()
    textLabel2.configure(font=fontTuple)
    # Created the entry box for the user to enter the WPM, and stored it in the variable wpm_entry
    wpm_entry = Entry(root, width=10)
    wpm_entry.pack()
    # returned it back into the fucntion in order for it to be used by the function convert(
    return root, textBox, wpm_entry

def convert():
    # Get the values from the entry boxes and convert them to strings and integers
    textToType = str(textBox.get())
    wpm = float(wpm_entry.get())
    intervals = float(14.20*(wpm**-1.15))
    updateButton()
    autoTyper(textToType, intervals)  # Call autoTyper with the converted values


def updateButton()  :
    startButton.config(text="Stop Typing", command = root.quit)
def autoTyper(textToType, intervals):
    time.sleep(3)
    pyautogui.write(textToType, interval= intervals)




root, textBox, wpm_entry = create_gui()

startButton = Button(root, text="Start Typing", command=convert)
startButton.pack()

root.mainloop()
