import numpy
import matplotlib
import re
from tkinter import Tk
root = Tk()
root.withdraw()
number = root.clipboard_get()

# Regex finds all coefficiants and properly sorts them
equation_regex = re.compile(r'''(
    ((-?\d*)[x])?           # x and its coef (a)
    \s*[+]?                 # space and/or plus
    (([-]?\d*)[y])?         # y and its coef (b)
    \s*[+]?                 # space and/or plus
    (([-]?\d*)[z])?         # z and its coef (c)
    \s*[=]\s*               # equal sign
    (-?\d+)                 # value of d
    )''', re.VERBOSE)

xn_m = re.compile(r'''(^(-?[123456789]\d*)?x([+-][123456789]\d*)?|-?[123456789]\d*$)''', re.VERBOSE)

text = str(root.clipboard_get())

matches = []

print(equation_regex.match(text))

for groups in equation_regex.findall(text):
    print(groups)

equations = []
for groups in equation_regex.findall(text):
    a = [groups[2], groups[4], groups[6], groups[7]] 

    if groups[2] == '' and groups[1] != '':
        a[0] = int(1)
    elif groups[2] == '' and groups[1] == '':
        a[0] = int(0)
    
    if groups[4] == '' and groups[3] != '':
        a[1] = int(1)
    elif groups[4] == '' and groups[3] == '':
        a[1] = int(0)
    
    if groups[6] == '' and groups[5] != '':
        a[2] = int(1)
    elif groups[6] == '' and groups[5] == '':
        a[2] = int(0)
    
    equations.append(a)

for x in equations:
    for i in range(len(x)):
        if x[i] == '-':
            x[i] = int(-1)
        elif x[i] == '+':
            x[i] = int(1)
        else:
            x[i] = int(x[i])
    
    print(x)

#print(equations)

wait = input()