import os

import argparse

from functools import wraps

from markov.models import Model


def exitcode(func):
    """Wrapper for logging any catched exception."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            return os.EX_TEMPFAIL
        except Exception as e:
            print("Error: {0}".format(e))
            raise
            return os.EX_SOFTWARE
        else:
            return os.EX_OK
    return wrapper


@exitcode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Book in 'txt' format")
    parser.add_argument("--order", default=2, type=int)
    args = parser.parse_args()

    m = Model(args.order)

    def _process(s, d):
        return "%".join(filter(lambda x: len(x) > 10, s.split(d)))

    with open(args.file, "r") as f:
        s = f.read()

    for d in ["\r\n", "...", "…", ".", "!", "?", "«", "»", "%"]:
        s = _process(s, d)

    for c in s.split("%"):
        words = c.split()
        if len(words) > 10:
            m.process(words)

    result = s[0]
    while result in s:
        result = m.generate_sentence()
    print(result)
