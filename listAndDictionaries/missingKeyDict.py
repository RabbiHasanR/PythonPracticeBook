# The built-in dict type’s setdefault method results in shorter code
# when handling missing keys in some specific circumstances (see Item
# 16: “Prefer get Over in and KeyError to Handle Missing Dictionary
# Keys” for examples). For many of those situations, the better tool for
# the job is the defaultdict type from the collections built-in module
# (see Item 17: “Prefer defaultdict Over setdefault to Handle Missing
# Items in Internal State” for why). However, there are times when nei-
# ther setdefault nor defaultdict is the right fit.
# For example, say that I’m writing a program to manage social network
# profile pictures on the filesystem. I need a dictionary to map profile
# picture pathnames to open file handles so I can read and write those
# images as needed. Here, I do this by using a normal dict instance
# and checking for the presence of keys using the get method and an
# assignment expression (introduced in Python 3.8; see Item 10: “Pre-
# vent Repetition with Assignment Expressions”)

pictures = {}
path = 'profile_1234.png'

if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()
print(image_data)
print(pictures)


# Although it’s possible to use the in expression or KeyError approaches
# to implement this same logic, those options require more dictionary
# accesses and levels of nesting. Given that these other options work,
# you might also assume that the setdefault method would work, too:

try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'Failed to open path {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()
print(image_data)
print(pictures)


# If you’re trying to manage internal state, another assumption you
# might make is that a defaultdict could be used for keeping track of
# these profile pictures. Here, I attempt to implement the same logic as
# before but now using a helper function and the defaultdict class:

from collections import defaultdict

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    
# pictures = defaultdict(open_picture)
# handle = pictures[path]
# handle.seek(0)
# image_data = handle.read()
# print(image_data)
# print(pictures)

# The problem is that defaultdict expects that the function passed to
# its constructor doesn’t require any arguments. This means that the
# helper function that defaultdict calls doesn’t know which specific key
# is being accessed, which eliminates my ability to call open . In this
# situation, both setdefault and defaultdict fall short of what I need.

# Fortunately, this situation is common enough that Python has
# another built-in solution. You can subclass the dict type and imple-
# ment the __missing__ special method to add custom logic for han-
# dling missing keys. Here, I do this by defining a new class that takes
# advantage of the same open_picture helper method defined above:

class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
print(image_data)
print(pictures)