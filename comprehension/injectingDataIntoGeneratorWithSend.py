# yield expressions provide generator functions with a simple way to
# produce an iterable series of output values (see Item 30: “Consider
# Generators Instead of Returning Lists”). However, this channel
# appears to be unidirectional: There’s no immediately obvious way to
# simultaneously stream data in and out of a generator as it runs. Hav-
# ing such bidirectional communication could be valuable for a variety
# of use cases.
# For example, say that I’m writing a program to transmit signals using
# a software-defined radio. Here, I use a function to generate an approx-
# imation of a sine wave with a given number of points:

import math

def wave(amplitude, steps):
    setp_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * setp_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output

def transmit(output):
    if output is None:
        print(f'Output is none')
    else:
        print(f'Output: {output:>5.1f}')

def run(it):
    for output in it:
        transmit(output)

run(wave(3.0, 8))
