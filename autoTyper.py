from tkinter import *
from tkinter import font
import pyautogui
import time
import threading


class ExpandoText(Text):
    def insert(self, *args, **kwargs):  # This method is responsible for inserting text into the widget whenever the
        # user types something.
        result = Text.insert(self, *args, **kwargs)  # This method is responsible for inserting text into the widget
        # whenever the user types into the word box
        self.resetHeight()  # calls method to recacluate the height of the widger based on its content.
        return result

    # self is used in class methods to refer to the instance of the class. *args collects all positional arguments
    # into a tuple. **kwargs collects all keyword arguments into a dictionary.

    def resetHeight(self):
        height = self.tk.call((self._w, "count", "-update", "-displaylines", "1.0", "end"))
        # self.tk.call(()) asks the systerm about the hieghg of out text widget.
        # seld._w refers to the internal name of the text widget
        # count -update -displaylines 1.0 end asks the system to count the number of lines in the text widget
        # 1.0 refers to the first line of the text widget
        # end refers to the last line of the text widget
        self.configure(height=height)


def create_gui():
    # Created the main window
    root = Tk()
    root.title("Auto Typer")

    # Created the text box using ExpandoText
    textLabel = Label(root, text="Enter text to type:")
    textLabel.pack()
    fontTuple = ("Comic Sans MS", 20, "bold")
    textLabel.configure(font=fontTuple)
    textBox = ExpandoText(root, width=50)
    textBox.pack()

    # Created the label that says WPM, used pack for formatting
    textLabel2 = Label(root, text="Enter WPM")
    textLabel2.pack()
    textLabel2.configure(font=fontTuple)

    # Created the entry box for the user to enter the WPM, and stored it in the variable wpm_entry
    wpm_entry = Entry(root, width=10)
    wpm_entry.pack()

    return root, textBox, wpm_entry


def convert():
    textToType = str(textBox.get("1.0",'end-1c'))
    if textToType == "":
        textToTypeLabel = Label(root, text="Enter text to type")
        textToTypeLabel.pack()
        textToTypeLabel.after(5000, textToTypeLabel.destroy)
    try:
        wpm = float(wpm_entry.get())
    except ValueError:
        errorLabel = Label(root, text="Please input a number in the WPM box")
        errorLabel.pack()
        errorLabel.after(5000, errorLabel.destroy)

    intervals = float(14.20 * (wpm ** -1.15))
    updateButton()
    threading.Thread(target=autoTyper, args=(textToType, intervals)).start()


def updateButton():
    if startButton.cget("text") == "Start Typing":
        startButton.config(text="Stop Typing", command=lambda: [stopTyping(), updateButton()])
    elif startButton.cget("text") == "Stop Typing":
        startButton.config(text="Start Typing", command=convert)


def stopTyping():
    pyautogui.moveTo(0, 0)


def autoTyper(textToType, intervals):
    time.sleep(3)
    pyautogui.write(textToType, interval=intervals)


root, textBox, wpm_entry = create_gui()

startButton = Button(root, text="Start Typing", command=convert)
startButton.pack()

root.mainloop()
