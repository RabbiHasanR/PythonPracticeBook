# The simplest choice for a function that produces a sequence of results
# is to return a list of items. For example, say that I want to find the
# index of every word in a string. Here, I accumulate results in a list
# using the append method and return it at the end of the function:

def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

# This works as expected for some sample input:

address = 'Four score and seven years ago...'
result = index_words(address)
print(result[:10])


# There are two problems with the index_words function.

# There are two problems with the index_words function.
# The first problem is that the code is a bit dense and noisy. Each time
# a new result is found, I call the append method. The method call’s
# bulk ( result.append ) deemphasizes the value being added to the list
# ( index + 1 ). There is one line for creating the result list and another
# for returning it. While the function body contains ~130 characters
# (without whitespace), only ~75 characters are important.


# A better way to write this function is by using a generator. Generators
# are produced by functions that use yield expressions. Here, I define a
# generator function that produces the same results as before:

def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

# When called, a generator function does not actually run but instead
# immediately returns an iterator. With each call to the next built-in
# function, the iterator advances the generator to its next yield expres-
# sion. Each value passed to yield by the generator is returned by the
# iterator to the caller:

itr = index_words_iter(address)
print(next(itr))
print(next(itr))


# The index_words_iter function is significantly easier to read because
# all interactions with the result list have been eliminated. Results are
# passed to yield expressions instead. You can easily convert the itera-
# tor returned by the generator to a list by passing it to the list built-in
# function if necessary

result = list(index_words_iter(address))
print(result)


# The second problem with index_words is that it requires all results to
# be stored in the list before being returned. For huge inputs, this can
# cause a program to run out of memory and crash.
# In contrast, a generator version of this function can easily be adapted
# to take inputs of arbitrary length due to its bounded memory require-
# ments. For example, here I define a generator that streams input from
# a file one line at a time and yields outputs one word at a time:


def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

# The working memory for this function is limited to the maximum
# length of one line of input. Running the generator produces the same
# results
import itertools
with open('address.txt', 'r') as f:
    it = index_file(f)
    results = itertools.islice(it, 0, 10)
    print(list(results))


# The only gotcha with defining generators like this is that the callers
# must be aware that the iterators returned are stateful and can’t be
# reused



# Things to Remember
# ✦ Using generators can be clearer than the alternative of having a
# function return a list of accumulated results.
# ✦ The iterator returned by a generator produces the set of values
# passed to yield expressions within the generator function’s body.
# ✦ Generators can produce a sequence of outputs for arbitrarily large
# inputs because their working memory doesn’t include all inputs and
# outputs.