# Accepting a variable number of positional arguments can make a
# function call clearer and reduce visual noise. (These positional argu-
# ments are often called varargs for short, or star args, in reference to
# the conventional name for the parameter *args. ) For example, say
# that I want to log some debugging information. With a fixed number
# of arguments, I would need a function that takes a message and a
# list of values:

def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('My number are', [1, 2])
log('Hi there',[])
#log('Hello')    #TypeError: log() missing 1 required positional argument: 'values'

# Having to pass an empty list when I have no values to log is cum-
# bersome and noisy. It’d be better to leave out the second argument
# entirely. I can do this in Python by prefixing the last positional
# parameter name with * . The first parameter for the log message is
# required, whereas any number of subsequent positional arguments
# are optional. The function body doesn’t need to change; only the call-
# ers do:

def log2(message, *values):     # the only difference
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log2('My message is', 3, 4)
log2('Hi there')    # much better


# You might notice that this syntax works very similarly to the starred
# expressions used in unpacking assignment statements (see Item 13:
# “Prefer Catch-All Unpacking Over Slicing”).
# If I already have a sequence (like a list ) and want to call a variadic
# function like log , I can do this by using the * operator. This instructs
# Python to pass items from the sequence as positional arguments to
# the function:

favorits = [7, 33, 99]
log2('Hi Rabbi', *favorits)


# There are two problems with accepting a variable number of posi-
# tional arguments.
# The first issue is that these optional positional arguments are always
# turned into a tuple before they are passed to a function. This means
# that if the caller of a function uses the * operator on a generator, it
# will be iterated until it’s exhausted (see Item 30: “Consider Genera-
# tors Instead of Returning Lists” for background). The resulting tuple
# includes every value from the generator, which could consume a lot of
# memory and cause the program to crash:

def my_generator():
    for x in range(10):
        yield x

def my_func(*args):
    print(args)

it = my_generator()
print(it)
my_func(*it)


# Functions that accept *args are best for situations where you know
# the number of inputs in the argument list will be reasonably small.
# *args is ideal for function calls that pass many literals or variable
# names together. It’s primarily for the convenience of the programmer
# and the readability of the code.
# The second issue with *args is that you can’t add new positional
# arguments to a function in the future without migrating every caller.
# If you try to add a positional argument in the front of the argument
# list, existing callers will subtly break if they aren’t updated:

def log3(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ','.join(str(x) for x in values)
        print(f'{sequence} - {message}: ', values_str)

log3(1, 'Favorites', 7, 33)     # new with *args ok
log3(2, 'Hi there')             # new message only ok
log3('Favorite numbers', 7, 33) # old usages breaks


# The problem here is that the third call to log used 7 as the message
# parameter because a sequence argument wasn’t given. Bugs like
# this are hard to track down because the code still runs without
# raising exceptions. To avoid this possibility entirely, you should use
# keyword-only arguments when you want to extend functions that90
# Chapter 3
# Functions
# accept *args (see Item 25: “Enforce Clarity with Keyword-Only and
# Positional-Only Arguments”). To be even more defensive, you could
# also consider using type annotations (see Item 90: “Consider Static
# Analysis via typing to Obviate Bugs”).

# Things to Remember
# ✦ Functions can accept a variable number of positional arguments by
# using *args in the def statement.
# ✦ You can use the items from a sequence as the positional arguments
# for a function with the * operator.
# ✦ Using the * operator with a generator may cause a program to run
# out of memory and crash.
# ✦ Adding new positional parameters to functions that accept *args
# can introduce hard-to-detect bugs.