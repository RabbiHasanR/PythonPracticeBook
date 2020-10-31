# In Python 3.5 and before, iterating over a dict would return keys in
# arbitrary order. The order of iteration would not match the order in
# which the items were inserted. For example, here I create a dictionary
# mapping animal names to their corresponding baby names and then
# print it out

baby_names = {
    'cat': 'kitten',
    'dog': 'puppy',
}

print(baby_names)

print(baby_names.keys())
print(baby_names.values())
print(baby_names.items())
print(baby_names.popitem())

# Now, the order of keyword arguments is always preserved to match
# how the programmer originally called the function:
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

my_func(goose='gosling', kangaroo='joey')

# Classes also use the dict type for their instance dictionaries.
class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'

a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')


# For example, say that I’m writing a program to show the results of a
# contest for the cutest baby animal. Here, I start with a dictionary con-
# taining the total vote count for each one:
votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

# I define a function to process this voting data and save the rank of
# each animal name into a provided empty dictionary. In this case, the
# dictionary could be the data model that powers a UI element:
def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


# I also need a function that will tell me which animal won the contest.
# This function works by assuming that populate_ranks will assign the
# contents of the ranks dictionary in ascending order, meaning that the
# first key must be the winner:
def get_winner(ranks):
    return next(iter(ranks))

# Here, I can confirm that these functions work as designed and deliver
# the result that I expected:
ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)


# Now, imagine that the requirements of this program have changed.
# The UI element that shows the results should be in alphabet-
# ical order instead of rank order. To accomplish this, I can use the
# collections.abc built-in module to define a new dictionary-like class
# that iterates its contents in alphabetical order:
# from collections.abc import MutableMapping

# class SortedDict(MutableMapping):
#     def __init__(self):
#         self.data = {}
    
#     def __getitem__(self, key):
#         return self.data[key]
    
#     def __setitem__(self, key, value):
#         self.data[key] = value

#     def __delitem__(self, key):
#         del self.data[key]

#     def __iter__(self):
#         keys = list(self.data.keys())
#         keys.sort()
#         for key in keys:
#             yield key

#     def __len__(self):
#         return len(self.data)


# # I can use a SortedDict instance in place of a standard dict with the
# # functions from before and no errors will be raised since this class
# # conforms to the protocol of a standard dictionary. However, the result
# # is incorrect:

# sorted_ranks = SortedDict()
# populate_ranks(votes, sorted_ranks)
# print(sorted_ranks.data)
# winner = get_winner(sorted_ranks)
# print(winner)

# There are three ways to mitigate this problem. First, I can reimple-
# ment the get_winner function to no longer assume that the ranks dic-
# tionary has a specific iteration order. This is the most conservative
# and robust solution:
# def get_winner(ranks):
#     for name, rank in ranks.items():
#         if rank == 1:
#             return name

# winner = get_winner(sorted_ranks)
# print(winner)


# The second approach is to add an explicit check to the top of the func-
# tion to ensure that the type of ranks matches my expectations, and
# to raise an exception if not. This solution likely has better runtime
# performance than the more conservative approach:

# def get_winner(ranks):
#     if not isinstance(ranks, dict):
#         raise TypeError('must provide a dict instance')
#     return next(iter(ranks))

# winner = get_winner(sorted_ranks)
# print(winner)


# The third alternative is to use type annotations to enforce that the
# value passed to get_winner is a dict instance and not a MutableMapping
# with dictionary-like behavior (see Item 90: “Consider Static Analysis
# via typing to Obviate Bugs”). Here, I run the mypy tool in strict mode
# on an annotated version of the code above:

from typing import Dict, MutableMapping

def populate_ranks(votes: Dict[str, int],
                    ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

def get_winner(ranks):
    return next(iter(ranks))

class SortedDict(MutableMapping[str, int]):
    def __init__(self):
        self.data = {}
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)

votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)