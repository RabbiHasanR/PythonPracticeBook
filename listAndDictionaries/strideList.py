# For example, stride makes it easy to group even and odd indexs in list

x = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = x[::2]
evens = x[1::2]

print(odds)
print(evens)

# The problem is that the stride syntax often causes unexpected behav-
# ior that can introduce bugs. For example, a common Python trick for
# reversing a byte string is to slice the string with a stride of -1 :
x = b'mongoose'
y = x[::-1]
print(y)

# This is also work correctly for unicode string
x = 'ᇓৌ'
y = x[::-1]
print(y)

# But it will break when unicode data is encoded as a UTF-8 byte string.
w = 'ᇓৌ'
x = w.encode('utf-8')
y = x[::-1]
print(y)
# z = y.decode('utf-8')
# print(z)

# Are negative strides besides -1 useful? Consider the following
# examples:
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(x[::2])   # ::2 means “Select every second item starting at the beginning.”
print(x[::-2])  # ::-2 means “Select every second item starting at the end and moving backward.”

# What do you think 2::2 means? What about -2::-2 vs. -2:2:-2 vs.
# 2:2:-2 ?

print(x[2::2])  # ['c', 'e', 'g']
print(x[-2::-2])    # ['g', 'e', 'c', 'a']
print(x[-2:2:-2])   # ['g', 'e']
print(x[2:2:-2])    # []


# If you must use a stride, prefer making it a
# positive value and omit start and end indexes. If you must use a stride
# with start or end indexes, consider using one assignment for striding
# and another for slicing:
y = x[::2]  # ['a', 'c', 'e', 'g']
z = y[1:-1] # ['c', 'e']

print(y)
print(z)