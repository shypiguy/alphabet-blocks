#!/usr/bin/env python3

#The MIT License (MIT)

#Copyright (c) 2022 Bill Jones

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE. 


import json
import argparse
import sys

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()
    
# reading the word data from the file
with open('../english-words/words_dictionary.json') as f:
    data = f.read()   
# reconstructing the word data as the original dictionary
o_dict = json.loads(data)

# initiate the collection of blocks as a dictionary

parser = argparse.ArgumentParser()
parser.add_argument("input_file",  help="the python dictionary file of the blocks to test")
args=parser.parse_args()

# reading the block data from the file
with open(args.input_file) as f:
    data = f.read()   
# reconstructing the word data as the original dictionary
blocks = json.loads(data)

# initiate the rejected words list
rejects = []

# initiate longest word that can be spelled, shortest that can't
longest_possible = ''
shortest_impossible = 'abcdefghijklmnopqrstuvwxyz'

# step through original dictionary
for key in progressBar(o_dict, prefix = 'Progress:', suffix = 'Complete', length = 50):
#for key in o_dict:
    word_letters_used = {}
    letter_count = 0
    # add word letters to the local dictionary of word letters used
    for letter in key:
        word_letters_used[letter] = word_letters_used.get(letter,  0) + 1
        letter_count = letter_count + 1
    # make a copy of blocks
    word_blocks = blocks.copy()
    # use non-conflicting blocks first
    for block in word_blocks:
        
        first_letter = block[:1]
        second_letter = block[1:2]
        for block_copy in range(word_blocks[block]):
            first_matched = 0
            second_matched = 0
        
            #identify if either letter on the block makes a match
            for letter in word_letters_used:
                if word_letters_used[letter] > 0:
                    if letter == first_letter:
                        first_matched = first_matched + 1
                    if letter == second_letter:
                        second_matched = second_matched + 1
            # use the block if it matched only one side
            if (first_matched > 0 and second_matched == 0) or (first_matched == 0 and second_matched > 0):
                for letter in word_letters_used:
                    if word_letters_used[letter] > 0 and (letter == first_letter or letter == second_letter):
                        word_letters_used[letter] = word_letters_used[letter] - 1
                        word_blocks[block] = word_blocks[block] -1 
                        letter_count = letter_count -1
    
    
    # use remaining blocks
    for block in word_blocks:
        if word_blocks[block]  > 0:
            first_letter = block[:1]
            second_letter = block[1:2]
            for block_copy in range(word_blocks[block]):
                first_matched = 0
                second_matched = 0
                #identify if either letter on the block makes a match
                for letter in word_letters_used:
                    if word_letters_used[letter] > 0:
                        if letter == first_letter:
                            first_matched = first_matched + 1
                        if letter == second_letter:
                            second_matched = second_matched + 1
                # use the block if either side matched
                if first_matched + second_matched > 0:
                    match_eliminated = 0
                    for letter in word_letters_used:
                        if match_eliminated == 0 and word_letters_used [letter] > 0:
                            if letter == first_letter or letter == second_letter:
                                word_letters_used[letter] = word_letters_used[letter] - 1
                                match_eliminated = 1
                                letter_count = letter_count -1
    # record the word if the letter count is still > 0
    if letter_count > 0 :
        rejects.append(key)
        if len(key) < len(shortest_impossible):
            shortest_impossible = key
    else:
        #update the longest possible word if this one is longer
        if len(key) > len(longest_possible):
            longest_possible = key
                
#rejects.sort()
print('Percentage of unspellable words:')
print(format(float(len(rejects))/float(len(o_dict)), '.4%'))
print('Total count of unspellable words:')
print(len(rejects))
#print(rejects)
print('Longest spellable word:')
print(longest_possible)
print('Shortest unspellable word:')
print(shortest_impossible)
