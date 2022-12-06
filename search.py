# pylint: disable=invalid-name

"""
Search module.
"""

import csv
import re

text = []
episode_index = []
episode = {}

with open("data.csv", encoding="ansi") as f:
    csv_file = csv.DictReader(f)
    line_index = 0
    for line in csv_file:
        script = line["Processed Script"].split()
        text += script
        for i in range(len(script)):
            episode_index.append(line_index)
        episode[line_index] = [line["Code"], line["Title"], line["Description"]]
        line_index += 1

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
                break
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
    ranks = {}
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
            rank += 1
            episode = episode_index[j]
            found = False
            for key in ranks:
                if key == episode:
                    ranks[episode].append((j, rank))
                    found = True
                    break
            if not found:
                ranks[episode] = [(j, rank)]
    return ranks

def bp_dp_search(pattern, word_bound, start=0, end=text_length):
    pattern, length = preprocess(pattern)
    return bp_dp_search_helper(process(pattern, length), length, word_bound, start, end)

# TODO: Optimize
def filter_search(pattern, word_bound):
    ranks = {}
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
            search = bp_dp_search_helper(index, pattern_length, word_bound, i,
                    i + pattern_length - word_bound)
            for result in search:
                found = False
                for rank in ranks:
                    if rank == result:
                        ranks[result] += search[result]
                        found = True
                        break
                if not found:
                    ranks[result] = search[result]
            i += 1
        else:
            i += position
    return ranks

def key(item_set):
    result = 0
    for j, rank in item_set:
        result -= rank
    return result

def search(pattern, characters, word_bound, use_filter):
    ranks = {}
    if use_filter:
        ranks = filter_search(pattern, word_bound)
    else:
        ranks = bp_dp_search(pattern, word_bound)
    return ranks
    #return [episode[k] for k, v in sorted(ranks.items(), key=lambda item: key(set(item[1])))]
