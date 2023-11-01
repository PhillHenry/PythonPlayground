from __future__ import annotations
import abc


class Node(abc.ABC):

    @staticmethod
    def root() -> Node:
        node = Node()
        return node

    def __init__(self):
        self.children = {}
        self.value = None

    def get_child(self, key) -> Node:
        child = self.children.get(key)
        if child is None:
            child = Node()
            self.children[key] = child
        return child

    def add(self, parent: Node, xs, value=None):
        current = self._traverse(parent, xs)
        current.value = value

    @staticmethod
    def _traverse(parent: Node, xs) -> Node:
        current = parent
        for i, x in enumerate(xs):
            current = current.get_child(xs[i])
        return current

    def value_for(self, parent: Node, xs):
        node = self._traverse(parent, xs)
        return node.value
