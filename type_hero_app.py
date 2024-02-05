from tkinter import *
import random
import csv
import datetime
import simpleaudio as sa
from image_processing import process_image
from prettytable import PrettyTable
import os
import sys

# APP EXPORT DECLARATIONS ________________________________
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

COMMON_WORDS_CSV_PATH = os.path.join(application_path, 'common_words.csv')
MICHAEL_JOHNSON_JPEG_PATH = os.path.join(application_path, 'michael johnson.jpeg')
SONIC_KEYBOARD_JPEG_PATH = os.path.join(application_path, 'sonic keyboard.jpeg')
UZI_JPEG_PATH = os.path.join(application_path, 'Uzi.jpeg')
BLANK_SCORES_CSV_PATH = os.path.join(application_path, 'blank_scores.csv')

START_WAV_PATH = os.path.join(application_path, 'START.wav')
FINISH_WAV_PATH = os.path.join(application_path, 'FINISH.wav')

# CONSTANTS ________________________________
start_sfx = sa.WaveObject.from_wave_file(START_WAV_PATH)
finish_sfx = sa.WaveObject.from_wave_file(FINISH_WAV_PATH)

file = open(COMMON_WORDS_CSV_PATH, "r")
WORDS = list(csv.reader(file))
file.close()
WORDS = WORDS[0]
print(WORDS)

INSTRUCTIONS = """The world needed a type hero. Your mission:\n
To type each word displayed on the screen followed by <return>.\n
Don't worry about upper/lower case. You have one minute.\n
\t\t\t\tReady?"""

GREY = "#E7DFD5"
LIGHT_BLUE = "#84A9AC"
MED_BLUE = "#3B6978"
DARK_BLUE = "#204051"
FONT_SERIF = "Palatino Linotype"
FONT_SANS = "Lucida Sans Unicode"

WORDS_SUCC_TYPED = 0

# RESULTS ________________________________
def show_results():
    global WORDS_SUCC_TYPED
    finish_sfx.play()
    canvas.delete('all')
    canvas.config(bg=DARK_BLUE)
    word_display.destroy()
    type_box.destroy()

    results.place(x=122, y=303)
    words_per_second = round(WORDS_SUCC_TYPED/60, 3)
    with open(BLANK_SCORES_CSV_PATH, 'a+', newline='') as scores:
        writer = csv.writer(scores)
        writer.writerow([now, words_per_second])

        scores.seek(0)
        reader = csv.reader(scores)
        high_scores = sorted(reader, key=lambda x: float(x[1]), reverse=True)[:5]
        leaderboard = PrettyTable()
        leaderboard.field_names = ["When", "Speed"]
        leaderboard.align = "c"
        for hs in high_scores:
            leaderboard.add_row(hs)

    results.config(text=f"You typed at a speed of {words_per_second} words per second!\n\n"
                        f"Your high scores: \n\n"
                        f"{leaderboard}")


# TYPING TEST ________________________________
def test_underway():
    start_sfx.play()
    canvas.delete('all')
    start_button.destroy()

    # USER TYPEBOX
    def user_entry(event):
        global WORDS_SUCC_TYPED, CURRENT_WORD, type_box
        user_input = type_box.get()
        type_box.delete(0, END)
        if user_input.lower() == CURRENT_WORD:
            WORDS_SUCC_TYPED += 1
            print(f"Words typed: {WORDS_SUCC_TYPED}")
            get_word()

    type_box.place(x=377, y=466)
    type_box.bind("<Return>", user_entry)
    type_box.focus_set()
    window.update_idletasks()

    # CYCLE THROUGH THE WORDS
    def get_word():
        global WORDS, CURRENT_WORD
        CURRENT_WORD = random.choice(WORDS).lower()
        WORDS.remove(CURRENT_WORD)
        print(CURRENT_WORD, len(WORDS))
        word_display.place(x=377, y=355)
        word_display.config(text=CURRENT_WORD.upper())

    get_word()

    seconds = [61]
    timer_display = canvas.create_text(480, 255, text=f"{seconds[0]} seconds remaining",
                                       fill=DARK_BLUE, font=(FONT_SERIF, 22))

    # COUNTDOWN TIMER
    def update_timer():
        seconds[0] -= 1
        canvas.itemconfig(timer_display, text=f"{seconds[0]} seconds remaining")

        if seconds[0] > 0:
            window.after(1000, update_timer)
        else:
            show_results()

    update_timer()

# UI ________________________________
window = Tk()
window.title("Typing Speed Challenge")
window.config(padx=22, pady=22)

now = datetime.datetime.now()
now = now.strftime("%H:%M %d/%m/%Y")

keyboard_img = process_image(SONIC_KEYBOARD_JPEG_PATH, (707, 707))
michael_j_img = process_image(MICHAEL_JOHNSON_JPEG_PATH, (202, 202))
uzi_img = process_image(UZI_JPEG_PATH, (222, 202))

canvas = Canvas(width=1001, height=1001, bg=GREY)
title=canvas.create_text(500, 202, text="Type Hero", fill=MED_BLUE, font=(FONT_SERIF, 55))
canvas.create_image(377, 313, image=uzi_img)
canvas.create_image(622, 313, image=michael_j_img)
opening_text=canvas.create_text(500, 477, text=INSTRUCTIONS, fill=DARK_BLUE, font=(FONT_SANS, 20))
canvas.create_image(500, 633+44, image=keyboard_img)
canvas.grid(column=1, row=1)

start_button = Button(text="Let's Go", highlightbackground=LIGHT_BLUE, highlightthickness=0,
                      command=test_underway, font=(FONT_SERIF, 33))
start_button.place(x=422, y=699+33)

word_display = Label(text=None, fg=MED_BLUE, bg=GREY, font=(FONT_SERIF, 44))
type_box = Entry(window, bg=LIGHT_BLUE, fg=DARK_BLUE)
results = Label(text=None, fg=LIGHT_BLUE, bg=DARK_BLUE, font=(FONT_SANS, 33))

window.mainloop()
