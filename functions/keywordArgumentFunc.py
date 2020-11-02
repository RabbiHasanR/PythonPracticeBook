# As in most other programming languages, in Python you may pass
# arguments by position when calling a function:

def reminder(number, divisor):
    return number % divisor

print(reminder(20, 7))  # 6

# All normal arguments to Python functions can also be passed by
# keyword, where the name of the argument is used in an assignment
# within the parentheses of a function call. The keyword arguments
# can be passed in any order as long as all of the required positional
# arguments are specified. You can mix and match keyword and posi-
# tional arguments. These calls are equivalent:
print(reminder(20, divisor=7))  # 6
print(reminder(number=20, divisor=7))   # 6
print(reminder(divisor=7, number=20))   # 6

# Positional arguments must be specified before keyword arguments
# print(reminder(number=20, 7))   # SyntaxError: positional argument follows keyword argument

# Each argument can be specified only once:
#print(reminder(20, number=7))   # TypeError: reminder() got multiple values for argument 'number'


# If you already have a dictionary, and you want to use its contents to
# call a function like remainder , you can do this by using the ** opera-
# tor. This instructs Python to pass the values from the dictionary as
# the corresponding keyword arguments of the function:

my_kwargs = {
    'number': 20,
    'divisor': 7,
}

print(reminder(**my_kwargs))    # 6


# You can mix the ** operator with positional arguments or keyword
# arguments in the function call, as long as no argument is repeated:
my_kwargs = {
    'divisor': 7,
}

print(reminder(number=20, **my_kwargs)) # 6


# You can also use the ** operator multiple times if you know that the
# dictionaries don’t contain overlapping keys:

my_kwargs = {
    'number': 20,
}

other_kwargs = {
    'divisor': 7,
}

assert reminder(**my_kwargs, **other_kwargs) == 6
print(reminder(**my_kwargs, **other_kwargs))    # 6


# And if you’d like for a function to receive any named keyword argu-
# ment, you can use the **kwargs catch-all parameter to collect those
# arguments into a dict that you can then process

def print_arguments(**kwargs):
    for key, value in kwargs.items():
        print(f'{key}: {value}')

print_arguments(alpha=1.5, beta=9, ghama=4)


# The flexibility of keyword arguments provides three significant
# benefits.
# The first benefit is that keyword arguments make the function call
# clearer to new readers of the code. With the call remainder(20, 7) , it’s
# not evident which argument is number and which is divisor unless
# you look at the implementation of the remainder method. In the call
# with keyword arguments, number=20 and divisor=7 make it immedi-
# ately obvious which parameter is being used for each purpose.

# The second benefit of keyword arguments is that they can have
# default values specified in the function definition. This allows a func-
# tion to provide additional capabilities when you need them, but you
# can accept the default behavior most of the time. This eliminates
# repetitive code and reduces noise.
# For example, say that I want to compute the rate of fluid flowing into
# a vat. If the vat is also on a scale, then I could use the difference
# between two weight measurements at two different times to deter-
# mine the flow rate:

def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print(f'{flow:.3} kg per second')


# In the typical case, it’s useful to know the flow rate in kilograms per
# second. Other times, it’d be helpful to use the last sensor measure-
# ments to approximate larger time scales, like hours or days. I can
# provide this behavior in the same function by adding an argument for
# the time period scaling factor:

def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period

# The problem is that now I need to specify the period argument every
# time I call the function, even in the common case of flow rate per sec-
# ond

flow_per_second = flow_rate(weight_diff, time_diff, 1)

print(f'{flow_per_second:.3} kg per second')

# To make this less noisy, I can give the period argument a default
# value:

def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

# The period argument is now optional:
flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print(f'{flow_per_second:.3} kg per second')
print(f'{flow_per_hour:.3} kg per hour')
# This works well for simple default values; it gets tricky for complex
# default values



# The third reason to use keyword arguments is that they provide a
# powerful way to extend a function’s parameters while remaining
# backward compatible with existing callers. This means you can pro-
# vide additional functionality without having to migrate a lot of exist-
# ing code, which reduces the chance of introducing bugs.
# For example, say that I want to extend the flow_rate function above
# to calculate flow rates in weight units besides kilograms. I can do this
# by adding a new optional parameter that provides a conversion rate to
# alternative measurement units:

def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period


# The default argument value for units_per_kg is 1 , which makes the
# returned weight units remain kilograms. This means that all existing
# callers will see no change in behavior. New callers to flow_rate can
# specify the new keyword argument to see the new behavior:

pounds_per_hour = flow_rate(weight_diff, time_diff, period=3600, units_per_kg=2.2)
print(f'{pounds_per_hour:.3} pound per hour')


# Providing backward compatibility using optional keyword arguments
# like this is also crucial for functions that accept *args (see Item 22:
# “Reduce Visual Noise with Variable Positional Arguments”).
# The only problem with this approach is that optional keyword argu-
# ments like period and units_per_kg may still be specified as posi-
# tional arguments:
pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)

# Supplying optional arguments positionally can be confusing because
# it isn’t clear what the values 3600 and 2.2 correspond to. The best
# practice is to always specify optional arguments using the keyword
# names and never pass them as positional arguments. As a function
# author, you can also require that all callers use this more explicit
# keyword style to minimize potential errors


# Things to Remember
# ✦ Function arguments can be specified by position or by keyword.
# ✦ Keywords make it clear what the purpose of each argument is when
# it would be confusing with only positional arguments.
# ✦ Keyword arguments with default values make it easy to add new
# behaviors to a function without needing to migrate all existing
# callers.
# ✦ Optional keyword arguments should always be passed by keyword
# instead of by position.