import unidecode

## attempt to replace any foreign characters with their english counterpart (aka c cedille --> c)

all_words = []

with open('foreign_too.txt', 'r') as foreign_words:
    for line in foreign_words:
        decoded = unidecode.unidecode(line)
        all_words.append(decoded)

with open('decoded.txt', 'w') as output_foreign:
    for word in all_words:
        output_foreign.write(word)
