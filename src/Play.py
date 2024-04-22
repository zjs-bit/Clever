import random
from dataclasses import dataclass

mydict = {1: 5}
myotherdict = {2: 3}

mydict.update(myotherdict)


@dataclass
class Myint:
    val: int = 5


def myfuncttest(*myint: Myint):
    start = 0
    for a in myint:
        start += a.val

    return start


b1 = Myint()
b2 = Myint(3)
l = [b1, b2]

print(myfuncttest(*l))
