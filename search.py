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
    """Outputs a pattern's list of words in lowercase, its length, and initial search values."""
    pattern = re.sub(r"[\s]+", " ", re.sub(r"[^\w\s]", "", pattern)).lower().strip().split()
    pattern_length = len(pattern)
    return pattern, pattern_length, (0, 0, (1 << pattern_length) - 1, 0, 0, pattern_length)

def process(pattern, pattern_length):
    """Outputs an index that stores the match vector for each word in a pattern."""
    index = {}
    for i in range(pattern_length):
        word = pattern[i]
        ith_bit = 1 << i
        if word in index:
            index[word] |= ith_bit
        else:
            index[word] = ith_bit
    return index

def get_mask(index, word):
    """Outputs the match vector for a word."""
    if word in index:
        return index[word]
    return 0

def bp_dp_search_helper(index, parameters, not_zero, search_range, previous_input):
    ranks = {}
    pattern_length, word_bound = parameters
    HP, HN, VP, VN, D0, score = previous_input
    next_input = None
    saved = False
    for j in search_range:
        PM = get_mask(index, text[j]) # preprocessed mask
        D0 = ((((PM & VP) + VP) ^ VP) | PM | VN) & not_zero
        HP = (VN | ~(D0 | VP)) & not_zero
        HN = VP & D0
        VP = ((HN << 1) | ~(D0 | (HP << 1))) & not_zero
        VN = (HP << 1) & D0
        score += ((HP >> pattern_length - 1) & 1) - ((HN >> pattern_length - 1) & 1)
        if not saved:
            next_input = (HP, HN, VP, VN, D0, score)
            saved = True
        rank = word_bound - score + 1
        if rank > 0:
            episode = episode_index[j]
            if episode in ranks:
                ranks[episode].append((j, rank))
            else:
                ranks[episode] = [(j, rank)]
    return ranks, next_input

def bp_dp_search(pattern, word_bound, search_range=range(0, text_length)):
    pattern, length, previous_input = preprocess(pattern)
    ranks, _ = bp_dp_search_helper(process(pattern, length), (length, word_bound),
            previous_input[2], search_range, previous_input)
    return ranks

# TODO: Optimize
def filter_search(pattern, word_bound):
    ranks = {}
    pattern, pattern_length, initial_input = preprocess(pattern)
    index = process(pattern, pattern_length)
    previous_input = initial_input
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
            search, previous_input = bp_dp_search_helper(index, (pattern_length, word_bound),
                    (1 << pattern_length) - 1, range(i, i + pattern_length - word_bound),
                    previous_input)
            for result in search:
                if result in ranks:
                    ranks[result] += search[result]
                else:
                    ranks[result] = search[result]
            i += 1
        else:
            i += position
            previous_input = initial_input
    return ranks

def sum_ranks(ranks):
    result = 0
    for j, rank in ranks:
        result -= rank
    return result

def search(pattern, characters, word_bound, use_filter):
    ranks = {}
    if use_filter:
        ranks = filter_search(pattern, word_bound)
    else:
        ranks = bp_dp_search(pattern, word_bound)
    codes = []
    titles = []
    descriptions = []
    for ep in [episode[k] for k, v in sorted(ranks.items(), key=lambda item: sum_ranks(item[1]))]:
        codes.append(ep[0])
        titles.append(ep[1])
        descriptions.append(ep[2])
    return codes, titles, descriptions
    