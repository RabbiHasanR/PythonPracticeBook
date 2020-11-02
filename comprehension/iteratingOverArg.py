# When a function takes a list of objects as a parameter, it’s often
# important to iterate over that list multiple times. For example, say
# that I want to analyze tourism numbers for the U.S. state of Texas.
# Imagine that the data set is the number of visitors to each city (in mil-
# lions per year). I’d like to figure out what percentage of overall tourism
# each city receives.
# To do this, I need a normalization function that sums the inputs to
# determine the total number of tourists per year and then divides each
# city’s individual visitor count by the total to find that city’s contribu-
# tion to the whole:

def normalize(numbers):
    total = sum(numbers)
    results = []
    for value in numbers:
        percent = 100 * value / total
        results.append(percent)
    return results

# This function works as expected when given a list of visits:
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0



# To scale this up, I need to read the data from a file that contains every
# city in all of Texas. I define a generator to do this because then I can
# reuse the same function later, when I want to compute tourism num-
# bers for the whole world—a much larger data set with higher memory
# requirements


def read_visits(data_path):
    with open(data_path, 'r') as f:
        for line in f:
            yield int(line)

# Surprisingly, calling normalize on the read_visits generator’s return
# value produces no results:

it = read_visits('my_numbers.txt')
# print(list(it))
percentages = normalize(it)
print(percentages)


# This behavior occurs because an iterator produces its results only
# a single time. If you iterate over an iterator or a generator that has
# already raised a StopIteration exception, you won’t get any results
# the second time around:
it = read_visits('my_numbers.txt')
print(list(it))
print(list(it))     # already exhusted


# Confusingly, you also won’t get errors when you iterate over an
# already exhausted iterator. for loops, the list constructor, and many
# other functions throughout the Python standard library expect the
# StopIteration exception to be raised during normal operation. These
# functions can’t tell the difference between an iterator that has no out-
# put and an iterator that had output and is now exhausted.
# To solve this problem, you can explicitly exhaust an input iterator and
# keep a copy of its entire contents in a list . You can then iterate over
# the list version of the data as many times as you need to. Here’s the
# same function as before, but it defensively copies the input iterator:

def normalize_copy(numbers):
    numbers = list(numbers)
    total = sum(numbers)
    results = []
    for value in numbers:
        percentages = 100 * value / total
        results.append(percentages)
    return results

# Now the function works correctly on the read_visits generator’s
# return value:
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0


# The problem with this approach is that the copy of the input iterator’s
# contents could be extremely large. Copying the iterator could cause
# the program to run out of memory and crash. This potential for scal-
# ability issues undermines the reason that I wrote read_visits as a
# generator in the first place. One way around this is to accept a func-
# tion that returns a new iterator each time it’s called:

def normalize_func(get_iter):
    total = sum(get_iter())     # new iterator
    results = []
    for value in get_iter():    # new iterator
        percentage = 100 * value / total
        results.append(percentage)
    return results


# To use normalize_func , I can pass in a lambda expression that calls
# the generator and produces a new iterator each time:

path = 'my_numbers.txt'
percentages = normalize_func(lambda : read_visits(path))
print(percentages)
assert sum(percentages) == 100.0
    

# Although this works, having to pass a lambda function like this is
# clumsy. A better way to achieve the same result is to provide a new
# container class that implements the iterator protocol.


# The iterator protocol is how Python for loops and related expressions
# traverse the contents of a container type. When Python sees a state-
# ment like for x in foo , it actually calls iter(foo) . The iter built-in
# function calls the foo.__iter__ special method in turn. The __iter__
# method must return an iterator object (which itself implements the
# __next__ special method). Then, the for loop repeatedly calls the
# next built-in function on the iterator object until it’s exhausted (indi-
# cated by raising a StopIteration exception).
# It sounds complicated, but practically speaking, you can achieve all of
# this behavior for your classes by implementing the __iter__ method
# as a generator. Here, I define an iterable container class that reads
# the file containing tourism data:

class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path, 'r') as f:
            for line in f:
                yield int(line)

# This new container type works correctly when passed to the original
# function without modifications:

path = 'my_numbers.txt'
readVisits = ReadVisits(path)
percentages = normalize(readVisits)
print(percentages)
assert sum(percentages) == 100.0



# This
# works because the sum method in normalize calls
# ReadVisits.__iter__ to allocate a new iterator object. The for loop to
# normalize the numbers also calls __iter__ to allocate a second iter-
# ator object. Each of those iterators will be advanced and exhausted
# independently, ensuring that each unique iteration sees all of the
# input data values. The only downside of this approach is that it reads
# the input data multiple times.


# Now that you know how containers like ReadVisits work, you can
# write your functions and methods to ensure that parameters aren’t
# just iterators. The protocol states that when an iterator is passed
# to the iter built-in function, iter returns the iterator itself. In con-
# trast, when a container type is passed to iter , a new iterator object is
# returned each time. Thus, you can test an input value for this behav-
# ior and raise a TypeError to reject arguments that can’t be repeatedly
# iterated over

def normalize_defensive(numbers):
    if iter(numbers) is numbers:    # An iterator -- bad
        raise TypeError('Must supply a container')
    total = sum(numbers)
    results = []
    for value in numbers:
        percentage = 100 * value / total
        results.append(percentage)
    return results

# Alternatively, the collections.abc built-in module defines an Iterator
# class that can be used in an isinstance test to recognize the potential
# problem

from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):
        raise TypeError('Must supply a container')
    total = sum(numbers)
    results = []
    for value in numbers:
        percentage = 100 * value / total
        results.append(percentage)
    return results


# The approach of using a container is ideal if you don’t want to copy
# the full input iterator, as with the normalize_copy function above, but
# you also need to iterate over the input data multiple times. This func-
# tion works as expected for list and ReadVisits inputs because they
# are iterable containers that follow the iterator protocol:

visits = [15, 35, 80]
percentages = normalize_defensive(visits)
print(percentages)
assert sum(percentages) == 100.0

visits = ReadVisits(path)
percentages = normalize_defensive(visits)
print(percentages)
assert sum(percentages) == 100.0



# The function raises an exception if the input is an iterator rather than
# a container:
visits = [15, 35, 80]
it = iter(visits)
# percentages = normalize_defensive(it)   # TypeError: Must supply a container


# The same approach can also be used for asynchronous iterators


# Things to Remember
# ✦ Beware of functions and methods that iterate over input argu-
# ments multiple times. If these arguments are iterators, you may see
# strange behavior and missing values.
# ✦ Python’s iterator protocol defines how containers and iterators inter-
# act with the iter and next built-in functions, for loops, and related
# expressions.
# ✦ You can easily define your own iterable container type by imple-
# menting the __iter__ method as a generator.
# ✦ You can detect that a value is an iterator (instead of a container)
# if calling iter on it produces the same value as what you passed
# in. Alternatively, you can use the isinstance built-in function along
# with the collections.abc.Iterator class.