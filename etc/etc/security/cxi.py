"""
Copyright © 2020 Deinx Inc
"""
import os
import sys
import math
import random

def is_even(number):
    return number % 2 == 0
    
def get_even_letters(text, key=0):
    even_letters = []
    for counter in range(key, len(text)):
        if is_even(counter):
            even_letters.append(text[counter])
    return even_letters
    
def get_odd_letters(text, key=0):
    odd_letters = []
    for counter in range(key, len(text)):
        if not is_even(counter):
            odd_letters.append(text[counter])
    return odd_letters
    
def encrypt(text, key=0):
    letter_list = []
    if not is_even(len(text)):
        text = text + ' '
    even_letters = get_even_letters(text)
    odd_letters = get_odd_letters(text)
    for counter in range(key, int(len(text)/2)):
        letter_list.append(odd_letters[counter])
        letter_list.append(even_letters[counter])
    etext = ''.join(letter_list)
    return etext

def decrypt(text, key=0):
    letter_list = []
    if not is_even(len(text)):
        text = text + ' '
    even_letters = get_even_letters(text)
    odd_letters = get_odd_letters(text)
    for counter in range(0, int(len(text)/2)):
        letter_list.append(odd_letters[counter])
        letter_list.append(even_letters[counter])
    dtext = ''.join(letter_list)
    return dtext

class secret:
    def key(str):
        st = encrypt(str)
        return st
    
    

