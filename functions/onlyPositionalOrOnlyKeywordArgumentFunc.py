# Passing arguments by keyword is a powerful feature of Python func-
# tions. The flexibility of keyword arguments enables you to write
# functions that will be clear to new readers of your code for many use
# cases.
# For example, say I want to divide one number by another but know
# that I need to be very careful about special cases. Sometimes, I want
# to ignore ZeroDivisionError exceptions and return infinity instead.
# Other times, I want to ignore OverflowError exceptions and return
# zero instead:

def safe_divisor(number, divisor,
                ignore_overflow, ignore_zero_divisor):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_divisor:
            return float('inf')
        else:
            raise

# Using this function is straightforward. This call ignores the float
# overflow from division and returns zero:

result = safe_divisor(1.0, 10**500, True, False)
print(result)

# This call ignores the error from dividing by zero and returns infinity:
result = safe_divisor(1.0, 0, False, True)
print(result)


# The problem is that it’s easy to confuse the position of the two Bool-
# ean arguments that control the exception-ignoring behavior. This can
# easily cause bugs that are hard to track down. One way to improve the
# readability of this code is to use keyword arguments. By default, the
# function can be overly cautious and can always re-raise exceptions:

def safe_divisor_b(number, divisor,
                ignore_overflow=False,
                ignore_zero_divisor=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_divisor:
            return float('inf')
        else:
            raise


# Then, callers can use keyword arguments to specify which of the
# ignore flags they want to set for specific operations, overriding the
# default behavior:

result = safe_divisor_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_divisor_b(1.0, 0, ignore_zero_divisor=True)
print(result)


# The problem is, since these keyword arguments are optional behavior,
# there’s nothing forcing callers to use keyword arguments for clarity.
# Even with the new definition of safe_division_b , you can still call it
# the old way with positional arguments:

assert safe_divisor_b(1.0, 10**500, True, False) == 0


# With complex functions like this, it’s better to require that callers are
# clear about their intentions by defining functions with keyword-only
# arguments. These arguments can only be supplied by keyword, never
# by position.
# Here, I redefine the safe_division function to accept keyword-only
# arguments. The * symbol in the argument list indicates the end
# of positional arguments and the beginning of keyword-only
# arguments:

def safe_divisor_c(numbers, divisor, *,
                   ignore_overflow=False,
                   ignore_zero_divisor=False):
    try:
        return numbers / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_divisor:
            return float('inf')
        else:
            raise

# Now, calling the function with positional arguments for the keyword
# arguments won’t work:

# result = safe_divisor_c(1.0, 10**500, True, False)  # TypeError: safe_divisor_c() takes 2 positional arguments but 4 were given
# print(result)


# But keyword arguments and their default values will work as expected
# (ignoring an exception in one case and raising it in another):

result = safe_divisor_c(1.0, 10**500, ignore_overflow=True)
print(result)   # 0
result = safe_divisor_c(1.0, 0, ignore_zero_divisor=True)
print(result)   # inf
assert result == float('inf')


try:
    result = safe_divisor_c(1.0, 0)
except ZeroDivisionError:
    print('Invalid inputs')


# However, a problem still remains with the safe_division_c version of
# this function: Callers may specify the first two required arguments
# ( number and divisor ) with a mix of positions and keywords:

assert safe_divisor_c(numbers=2, divisor=5) == 0.4
assert safe_divisor_c(divisor=5, numbers=2) == 0.4
assert safe_divisor_c(2, divisor=5) == 0.4


# Later, I may decide to change the names of these first two arguments
# because of expanding needs or even just because my style preferences
# change:

def safe_divisor_d(numerator, denominator, *,
                   ignore_overflow=False,
                   ignore_zero_divisor=False):
    try:
        return numbers / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_divisor:
            return float('inf')
        else:
            raise


# Unfortunately, this seemingly superficial change breaks all the exist-
# ing callers that specified the number or divisor arguments using
# keywords:

# result = safe_divisor_d(numbers=2, divisor=5)   #   TypeError: safe_divisor_d() got an unexpected keyword argument 'numbers'


# Python 3.8 introduces a solution to this problem, called positional-only
# arguments. These arguments can be supplied only by position and
# never by keyword (the opposite of the keyword-only arguments
# demonstrated above).
# Here, I redefine the safe_division function to use positional-only
# arguments for the first two required parameters. The / symbol in the
# argument list indicates where positional-only arguments end:


def safe_divisor_e(numerator, denominator, /, *,
                   ignore_overflow=False,
                   ignore_zero_divisor=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_divisor:
            return float('inf')
        else:
            raise

# I can verify that this function works when the required arguments
# are provided positionally:

assert safe_divisor_e(2, 5) == 0.4

# But an exception is raised if keywords are used for the positional-only
# parameters:

# result = safe_divisor_e(numerator=2, denominator=5) # TypeError: safe_divisor_e() got some positional-only arguments passed as keyword arguments: 'numerator, denominator'
# print(result)


# Now, I can be sure that the first two required positional arguments
# in the definition of the safe_division_e function are decoupled from
# callers. I won’t break anyone if I change the parameters’ names again.
# One notable consequence of keyword- and positional-only arguments
# is that any parameter name between the / and * symbols in the argu-
# ment list may be passed either by position or by keyword (which is
# the default for all function arguments in Python). Depending on your
# API’s style and needs, allowing both argument passing styles can
# increase readability and reduce noise. For example, here I’ve added
# another optional parameter to safe_division that allows callers to
# specify how many digits to use in rounding the result:

def safe_divisor_f(numerator, denominator, /,
                    ndigits=10, *,
                    ignore_overflow=False,
                    ignore_zero_divisor=False):
    try:
        fraction = numerator / denominator
        return round(fraction, ndigits)
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_divisor:
            return float('inf')
        else:
            raise


# Now, I can call this new version of the function in all these differ-
# ent ways, since ndigits is an optional parameter that may be passed
# either by position or by keyword:

result = safe_divisor_f(22, 7)
print(result)
result = safe_divisor_f(22, 7, 5)
print(result)
result = safe_divisor_f(22, 7, ndigits=2)
print(result)


# Things to Remember
# ✦ Keyword-only arguments force callers to supply certain arguments
# by keyword (instead of by position), which makes the intention of a
# function call clearer. Keyword-only arguments are defined after a
# single * in the argument list.
# ✦ Positional-only arguments ensure that callers can’t supply
# certain parameters using keywords, which helps reduce coupling.
# Positional-only arguments are defined before a single / in the argu-
# ment list.
# ✦ Parameters between the / and * characters in the argument list
# may be supplied by position or keyword, which is the default for
# Python parameters.