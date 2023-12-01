import random
from collections import Counter
 
# This function calculates the freq of the (i+1)th
# word in the whole corpus, where i is the index of
# the sentence or the word.
 
def next_word_freq(array, sentence):
     
    sen_len, word_list = len(sentence.split()), []
     
    for i in range(len(array)):
 
        # If the sentence matches the sentence in the range (i, i+x)
        # and the length is less than the length of the corpus, append
        # the word to word_list.
         
        if ' '.join(array[i : i + sen_len]).lower() == sentence.lower():
 
            if i + sen_len < len(array) - 1:
 
                word_list.append(array[i + sen_len])
 
    # Return the count of each word in word_list
     
    return dict(Counter(word_list))
 
# Calculate the CDF of each word in the
# Counter dictionary.
 
def CDF(d):
     
    prob_sum, sum_vals = 0, sum(d.values())
     
    for k, v in d.items():
 
        # Calculate the PMF of each word by dividing
        # the freq. by total of all frequencies then add
        # all the PMFs till ith word which is the CDF of
        # the ith word.
         
        pmf = v / sum_vals
        prob_sum += pmf
        d[k] = prob_sum
 
    # Return cdf dictionary
     
    return d
 
# The main function reads the sentence/word as input
# from user and reads the corpus file. For faster processing,
# we have taken only the first 1000 words.
 
 
def main(sent, x, n):
 
    # I am using this sample text here to illustrate the output.
    # If anyone wants to use a text file, he can use the same. The code
    # to read corpus from file has been commented below.
 
    # corpus = open('a.txt','r').read()
 
    corpus = '''text The chance is unlikely if not done programmatically. 
    However, imagine the game spawning multiple players at a spawn point,
    this would be the exact same location. I'm not quite sure what you 
    mean with spin,     what does the integer reflect? Why is it a 
    mismatch between data and structure? The structure does not
    assume a set amount of objects, it can be anything, that's why new
    nodes are created. It simply makes sure that there are not more than
    X leafs inside 1 node. The random is no option of course.
    My splitting algorithm always created the maximum amount of nodes 
    already, split over the current node. But I guess I have to change
    this behaviour? Actually, all the books have different authors. And
    most have a different location too. There will be some with the same
    location, but different authors, though. I think my library should be
    able to store books with the same position. There are never 
    equally-attractive leaf nodes. If a node is split, all childs will
    reflect a different part of the parent node.'''
     
    l = corpus.split()
 
    # "temp_out" will be used to store each partial sentence
    # which will later be stored into "sent". "out" is used to store
    # the final output.
     
    temp_out = ''
    out = sent + ' '
     
    for i in range(n - x):
 
        # calling the next_word_freq method that returns
        # the frequency of each word next to sent in the
        # whole word corpus.
         
        func_out = next_word_freq(l, sent)
 
        # cdf_dict stores the cdf of each word in the above map
        # that is calculated using method CDF.
         
        cdf_dict = CDF(func_out)
         
        # We use a random number to predict the next word.
        # The word having its CDF greater than or equal to rand
        # and less than or equal to 1.
         
        rand = random.uniform(0, 1)
 
        # If cdf_dict is empty, it means the word.sentence entered by you
        # does not exist in the corpus. Hence, break the loop and just print
        # the word entered by you. To implement this we use try-except block.
        # If an error occurs it implies there aren't enough values to unpack
        # and this can happen only when your input is absent from the corpus.
         
        try: key, val = zip(*cdf_dict.items())
        except: break
 
        # Iterate through the cdf values and find the smallest value
        # greater than or equal to the random number. That value is the
        # cdf of your predicted word. Add the key of the value to the output
        # string and update the "sent" variable as "temp_out".
         
        for j in range(len(val)):
             
            if rand <= val[j]:
                pos = j
                break
                     
        temp_out = key[pos]
        out = out + temp_out + ' '
        sent = temp_out
         
    print(out, end = '\n\n')
 
if __name__ == '__main__':
 
    inp_sent = 'is'
    # The output will have 10 words, including the input sentence/word.
    main(inp_sent, len(inp_sent), 10)
 
# Code contributed by Gagan Talreja.