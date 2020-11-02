# A common pattern with comprehensions—including list , dict , and
# set variants—is the need to reference the same computation in mul-
# tiple places. For example, say that I’m writing a program to manage
# orders for a fastener company. As new orders come in from customers,
# I need to be able to tell them whether I can fulfill their orders. I need
# to verify that a request is sufficiently in stock and above the mini-
# mum threshold for shipping

stock = {
    'nails': 125,
    'screws': 35,
    'wingnuts': 8,
    'washers': 24,
}

order = ['screws', 'wingnuts', 'clips']

def get_batches(count, size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches
print(result)

# Here, I implement this looping logic more succinctly using a dictio-
# nary comprehension

found = {name: get_batches(stock.get(name, 0), 8)
        for name in order
        if get_batches(stock.get(name, 0), 8)}
print(found)


# Although this code is more compact, the problem with it is that the
# get_batches(stock.get(name, 0), 8) expression is repeated. This
# hurts readability by adding visual noise that’s technically unneces-
# sary. It also increases the likelihood of introducing a bug if the two
# expressions aren’t kept in sync. For example, here I’ve changed the
# first get_batches call to have 4 as its second parameter instead of 8 ,
# which causes the results to be different:

has_bug = {name: get_batches(stock.get(name, 0), 4)
            for name in order
            if get_batches(stock.get(name, 0), 8)}
print(f'Expected: {found}')
print(f'Found: {has_bug}')


# An easy solution to these problems is to use the walrus operator ( := ),
# which was introduced in Python 3.8, to form an assignment expres-
# sion as part of the comprehension

found = {name: batches for name in order
        if (batches := get_batches(stock.get(name, 0), 8))}

print(found)


# The assignment expression ( batches := get_batches(...) ) allows me
# to look up the value for each order key in the stock dictionary a single
# time, call get_batches once, and then store its corresponding value in
# the batches variable. I can then reference that variable elsewhere in
# the comprehension to construct the dict ’s contents instead of having
# to call get_batches a second time. Eliminating the redundant calls
# to get and get_batches may also improve performance by avoiding
# unnecessary computations for each item in the order list .


# It’s valid syntax to define an assignment expression in the value
# expression for a comprehension. But if you try to reference the vari-
# able it defines in other parts of the comprehension, you might get an
# exception at runtime because of the order in which comprehensions
# are evaluated:

# result = {name: (tenth := count // 10)
#          for name, count in stock.items() if tenth > 0}     # NameError: name 'tenth' is not defined
# print(result)


# I can fix this example by moving the assignment expression into the
# condition and then referencing the variable name it defined in the
# comprehension’s value expression:

result = {name: tenth for name, count in stock.items()
         if (tenth := count // 10) > 0}
print(result)


# If a comprehension uses the walrus operator in the value part of the
# comprehension and doesn’t have a condition, it’ll leak the loop vari-
# able into the containing scope
half = [(last := count // 2) for count in stock.values()]
print(f'Last item of {half} in {last}')

# This leakage of the loop variable is similar to what happens with a
# normal for loop:

for count in stock.values():    # leek loop variable
    pass

print(f'Last item of {stock.values()} is {count}')


# However, similar leakage doesn’t happen for the loop variables from
# comprehensions:

half = [value // 2 for value in stock.values()]
print(half)
# print(value)    # # Exception because loop variable didn't leak

# It’s better not to leak loop variables, so I recommend using assign-
# ment expressions only in the condition part of a comprehension.



# Using an assignment expression also works the same way in gener-
# ator expressions (see Item 32: “Consider Generator Expressions for
# Large List Comprehensions”). Here, I create an iterator of pairs con-
# taining the item name and the current count in stock instead of a
# dict instance:

found = ((name, batches) for name in order
        if (batches := get_batches(stock.get(name, 0), 8)))

print(next(found))
print(next(found))



# Things to Remember
# ✦ Assignment expressions make it possible for comprehensions and
# generator expressions to reuse the value from one condition else-
# where in the same comprehension, which can improve readability
# and performance.
# ✦ Although it’s possible to use an assignment expression outside of
# a comprehension or generator expression’s condition, you should
# avoid doing so.