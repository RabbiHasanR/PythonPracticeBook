# The list built-in type provides a sort method for ordering the items
# in a list instance based on a variety of criteria. By default, sort will
# order a list ’s contents by the natural ascending order of the items.
# For example, here I sort a list of integers from smallest to largest:
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)

# The sort method works for nearly all built-in types (strings, floats,
# etc.) that have a natural ordering to them. What does sort do with
# objects? For example, here I define a class—including a __repr__
# method so instances are printable; “Use repr Strings for
# Debugging Output”—to represent various tools you may need to use
# on a construction site:

class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __repr__(self):
        return f'Tool{self.name!r}, {self.weight}'


tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]

# Sorting objects of this type doesn’t work because the sort method
# tries to call comparison special methods that aren’t defined by the
# class:
#tools.sort()    # TypeError: '<' not supported between instances of 'Tool' and 'Tool'


# Here, I use the lambda keyword to define a function for the key param-
# eter that enables me to sort the list of Tool objects alphabetically by
# their name :
#print(tools)
print('Unsorted: ', repr(tools))
tools.sort(key=lambda x : x.name)
print('Sorted: ', tools)


# I can just as easily define another lambda function to sort by weight
# and pass it as the key parameter to the sort method:
tools.sort(key=lambda x : x.weight)
print('Sorted by weight: ', tools)

# For basic types like strings, you may even want to use the key func-
# tion to do transformations on the values before sorting. For example,
# here I apply the lower method to each item in a list of place names to
# ensure that they’re in alphabetical order, ignoring any capitalization
# (since in the natural lexical ordering of strings, capital letters come
# before lowercase letters):
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('Case sensitive: ', places)
places.sort(key=lambda x : x.lower())
print('Case insensitive: ', places)


# Sometimes you may need to use multiple criteria for sorting. For
# example, say that I have a list of power tools and I want to sort them
# first by weight and then by name . How can I accomplish this?
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]

# The simplest solution in Python is to use the tuple type. Tuples are
# immutable sequences of arbitrary Python values. Tuples are compara-
# ble by default and have a natural ordering, meaning that they imple-
# ment all of the special methods, such as __lt__ , that are required by
# the sort method. Tuples implement these special method comparators
# by iterating over each position in the tuple and comparing the cor-
# responding values one index at a time. Here, I show how this works
# when one tool is heavier than another:

saw = (5, 'circular saw')
jackhammer = (40, 'jackhammer')
print(jackhammer < saw)
assert not jackhammer < saw 

# If the first position in the tuples being compared are equal— weight
# in this case—then the tuple comparison will move on to the second
# position, and so on:
drill = (4, 'drill')
sander = (4, 'sander')
print(drill[0] == sander[0])
print(drill[1] < sander[1])
print(drill < sander)
assert drill[0] == sander[0]    # Same weight
assert drill[1] < sander[1]     # Alphabetically less
assert drill < sander           # Thus, drill comes first


# You can take advantage of this tuple comparison behavior in order
# to sort the list of power tools first by weight and then by name . Here,
# I define a key function that returns a tuple containing the two attri-
# butes that I want to sort on in order of priority:
power_tools.sort(key=lambda x : (x.weight, x.name))
print(power_tools)


# One limitation of having the key function return a tuple is that the
# direction of sorting for all criteria must be the same (either all in
# ascending order, or all in descending order). If I provide the reverse
# parameter to the sort method, it will affect both criteria in the tuple
# the same way (note how 'sander' now comes before 'drill' instead of
# after):
power_tools.sort(key=lambda x : (x.weight, x.name), reverse=True)
print(power_tools)


# For numerical values it’s possible to mix sorting directions by using
# the unary minus operator in the key function. This negates one of
# the values in the returned tuple , effectively reversing its sort order
# while leaving the others intact. Here, I use this approach to sort by
# weight descending, and then by name ascending (note how 'sander'
# now comes after 'drill' instead of before):

power_tools.sort(key=lambda x  : (-x.weight, x.name))
print(power_tools)


# Unfortunately, unary negation isn’t possible for all types. Here, I try
# to achieve the same outcome by using the reverse argument to sort
# by weight descending and then negating name to put it in ascending
# order:
# power_tools.sort(key=lambda x : (x.weight, -x.name))    # TypeError: bad operand type for unary -: 'str'
# print(power_tools)


# For situations like this, Python provides a stable sorting algorithm.
# The sort method of the list type will preserve the order of the input
# list when the key function returns values that are equal to each
# other. This means that I can call sort multiple times on the same
# list to combine different criteria together. Here, I produce the same
# sort ordering of weight descending and name ascending as I did above
# but by using two separate calls to sort :

power_tools.sort(key=lambda x : x.name)     # Name ascending
print(power_tools)
power_tools.sort(key=lambda x: x.weight, reverse=True)    # Weight descending
print(power_tools)

