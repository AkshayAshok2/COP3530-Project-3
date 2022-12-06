# pylint: disable=invalid-name

"""
Search module.
"""

import re

text = []

with open("family_guy.txt", encoding="ansi") as f:
    text = f.read().split()

text_length = len(text)

def preprocess(pattern):
    """Outputs a pattern's list of words in lowercase and its length."""
    pattern = re.sub(r"[\s]+", " ", re.sub(r"[^\w\s]", "", pattern)).lower().strip().split()
    return pattern, len(pattern)


def process(pattern, pattern_length):
    """Outputs an index that stores the match vector for each word in a pattern."""
    index = {}
    for i in range(pattern_length):
        word = pattern[i]
        ith_bit = 1 << i
        found = False
        for key in index:
            if key == word:
                index[word] |= ith_bit
                found = True
        if not found:
            index[word] = ith_bit
    return index

def get_mask(index, word):
    """Outputs the match vector for a word."""
    for key in index:
        if key == word:
            return index[word]
    return 0

def bp_dp_search_helper(index, pattern_length, word_bound, start, end):
    not_zero = (1 << pattern_length) - 1
    HP = 0 # horizontal positive
    HN = 0 # horizontal negative
    VN = 0 # vertical negative
    D0 = 0 # diagonal zero
    VP = not_zero # vertical positive
    score = pattern_length
    for j in range(start, end):
        PM = get_mask(index, text[j]) # preprocessed mask
        D0 = ((((PM & VP) + VP) ^ VP) | PM | VN) & not_zero
        HP = (VN | ~(D0 | VP)) & not_zero
        HN = VP & D0
        VP = ((HN << 1) | ~(D0 | (HP << 1))) & not_zero
        VN = (HP << 1) & D0
        score += ((HP >> pattern_length - 1) & 1) - ((HN >> pattern_length - 1) & 1)
        rank = word_bound - score
        if rank >= 0:
            print(j, score)

def bp_dp_search(pattern, word_bound, start=0, end=text_length):
    pattern, pattern_length = preprocess(pattern)
    bp_dp_search_helper(process(pattern, pattern_length), pattern_length, word_bound, start, end)

# TODO: Optimize
def filter_search(pattern, word_bound):
    pattern, pattern_length = preprocess(pattern)
    index = process(pattern, pattern_length)
    i = 0
    while i < text_length - pattern_length + word_bound:
        counter = 0
        position = pattern_length - word_bound
        while position > 0:
            if get_mask(index, text[i + position - 1]) == 0:
                counter += 1
            if counter > word_bound:
                break
            position -= 1
        if position == 0:
            bp_dp_search_helper(index, pattern_length, word_bound, i,
                    i + pattern_length + word_bound)
            i += 1
        else:
            i += position
