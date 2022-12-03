class TrieNode:
    """
     Trie data structure node.
    """
    def __init__(self):
        self.children = {}
        self.last = False


class Trie:
    """
    Trie data structure implementation.
    """
    def __init__(self):
        self.root = TrieNode()

        """
        Inserts a the given key to this trie structure.
        Returns list of nodes representing the path of the word in this trie. 
        """
    def insert(self, key) -> list[TrieNode]:
        path: list = list()
        node = self.root

        for a in key:
            if not node.children.get(a):
                node.children[a] = TrieNode()

            node = node.children[a]
            path.append(node)

        node.last = True
        return path

    def get_node(self, key) -> TrieNode:
        """
        Return the last node in the path that matches the given key;
        If no match is found root node is returned.
        """
        node = self.root

        for a in key:
            if not node.children.get(a):
                return node

            node = node.children[a]

        return node
