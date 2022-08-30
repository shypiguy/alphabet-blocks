# alphabet-blocks
tool to generate and evaluate 2-sided alphabet blocks for their vocabulary size
## History
In the summer of 2022, my family made a group craft project in the anticipation of the imminent birth of my niece. Their plan was to create a set of 40 alphabet blocks, each one decorated by hand in decoupage and bearing a letter of the alphabet on each of two opposing sides. Before the completion of the project, I was asked "what's the best way to arrange the letters of the alphabet on these blocks so they can be used to spell the most words?" I was intrigued by the puzzle.
To answer that question, I wrote this python project to both generate a set of blocks, and to score them for how many English words they could spell when using only one side of each of the available blocks.
## Structure and use
### Contents
* **test_blocks.py** - the scoring script, it takes a single argument, the path to a json dictionary file listing the blocks to be scored. the script compares the blocks to a comprehensive English dictianry file (described below in *dependencies*), and returns:
  * the percentage of English words which could not be spelled with the blocks
  * the count of English words which could not be spelled with the blocks
  * The longest English word which can be spelled with the blocks
  * The shortest English word which *can't* be spelled with the blocks
* **blocks.py** - the script I used to generate the set of blocks we used for my niece's craft project
* **ellie.blocks.dic** - the json dictionary filke describing the set of blocks that I have found to spell the most English words - the set was created by starting with the assumption that there wopuld be at lease two of each letter of the alphabet, and the algorithm penalized the generation of blocks with the same letter on its oppostie sides
* **simple_test.blocks.dic** - a json dioctionary file describing a set of blocks created by starting with the assumption that there wopuld be at lease one of each letter of the alphabet, and the algorithm *did not penalize* the generation of blocks with the same letter on its oppostie sides
* **better_test.blocks.dic** - a json dioctionary file describing a set of blocks created by starting with the assumption that there wopuld be at two of each letter of the alphabet, and the algorithm *did not penalize* the generation of blocks with the same letter on its oppostie sides
* **matching_letters.blocks.dic** - a json dioctionary file describing a set of blocks created with the rule that the letters on opposing sides of each block *must match*
### Dictionary format
The json dictionary entries each describe a block/letter configuration, and enumerate how many of the blocks are in the set. For example:
```
"cu": 2
```
indicates there are two blocks in the set with the letters "C and "U" on their opposing sides
## Dependencies
Both code modules reference the **words_dictionary.json* file from the excellent project [dwl/english-words](https://github.com/dwyl/english-words)
