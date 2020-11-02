# A function can also generate another function. 
# We'll show that below using an example.

def hello_function():
    def say_hi():
        return 'Hi'
    return say_hi

hello = hello_function()
print(hello())