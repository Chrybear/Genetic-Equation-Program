# Author: Charles Ryan Barrett
# Purpose: Use a genetic algorithm to find the correct, or very close to correct, equation for the supplied values

import random

# This is the object for each tree node
class Node:
    val = None
    left_child = None
    right_child = None
    operator = False

    # Constructor
    def __init__(self, val, l_c=None, r_c=None):
        self.val = val
        self.right_child = r_c
        self.left_child = l_c
        # Check if value entered is an operator, if so this will become a root node
        if not isinstance(val, int):
            if val != 'x':  # x also counts as a numeric value
                self.operator = True

    # Getters
    def get_val(self):
        return self.val

    def get_lc(self):
        return self.left_child

    def get_rc(self):
        return self.right_child

    def is_operator(self):
        return self.operator

    # Setters
    def set_lc(self, node):
        self.left_child = node

    def set_rc(self, node):
        self.right_child = node



# Method to construct a random expression tree
def random_tree():
    # Possible node Values
    x = 'x'  # This is the variable. 'x' is just a placeholder value.
    node_value = [x, '+', '-', '*', '/', -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    # Randomly select from node_values
    val = random.choice(node_value)

    if isinstance(val, str) and val != 'x':  # Every operator needs 2 children. x counts as number
        node = Node(val, random_tree(), random_tree())
    else:
        node = Node(val)  # If not an operator, node will be leaf

    return node





def parse_tree(tree):

    if tree.get_lc():
        # exp += parse_tree(tree.get_lc()) + tree.get_val()
        parse_tree(tree.get_lc())
    print(tree.get_val())
    if tree.get_rc():
        # exp += tree.get_rc().get_val() + parse_tree(tree.get_rc())
        parse_tree(tree.get_rc())


# This method will return the value from all the expressions in the tree
def eval_exp(tree, x):
    val = 0
    if not tree.is_operator():  # Value is not an operator, therefore it is a leaf node.
        if tree.get_val() == 'x':
            return x
        else:
            return tree.get_val()
    else:
        val += eval_exp(tree.get_lc(), x)
        # Left subtrees of the node have been fully traversed after above recursive call finishes
        # Begin traversing right subtrees
        if tree.get_val() == '+':
            val += eval_exp(tree.get_rc(), x)
        elif tree.get_val() == '-':
            val -= eval_exp(tree.get_rc(), x)
        elif tree.get_val() == '*':  # The book uses 'X' for multiplication, but I don't like that.
            val *= eval_exp(tree.get_rc(), x)
        elif tree.get_val() == '/':
            val /= eval_exp(tree.get_rc(), x)  # Apparently, python doesn't have switch cases?
    return val


# Main
def main():
    # Testing Area
    print('heh')
    for x in range(0, 12):
        n = random_tree()
        parse_tree(n)
        print('That tree when x = 1 is ', eval_exp(n, 1))
        print()
    #parse_tree(n)
    # tree = Node('+',Node(3),Node(2))
    # parse_tree(tree)
    # print()
    # q = Node('*', Node(3), Node('+', Node(4), Node(7)))
    # tree.set_lc(q)
    # parse_tree(tree)
# End of Main
if __name__ == '__main__':
    main()