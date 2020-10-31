# When working with a dictionary that you didn’t create, there are a
# variety of ways to handle missing keys (see Item 16: “Prefer get Over
# in and KeyError to Handle Missing Dictionary Keys”). Although using
# the get method is a better approach than using in expressions and
# KeyError exceptions, for some use cases setdefault appears to be the
# shortest option.
# For example, say that I want to keep track of the cities I’ve visited in
# countries around the world. Here, I do this by using a dictionary that
# maps country names to a set instance containing corresponding city
# names:

visits = {
    'Mexico': {'Tulum', 'Puerto Vallarta'},
    'Japan': {'Hakone'},
}


# I can use the setdefault method to add new cities to the sets, whether
# the country name is already present in the dictionary or not. This
# approach is much shorter than achieving the same behavior with the
# get method and an assignment expression (which is available as of
# Python 3.8):

visits.setdefault('France', set()).add('Arles')     # short
print(visits)

if(japan := visits.get('Japan')) is None:           # long
    visits['Japan'] = japan = set()
japan.add('Kyoto')
print(visits)


# What about the situation when you do control creation of the dictio-
# nary being accessed? This is generally the case when you’re using a
# dictionary instance to keep track of the internal state of a class, for
# example. Here, I wrap the example above in a class with helper meth-
# ods to access the dynamic inner state stored in a dictionary:

class Visits:
    def __init__(self):
        self.data = {}
    
    def add(self, country, city):
        city_set = self.data.setdefault(country, set())
        city_set.add(city)

# This new class hides the complexity of calling setdefault correctly,
# and it provides a nicer interface for the programmer:

visits = Visits()
visits.add('Russia', 'Yekaterinburg')
visits.add('Tanzania', 'Zanzibar')
print(visits.data)


# However, the implementation of the Visits.add method still isn’t ideal.
# The setdefault method is still confusingly named, which makes it
# more difficult for a new reader of the code to immediately understand
# what’s happening. And the implementation isn’t efficient because it
# constructs a new set instance on every call, regardless of whether the
# given country was already present in the data dictionary

# Luckily, the defaultdict class from the collections built-in module
# simplifies this common use case by automatically storing a default
# value when a key doesn’t exist. All you have to do is provide a function
# that will return the default value to use each time a key is missing
# (an example of Item 38: “Accept Functions Instead of Classes for Sim-
# ple Interfaces”). Here, I rewrite the Visits class to use defaultdict :

from collections import defaultdict

class Visits:
    def __init__(self):
        self.data = defaultdict(set)
    
    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('England', 'Batah')
visits.add('England', 'London')
print(visits.data)