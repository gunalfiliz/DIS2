#!/usr/bin/env
# -- coding: utf-8 --

"""
Submission for Project Milestone 1, Task 3
by  Filiz Günal (#431174)
and Samuel Kwong (#430273)
"""

from tkinter import *

# Initialize Language and Greeting Dictionary
language_dict = {
    'Deutsch': 'Guten Tag',
    'English': 'Hello',
    'Français': 'Bonjour',
}

# Initialize Langauge Options
language_options = ['Deutsch', 'English', 'Francais']

# Function to change the greeting label when a language is selected
def change_label(language_option):
    language_string = language_dict[language_option]
    languageLabel_string_var.set(language_string)

# Function to quit window when quit button is clicked
def quit_window():
    window.destroy()

window = Tk()
window.geometry('250x300')

# Initialize the StringVar that holds the greeting String
languageLabel_string_var = StringVar()
languageLabel_string_var.set('Please select a language.')

# Initialize the label with the StringVar that displays the greeting
languageLabel = Label(window, textvariable=languageLabel_string_var, fg='#F6A800')
languageLabel.pack(pady=4)

# Button frame that is the parent view for the buttons
buttonFrame = Frame(window)

# Creates a button for every language option, calls the change_label function when pressed
for language_option in language_options:
    button = Button(buttonFrame,
                       text=language_option,
                       width=8,
                       fg="black",
                       command= lambda l=language_option: change_label(l))
    button.pack(side=TOP, padx=4, pady=4)
buttonFrame.pack()

# Create the quit button at the bottom right of the window, calls the quit_window function when pressed
quit_button = Button(window,
                        text="Quit",
                        width=8,
                        fg="black",
                        command=quit_window
                    )
quit_button.pack(side=BOTTOM, anchor=SE, padx=4, pady=4)

window.mainloop()