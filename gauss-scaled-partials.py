import numpy
import matplotlib
import re
import os

# Main Function
# Runs all methods in here to keep main clean
def main():
    equations = get_equations() # Takes care of input, returns a numpy 2d array of coefficients & b
    print("Your coefficients:\n", equations)
    print()
    index_vector = gauss_scaled_partial_pivot(equations) # Runs equations through gaussian elimination with scaled partial pivots as demonstrated in leture videos, return index vector
    X_list = solve_post_gauss(equations, index_vector) # Takes equations and index vectors (post gaus) and solves for x


    # Prints x values line by line
    print(f'The solutions to your system of equations are:')
    for i in range(len(X_list)):
        print(f'X{i} = {numpy.round(X_list[i], decimals=2)}')
    
    wait = input()

# Parameters: 2d numpy array of equations, list of index vectors
# This function solves for Xn, and places the X's in the proper position in their list
def solve_post_gauss(equations, index_vector):

    X_values = [None for i in range(len(equations))]
    for i in range(len(equations)):
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

    # This loop goes through each row, and calculates the ratio need to multiply our pivot row
    # by to then subtract that from our other rows
    for i in range(equ_len):
            # If this row is the pivot row, skip this step of the loop
            if i == pivot_row:
                continue
            
            # Ratio between pivot row value and current row value, used to multiply entire lists at once
            if equations[pivot_row][0] == 0:
                ratio = 0
            else:
                # Getting the ratio
                ratio = equations[i][0]/equations[pivot_row][0]

            # Subtracting from the proper row
            equations[i] = numpy.subtract(equations[i], equations[pivot_row] * ratio)

    # Swaps indexes in the index vector
    swap_positions(index_vector, 0, pivot_row)
        
    # While loop repeats above steps with some additional steps (will be the ones commented on)
    column = 0
    while column <= equ_len-1:
        
        # Traverses through row indices, same for loop as above
        # Does calculations for the ratio need, and for the rows we are subtracting from
        for i in range(equ_len):
            
            if i == pivot_row:
                continue
            
            if equations[pivot_row][column] == 0:
                ratio = 0
            else:
                ratio = equations[i][column]/equations[pivot_row][column]
            
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



def get_equations():
    # Input menu
    print("Welcome to the automatic linear equations solver!")
    print("This version utiziles Gaussian Elimination with Scaled Partial Pivoting to solve linear equations!")
    print("Would you like to:")
    print("(A) Enter in your equations manually or")
    print("(B) Enter a file name (Must run this program from the same directory as your file)")
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
    if choice == 'b' or choice == 'B':

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


# Swap function 
def swap_positions(list, pos1, pos2): 
    if pos1 == pos2:
        return list

    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list


if __name__ == "__main__":
    # execute only if run as a script
    main()