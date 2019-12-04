import _pickle as pickle
import nltk
from nltk import PorterStemmer

trie_name = 'data/trie'
trie_file = open(trie_name, mode='rb')
trie = pickle.load(trie_file)
s = PorterStemmer()

# Links file containing all links' ids, article titles and their links
# The format of this link file is as follows:
# Link id
# Title
# url
# ...
links_file = open('data/links', 'r')
links_file_content = links_file.readlines()
links_id = links_file_content[::3]
links = links_file_content[1::3]
links_title = links_file_content[2::3]

while True:
    print("Please input any word or words(split with a space) and Enter; input exit() to exit.")
    input_words = input().strip()
    words = input_words.lower().split(' ')
    # searched links set contains the intersection of occurrence lists of each input word
    searched_links_set = set()
    # key of searched links table: link id
    # value of searched links table: the overall frequency of input words
    searched_links_table = dict()
    for word in words:
        if word == "":
            continue
        if word == 'exit()':
            break
        word_stem = s.stem(word)
        word_id = trie.compress_search(word_stem)
        if word_id is None:
            print("Your search \"", input_words,"\" did not match any documents")
            break
        word_list_filename = "data/lists/list" + str(word_id)
        word_list_file = open(word_list_filename, mode='rb')
        word_list = pickle.load(word_list_file)
        # all links containing current word
        word_list_set = set()
        # the frequency of the current word in each link
        word_list_dict = dict()

        for link_id, word_freq in word_list:
            link_id = int(link_id)
            word_list_set.add(link_id)
            word_list_dict[link_id] = word_freq

        # for the first word
        if len(searched_links_set)==0:
            searched_links_set = word_list_set
            searched_links_table = word_list_dict
        # for the remaining words
        else:
            # intersection
            searched_links_set = searched_links_set.intersection(word_list_set)
            # no intersection
            if len(searched_links_set)==0:
                print("Your search \"", input_words,"\" did not match any documents")
                break
            for link_id in searched_links_set:
                searched_links_table[link_id] += word_list_dict[link_id]
    # finally the intersection is not empty
    else:
        final_list = []
        for link_id in searched_links_set:
            final_list.append([link_id, searched_links_table[link_id]])
        final_list_sorted = sorted(final_list, key=lambda x: -x[1])
        for link_id, _ in final_list_sorted:
            link_id = int(link_id)
            link = links[link_id]
            link_title = links_title[link_id]
            print(link_title, link)

    # print(word_list)
    # print(word_list_sorted)