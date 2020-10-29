# The basic form of the slicing syntax is somelist[start:end] , where
# start is inclusive and end is exclusive:
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('Middle Two: ', a[3:5])
print('All but ends: ', a[1:7])

# When slicing from the start of a list , you should leave out the zero
# index to reduce visual noise:
assert a[:5] == a[0:5]

# When slicing to the end of a list , you should leave out the final index
# because it’s redundant:
assert a[1:] == a[1:len(a)]

# Using negative numbers for slicing is helpful for doing offsets relative
# to the end of a list . All of these forms of slicing would be clear to
# a new reader of your code:
print(a[:])     # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(a[:5])    # ['a', 'b', 'c', 'd', 'e']
print(a[:-1])   # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print(a[4:])    # ['e', 'f', 'g', 'h']
print(a[-3:])   # ['f', 'g', 'h']
print(a[2:5])   # ['c', 'd', 'e']
print(a[2:-1])  # ['c', 'd', 'e', 'f', 'g']
print(a[-3:-1]) # ['f', 'g']


# Slicing deals properly with start and end indexes that are beyond the
# boundaries of a list by silently omitting missing items. This behav-
# ior makes it easy for your code to establish a maximum length to
# consider for an input sequence:
b = [1, 2, 3, 4, 5, 6]
first_twenty_item = b[:20]
last_twentry_item = b[-20:]

print(first_twenty_item)
print(last_twentry_item)

# In contrast, accessing the same index directly causes an exception:
#print(b[20])    #IndexError: list index out of range

# result of the slicing list return a new list
# Modifying the result of
# slicing won’t affect the original list :
c = a[3:]
print('Before: ', c)
c[1] = 99
print('After: ', c)
print('No Change: ', a)

print('Before: ', a)
a[2:7] = [99, 22, 14]
print('After: ', a)     # the list shrinks because replacement list is shorter then specified list


print('Before: ', a)
a[2:3] = [47, 11]
print('After: ', a)     # the list grows because assigned list is longer then specified list


d = a[:]    # if you leave out both the start and end index when slicing ,you end up with a copy of original list
assert d == a and d is not a


d = a   # if you assign to a slice with no start or end indexs ,
        # you replace the entire contecs of the list with a copy of what's referenced
        # (instead of allocating a new list )

print('Before a: ', a)
print('Before d: ', d)
a[:] = [101, 102, 103]
assert a is d               # Still the same list object
print('After a: ', a)       # Now has different contents
print('After b: ', d)       # Same list, so same contents as a
