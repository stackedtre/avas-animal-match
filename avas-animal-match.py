#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 22:36:46 2025

@author: tre
"""

# -*- coding: utf-8 -*-

## Import Libraries


import tkinter as tk              # GUI
from functools import partial     # Button functions
from PIL import Image, ImageTk    # Loading and resizing images
import random                     # To shuffle cards
from playsound import playsound   # Play audio files
import threading                  # Run sounds without pausing the GUI


"""## Open Window"""

root = tk.Tk()                            # Create window
root.title("Ava's Animal Match Game")     # Window title
rows = 4
cols = 4

"""## List of Dictionaries for Animals"""

animals = [
    {"name": "cat", "image": "images/cat.png", "sound": "sounds/cat.wav"},
    {"name": "dog", "image": "images/dog.png", "sound": "sounds/dog.wav"},
    {"name": "cow", "image": "images/cow.png", "sound": "sounds/cow.wav"},
    {"name": "duck", "image": "images/duck.png", "sound": "sounds/duck.wav"},
    {"name": "lion", "image": "images/lion.png", "sound": "sounds/lion.wav"},
    {"name": "elephant", "image": "images/elephant.png", "sound": "sounds/elephant.wav"},
    {"name": "sheep", "image": "images/sheep.png", "sound": "sounds/sheep.wav"},
    {"name": "horse", "image": "images/horse.png", "sound": "sounds/horse.wav"}
]

"""## Card Assignment"""

cards = animals * 2         # Duplicate the animals
random.shuffle(cards)       # Shuffle the list randomly

"""## Create image cache to prevent garbage collection"""

image_cache = {}

"""## Load card back image"""

try:
    card_back_img = Image.open("images/card_back.png").resize((80, 80))
    card_back = ImageTk.PhotoImage(card_back_img)
    image_cache["card_back"] = card_back
except Exception as e:
    print(f"Error loading card back image: {e}")
    # Fallback card back if image loading fails
    card_back = None

"""## Load and resize animal photos on cards"""

for animal in cards:
    try:
        img = Image.open(animal["image"]).resize((80, 80))
        animal_photo = ImageTk.PhotoImage(img)
        animal["photo"] = animal_photo
        image_cache[animal["name"]] = animal_photo  # Keep reference to prevent garbage collection
    except Exception as e:
        print(f"Error loading image for {animal['name']}: {e}")
    
"""## Create button and function variables"""

buttons = []
revealed = []
matched = []

"""## Add sounds"""

def play_animal_sound(sound_path):
    try:
        threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
    except Exception as e:
        print(f"Error playing sound {sound_path}: {e}")

"""## Button clicks"""

def on_card_click(row, col):
    idx = row * cols + col
    
    # Skip if the card is already matched or revealed
    if idx in matched or idx in revealed:
        return
    
    button = buttons[idx]
    button.config(image=cards[idx]['photo'], state='disabled')
    revealed.append(idx)
    
    # Check for a match when two cards are revealed
    if len(revealed) == 2:
        root.after(1000, check_match)

def check_match():
    i1, i2 = revealed[0], revealed[1]
    
    if cards[i1]["name"] == cards[i2]["name"]:
        matched.append(i1)
        matched.append(i2)
        play_animal_sound(cards[i1]["sound"])
        revealed.clear()
    else:
        buttons[i1].config(image=image_cache["card_back"], state='normal')
        buttons[i2].config(image=image_cache["card_back"], state='normal')
        revealed.clear()
    
    # Check for win condition
    if len(matched) == len(cards):
        win_label = tk.Label(root, text="Yay! Ava matched all the animals! 🐾", font=("Arial", 16))
        win_label.grid(row=rows, column=0, columnspan=cols)

"""## Button Grid"""

for r in range(rows):
    for c in range(cols):
        idx = r * cols + c
        btn = tk.Button(root, image=image_cache["card_back"], width=80, height=80, command=partial(on_card_click, r, c))
        btn.grid(row=r, column=c, padx=5, pady=5)
        buttons.append(btn)

# Start the main loop
root.mainloop()