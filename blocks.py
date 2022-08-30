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

# inport dependencies
import json

# reading the word data from the file
with open('../english-words/words_dictionary.json') as f:
    data = f.read()   
# reconstructing the word data as the original dictionary
o_dict = json.loads(data)

# initiate the dictionary of nonce2s
n_dict = {}

#iterate the 2 letter combinations, set counts to 0
for f in range(97, 123):
    for s in range(f, 123):
        if f == s :
            n_dict[chr(f)+chr(s)] = 20000
        else:
            n_dict[chr(f)+chr(s)] = 0

# initiate the dictionary of duplicates
d_dict = {}

# initiate the dictionary of uses
u_dict = {}

# step through original dictionary
for key in o_dict:
    word_letters_used = {}
    # add word letters to the local dictionary of word letters used
    for letter in key:
        word_letters_used[letter] = word_letters_used.get(letter,  0) + 1
    # increment the count of duplicate letter usage
    for letter in word_letters_used:
        if letter != '-':
            u_dict[letter] = u_dict.get(letter, 0) + 1
        if word_letters_used[letter] >  1:
            d_dict[letter+str(word_letters_used[letter])] = d_dict.get(letter+str(word_letters_used[letter]), 0) +1
    # increment the count of 2 letter combinations used
    for first_letter in word_letters_used:
        for second_letter in word_letters_used:
            if first_letter == second_letter:
                if word_letters_used[first_letter] > 1:
                   n_dict[first_letter+second_letter] = n_dict[first_letter+second_letter] +1
            if second_letter > first_letter:
                try:
                    n_dict[first_letter+second_letter] = n_dict[first_letter+second_letter] +1
                except:
                    pass
            

value_key_pairs = ((value, key) for (key,value) in d_dict.items())
sorted_incidence_of_repeated_letters = sorted(value_key_pairs, reverse=True)

value_key_pairs = ((value, key) for (key,value) in n_dict.items())
sorted_incidence_of_two_letter_combos = sorted(value_key_pairs)

# initiate the dictionary of block sides
block_sides = {}

# add the base alphabet to the block sides
for letter in range(97, 123):
    block_sides[chr(letter)] = 2
block_sides_count = 52

# add the most popular multiples to block sides until there are 80
for duplicate_letter in sorted_incidence_of_repeated_letters:
    if block_sides_count < 80:
        letter_number = duplicate_letter[1]
        letter = letter_number[:1]
        block_sides[letter] = block_sides[letter] + 1
        block_sides_count = block_sides_count + 1

value_key_pairs = ((value, key) for (key,value) in u_dict.items())
sorted_block_sides = sorted(value_key_pairs,  reverse = True)


# initiate the list of blocks
blocks = []

# step through the most popular block sides to create blocks
for side_letter_entry in sorted_block_sides:
    side_letter = side_letter_entry[1]
    while block_sides[side_letter] > 0:
        for letter_pair in sorted_incidence_of_two_letter_combos:
            first_letter = letter_pair[1][:1]
            second_letter = letter_pair[1][1:2]
            if side_letter == first_letter or side_letter == second_letter:
                if (first_letter != second_letter and block_sides[first_letter] >0 and block_sides[second_letter] > 0) \
                or (first_letter == second_letter and block_sides[first_letter] > 1) : 
                    blocks.append ([first_letter,  second_letter])
                    block_sides[first_letter] = block_sides[first_letter] - 1
                    block_sides[second_letter] = block_sides[second_letter] - 1


# create a dictionary of the block set
block_dic = {}

# populate the block dictionary
for block in blocks:
    final_block = block[0]+block[1]
    block_dic[final_block] = block_dic.get(final_block, 0) + 1

print(json.dumps(block_dic))
  
#print("Data type after reconstruction : ", type(o_dict))
#print(js)
