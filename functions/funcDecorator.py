# Python has special syntax for decorators that can be applied to
# functions. A decorator has the ability to run additional code before
# and after each call to a function it wraps. This means decorators
# can access and modify input arguments, return values, and raised
# exceptions. This functionality can be useful for enforcing semantics,
# debugging, registering functions, and more.
# For example, say that I want to print the arguments and return value
# of a function call. This can be especially helpful when debugging
# the stack of nested function calls from a recursive function. Here,
# I define such a decorator by using *args and **kwargs (see Item 22:
# “Reduce Visual Noise with Variable Positional Arguments” and Item
# 23: “Provide Optional Behavior with Keyword Arguments”) to pass
# through all parameters to the wrapped function:

def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__} ({args!r}, {kwargs!r}) -> {result!r}')
        return result
    return wrapper


# I can apply this decorator to a function by using the @ symbol:
@trace
def fibonacci(n):
    """Return the n-th fibonacci number"""
    if n in (0,1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

# Using the @ symbol is equivalent to calling the decorator on the func-
# tion it wraps and assigning the return value to the original name in
# the same scope:

# fibonacci = trace(fibonacci)


# The decorated function runs the wrapper code before and after
# fibonacci runs. It prints the arguments and return value at each
# level in the recursive stack:

result = fibonacci(4)
print(result)   # 3


# This works well, but it has an unintended side effect. The value
# returned by the decorator—the function that’s called above—doesn’t
# think it’s named fibonacci :

print(fibonacci)    # <function trace.<locals>.wrapper at 0x7feab0b341f0>


# The cause of this isn’t hard to see. The trace function returns the
# wrapper defined within its body. The wrapper function is what’s
# assigned to the fibonacci name in the containing module because
# of the decorator. This behavior is problematic because it undermines
# tools that do introspection, such as debuggers (see Item 80: “Consider
# Interactive Debugging with pdb ”).
# For example, the help built-in function is useless when called on the
# decorated fibonacci function. It should instead print out the doc-
# string defined above ( 'Return the n-th Fibonacci number' ):

# help(fibonacci)


# Object serializers (see Item 68: “Make pickle Reliable with copyreg ”)
# break because they can’t determine the location of the original func-
# tion that was decorated:

import pickle

# pickle.dumps(fibonacci)     # AttributeError: Can't pickle local object 'trace.<locals>.wrapper'


# The solution is to use the wraps helper function from the functools
# built-in module. This is a decorator that helps you write decorators.
# When you apply it to the wrapper function, it copies all of the import-
# ant metadata about the inner function to the outer function:

import functools


def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__} ({args!r}, {kwargs!r}) -> {result!r}')
        return result
    return wrapper


# I can apply this decorator to a function by using the @ symbol:
@trace
def fibonacci(n):
    """Return the n-th fibonacci number"""
    if n in (0,1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


# Now, running the help function produces the expected result, even
# though the function is decorated:

# help(fibonacci)


print(pickle.dumps(fibonacci))

# Beyond these examples, Python functions have many other standard
# attributes (e.g., __name__ , __module__ , __annotations__ ) that must
# be preserved to maintain the interface of functions in the language.
# Using wraps ensures that you’ll always get the correct behavior.
# Things to Remember
# ✦ Decorators in Python are syntax to allow one function to modify
# another function at runtime.
# ✦ Using decorators can cause strange behaviors in tools that do intro-
# spection, such as debuggers.
# ✦ Use the wraps decorator from the functools built-in module when
# you define your own decorators to avoid issues.