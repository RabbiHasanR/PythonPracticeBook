# Sometimes we might need to define a decorator that accepts arguments.
# We achieve this by passing the arguments to the wrapper function. 
# The arguments will then be passed to the function that is being decorated at call time.

def decorator_with_argument(function):
    def wrapper_accepting_arguments(arg1, arg2):
        print(f'My arguments are {arg1}, {arg2}')
        function(arg1, arg1)
    return wrapper_accepting_arguments


@decorator_with_argument
def cities(city1, city2):
    print(f'Cities i love are {city1} and {city2}')

cities('Dhaka', 'London')