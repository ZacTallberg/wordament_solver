class TrieNode:
    def __init__(self, char: str):
        self.char = char
        self.children = {}
        self.word_finished = False
        # how many words exist with this prefix
        self.counter = 1

    def __str__(self):
        return self.char

class Trie:
    """
    Trie data structure for storing strings. Provides fast lookups
    Has the following interfaces:
    `add_word` : to add a word to the words
    `add_word_list` : to add a list of words
    `find_prefix` : to look up for a word
    """
    def __init__(self):
        self.root = TrieNode('')

    def add_word(self, word: str):
        """
        Add a word in the `Trie`, starting from `Trie.root`
        """
        node = self.root
        for char in word:
            if char in node.children:
                child = node.children[char]
                child.counter += 1
                node = child
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # adding done, now mark the node as word end
        node.word_finished = True

    def add_word_list(self, word_list):
        for word in word_list:
            self.add_word(word)

    def find_prefix(self, prefix: str):
        """
        Check if the prefix exists in the trie.
        Returns (exists, counter, word_finished)
        """
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return False, 0, False

        return True, node.counter, node.word_finished
