# To define a general purpose decorator that can be applied to any function 
# we use args and **kwargs. args and **kwargs collect all positional and 
# keyword arguments and stores them in the args and kwargs variables. 
# args and kwargs allow us to pass as many arguments as we would like during function calls.

def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print(f'The positional arguments are: {args}')
        print(f'The keyword arguments are: {kwargs}')
        function_to_decorate(*args)
    return a_wrapper_accepting_arbitrary_arguments

@a_decorator_passing_arbitrary_arguments
def function_with_no_arguments():
    print('No arguments here')

function_with_no_arguments()


# Let's see how we'd use the decorator using positional arguments.

@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print(a, b, c)

function_with_arguments(1, 2, 3)


# Keyword arguments are passed using keywords. An illustration of this is shown below.
@a_decorator_passing_arbitrary_arguments
def funciton_with_keyword_arguments():
    print('This has shows keyword arguments')

funciton_with_keyword_arguments(first_name="Derrick", last_name="Mwiti")