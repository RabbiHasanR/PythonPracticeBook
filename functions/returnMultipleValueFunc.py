# One effect of the unpacking syntax (see Item 6: “Prefer Multiple
# Assignment Unpacking Over Indexing”) is that it allows Python func-
# tions to seemingly return more than one value. For example, say
# that I’m trying to determine various statistics for a population of
# alligators. Given a list of lengths, I need to calculate the minimum
# and maximum lengths in the population. Here, I do this in a single
# function that appears to return two values:

def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]
minimum, maximum = get_stats(lengths)                   # Two returns values
print(f'Min: {minimum}, Max: {maximum}')


# The way this works is that multiple values are returned together in a
# two-item tuple . The calling code then unpacks the returned tuple by
# assigning two variables. Here, I use an even simpler example to show
# how an unpacking statement and multiple-return function work the
# same way:

first, seconde = 1, 2
assert first == 1
assert seconde == 2

def my_function():
    return 1, 2

first, seconde = my_function()
assert first == 1
assert seconde == 2


# Multiple return values can also be received by starred expressions for
# catch-all unpacking (see Item 13: “Prefer Catch-All Unpacking Over
# Slicing”). For example, say I need another function that calculates
# how big each alligator is relative to the population average. This func-
# tion returns a list of ratios, but I can receive the longest and shortest
# items individually by using a starred expression for the middle por-
# tion of the list :

def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled

longest, *middle, shortest = get_avg_ratio(lengths)

print(f'Longest: {longest:>4.0%}')
print(f'Shortest: {shortest:>4.0%}')
print(f'Middle: {middle}')


# Now, imagine that the program’s requirements change, and I need to
# also determine the average length, median length, and total popula-
# tion size of the alligators. I can do this by expanding the get_stats
# function to also calculate these statistics and return them in the
# result tuple that is unpacked by the caller

def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]
    return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats(lengths)
print(f'Min: {minimum}, Max: {maximum}')
print(f'Average: {average}, Median: {median}, Count: {count}')