from Trie import Trie
import itertools
import random

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

def sort_human_like(solutions):
    """
    Sorts the solution list to mimic human intuition:
    - Starts with short words.
    - Follows "trains of thought" (extensions, shared prefixes).
    - Switches topics when no obvious connection is found.
    """
    solutions = list(solutions)
    if not solutions:
        return []

    # Start with shortest words as they are easiest to spot
    solutions.sort(key=len)

    result = []
    pool = set(solutions)

    # Pick the first seed (shortest word)
    if not pool:
        return []

    current = solutions[0]
    result.append(current)
    pool.remove(current)

    while pool:
        best_candidate = None
        best_score = -float('inf')

        # We sample the pool if it's very large, but for standard games (<1000 words), this is fine.
        candidates = list(pool)

        for cand in candidates:
            score = 0

            # 1. Extension / Substring (Strongest connection)
            if cand.startswith(current):
                score += 100
                # Penalty for length diff (prefer "runs" over "runnings" next)
                score -= (len(cand) - len(current)) * 2
            elif current.startswith(cand):
                score += 80
                score -= (len(current) - len(cand)) * 2

            # 2. Shared Prefix (The "cluster" effect)
            elif len(cand) >= 3 and len(current) >= 3 and cand[:3] == current[:3]:
                score += 50
                score -= abs(len(cand) - len(current))
            elif len(cand) >= 2 and len(current) >= 2 and cand[:2] == current[:2]:
                score += 20
                score -= abs(len(cand) - len(current))

            # 3. Length Similarity (weakest)
            else:
                score -= abs(len(cand) - len(current))

            # Add noise for "intuition"
            score += random.uniform(0, 5)

            if score > best_score:
                best_score = score
                best_candidate = cand

        # Threshold to switch topic
        if best_score < 15:
            # No strong relation found. Pick a new "easy" word (shortest).
            best_candidate = min(pool, key=len)

        current = best_candidate
        result.append(current)
        pool.remove(current)

    return result

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

    # Sort by human-like intuition
    solution_list = sort_human_like(solution_list)

    print(f"Found {len(solution_list)} words.")

    with open('solution_words.txt', 'w') as file:
        for word in solution_list:
            file.write(word+"\n")

if __name__ == "__main__":
    run_program()
