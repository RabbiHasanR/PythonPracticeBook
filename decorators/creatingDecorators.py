# With these prerequisites out of the way, let's go ahead and create a 
# simple decorator that will convert a sentence to uppercase. 
# We do this by defining a wrapper inside an enclosed function. 
# As you can see it very similar to the function inside another 
# function that we created earlier.

def uppercase_decorator(function):
    def wrapper():
        make_uppercase = function().upper()
        return make_uppercase
    return wrapper

# Our decorator function takes a function as an argument,
# and we shall, therefore, define a function and pass it to our decorator. 
# We learned earlier that we could assign a function to a variable. 
# We'll use that trick to call our decorator function.

def say_hi():
    return 'hello there'

decorator = uppercase_decorator(say_hi)
print(decorator())


# However, Python provides a much easier way for us to apply decorators. 
# We simply use the @ symbol before the function we'd like to decorate. 
# Let's show that in practice below.

@uppercase_decorator
def say_hello():
    return 'hi there'

print(say_hello())