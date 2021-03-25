from sympy import *

import numpy as np
import string
import hill_cipher_samples

init_printing(use_latex='mathjax')

def show_encoding():
    alphabet = '_' + string.ascii_uppercase
    for c in alphabet:
        print("{:>3}".format(c), end='')
    print('')
    for n in range(len(alphabet)):
        print("{:>3}".format(n), end='')

def num2char(numlist):
    N = 20
    chars = []
    for i, n in enumerate(numlist):
        n = int(round(n))
        print("{:>4}".format(n), end = ''),
        if n == 0:
            chars.append('_')
        elif n < 0 or n > 26:
            chars.append("#")
        else:
            chars.append(chr(n+64))
        if (i+1)%N == 0 or i == len(numlist)-1:
            print('')
            for c in chars:
                print("{:>4}".format(c), end = ''),
            print('\n')
            chars = []

def num2char_text_only(numlist):
    chars = []
    for n in numlist:
        n = int(round(n))
        if n == 0:
            chars.append('_')
        elif n < 0 or n > 26:
            chars.append("#")
        else:
            chars.append(chr(n+64))
    return "".join(chars)

def char2num(s):
    numlist = []
    S = s.upper()
    for c in S:
        if c in string.ascii_uppercase:
            numlist.append(ord(c) - ord('A') + 1)
        elif c == ' ':
            numlist.append(0)
        else:
            numlist.append(99)
    return numlist

def choose_key():
    d = 0
    while d not in  [1, -1]:
        A = Matrix(np.random.randint(0, 4, (3,3)))
        d = A.det()
    return A, A.inv()

def hill_encoder(A=None, text=None,s=None):
    if text == None:
            lines = text_samples.split("\n")
            text = np.random.choice(lines).strip()
    text = text + ' '*(((-1)*len(text))%3)
    nums = Matrix(char2num(text)).reshape(len(text)//3, 3).T
    if A != None:
        AI = A.inv()
    else:
        A, AI = choose_key()
    cipher = [int(x) for x in list((A*nums).T)]
    if s == 'show':
        return cipher, text, A, AI
    else:
        return cipher

def make_cipher(s=None):
    lines = text_samples.split("\n")
    text = 'CLASSIFIED ' + np.random.choice(lines).strip()
    return hill_encoder(s=s, text=text)

def tokenizer(*, kl, sz):
    m =  Matrix(sz).reshape(len(sz)//3, 3).T
    return num2char_text_only([int(x) for x in list((kl*m).T)])

def simple_num_generator(seed):
    a = 1103515245
    c = 12345
    m = 181
    return (a*seed + c) % m

def cipher_generator(pnum):
    try:
        pnum = int(pnum)
        cnum = simple_num_generator(pnum)
        cipher = hill_cipher_samples.encoded["ciphers"][cnum]
    except Exception:
        print("Error: Invalid format of the UB person number")
        return None
    return cipher
