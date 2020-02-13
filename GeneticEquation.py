# Author: Charles Ryan Barrett
# Purpose: Use a genetic algorithm to find the correct, or very close to correct, equation for the supplied values

import random

# This is the object for each tree node
class Node:
    val = None
    parent = None
    left_child = None
    right_child = None
    operator = False
    fit = 0

    # Constructor
    def __init__(self, val, l_c=None, r_c=None):
        self.val = val
        self.right_child = r_c
        self.left_child = l_c
        # Check if value entered is an operator, if so it will have 2 children
        if not isinstance(val, int):
            if val != 'x':  # x also counts as a numeric value
                self.operator = True


depth = 1  # This global variable keeps track of each node's depth (how many children it has)
# It is global because it makes it easier to keep track outside of each recursion.


# Method to construct a random expression tree
def random_tree():
    global depth
    # print(depth)
    # Possible node Values
    x = 'x'  # This is the variable. 'x' is just a placeholder value.
    node_value = [x, '+', '-', '*', '/', random.randint(-5, 5)]
    # Randomly select from node_values
    val = random.choice(node_value)
    if depth <= 3:
        if isinstance(val, str) and val != 'x':  # Every operator needs 2 children. x counts as a number
            depth += 1  # Increment depth
            node = Node(val, random_tree(), random_tree())
            node.left_child.parent = node
            node.right_child.parent = node
        else:
            depth += 1  # Increment depth
            node = Node(val)  # If not an operator, node will be leaf
        return node
    else:
        return Node(random.randint(-5, 5))  # If depth max is reached, end the tree.
        # Sometimes it goes crazy and maxes out python's max recursions without this safety net


def make_tree():
    global depth
    # In the book, it states that it is possible to make trees that are only a single value with no operators
    # However, this seems rather pointless, so this method ensures that each tree will be, at least, 1 expression
    node_values = ['+', '-', '*', '/']
    tree = Node(random.choice(node_values), random_tree(), random_tree())
    tree.left_child.parent = tree
    tree.right_child.parent = tree
    #print('depth =', depth)
    depth = 1  # Reset depth
    tree.fit = fitness(tree)
    return tree


# Method to crossover between 2 trees
def cross_over(mama, papa):
    # Two trees will have one of their subtree chains randomly swapped between each other.

    # Find first subtree
    sub_tree1 = get_subtree(mama)
    # Find second subtree
    sub_tree2 = get_subtree(papa)

    # Create first child
    parent = sub_tree1.parent
    if parent.left_child == sub_tree1:
        parent.left_child = sub_tree2
    else:
        parent.right_child = sub_tree2
    new_tree1 = parent

    # Traverse up tree until reaching root node
    while new_tree1.parent:
        new_tree1 = new_tree1.parent

    # Add chance for mutation
    if random.randint(1, 20) == random.randint(1, 20):
        if random.randint(1, 2) == 2:
            new_tree1.left_child = random_tree()
            new_tree1.left_child.parent = new_tree1
        else:
            new_tree1.right_child = random_tree()
            new_tree1.right_child.parent = new_tree1

    # Create second child
    parent = sub_tree2.parent
    if parent.left_child == sub_tree2:
        parent.left_child = sub_tree1
        new_tree1.left_child.parent = new_tree1
    else:
        parent.right_child = sub_tree1
        new_tree1.right_child.parent = new_tree1

    new_tree2 = parent

    # Traverse up tree until reaching root node
    while new_tree2.parent:
        new_tree2 = new_tree2.parent

    # Add chance for mutation
    if random.randint(1, 20) == random.randint(1, 20):
        if random.randint(1, 2) == 2:
            new_tree2.left_child = random_tree()
            new_tree2.left_child.parent = new_tree2
        else:
            new_tree2.right_child = random_tree()
            new_tree2.right_child.parent = new_tree2

    # Get new fitness for the trees
    new_tree1.fit = fitness(new_tree1)
    new_tree2.fit = fitness(new_tree2)

    return new_tree1, new_tree2


# This holds the randomly selected sub_tree from pick_subtree
# It is a global variable to make recursion easier
sub_tree = None


# Method to get a subtree
def get_subtree(tree):
    global sub_tree
    sub_tree = None  # Reset sub_tree
    pick_subtree(tree)
    # There is the chance that no subtree was selected and we ran out of tree to pick from
    # In that case, we randomly select one of the root node's children to be the subtree
    if not sub_tree:
        if random.randint(0, 1) == 1:
            sub_tree = tree.left_child
        else:
            sub_tree = tree.right_child

    return sub_tree


# Method to randomly select a subtree
def pick_subtree(tree):
    global sub_tree

    if not sub_tree:  # If the subtree was already found, stop trying to find it
        if tree.parent:
            if random.randint(1, 3) == 1:
                sub_tree = tree
            elif tree.right_child and tree.left_child:  # Make sure it is not a leaf
                pick_subtree(tree.left_child)
                pick_subtree(tree.right_child)
        else:  # If the node is the root node, we don't want it to be a potential slicing point; only it's children
            pick_subtree(tree.left_child)
            if not sub_tree:
                pick_subtree(tree.right_child)


# This will hold the entire tree structure to make it easier to see when printed out
full_tree = []


# This will print out the tree in in-order traversal
def print_tree(tree):
    global full_tree
    full_tree = []
    parse_tree(tree)
    print(full_tree)


def parse_tree(tree):
    global full_tree
    if tree.operator:
        parse_tree(tree.left_child)
        full_tree.append(tree.val)
        parse_tree(tree.right_child)
    else:
        full_tree.append(tree.val)


# This method calculates the value of the expression tree
def eval_exp(tree, x=1):  # 1 is just a default value
    val = 0
    if not tree.operator:  # Value is not an operator, therefore it is a leaf node.
        if tree.val == 'x':
            return x
        else:
            return tree.val
    else:
        val += eval_exp(tree.left_child, x)
        # Left subtrees of the node have been fully traversed after above recursive call finishes
        # Begin traversing right subtrees
        if tree.val == '+':
            val += eval_exp(tree.right_child, x)
        elif tree.val == '-':
            val -= eval_exp(tree.right_child, x)
        elif tree.val == '*':  # The book uses 'X' for multiplication, but I don't like that.
            val *= eval_exp(tree.right_child, x)
        elif tree.val == '/':
            tmp = eval_exp(tree.right_child, x)
            if tmp == 0:
                val = 0
            else:
                val /= tmp
            # If we divide by zero, we will just say that is equal to 0.
    return val


# Method to evaluate fitness of an expression
def fitness(tree):
    fit = 0
    x = 0.0
    y = [0, .005, .020, .045, .080, .125, .180, .245, .320, .405]
    # print('Tree being evaluated: ')
    # print_tree(tree)
    for i in y:
        x = round(x, 1)
        fit += pow((eval_exp(tree, x) - i), 2)
        # print('fit =',fit,' when x = ',x)
        x += 0.1
    return fit


# Method to make a population of expressions
def populate(size):
    popu = []
    while size > 0:
        popu.append(make_tree())
        size -= 1
    return popu


# Method to go through generations of expressions and return the best match
def get_exp(popu, gens):
    og = gens

    # This will hold our fittest expression
    champ = popu[0]

    while gens > 0:
        # Make new generation
        popu = generation(popu)

        # Sort new population based on best (smallest) fitness
        popu = sortPopulation(popu, 0, len(popu) - 1)

        # Check to see if we have found a better expression
        if abs(champ.fit) > abs(popu[0].fit):
            champ = popu[0]
            # Add a few extra generations
            # gens += og//2  # Half of our original generation number
        gens -= 1

    # Once out of loop, we have found our best expression (hopefully)
    best_fit(champ)


# Method to handle a single generation
def generation(popu):
    # Sort our current populations based on best (smallest) fitness
    popu = sortPopulation(popu, 0, len(popu) - 1)

    # Let the top half of the population reproduce for new expressions
    chosen = len(popu)//2
    if chosen % 2 != 0:  # Each crossover needs two parents, so make sure we have an even number
        chosen += 1
    for x in range(0, chosen-2):
        popu[x], popu[x+1] = cross_over(popu[x], popu[x+1])

    # The remaining population that was not chosen will be replaced with new expressions
    for x in range(chosen-1, len(popu)):
        popu[x] = make_tree()

    # Return the new generation of expressions
    return popu


# Method to show best fit expression
def best_fit(champ):
    print('In Order Traversal: ')
    print_tree(champ)
    print()
    x = 0.0
    while x < 1.0:
        x = round(x, 1)
        print('When x = ', x, ' above expression = ', eval_exp(champ, x))
        x += 0.1

# methods to sort population from best (lowest) to worst (largest) fitness
def sortPopulation(popu, low, high):
    if low < high:
        piv = partition(popu, low, high)
        sortPopulation(popu, low, piv-1)
        sortPopulation(popu, piv+1, high)
    return popu
def partition(popu, low, high):
    x = low-1
    piv = popu[high].fit
    for i in range(low, high, 1):
        if popu[i].fit < piv:
            x = x+1
            popu[x], popu[i] = popu[i], popu[x]
    popu[x+1], popu[high] = popu[high], popu[x+1]
    return x+1


# Main
def main():
    p = populate(50)
    get_exp(p, 5)


# End of Main
if __name__ == '__main__':
    main()




# I tried so many ways to bypass the recursion max. Even when I completely reworked a recursive method, (below)
# It still would go into max recursion depth.
# This method will return the value from all the expressions in the tree
# def eval_exp(tree, x=1):
#     global full_tree
#     parse_tree(tree)
#     t = full_tree
#     full_tree = []  # Reset full tree
#     total_value = 0
#     eq =[]
#     for i in range(0, len(t)):
#         eq.append(t[i])
#         if len(eq) == 3:
#             total_value += decide_op(eq[0], eq[1], eq[2], x)
#             eq = [total_value]
#     return total_value
#
#
# def decide_op(n, op, n2, x):
#     if n == 'x':
#         n = x
#     if n2 == 'x':
#         n2 = x
#
#     if op == '+':
#         return n + n2
#     elif op == '-':
#         return n - n2
#     elif op == '*':  # The book uses 'X' for multiplication, but I don't like that.
#         return n * n2
#     elif op == '/':
#         if n2 == 0:
#             return 0
#         else:
#             return n//n2
#     # Need to make a special case for division of 0 or else we enter the uh oh zone.
#     # If we divide by zero, we will just say that is equal to 0.
