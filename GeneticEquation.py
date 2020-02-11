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

    # Setters
    # def set_lc(self, node):
    #     self.left_child = node
    #
    # def set_rc(self, node):
    #     self.right_child = node


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


# Method to crossover between 2 trees
def cross_over(t1, t2):
    # The way cross over works for this program is the two trees will have one of their subtree chains randomly swapped between each
    # other.
    new_tree = None
    new_tree2 = None
    new_subtree1 = None
    new_subtree2 = None

    # Find splicing point for t1
    while t1.right_child or t1.left_child:
        splice_1 = t1.right_child
        if random.choice(1,2,3) == 1:
            break

    return new_tree, new_tree2

# Method to search through a tree and randomly find a point to splice
#def splice(tree, subtree):

def parse_tree(tree):

    if tree.left_child:
        # exp += parse_tree(tree.get_lc()) + tree.get_val()
        parse_tree(tree.left_child)
    print(tree.val)
    if tree.right_child:
        # exp += tree.get_rc().get_val() + parse_tree(tree.get_rc())
        parse_tree(tree.right_child)


# This method will return the value from all the expressions in the tree
def eval_exp(tree, x=1): # 1 is just a default value
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
            val /= eval_exp(tree.right_child, x)  # Apparently, python doesn't have switch cases?
    return val


# Main
def main():
    # Testing Area
    x = Node('+',Node(1),Node(2))
    y = Node('*',Node(3),Node(9))
    parse_tree(x), parse_tree(y)
    print(eval_exp(x), eval_exp(y))
    tm = x.left_child
    tw = y.right_child
    x.left_child, y.right_child = y.right_child, x.left_child
    parse_tree(x), parse_tree(y)
    print(eval_exp(x), eval_exp(y))


    # for x in range(0, 12):
    #     n = random_tree()
    #     parse_tree(n)
    #     print('That tree when x = 1 is ', eval_exp(n, 1))
    #     print()
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