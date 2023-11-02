from __future__ import annotations
import abc


class PriorityQueue(abc.ABC):

    def __init__(self):
        self.backing = []

    def add_item(self, x: int):
        self.backing.append(x)
        pos = len(self.backing) - 1

        not_found = pos > 0
        while not_found:
            pivot = (pos - 1) // 2
            tmp = self.backing[pivot]
            if tmp < x:
                self.backing[pivot] = x
                self.backing[pos] = tmp
                pos = pivot
            else:
                not_found = False
            not_found = not_found and pivot > 0

    def peek(self) -> int:
        return self.backing[0]

    def remove(self) -> int:
        tmp = self.backing
        self.backing = []
        for x in tmp[1:]:
            self.add_item(x)
        return tmp[0]

