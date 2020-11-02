# Python provides compact syntax for deriving a new list from another
# sequence or iterable. These expressions are called list comprehensions.
# For example, say that I want to compute the square of each number
# in a list . Here, I do this by using a simple for loop:

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)

print(squares)


# With a list comprehension, I can achieve the same outcome by specify-
# ing the expression for my computation along with the input sequence
# to loop over:

squares = [x**2 for x in a]     # list comprehension
print(squares)


# Unless you’re applying a single-argument function, list comprehen-
# sions are also clearer than the map built-in function for simple cases.
# map requires the creation of a lambda function for the computation,
# which is visually noisy:
alt = map(lambda x: x ** 2, a)
print(list(alt))


# Unlike map , list comprehensions let you easily filter items from the
# input list , removing corresponding outputs from the result. For
# example, say I want to compute the squares of the numbers that are
# divisible by 2. Here, I do this by adding a conditional expression to
# the list comprehension after the loop:

even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)

# The filter built-in function can be used along with map to achieve the
# same outcome, but it is much harder to read:

alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)


# Dictionaries and sets have their own equivalents of list comprehen-
# sions (called dictionary comprehensions and set comprehensions,
# respectively). These make it easy to create other types of derivative
# data structures when writing algorithms:

even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cube_set = {x**3 for x in a if x % 3 == 0}
print(even_squares_dict)
print(threes_cube_set)


# Achieving the same outcome is possible with map and filter if you
# wrap each call with a corresponding constructor. These statements
# get so long that you have to break them up across multiple lines,
# which is even noisier and should be avoided:

alt_dict = dict(map(lambda x: (x, x ** 2),
                filter(lambda x: x % 2 == 0,a)))
alt_set = set(map(lambda x: x ** 3,
            filter(lambda x: x % 3 == 0, a)))

print(alt_dict)
print(alt_set)



# Things to Remember
# ✦ List comprehensions are clearer than the map and filter built-in
# functions because they don’t require lambda expressions.
# ✦ List comprehensions allow you to easily skip items from the input
# list , a behavior that map doesn’t support without help from filter .
# ✦ Dictionaries and sets may also be created using comprehensions.