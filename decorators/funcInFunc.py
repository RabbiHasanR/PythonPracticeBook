# Next, we'll illustrate how you can define a function inside another function in Python.
# Stay with me, we'll soon find out how all this is relevant in creating and understanding 
# decorators in Python.

def plus_one(number):
    def add_one(number):
        return number + 1
    result = add_one(number)
    return result

print(plus_one(5))  # 6