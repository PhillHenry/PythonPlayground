from katas.my_trie import Node

KEY_TO_VAL = {"A": 15, "to": 7, "tea": 3, "ted": 4, "ten": 12, "i": 11, "in": 5,
                            "inn": 9}


def test_get_child_when_none():
    root = Node.root()
    child = root.get_child("x")
    assert child is not None
    assert child.children == {}


def test_add_nodes():
    root = create_root()
    for key, val in KEY_TO_VAL.items():
        assert root.value_for(root, key) == val


def create_root():
    # see https://en.wikipedia.org/wiki/Trie
    root = Node.root()
    for key, val in KEY_TO_VAL.items():
        root.add(root, key, val)
    return root


def test_number_of_nodes():
    root = create_root()

    def count_recursively(node: Node, count: int) -> int:
        children = node.children
        count += len(children)
        for child in children.values():
            count = count_recursively(child, count)
        return count

    assert count_recursively(root, 1) == 11
