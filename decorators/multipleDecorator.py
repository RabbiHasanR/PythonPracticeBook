# We can use multiple decorators to a single function. 
# However, the decorators will be applied in the order that we've called them. 
# Below we'll define another decorator that splits the sentence into a list.
# We'll then apply the uppercase_decorator and split_string decorator to a single function.

def uppercase_decorator(function):
    def wrapper():
        make_uppercase = function().upper()
        return make_uppercase
    return wrapper

def split_string(function):
    def wrapper():
        splitted_string = function().split()
        return splitted_string
    return wrapper

@split_string
@uppercase_decorator
def say_hi():
    return 'hi rabbi'

print(say_hi())


# From the above output, we notice that the application of decorators is from the bottom up. 
# Had we interchanged the order, we'd have seen an error since lists don't have an upper
# attribute. The sentence has first been converted to uppercase and then split into a list