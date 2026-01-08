from Trie import Trie
import itertools

def load_digram(digram_txt):
    """
    Returns digram loaded from the file name `"digram_txt"`
    """
    digram = []
    with open(digram_txt, 'r') as digram_file:
        for line in digram_file:
            row = line.strip().lower()
            if row:
                digram.append(row.split(' '))
    return digram

def get_char_freq(text):
    freq = [0]*26
    for ch in text:
        if 'a' <= ch <= 'z':
            freq[ord(ch)-ord('a')] += 1
    return freq

def word_possible(word_freq, digram_freq):
    for w_f, d_f in zip(word_freq, digram_freq):
        if w_f > d_f:
            return False
    return True

def get_word_list(full_word_list_txt, digram):
    """
    Returns a list of all words that can possibly be created 
    on the basis of the frequency count of the `digram`
    """
    # flatten digram to a single string to count frequencies
    digram_chars = []
    for row in digram:
        for cell in row:
            digram_chars.append(cell)
    digram_str = ''.join(digram_chars)

    digram_freq = get_char_freq(digram_str)

    word_list = []
    try:
        with open(full_word_list_txt, 'r') as word_list_file:
            for line in word_list_file:
                word = line.strip().lower()
                if not word:
                    continue
                if word_possible(get_char_freq(word), digram_freq):
                    word_list.append(word)
    except FileNotFoundError:
        print(f"Warning: {full_word_list_txt} not found.")
        return []

    return word_list

def dfs(row, col, node, path, visited, solutions, digram, rows, cols):
    # Check if current path is a valid word
    if node.word_finished:
        solutions.add(path)

    visited[row][col] = True

    # Iterate over all 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            nr, nc = row + dr, col + dc

            # Check bounds and if visited
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                char_seq = digram[nr][nc]

                # Check if this move is valid in the Trie
                next_node = node
                valid_move = True
                for char in char_seq:
                    if char in next_node.children:
                        next_node = next_node.children[char]
                    else:
                        valid_move = False
                        break

                if valid_move:
                    dfs(nr, nc, next_node, path + char_seq, visited, solutions, digram, rows, cols)

    visited[row][col] = False

def begin_dfs(digram, trie):
    """
    Returns a set of all words that can be created using the `digram`, 
    using `trie` as the dictionary of all plausible words
    """
    solutions = set()
    if not digram:
        return solutions

    rows = len(digram)
    cols = len(digram[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            char_seq = digram[r][c]

            # Navigate trie for the starting cell
            node = trie.root
            valid_start = True
            for char in char_seq:
                if char in node.children:
                    node = node.children[char]
                else:
                    valid_start = False
                    break

            if valid_start:
                dfs(r, c, node, char_seq, visited, solutions, digram, rows, cols)

    return solutions

def run_program():
    digram_file_name = "array.txt"
    full_word_list = "all_words.txt"

    trie = Trie()
    digram = load_digram(digram_file_name)
    print(f"Digram loaded: {digram}")

    word_list = get_word_list(full_word_list, digram)
    print(f"Words filtered: {len(word_list)}")

    trie.add_word_list(word_list)

    solution_list = list(begin_dfs(digram, trie))
    solution_list = sorted(solution_list, key=len, reverse=True)

    print(f"Found {len(solution_list)} words.")

    with open('solution_words.txt', 'w') as file:
        for word in solution_list:
            file.write(word+"\n")

if __name__ == "__main__":
    run_program()
