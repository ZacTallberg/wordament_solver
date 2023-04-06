import nltk

## get a list of *most* of the recognizable english words

from nltk.corpus import words
word_list = words.words()
# prints 236736
file = open('nltk_words.txt', 'w')
for word in word_list:
    file.write(word+"\n")
file.close()