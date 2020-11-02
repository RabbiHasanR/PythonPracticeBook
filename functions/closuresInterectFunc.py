# Say that I want to sort a list of numbers but prioritize one group of
# numbers to come first. This pattern is useful when you’re rendering a
# user interface and want important messages or exceptional events to
# be displayed before everything else.
# A common way to do this is to pass a helper function as the key argu-
# ment to a list’s sort method (see Item 14: “Sort by Complex Criteria
# Using the key Parameter” for details). The helper’s return value will
# be used as the value for sorting each item in the list . The helper can
# check whether the given item is in the important group and can vary
# the sorting value accordingly:

def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)


# There are three reasons this function operates as expected:
# ■ Python supports closures—that is, functions that refer to variables
# from the scope in which they were defined. This is why the helper
# function is able to access the group argument for sort_priority .
# ■ Functions are first-class objects in Python, which means you can
# refer to them directly, assign them to variables, pass them as
# arguments to other functions, compare them in expressions and
# if statements, and so on. This is how the sort method can accept
# a closure function as the key argument.
# ■ Python has specific rules for comparing sequences (including
# tuples). It first compares items at index zero; then, if those are
# equal, it compares items at index one; if they are still equal, it
# compares items at index two, and so on. This is why the return
# value from the helper closure causes the sort order to have two
# distinct groups.
# It’d be nice if this function returned whether higher-priority items
# were seen at all so the user interface code can act accordingly. Add-
# ing such behavior seems straightforward. There’s already a closure
# function for deciding which group each number is in. Why not also
# use the closure to flip a flag when high-priority items are seen? Then,
# the function can return the flag value after it’s been modified by the
# closure.
# Here, I try to do that in a seemingly obvious way:

def sort_priority2(values, group):
    found = False
    def helper(x):
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

# I can run the function on the same inputs as before:
found = sort_priority2(numbers, group)
print(f'Found : {found}')
print(numbers)

# This problem is sometimes called the scoping bug because it can be
# so surprising to newbies. But this behavior is the intended result: It
# prevents local variables in a function from polluting the containing
# module. Otherwise, every assignment within a function would put
# garbage into the global module scope. Not only would that be noise,
# but the interplay of the resulting global variables could cause obscure
# bugs.
# In Python, there is special syntax for getting data out of a closure.
# The nonlocal statement is used to indicate that scope traversal should
# happen upon assignment for a specific variable name. The only limit
# is that nonlocal won’t traverse up to the module-level scope (to avoid
# polluting globals).
# Here, I define the same function again, now using nonlocal :

def sort_priority3(values, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

found = sort_priority3(numbers, group)
print(f'Found : {found}')
print(numbers)


# The nonlocal statement makes it clear when data is being assigned
# out of a closure and into another scope. It’s complementary to the
# global statement, which indicates that a variable’s assignment should
# go directly into the module scope.
# However, much as with the anti-pattern of global variables, I’d cau-
# tion against using nonlocal for anything beyond simple functions.
# The side effects of nonlocal can be hard to follow. It’s especially hard
# to understand in long functions where the nonlocal statements and
# assignments to associated variables are far apart.
# When your usage of nonlocal starts getting complicated, it’s better to
# wrap your state in a helper class. Here, I define a class that achieves
# the same result as the nonlocal approach; it’s a little longer but much
# easier to read

class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False
    
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
print(f'Found: {sorter.found}')
print(numbers)


# Things to Remember
# ✦ Closure functions can refer to variables from any of the scopes in
# which they were defined.
# ✦ By default, closures can’t affect enclosing scopes by assigning
# variables.
# ✦ Use the nonlocal statement to indicate when a closure can modify a
# variable in its enclosing scopes.
# ✦ Avoid using nonlocal statements for anything beyond simple
# functions.