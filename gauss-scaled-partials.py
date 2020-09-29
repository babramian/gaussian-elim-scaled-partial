import numpy
import matplotlib
import re
import os
from tkinter import Tk
root = Tk()
root.withdraw()
number = root.clipboard_get()

def main():

    print("Welcome to the automatic linear equations solver!")
    print("This version utiziles Gaussian Elimination with Scaled Partial Pivoting to solve linear equations!")
    print("Would you like to:")
    print("(A) Enter in your equations manually or")
    print("(B) Enter a file name (Must run this program from the same directory as your file)")
    choice = input()


    equations = None
    if choice == 'a' or choice == 'A':
        num_equations = int(input('How many equations will you be providing? (n<=10)\n'))
        while num_equations > 10:
            num_equations = int(input('Please enter a number between 0 and 10: '))
        
        equ_list_plain_txt = ''
        for i in range(num_equations):
            print('Equation #',i+1)
            equ_list_plain_txt += input()
            equ_list_plain_txt += '\t'
        
        equations = numpy.array(get_equations(equ_list_plain_txt))


    if choice == 'b' or choice == 'B':
        with open('equations.txt', 'r') as file:
            equations = numpy.array(get_equations(file.read()))

    print(equations)
    wait = input()


def get_equations(text):

    text = text.replace(" ", "")
    print(text)
    
    # Regex finds all coefficiants and properly sorts them
    equation_regex = re.compile(r'''(
        ((-?\d*)[x])?           # x and its coef (a)
        \s*[+]?\s*              # space and/or plus
        (([-]?\s*\d*)[y])?         # y and its coef (b)
        \s*[+]?\s*              # space and/or plus
        (([-]?\s*\d*)[z])?         # z and its coef (c)
        \s*[=]\s*               # equal sign
        (-?\d+)                 # value of d
        )''', re.VERBOSE)

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

    #print(equations)

    for x in equations:
        for i in range(len(x)):
            if x[i] == '-':
                x[i] = int(-1)
            elif x[i] == '+':
                x[i] = int(1)
            else:
                x[i] = int(x[i])
        
    return equations


if __name__ == "__main__":
    # execute only if run as a script
    main()