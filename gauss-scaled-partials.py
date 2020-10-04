import numpy
import re
import os
from math import sqrt

# Main Function
# Runs all methods in here to keep main clean
def main():
    equations = get_equations() # Takes care of input, returns a numpy 2d array of coefficients & b

    A, b = split_matrix(equations)
    print(f'A:\n{A}')
    print(f'b:\n{b}\n')
    jacobi_sol = jacobi_iterative(A, b, len(A))
    #index_vector = gauss_scaled_partial_pivot(equations) # Runs equations through gaussian elimination with scaled partial pivots as demonstrated in leture videos, return index vector
    #X_list = solve_post_gauss(equations, index_vector) # Takes equations and index vectors (post gaus) and solves for x


    # Prints x values line by line
    #print_array(X_list)
    
    wait = input()


def jacobi_iterative(A, b, n, x=None):

    if not isDMM(A, n):
        print(f'Please restart and enter a matrix that is diagonally dominant.')
        return

    print(f'Please enter your desired stopping error: ')
    stop_error = float(input())
    print()
    print(f'Please enter your starting solution: ')
    print()
    x = []
    for i in range(0, n):
        x.append(int(input()))

    # Vector of the diagonals in A (I know it's just A[n][n], numpy just makes it cleaner)
    D = numpy.diag(A)
    #print(f'D:\n{D}')
    #print(f'Flat D:\n{numpy.diagflat(D)}')
    R = numpy.subtract(A, numpy.diagflat(D)) # Subtract them from A
    #print(f'R:\n{R}')

    
    for i in range(50):
        x_prev = x
        #print(f'X:\n{x}')
        x = (b - numpy.dot(R,x))/D
        if i == 1:
            print(f'{i+1}st Approximation:\n{x}T')
        elif i == 2:
            print(f'{i+1}nd Approximation:\n{x}T')
        elif i == 3:
            print(f'{i+1}rd Approximation:\n{x}T')
        else:
            print(f'{i+1}th Approximation:\n{x}T')

        error = calculate_L2(numpy.subtract(x, x_prev))/calculate_L2(x)
        #print(f'Current Error:\n{error}')
        if error < stop_error:
            break

        if i == 49:
            print("The error was not reached.\n")

    print(f'Solution by Jacobi Method:\n')
    print_array(x)
    print(f'With a final error of {error}')
    return x


def calculate_L2(arr):
    L2 = float(0)
    for num in arr:
        L2 += num*num
    return sqrt(abs(L2))


def isDMM(m, n) : 
  
    # for each row 
    for i in range(0, n) :          
      
        # for each column, finding 
        # sum of each row. 
        sum = 0
        for j in range(0, n) : 
            sum = sum + abs(m[i][j])      
  
        # removing the  
        # diagonal element. 
        sum = sum - abs(m[i][i]) 
  
        # checking if diagonal element is less than sum of non-diagonal 
        # element. 
        if (abs(m[i][i]) < sum) : 
            return False
  
    return True



def get_equations():
    # Input menu
    print("Welcome to the automatic linear equations solver!")
    print("This version utiziles Gaussian Elimination with Scaled Partial Pivoting to solve linear equations!")
    print("Would you like to:")
    print("(A) Enter in your equations manually or")
    print("(B) Enter a file name (Must run this program from the same directory as your file)")
    choice = input()

    while choice != 'A' and choice != 'a' and choice != 'b'and choice != 'B':
        print(f'Please enter a valid option:')
        choice = input()

    # A means manul input, B means file input
    # Goes through and asks user for number of equations (n) and creates n x n+1 matrix based
    # on what numbers user continues to input
    if choice == 'a' or choice == 'A':
        num_equations = int(input('How many equations will you be providing? (n<=10)\n'))
        while num_equations > 10 or num_equations < 0: # Check to make sure correct amount is entered
            num_equations = int(input('Please enter a number between 0 and 10: '))
        
        equ_list = []
        for i in range(num_equations):
            equ_list.append([]) # append an empty list first

            print('Equation #',i+1)
            print()
            for j in range(num_equations): # Gets input for current equation
                print(f'Coefficient #{j+1}')
                coef = input()
                equ_list[i].append(coef)

            print(f'What is your b value for Equation {i+1}?') # b value
            equ_list[i].append(input())
            print()

        # Returns al numpy array with dtype float
        return numpy.array(equ_list, dtype=float)


    # File input
    elif choice == 'b' or choice == 'B':

        # asks for file name
        file_name = input("Please enter your files name (Must be in same directory as program): ")
        equ_list = []
        with open('equations.txt', 'r') as file:
            for line in file:
                number_strings = line.split() # Split the line on runs of whitespace
                numbers = [int(n) for n in number_strings] # Convert to integers
                equ_list.append(numbers) # Add the "row" to your list.
        
        # Removes empty lists (caused by empty lines)
        equ_list = [x for x in equ_list if x!=[]]
        
        # Checks to make sure the length of each equation is long enough 
        for i in range(len(equ_list)):
            if len(equ_list)+1 != len(equ_list[i]):
                print("Please enter a file with n*n coeficients and b values as well.")
                exit()

        return numpy.array(equ_list, dtype=float)


# Prints a 1d array
def print_array(arr):
    print(f'\nThe solutions to your system of equations are:')
    for i in range(len(arr)):
        print(f'X{i} = {numpy.round(arr[i], decimals=2)}')


# Swap function 
def swap_positions(list, pos1, pos2): 
    if pos1 == pos2:
        return list

    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list






# Parameters: 2d numpy array of equations, list of index vectors
# This function solves for Xn, and places the X's in the proper position in their list
def solve_post_gauss(equations, index_vector):

    X_values = [None for i in range(len(equations))]
    for i in range(len(X_values)):
        # index_vector holds which 'row' the current iteration of x should calculate
        # This ensures our X values are accurate and not just placed randomly
        # Solves for x on each row
        X_values[i] = equations[index_vector[i]][len(equations)]/equations[index_vector[i]][i]
        
    return numpy.array(X_values)



def gauss_scaled_partial_pivot(equations):

    # We calculate our vectors and pivot row once before entering a while loop
    equ_len = len(equations)
    index_vector = [num for num in range(equ_len)]
    scale_vector = [max(abs(list[0:len(list)-1])) for list in equations]
    ratio_vector = [abs(equations[i][0])/scale_vector[i] for i in range(equ_len)]
    pivot_row = ratio_vector.index(max(ratio_vector))

    # Printing the initial vectors and pivot row
    print("Beginning vectors & pivot row:")
    print(f'Index Vector: {index_vector}')
    print(f'Scale Vector: {scale_vector}')
    print(f'Ratio Vector: {numpy.around(ratio_vector, decimals=2)}')
    print(f'Pivot Row: {pivot_row}\n')

        
    # While loop repeats above steps with some additional steps (will be the ones commented on)
    column = 0
    while column <= equ_len-1:
        
        # This loop goes through each row, and calculates the ratio need to multiply our pivot row
        # by to then subtract that from our other rows
        for i in range(equ_len):
            
            if i == pivot_row:
                continue
            
            if equations[pivot_row][column] == 0:
                # This fixes the issue that arises from dividing by zero
                ratio = 0
            else:
                # Getting the ratio
                ratio = equations[i][column]/equations[pivot_row][column]
            
            # Subtracting from the proper row
            equations[i] = numpy.subtract(equations[i], equations[pivot_row] * ratio)
        
        # Prints intermediate matrix, labels it's steps as well
        print(f'Matrix after step {column+1}: \n{numpy.round(equations, decimals=2)}')

        # Swapping the pivot row in the index vector
        swap_positions(index_vector, column, index_vector.index(pivot_row))

        # Breaks out of loop if we've hit the final column (no need to run anything past this)
        if column == equ_len-1:
            break
        
        # Setting used rows as -inf for scale vector and ratios vector
        # Also recalculating retio vector with new equations, and setting new pivot row
        scale_vector[pivot_row] = float("-inf")
        ratio_vector = [abs(equations[i][column+1])/scale_vector[i] for i in range(equ_len)]
        ratio_vector[pivot_row] = float("-inf")
        pivot_row = ratio_vector.index(max(ratio_vector))
        
        # Printing out ratios and pivot row
        print(f'Scaled Ratios: {numpy.round(ratio_vector, decimals=2)}')
        print(f'Pivot Row: {pivot_row}\n')


        column += 1
    
    # Returning index vector to be used in finding the x values
    return index_vector


def split_matrix(m):
    A = []
    b = []
    for i in range(len(m)):
        row = []
        for j in range(len(m)+1):
            if j == len(m):
                b.append(m[i][j])
            else:
                row.append(m[i][j])
        A.append(row)
    
    return numpy.array(A), numpy.array(b)


if __name__ == "__main__":
    # execute only if run as a script
    main()