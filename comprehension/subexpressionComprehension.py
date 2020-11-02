# Beyond basic usage (see Item 27: “Use Comprehensions Instead of map
# and filter ”), comprehensions support multiple levels of looping. For
# example, say that I want to simplify a matrix (a list containing other
# list instances) into one flat list of all cells. Here, I do this with a list
# comprehension by including two for subexpressions. These subex-
# pressions run in the order provided, from left to right:

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)


# This example is simple, readable, and a reasonable usage of multiple
# loops in a comprehension. Another reasonable usage of multiple loops
# involves replicating the two-level-deep layout of the input list . For
# example, say that I want to square the value in each cell of a two-
# dimensional matrix. This comprehension is noisier because of the
# extra [] characters, but it’s still relatively easy to read:

squared = [[x**2 for x in row] for row in matrix]
print(squared)

# If this comprehension included another loop, it would get so long that
# I’d have to split it over multiple lines:
my_lists = [
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
]

flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]
print(flat)


# At this point, the multiline comprehension isn’t much shorter than
# the alternative. Here, I produce the same result using normal loop
# statements. The indentation of this version makes the looping clearer
# than the three-level-list comprehension:

flat = []

for sublist1 in my_lists:
    for sublist2 in sublist1:
        for x in sublist2:
            flat.append(x)
print(flat)


# Comprehensions support multiple if conditions. Multiple conditions
# at the same loop level have an implicit and expression. For example,
# say that I want to filter a list of numbers to only even values greater
# than 4. These two list comprehensions are equivalent:
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 ==0]
print(b)
print(c)
assert b == c


# Conditions can be specified at each level of looping after the for sub-
# expression. For example, say I want to filter a matrix so the only cells
# remaining are those divisible by 3 in rows that sum to 10 or higher.
# Expressing this with a list comprehension does not require a lot of
# code, but it is extremely difficult to read:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filterd = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]

print(filterd)



# Although this example is a bit convoluted, in practice you’ll see
# situations arise where such comprehensions seem like a good fit.
# I strongly encourage you to avoid using list , dict , or set comprehen-
# sions that look like this. The resulting code is very difficult for new
# readers to understand. The potential for confusion is even worse for
# dict comprehensions since they already need an extra parameter to
# represent both the key and the value for each item.
# The rule of thumb is to avoid using more than two control subexpres-
# sions in a comprehension. This could be two conditions, two loops,
# or one condition and one loop. As soon as it gets more complicated
# than that, you should use normal if and for statements and write a
# helper function


# Things to Remember
# ✦ Comprehensions support multiple levels of loops and multiple con-
# ditions per loop level.
# ✦ Comprehensions with more than two control subexpressions are
# very difficult to read and should be avoided.