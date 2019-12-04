class Trie:
    """
    Use dict to store the node (key, value)
    a key of the dict: the key of the child node
    value of the dict: child of node
    """
    def __init__(self):
        self.root = {"*":"*"}
        self.length = 0

    def insert(self, word, index):
        """
        Inserts a word into the standard trie.
        Input: a word and the index of the word
        """
        current_node = self.root
        for w in word:
            # if the character w is not in the current node
            # add w to the current as a child
            if w not in current_node:
                current_node[w] = {}
            # move to the child of current node
            current_node = current_node[w]
        # word ends here
        # use "*" as the key of the external node
        # use word index as the value
        current_node["*"] = index
        self.length += 1

    def search(self, word):
        """
        Search if the word is in the standard trie, return its index if it exists or None.
        Input: a word
        Output: Index of word if it exists; None if it does not exist.
        """
        current_node = self.root
        for w in word:
            if w not in current_node:
                return None
            current_node = current_node[w]
        # if we find an external node, the word exists.
        if "*" in current_node:
            return current_node["*"]
        else:
            return None

    def compress_trie(self):
        """
        compress a standard trie to a compressed trie
        """
        for w, child in self.root.items():
            self._compress(self.root, child, w)

    def _compress(self, pnode, node, w):
        """
        recursively compress from an internal node to an external node
        Input: pnode: parent node;
               node: current node;
               w: the key of the node to compress (stored in pnode)
        """

        # root node
        if node == "*":
            return
        # node only has one child
        if len(node) == 1:
            key, value = list(node.items())[0]
            # external node is not compressed
            if key == "*":
                return
            # compress internal node with its child
            new_key = w + key
            del pnode[w]
            pnode[new_key] = value
            del node
            # continue to compress
            self._compress(pnode, value, new_key)
        # compress the children of a node which has two or more children
        elif len(node) > 1:
            for w, child in node.items():
                if w != "*":
                    self._compress(node, child, w)

    def count_word_in_trie(self):
        return self.length

    def compress_search(self, word):
        """
        Search if the word is in the compressed trie, return its index if it exists or None.
        Input: a word
        Output: Index of word if it exists; None if it does not exist.
        """
        node = self.root
        prefix = ''
        ending = -1
        for i, w in enumerate(word):
            prefix += w
            if prefix in node:
                node = node[prefix]
                prefix = ''
                ending = i
        if ending == len(word)-1:
            if "*" in node:
                return node["*"]
        return None