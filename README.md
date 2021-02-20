# Genetic-Equation-Program
CSC 320 assignment 2, work in progresss

This program is meant to use genetic programming to find the equation, or closest match equation, for a set of values.

The default values are: [0, .005, .020, .045, .080, .125, .180, .245, .320, .405] @ line 221 in the code.

When ran, the program will create 50 different equation trees and run through 5 generations to try and find the best or exact equation to match the above values.

*Error* There seems to be a common error in which max recursion depth is reached. This is why the default generations is set to 5, as increasing it and/or the number of equation trees increases the liklihood of envoking a max recursion error.
