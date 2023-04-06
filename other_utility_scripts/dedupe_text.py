from itertools import groupby

all_words = []
all_words_unique = []

## Deduplicate two sorted textfiles of single-line-words

with open('dedupe.txt', 'r') as file_c, open('output.txt', 'w') as outfile, open('all_unique_words.txt', 'w') as uniquefile:
    for line, group in groupby(file_c):
        
        
        # group is an iterator of all the lines in c that are equal
        # the same value is already in line, so all we need to do is
        # *count* how many such lines there are:
        
        count = sum(1 for line in group)  # get an efficient count
        if count == 1:
            # line is unique, write it out
            all_words.append(line)
        all_words_unique.append(line)
    
    all_words = sorted(all_words)
    all_words_unique = sorted(all_words_unique)

    for word in all_words:
        outfile.write(word)

    for word in all_words_unique:
        uniquefile.write(word)