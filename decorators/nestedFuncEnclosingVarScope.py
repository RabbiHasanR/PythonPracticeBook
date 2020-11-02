# python allows a nested function to access the outer scope of the enclosing function. 
# This is a critical concept in decorators -- this pattern is known as a Closure.

def print_message(message):
    "Enclosing function"
    name = "Rabbi"
    def message_sender():
        "Nested function"
        print(name)
        if True:
            # name = "Hasan"
            print(f'{message} {name}')
            return 4
        return 4
    message_sender()
    return name
    

name = print_message("Hi")
print(name)


