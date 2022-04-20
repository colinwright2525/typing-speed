from tkinter import *
import json
import requests
import tkinter
from PIL import ImageTk, Image
import time

stopwatch = None
count = 0

#-------API Request--------#
API_ENDPOINT = 'https://random-word-api.herokuapp.com/word?number=15'

all_response = ''
for steps in range(12):
    response = requests.get(url=API_ENDPOINT).json()
    response.append('\n')
    response_text = ' '.join(response)
    print(response_text)
    all_response = all_response + response_text
    print(all_response)

#------Run Times-------#
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


#--------Timer---------#
@run_once
def start_count(event):
    global count, stopwatch
    count = 60
    if count > 0:
        stopwatch = window.after(1000, count_down, count -1)


def count_down(count):
    global stopwatch
    timer.config(text=str(count))
    if count > 0:
        stopwatch = window.after(1000, count_down, count -1)
    else:
        wpm = determine_speed()
        timer.config(text=f'Time\'s up! You scored {wpm} wpm. Not bad!')

def determine_speed():
    tally = 0
    words_typed = typing_space.get()
    words_typed_list = words_typed.split()
    all_response_list = all_response.split()
    for word in words_typed_list:
        if word in all_response_list:
            tally += 1
    return tally






#---------GUI-----------#

window = Tk()
window.title('Typing Speed')
window.config(padx=10, pady=20)

font_tuple = ("Helvetica", 12)
title_tuple = ("Terminal", 24, 'bold')

title = Label(text='SPEED TYPING', font=title_tuple, fg='green')
title.grid(column=0, row=0, columnspan=2)

canvas = Canvas(width=125, height=125)
type_img = ImageTk.PhotoImage(Image.open('static/images/typing_fast.jpeg'))
canvas.create_image(62.5, 62.5, image=type_img)
canvas.grid(column=0, row=1, columnspan=2)

timer = Label(text='Timer: 60', fg='orange', font=('courier', 32, 'bold'))
timer.grid(column=0, row=2, columnspan=2)

text = Label(text=all_response, font=font_tuple)
text.grid(column=0, row=3, columnspan=2)

begin_typing = Label(text='Begin typing here when ready:', font=font_tuple, fg='green')
begin_typing.grid(column=0, row=4)

typing_space = Entry(width=100, font=font_tuple)
typing_space.grid(column=1, row=4)

#-------Key Response--------#
window.bind('<Key>', start_count)



window.mainloop()
