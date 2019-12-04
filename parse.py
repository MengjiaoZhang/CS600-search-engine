import _pickle as pickle

from goose3 import Goose
import nltk
from nltk import PorterStemmer
from nltk.corpus import stopwords
from trie import Trie


links_file = open('data/links', 'r')
links_file_content = links_file.readlines()
links_id = links_file_content[::3]
links = links_file_content[1::3]
links_title = links_file_content[2::3]

g = Goose({
    'enable_image_fetching': False,
    "use_meta_language": False
})
stopwords_set = set(stopwords.words('english'))
s = PorterStemmer()

trie = Trie()

# For each link, get all words in it;
# For each word w_i in this link, compute the frequency;
# Store the link id and frequency to a list corresponding to w_i.
for id_, link, title in zip(links_id, links, links_title):
    id_ = id_.strip()
    htm_name = "data/html/" + id_ + ".htm"
    htm_file = open(htm_name, 'r', encoding='utf-8')
    htm_content = htm_file.read()
    article = g.extract(raw_html=htm_content)
    # the content of the article in html
    text = article.cleaned_text

    words = nltk.word_tokenize(text)
    # new_word contains all words in text and their counts.
    new_words = dict()
    count_words = 0
    # calculate the count of each word in the text
    for word in words:
        w = s.stem(word).lower()
        if w not in stopwords_set:
            if w in new_words:
                new_words[w] += 1
            else:
                new_words[w] = 1
        count_words += 1
    # insert the word to trie
    for word, count in new_words.items():
        freq = count / count_words
        word_id = trie.search(word)
        # insert a word which is not exist in current trie
        if word_id is None:
            word_id = trie.count_word_in_trie()
            trie.insert(word, word_id)
            # create a new list containing the link id and frequency
            word_list = [[id_, freq]]
            word_list_name = "data/lists/list" + str(word_id)
            word_list_file = open(word_list_name, mode='wb')
            pickle.dump(word_list, word_list_file)
        else:
            word_list_name = "data/lists/list" + str(word_id)
            word_list_file = open(word_list_name, mode='rb')
            word_list = pickle.load(word_list_file)
            word_list_file.close()
            word_list_file = open(word_list_name, mode='wb')
            # add the link id and frequency to the existing list
            word_list.append([id_, freq])
            pickle.dump(word_list, word_list_file)

# save the trie to disk
trie.compress_trie()
trie_name = 'data/trie'
trie_file = open(trie_name, mode='wb')
pickle.dump(trie, trie_file)


# value = trie.compress_search("learn")
# word_list_name = "data/lists/list" + str(value)
# word_list_file = open(word_list_name, mode='rb')
# word_list = pickle.load(word_list_file)
# print(word_list)
