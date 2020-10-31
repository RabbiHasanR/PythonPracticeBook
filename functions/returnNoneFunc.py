# When writing utility functions, there’s a draw for Python program-
# mers to give special meaning to the return value of None . It seems to
# make sense in some cases. For example, say I want a helper function
# that divides one number by another. In the case of dividing by zero,
# returning None seems natural because the result is undefined:

def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

#Code using this function can interpret the return value accordingly:

x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print('Invalid inputs.')



# What happens with the careful_divide function when the numerator
# is zero? If the denominator is not zero, the function returns zero. The
# problem is that a zero return value can cause issues when you evalu-
# ate the result in a condition like an if statement. You might acciden-
# tally look for any False -equivalent value to indicate errors instead of
# only looking for None

x, y = 0, 5
result = careful_divide(x, y)
if not result:
    print('Invalid inputs.')    # This runs ! but shouldn't


# This misinterpretation of a False -equivalent return value is a common
# mistake in Python code when None has special meaning. This is why
# returning None from a function like careful_divide is error prone.
# There are two ways to reduce the chance of such errors.
# The first way is to split the return value into a two-tuple (see Item 19:
# “Never Unpack More Than Three Variables When Functions Return
# Multiple Values” for background). The first part of the tuple indicates
# that the operation was a success or failure. The second part is the
# actual result that was computed:

def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None

# Callers of this function have to unpack the tuple . That forces them
# to consider the status part of the tuple instead of just looking at the
# result of division:

success, result = careful_divide(x, y)
if not success:
    print('Invalid inputs.')
else:
    print(result)


# The problem is that callers can easily ignore the first part of the tuple
# (using the underscore variable name, a Python convention for unused
# variables). The resulting code doesn’t look wrong at first glance, but
# this can be just as error prone as returning None :

_, result = careful_divide(x, y)
if not result:
    print('Invalid results')


# The second, better way to reduce these errors is to never return
# None for special cases. Instead, raise an Exception up to the caller
# and have the caller deal with it. Here, I turn a ZeroDivisionError into
# a ValueError to indicate to the caller that the input values are bad

def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

# The caller no longer requires a condition on the return value of the
# function. Instead, it can assume that the return value is always
# valid and use the results immediately in the else block after try

x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print(f'Result is {result}')


# This approach can be extended to code using type annotations
# (see Item 90: “Consider Static Analysis via typing to Obviate Bugs”
# for background). You can specify that a function’s return value will
# always be a float and thus will never be None . However, Python’s
# gradual typing purposefully doesn’t provide a way to indicate when
# exceptions are part of a function’s interface (also known as checked
# exceptions). Instead, you have to document the exception-raising
# behavior and expect callers to rely on that in order to know which
# Exceptions they should plan to catch (see Item 84: “Write Docstrings
# for Every Function, Class, and Module”).
# Pulling it all together, here’s what this function should look like when
# using type annotations and docstrings:

def careful_divide(a: float, b: float) -> float:
    """Divides a by b.

    Raises:
        ValueError: When the inputs cannot be divided. 
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

x, y = 0, 5
try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print(f'Result is {result}')