# The problem with list comprehensions (see Item 27: “Use Comprehen-
# sions Instead of map and filter ”) is that they may create new list
# instances containing one item for each value in input sequences. This
# is fine for small inputs, but for large inputs, this behavior could con-
# sume significant amounts of memory and cause a program to crash.
# For example, say that I want to read a file and return the number of
# characters on each line. Doing this with a list comprehension would
# require holding the length of every line of the file in memory. If the
# file is enormous or perhaps a never-ending network socket, using list
# comprehensions would be problematic. Here, I use a list comprehen-
# sion in a way that can only handle small input values:

value = [len(x) for x in open('my_file.txt')]
print(value)



# To solve this issue, Python provides generator expressions, which are
# a generalization of list comprehensions and generators. Generator
# expressions don’t materialize the whole output sequence when they’re
# run. Instead, generator expressions evaluate to an iterator that yields
# one item at a time from the expression.
# You create a generator expression by putting list-comprehension-like
# syntax between () characters. Here, I use a generator expression
# that is equivalent to the code above. However, the generator expres-
# sion immediately evaluates to an iterator and doesn’t make forward
# progress:

it = (len(x) for x in open('my_file.txt'))
print(it)

# The returned iterator can be advanced one step at a time to produce
# the next output from the generator expression, as needed (using
# the next built-in function). I can consume as much of the generator
# expression as I want without risking a blowup in memory usage:
print(next(it))
print(next(it))


# Another powerful outcome of generator expressions is that they can
# be composed together. Here, I take the iterator returned by the gen-
# erator expression above and use it as the input for another generator
# expression:

roots = ((x, x*0.5) for x in it)


# Each time I advance this iterator, it also advances the interior itera-
# tor, creating a domino effect of looping, evaluating conditional expres-
# sions, and passing around inputs and outputs, all while being as
# memory efficient as possible:

print(next(roots))



# Chaining generators together like this executes very quickly in
# Python. When you’re looking for a way to compose functionality that’s
# operating on a large stream of input, generator expressions are a
# great choice. The only gotcha is that the iterators returned by gener-
# ator expressions are stateful, so you must be careful not to use these
# iterators more than once


# Things to Remember
# ✦ List comprehensions can cause problems for large inputs by using
# too much memory.
# ✦ Generator expressions avoid memory issues by producing outputs
# one at a time as iterators.
# ✦ Generator expressions can be composed by passing the iterator from
# one generator expression into the for subexpression of another.
# ✦ Generator expressions execute very quickly when chained together
# and are memory efficient.