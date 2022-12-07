# pylint: disable=invalid-name

"""
Search module.
"""

import ast
import csv
import re

text = []
episode_index = []
episode_data = {}

with open("data.csv", encoding="ansi") as f:
    csv_file = csv.DictReader(f)
    line_index = 0
    for line in csv_file:
        script = line["Processed Script"].split()
        text += script
        for _ in range(len(script)):
            episode_index.append(line_index)
        episode_data[line_index] = {"Code": line["Code"], "Title": line["Title"],
                "Description": line["Description"],
                "Characters": ast.literal_eval(line["Characters"])}
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
    """Helper function for BP-DP-Search."""
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
                ranks[episode] -= rank
            else:
                ranks[episode] = -rank
    return ranks, next_input

def bp_dp_search(pattern, word_bound, search_range=range(0, text_length)):
    """Implements BP-DP-Search."""
    pattern, length, previous_input = preprocess(pattern)
    ranks, _ = bp_dp_search_helper(process(pattern, length), (length, word_bound),
            previous_input[2], search_range, previous_input)
    return ranks

def filter_search(pattern, word_bound):
    """Implements Filter Search."""
    ranks = {}
    pattern, pattern_length, initial_input = preprocess(pattern)
    index = process(pattern, pattern_length)
    previous_input = initial_input
    initial_position = pattern_length - word_bound
    end = text_length - initial_position
    i = 0
    while i < end:
        counter = 0
        position = initial_position
        while position > 0:
            if text[i + position - 1] not in index:
                counter += 1
            if counter > word_bound:
                break
            position -= 1
        if position == 0:
            result, previous_input = bp_dp_search_helper(index, (pattern_length, word_bound),
                    (1 << pattern_length) - 1, range(i, i + initial_position),
                    previous_input)
            for k, v in result.items():
                if k in ranks:
                    ranks[k] += v
                else:
                    ranks[k] = v
            i += 1
        else:
            i += position
            previous_input = initial_input
    return ranks


def search(pattern, characters, word_bound, use_filter):
    """Outputs codes, titles, and descriptions of episodes containing a pattern or characters."""
    output = ([], [], [])
    pattern_ranks = {}
    character_ranks = {}
    ranks = []
    no_pattern = pattern == ""
    no_characters = characters == ""
    if not no_pattern:
        if use_filter:
            pattern_ranks = filter_search(pattern, word_bound)
        else:
            pattern_ranks = bp_dp_search(pattern, word_bound)
        if no_characters:
            ranks = [(k, (v, 0)) for k, v in pattern_ranks.items()]
    if not no_characters:
        for k, v in episode_data.items():
            episode_characters = v["Characters"]
            if all(character in episode_characters for character in characters.split(";")):
                character_ranks[k] = len(episode_characters)
        if no_pattern:
            ranks = [(k, (v, 0)) for k, v in character_ranks.items()]
        else:
            for k, v in pattern_ranks.items():
                if k in character_ranks:
                    ranks.append((k, (v, character_ranks[k])))
    ranks.sort(key=lambda rank: rank[1])
    for episode in [episode_data[rank[0]] for rank in ranks]:
        output[0].append(episode["Code"])
        output[1].append(episode["Title"])
        output[2].append(episode["Description"])
    return output