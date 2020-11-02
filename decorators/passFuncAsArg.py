# Functions can also be passed as parameters to other functions.
# Let's illustrate that below.

def plus_one(number):
    return number + 1

def function_call(function):
    num_to_add = 5
    return function(num_to_add)

print(function_call(plus_one))  # 6