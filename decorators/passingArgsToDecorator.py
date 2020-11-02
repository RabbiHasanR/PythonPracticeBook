# Now let's see how we'd pass arguments to the decorator itself. 
# In order to achieve this, we define a decorator maker that accepts arguments 
# then define a decorator inside it.
# We then define a wrapper function inside the decorator as we did earlier.

def decorator_maker_with_arguments(decorator_arg1, decorator_arg2, decorator_arg3):
    def decorator(func):
        def wrapper(func_arg1, func_arg2, func_arg3):
            "This is a wrapper function"
            print("The wrapper can access all the variables\n"
                  "\t- from the decorator maker: {0} {1} {2}\n"
                  "\t- from the function call: {3} {4} {5}\n"
                  "and pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,decorator_arg3,
                          func_arg1, func_arg2,func_arg3))
            return func(func_arg1, func_arg2, func_arg3)
        return wrapper
    return decorator

panda = 'pandas'
@decorator_maker_with_arguments(panda, 'Numpy', 'Scikit-learn')
def decorated_function_with_arguments(func_arg1, func_arg2, func_arg3):
    print("This is the decorated function and it only knows about its arguments: {0}"
           " {1}" " {2}".format(func_arg1, func_arg2,func_arg3))

decorated_function_with_arguments(panda, "Science", "Tools")


# Debugging Decorators
# As we have noticed, decorators wrap functions. The original function name, 
# its docstring, and parameter list are all hidden by the wrapper closure: 
# For example, when we try to access the decorated_function_with_arguments metadata, 
# we'll see the wrapper closure's metadata. This presents a challenge when debugging.

print(decorated_function_with_arguments.__name__)   # wrapper
print(decorated_function_with_arguments.__doc__)    # This is a wrapper function



# In order to solve this challenge Python provides a functools.
# wraps decorator. This decorator copies the lost metadata from 
# the undecorated function to the decorated closure. Let's show how we'd do that.

import functools

def uppercase_decorator(function):
    @functools.wraps(function)
    def wrapper():
        return function().upper()
    return wrapper

@uppercase_decorator
def say_hi():
    "This will say hello world"
    return 'Hello wrold'

print(say_hi)
print(say_hi())


# When we check the say_hi metadata, we notice that it is now referring 
# to the function's metadata and not the wrapper's metadata.
print(say_hi.__name__)  # say_hi
print(say_hi.__doc__)   # This will say hello world