from katas.my_priority_queue import PriorityQueue
from random import shuffle

NUMBERS = [100, 19, 36, 17, 3, 25, 1, 2, 7]
ORDERED = sorted(NUMBERS)[::-1]


def create_queue(xs: [int]) -> PriorityQueue:
    pq = PriorityQueue()
    copied = xs.copy()
    shuffle(copied)
    for x in copied:
        pq.add_item(x=x)
    return pq


def test_peek():
    pq = create_queue(NUMBERS)
    assert pq.peek() == ORDERED[0]
    for x in ORDERED:
        assert pq.remove() == x
