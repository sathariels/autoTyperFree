from tkinter import *
from tkinter import font
import pyautogui
import time
import threading
import string
import random
randomInt = random.randint(50,70)
pauseDuration = random.uniform(4, 10)
isPaused = False # Both functions need to pause and resume together to maintain consistent behavior. The flag communicates the pause state to both functions.
# The flag provides a simple mechanism to control the flow of the functions based on whether a pause is required.
lock = threading.Lock() # used in order to surcumvent teh race condition wheere both chooseLEtter and autoTyper are using the same shared data lock prevents them from doing so and thuse allows it to work
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
        # self._w refers to the internal name of the text widget
        # count -update -displaylines 1.0 end asks the system to count the number of lines in the text widget
        # 1.0 refers to the first line of the text widget
        # end refers to the last line of the text widget
        self.configure(height=height)


def create_gui():
    # Created the main window
    root = Tk()
    root.title("Auto Typer")
    root.configure(bg="#000000")  # Set background color for the main window

    # Define color scheme
    bg_color = "#000000"  # Black background
    frame_bg_color = "#333333"  # Dark gray for frames
    label_color = "#ffffff"  # White text for labels
    entry_bg_color = "#666666"  # Medium gray for entry backgrounds
    font_tuple = ("Arial", 14)
    label_font_tuple = ("Arial", 12, "bold")
    author_font_tuple = ("Arial", 10, "italic")

    # Frame for Text Input
    text_frame = Frame(root, bg=frame_bg_color, bd=2, relief="groove", padx=10, pady=10)
    text_frame.pack(pady=10, padx=10, fill='x')

    textLabel = Label(text_frame, text="Enter text to type:", font=label_font_tuple, bg=frame_bg_color, fg=label_color)
    textLabel.grid(row=0, column=0, sticky='w')

    textBox = ExpandoText(text_frame, width=50, height=10, bg=entry_bg_color, fg=label_color)
    textBox.grid(row=1, column=0, pady=5)

    # Frame for WPM Input
    wpm_frame = Frame(root, bg=frame_bg_color, bd=2, relief="groove", padx=10, pady=10)
    wpm_frame.pack(pady=10, padx=10, fill='x')

    textLabel2 = Label(wpm_frame, text="Enter WPM:", font=label_font_tuple, bg=frame_bg_color, fg=label_color)
    textLabel2.grid(row=0, column=0, sticky='w')

    wpm_entry = Entry(wpm_frame, width=10, bg=entry_bg_color, fg=label_color)
    wpm_entry.grid(row=0, column=1, padx=5)

    # Frame for Mistakes Input
    mistakes_frame = Frame(root, bg=frame_bg_color, bd=2, relief="groove", padx=10, pady=10)
    mistakes_frame.pack(pady=10, padx=10, fill='x')

    textLabel3 = Label(mistakes_frame, text="Enter Mistakes:", font=label_font_tuple, bg=frame_bg_color, fg=label_color)
    textLabel3.grid(row=0, column=0, sticky='w')

    mistakesEntry = Entry(mistakes_frame, width=10, bg=entry_bg_color, fg=label_color)
    mistakesEntry.grid(row=0, column=1, padx=5)

    # Frame for Frequency Input
    frequency_frame = Frame(root, bg=frame_bg_color, bd=2, relief="groove", padx=10, pady=10)
    frequency_frame.pack(pady=10, padx=10, fill='x')

    textLabel4 = Label(frequency_frame, text="Enter Frequency (s):", font=label_font_tuple, bg=frame_bg_color,
                       fg=label_color)
    textLabel4.grid(row=0, column=0, sticky='w')

    frequenciesEntry = Entry(frequency_frame, width=10, bg=entry_bg_color, fg=label_color)
    frequenciesEntry.grid(row=0, column=1, padx=5)

    # Author Label
    authorLabel = Label(root, text="Project by Sathariel", font=author_font_tuple, bg=bg_color, fg=label_color)
    authorLabel.pack(pady=20)

    return root, textBox, wpm_entry, mistakesEntry, frequenciesEntry


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
    try:
        mistakes = int(mistakesEntry.get())
    except ValueError:
        errorLabel = Label(root, text="Please input a number in the mistakes box")
        errorLabel.pack()
        errorLabel.after(5000, errorLabel.destroy)
        stopTyping()
    try:
        frequencies = int(frequenciesEntry.get())
    except ValueError:
        errorLabel = Label(root, text="Please input a number in the frequency box")
        errorLabel.pack()
        errorLabel.after(5000, errorLabel.destroy)
        stopTyping()


    intervals = float(14.20 * (wpm ** -1.15))
    updateButton()
    threading.Thread(target=autoTyper, args=(textToType, intervals)).start()
    time.sleep(frequencies)
    threading.Thread(target=chooseLetter, args= (mistakes, frequencies, lock)).start()
root, textBox, wpm_entry, mistakesEntry, frequenciesEntry = create_gui()

def updateButton():
    if startButton.cget("text") == "Start Typing":
        startButton.config(text="Stop Typing", command=lambda: [stopTyping(), updateButton()])
    elif startButton.cget("text") == "Stop Typing":
        startButton.config(text="Start Typing", command=convert)


def stopTyping():
    pyautogui.moveTo(0, 0)




def autoTyper(textToType, intervals):
    global isPaused # have to use both lock and flag because if we were ot just use flag then autoTYper and chooseFlag will acesss the isPuased fucntion resulatin gin the race conditon. Also the state of the lock may change thus causing a rce codniton. 
    time.sleep(3)
    counter = 0
    for char in textToType:
        pyautogui.write(char, interval=intervals)
        counter += 1
        if counter % randomInt == 0:
            with lock:
                isPaused = True  # Indicate that autoTyper is paused
                time.sleep(pauseDuration) #Simulate a pause in typing
                isPaused = False  # Indicate that autoTyper has resumed
                counter = 0

    updateButton()
    stopTyping()

def chooseLetter(mistakes, frequencies, lock):
    global isPaused
    i = 0
    while i <= mistakes:
        with lock: # acquire lock to check is the isPaused flag
            if isPaused:  # If autoTyper is paused, pause chooseLetter as well
            time.sleep(pauseDuration)
            listOfLetter = list(string.ascii_lowercase)
            randomLetter = random.choice(listOfLetter)
            pyautogui.write(randomLetter)
            i += 1
            time.sleep(.9)
            if i == mistakes:
                mistakeEveryXSecond(mistakes, frequencies, lock)

def mistakeEveryXSecond(mistakes, frequencies, lock):
    threading.Timer(frequencies + 2*pauseDuration, chooseLetter, args=(mistakes, frequencies, lock)).start()
    print("Waiting for")



startButton = Button(root, text="Start Typing", command=convert)
startButton.pack()

root.mainloop()
