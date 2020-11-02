# Generators provide a variety of benefits (see Item 30: “Consider Gen-
# erators Instead of Returning Lists”) and solutions to common prob-
# lems (see Item 31: “Be Defensive When Iterating Over Arguments”).
# Generators are so useful that many programs start to look like layers
# of generators strung together.
# For example, say that I have a graphical program that’s using gener-
# ators to animate the movement of images onscreen. To get the visual
# effect I’m looking for, I need the images to move quickly at first, pause
# temporarily, and then continue moving at a slower pace. Here, I define
# two generators that yield the expected onscreen deltas for each part of
# this animation:


def move(period, speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0


# To create the final animation, I need to combine move and pause
# together to produce a single sequence of onscreen deltas. Here, I do
# this by calling a generator for each step of the animation, iterating
# over each generator in turn, and then yielding the deltas from all of
# them in sequence:

def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta

# Now, I can render those deltas onscreen as they’re produced by the
# single animation generator:

def render(delta):
    print(f'Delta: {delta:.1f}')

def run(fun):
    for delta in fun():
        render(delta)

run(animate)



# The problem with this code is the repetitive nature of the animate
# function. The redundancy of the for statements and yield expres-
# sions for each generator adds noise and reduces readability. This
# example includes only three nested generators and it’s already hurt-
# ing clarity; a complex animation with a dozen phases or more would
# be extremely difficult to follow.
# The solution to this problem is to use the yield from expression.
# This advanced generator feature allows you to yield all values from
# a nested generator before returning control to the parent generator.
# Here, I reimplement the animation function by using yield from :

def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)

print('Use yield from:')
run(animate_composed)



# The result is the same as before, but now the code is clearer and more
# intuitive. yield from essentially causes the Python interpreter to han-
# dle the nested for loop and yield expression boilerplate for you, which
# results in better performance. Here, I verify the speedup by using the
# timeit built-in module to run a micro-benchmark:

import timeit

def child():
    for i in range(1_000_000):
        yield i

def slow():
    for i in child():
        yield i

def fast():
    yield from child()


baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50
)

print(f'Manual nesting {baseline:.2f}s')


comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50
)

print(f'Composed nesting {comparison:.2f}s')

reduction = -(comparison - baseline) / baseline
print(f'{reduction:.1%} less time')

# If you find yourself composing generators, I strongly encourage you to
# use yield from when possible.


# Things to Remember
# ✦
# The yield from expression allows you to compose multiple nested
# generators together into a single combined generator.
# ✦ yield
# from provides better performance than manually iterating
# nested generators and yielding their outputs.