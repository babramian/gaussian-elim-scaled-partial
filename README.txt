CS 3010.03 Programming Project 1

Write a program that asks the user for the number of linear equations to solve (let’s say n <=10) using the the Gaussian elimination with Scaled Partial Pivoting method. Ask the user to first enter the number of equations and then give them the choice to enter the coefficients from the command line (by asking for each row that includes the b value) or have them enter a file name which has the augmented coefficient matrix (including the b values) in a simple text file format as seen below for an example of 3 equations : 

 E.g. the contents of a file for 3 linear equations 2x+3y = 8, -x+2y-z=0, 3x+2z=9 will be

2 3 0 8

-1 2 -1 0

3 0 2 9

Your program should output the scaled ratios at each step, and mention the pivot row selected based on the scaled ratio. Show the intermediate matrix at each step of the Gaussian Elimination process. Finally, the final output of your program should be the solution in the following format :

x=1

y=2

z=3

What to Submit to BB:

Upload your code, executable and report. Zip up your code and executable separately from the report (in pdf or word format). The report will have snapshots running your program for a test case for any set of linear equations you choose. Please make sure that you don't put the report in the zip file. So you will be uploading these two files, a PDF for report and the zip file that has code and executable. 

Grading: 40 points for the correct execution of the program. 5 points for report showing snapshots of an execution for any set of linear equations you choose. 5 points for being able to read matrix coefficients from a text file.

