import numpy
import matplotlib
import re
import os
from tkinter import Tk
root = Tk()
root.withdraw()
number = root.clipboard_get()

def main():
    equations = get_equations()
    index_vector = gauss_scaled_partial_pivot(equations)
    X_list = solve_post_gauss(equations, index_vector)
    print(f'The solutions to your system of equations are:')
    for i in range(len(X_list)):
        print(f'X{i} = {numpy.round(X_list[i], decimals=2)}')
    
    #wait = input()


def solve_post_gauss(equations, index_vector):
    X_values = [None for i in range(len(equations))]
    for i in range(len(equations)):
        X_values[index_vector[i]] = equations[i][len(equations)]/equations[i][index_vector[i]]
        
    return numpy.array(X_values)

def gauss_scaled_partial_pivot(equations):
    equ_len = len(equations)
    index_vector = [num for num in range(equ_len)]
    scale_vector = [max(abs(list[0:len(list)-1])) for list in equations]
    ratio_vector = [abs(equations[i][0])/scale_vector[i] for i in range(equ_len)]
    pivot_row = ratio_vector.index(max(ratio_vector))

    print("Initial vectors:")
    print(f'Index Vector: {index_vector}')
    print(f'Scale Vector: {scale_vector}')
    print(f'Ratio Vector: {numpy.around(ratio_vector, decimals=2)}')
    print(f'Pivot Row: {pivot_row}\n')
    for i in range(equ_len):
            if i == pivot_row:
                continue
            
            # Ratio between pivot row value and current row value, used to multiply entire lists at once
            if equations[pivot_row][0] == 0:
                ratio = 0
            else:
                ratio = equations[i][0]/equations[pivot_row][0]
            equations[i] = numpy.subtract(equations[i], equations[pivot_row] * ratio)

    print(f'Matrix after step 1:\n{numpy.round(equations, decimals=2)}')
    print(f'Index Vector: {index_vector}')
    print(f'Ratio Vector: {numpy.around(ratio_vector, decimals=2)}')
    print(f'Pivot Row: {pivot_row}\n')

    swap_positions(index_vector, 0, pivot_row)
    

    column = 0
    while column <= equ_len-1:
        
        for i in range(equ_len):
            if i == pivot_row:
                continue
            
            # Ratio between pivot row value and current row value, used to multiply entire lists at once
            if equations[pivot_row][column] == 0:
                ratio = 0
            else:
                ratio = equations[i][column]/equations[pivot_row][column]
            
            equations[i] = numpy.subtract(equations[i], equations[pivot_row] * ratio)
        
        print(f'Matrix after step {column+1}: \n{numpy.round(equations, decimals=2)}')
        swap_positions(index_vector, column, pivot_row)
        print(f'Index Vector: {index_vector}')
        if column == equ_len-1:
            break

        scale_vector[pivot_row] = float("-inf")
        ratio_vector = [abs(equations[i][column+1])/scale_vector[i] for i in range(equ_len)]
        ratio_vector[pivot_row] = float("-inf")
        pivot_row = ratio_vector.index(max(ratio_vector))
        
        
        print(f'Scale Vector: {scale_vector}')
        print(f'Ratio Vector: {numpy.round(ratio_vector, decimals=2)}')
        print(f'Pivot Row: {pivot_row}\n')

        

        column += 1
    
    return index_vector



def get_equations():
    print("Welcome to the automatic linear equations solver!")
    print("This version utiziles Gaussian Elimination with Scaled Partial Pivoting to solve linear equations!")
    print("Would you like to:")
    print("(A) Enter in your equations manually or")
    print("(B) Enter a file name (Must run this program from the same directory as your file)")
    choice = input()

    #equations = None
    if choice == 'a' or choice == 'A':
        num_equations = int(input('How many equations will you be providing? (n<=10)\n'))
        while num_equations > 10:
            num_equations = int(input('Please enter a number between 0 and 10: '))
        
        equ_list = []
        for i in range(num_equations):
            equ_list.append([])
            print('Equation #',i+1)
            for j in range(num_equations+1):
                print(f'Coefficient #{j+1}')
                coef = input()
                equ_list[i].append(coef)
            print(f'What is your b val;ue for Equation {i+1}?')
            equ_list[i].append(input())

        
        return numpy.array(equ_list, dtype=float)


    if choice == 'b' or choice == 'B':
        file_name = input("Please enter your files name (Must be in same directory as program): ")
        equ_list = []
        with open('equations.txt', 'r') as file:
            for line in file:
                #line = line.replace(" ","")
                number_strings = line.split() # Split the line on runs of whitespace
                numbers = [int(n) for n in number_strings] # Convert to integers
                equ_list.append(numbers) # Add the "row" to your list.
        
        equ_list = [x for x in equ_list if x!=[]]
        print(equ_list)

        for i in range(len(equ_list)):
            if len(equ_list)+1 != len(equ_list[i]):
                print("Please enter a file with n*n coeficients and b values as well.")
                exit()
        return numpy.array(equ_list, dtype=float)


# Swap function 
def swap_positions(list, pos1, pos2): 
    if pos1 == pos2:
        return list

    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list


if __name__ == "__main__":
    # execute only if run as a script
    main()