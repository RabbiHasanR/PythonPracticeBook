# Here, I define a dictio-
# nary of counters with the current votes for each style:

counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}

# To increment the counter for a new vote, I need to see if the key exists,
# insert the key with a default counter value of zero if it’s missing, and
# then increment the counter’s value. This requires accessing the key
# two times and assigning it once. Here, I accomplish this task using
# an if statement with an in expression that returns True when the key
# is present:

key = 'wheat'

if key not in counters:
    counters[key] = 0
counters[key] += 1
print(counters)


if key in counters:
    count = counters[key]
else:
    count = 0
counters[key] = count + 1
print(counters)

# Another way to accomplish the same behavior is by relying on how
# dictionaries raise a KeyError exception when you try to get the value
# for a key that doesn’t exist. This approach is more efficient because it
# requires only one access and one assignment:

try:
    count = counters[key]
except KeyError:
    count = 0
counters[key] = count + 1
print(counters)


# This flow of fetching a key that exists or returning a default value
# is so common that the dict built-in type provides the get method to
# accomplish this task. The second parameter to get is the default value
# to return in the case that the key—the first parameter—isn’t present.
# This also requires only one access and one assignment, but it’s much
# shorter than the KeyError example:

count = counters.get(key, 0)
counters[key] = count + 1
print(counters)


# What if the values of the dictionary are a more complex type, like a
# list ? For example, say that instead of only counting votes, I also want
# to know who voted for each type of bread. Here, I do this by associat-
# ing a list of names with each key:

votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}

key = 'brioche'
who = 'Elmer'

# if key in votes:
#     names = votes[key]
# else:
#     votes[key] = names = []
# names.append(who)
# print(votes)


# It’s also possible to rely on the KeyError exception being raised when
# the dictionary value is a list . This approach requires one key access
# if the key is present, or one key access and one assignment if it’s
# missing, which makes it more efficient than the in condition:

# try:
#     names = votes[key]
# except KeyError:
#     votes[key] = names = []
# names.append(who)
# print(votes)


# Similarly, you can use the get method to fetch a list value when the
# key is present, or do one fetch and one assignment if the key isn’t
# present:

# names = votes.get(key)
# if names is None:
#     votes[key] = names = []
# names.append(who)
# print(votes)


# The approach that involves using get to fetch list values can
# further be shortened by one line if you use an assignment expres-
# sion ( introduced in Python 3.8; see Item 10: “Prevent Repetition
# with Assignment Expressions”) in the if statement, which improves
# readability:

# if (names := votes.get(key)) is None:
#     votes[key] = names = []
# names.append(who)
# print(votes)


# The dict type also provides the setdefault method to help shorten
# this pattern even further. setdefault tries to fetch the value of a key
# in the dictionary. If the key isn’t present, the method assigns that key
# to the default value provided. And then the method returns the value
# for that key: either the originally present value or the newly inserted
# default value. Here, I use setdefault to implement the same logic as in
# the get example above:

names = votes.setdefault(key, [])
names.append(who)
print(votes)


# There’s also one important gotcha: The default value passed to
# setdefault is assigned directly into the dictionary when the key is
# missing instead of being copied. Here, I demonstrate the effect of this
# when the value is a list :

data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('Befor: ', data)
value.append('hello')
print('After: ', data)