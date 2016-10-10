import random as _random
import string as _string


# generating word
def _gen_word(length):
    'This hidden function generate and return random word'
    return ''.join((
        _random.choice(
            _random.choice((
                _string.ascii_letters,
                _string.digits)))
        for i in range(length)))


# generating more
def generate(count=1, length=10):
    'This function return random word(s)'
    assert count >= 1, 'count must be 1 or greater'
    assert length >= 1, 'length must be 1 or greater'
    result = (
        _gen_word(length)
        if count == 1
        else [_gen_word(length) for i in range(count)])
    return result

gen = generate
