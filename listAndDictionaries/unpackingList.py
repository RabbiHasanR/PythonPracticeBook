# For example, here I have
# a list of the ages of cars that are being traded in at a dealership.
# When I try to take the first two items of the list with basic unpack-
# ing, an exception is raised at runtime:
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
print(car_ages_descending)
# oldest, second_oldest = car_ages_descending     # ValueError: too many values to unpack (expected 2)
# print(oldest, second_oldest)


# For example, here
# I extract the oldest, second oldest, and other car ages from a list of at
# least two items:
oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others)

# I use a starred expres-
# sion to achieve the same result as above without indexing or slicing:
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

# A starred expression may appear in any position, so you can get the
# benefits of catch-all unpacking anytime you need to extract one slice:
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)
*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)


# However, to unpack assignments that contain a starred expres-
# sion, you must have at least one required part, or else you’ll get a
# SyntaxError . You can’t use a catch-all expression on its own:
# *others = car_ages_descending   # SyntaxError: starred assignment target must be in a list or tuple
# print(others)

# You also can’t use multiple catch-all expressions in a single-level
# unpacking pattern:
# first , *middle, *second_middle, last = [1, 2, 3, 4, 5, 6, 7, 8]    # SyntaxError: two starred expressions in assignment
# print(first, middle, second_middle, last)


# But it is possible to use multiple starred expressions in an unpacking
# assignment statement, as long as they’re catch-alls for different parts
# of the multilevel structure being unpacked. I don’t recommend doing
# the following but
# understanding it should help you develop an intuition for how starred
# expressions can be used in unpacking assignments:
car_inventory = {
    'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
    'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}

((lock1, (best1, *rest1)),
  (lock2, (best2, *rest2))) = car_inventory.items()

print(f'Best at {lock1} is {best1}, {len(rest1)} others')
print(f'Best at {lock2} is {best2}, {len(rest2)} others')


# Starred expressions become list instances in all cases. If there are
# no leftover items from the sequence being unpacked, the catch-all
# part will be an empty list . This is especially useful when you’re pro-
# cessing a sequence that you know in advance has at least N elements:
short_list = [1,2]
first, second, *rest = short_list
print(first, second, rest)


# You can also unpack arbitrary iterators with the unpacking syntax.
# This isn’t worth much with a basic multiple-assignment statement.
# For example, here I unpack the values from iterating over a range
# of length 2. This doesn’t seem useful because it would be easier
# to just assign to a static list that matches the unpacking pattern
# (e.g., [1, 2] ):
it = iter(range(1, 3))
print(it)
first, second = it
print(f'{first} and {second}')

# But with the addition of starred expressions, the value of unpack-
# ing iterators becomes clear. For example, here I have a generator
# that yields the rows of a CSV file containing all car orders from the
# ealership this week:
def generate_csv():
    yield ('Date', 'Make' , 'Model', 'Year', 'Price')

# Processing the results of this generator using indexes and slices is
# fine, but it requires multiple lines and is visually noisy:
all_csv_rows = list(generate_csv())
print(all_csv_rows)
header = all_csv_rows[0]
rows = all_csv_rows[1:]
print('CSV header: ', header)
print('Row count: ', len(rows))

# Unpacking with a starred expression makes it easy to process the first
# row—the header—separately from the rest of the iterator’s contents.
# This is much clearer:
it = generate_csv()
header, *rows = it
print('CSV header: ', header)
print('Row count: ', len(rows))