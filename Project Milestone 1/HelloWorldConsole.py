#!/usr/bin/env
# -- coding: utf-8 --

"""
Submission for Project Milestone 1, Task 2
by  Filiz Günal (#431174)
and Samuel Kwong (#430273)
"""


# Initialize dict with the corresponding language and greetings
language_dict = {
    'D': 'Guten Tag',
    'E': 'Hello',
    'F': 'Bonjour',
}

# List of language options
menu_options = ['[D]eutsch', '[E]nglish', '[F]rancais', '[Q]uit']

# Menu function that displays the language options
def print_menu():
    print("\nSelect one of the following:")
    for menu_option in menu_options:
        if menu_option != '[Q]uit':
            print("    ", end="")
        print(f"{menu_option}")
    print(">", end="")

# Console loop
while True:
    print_menu()
    selection = input().upper()
    # Quit if the input is a 'q'
    if selection == 'Q':
        print("Quitting...")
        break
    # Print invalid input if the input is not in the language dict
    if selection not in language_dict:
        print("Invalid input, please try again.")
    # Print the corresponding greeting from the langauge dict
    else:
        greeting = language_dict[selection]
        print(greeting)