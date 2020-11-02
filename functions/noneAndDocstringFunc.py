# Sometimes you need to use a non-static type as a keyword argument’s
# default value. For example, say I want to print logging messages that
# are marked with the time of the logged event. In the default case,
# I want the message to include the time when the function was
# called. I might try the following approach, assuming that the default
# arguments are reevaluated each time the function is called:

from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

log('Hi there')
sleep(0.1)
log('Hello again')


# This doesn’t work as expected. The timestamps are the same because
# datetime.now is executed only a single time: when the function is
# defined. A default argument value is evaluated only once per module
# load, which usually happens when a program starts up. After the
# module containing this code is loaded, the datetime.now() default
# argument will never be evaluated again.
# The convention for achieving the desired result in Python is to provide
# a default value of None and to document the actual behavior in the
# docstring (see Item 84: “Write Docstrings for Every Function, Class,
# and Module” for background). When your code sees the argument
# value None , you allocate the default value accordingly:

def log(message, when=None):
    """Log a message with a timestamp
    Args:
        message: Message to print.
        when: datetime when the message is occured.
            Defaults to the present time
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

# Now the timestamps will be different:

log('Hi there')
sleep(0.1)
log('Hello again')


# Using None for default argument values is especially important when
# the arguments are mutable. For example, say that I want to load a
# value encoded as JSON data; if decoding the data fails, I want an
# empty dictionary to be returned by default:
import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

# The problem here is the same as in the datetime.now example above.
# The dictionary specified for default will be shared by all calls to
# decode because default argument values are evaluated only once (at
# module load time). This can cause extremely surprising behavior:

foo = decode('bad data')
print(foo)
foo['stuff'] = 5
print(foo)
bar = decode('also bad')
print(bar)
bar['meep'] = 1
print(bar)
print(f'Foo: {foo}')
print(f'Bar: {bar}')

# You might expect two different dictionaries, each with a single key
# and value. But modifying one seems to also modify the other. The cul-
# prit is that foo and bar are both equal to the default parameter. They
# are the same dictionary object:

assert foo is bar

# The fix is to set the keyword argument default value to None and then
# document the behavior in the function’s docstring:

def decode(data, default=None):
    """Load JSON data from a string.
    Args:
        data: JSON data to decode.
        default: alue to return if decoding fails.
            Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default

# Now, running the same test code as before produces the expected
# result:

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad data')
bar ['meep'] = 1
print(f'Foo: {foo}')
print(f'Bar: {bar}')

assert foo is not bar


# This approach also works with type annotations (see Item 90: “Con-
# sider Static Analysis via typing to Obviate Bugs”). Here, the when
# argument is marked as having an Optional value that is a datetime .
# Thus, the only two valid choices for when are None or a datetime object:

from typing import Optional

def log_typed(message: str,
              when: Optional[datetime]=None) -> None:
    """Log a message with a timestamp.
        Args:
            message: Message to print.
            when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')


# Things to Remember
# ✦ A default argument value is evaluated only once: during function
# definition at module load time. This can cause odd behaviors for
# dynamic values (like {} , [] , or datetime.now() ).
# ✦ Use None as the default value for any keyword argument that has a
# dynamic value. Document the actual default behavior in the func-
# tion’s docstring.
# ✦ Using None to represent keyword argument default values also
# works correctly with type annotations.