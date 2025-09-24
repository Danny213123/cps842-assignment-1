# CPS842: Information Retrieval and Web Search

## Inputs

First the invert.py program will gather several inputs from the user when executing the program:
- `--input`: the input file containing the information to be processed.
- `--output`: the output location for the output information
- `--stopwords`: boolean input, whether or not to prune stop words
- `--stopwords_file`: file of common words that will be pruned during the tokenization process
- `--stemming`: boolean input, whether or not to employ PorterStemming algorithm during the tokenization process

### File Input

The program assumes that the input file is organized in a particular way, but can handle missing inputs in the file,

```txt
.I 1
.T
Preliminary Report-International Algebraic Language
.B
CACM December, 1958
.A
Perlis, A. J.
Samelson,K.
.N
CA581203 JB March 22, 1978  8:28 PM
.X
100	5	1
123	5	1
164	5	1
...
```

## Invert.py

In this program, the inverted index will be created, all of the doucments will be processed, with the text being tokenized and sorted depending on documentID, and term strings

### Tokenization

When the user provides the correct arguments and inputs, the program will begin processing the file and create a document object. Information for the document class can be viewed within `document.py`. For each document, the document ID, publication date, text, author(s), and any other information are stored in memory. Once all the document objects are created, the process will begin to tokenize the text of each document. First, the text is split up using nltk's tokenize function and whitespace splitting. In Python, this can be achieved with just a `.split(" ")`. 

After the text has been tokenized, it will then be further normalized by removing punctuation and numerical values, and subsequently stripped of white spaces and converted to lowercase. During the tokenization process, an index dictionary will be created through a straightforward key-value creation process. It will check if a key already exists and increment the frequency value; otherwise, it will create a new key with a frequency of 0. 

The term object is also created, with the document ID being searched, the term frequency being incremented for each occurrence of a term within the document ID, and the position of the term within the document being tracked using a simple position pointer.

### PorterStemming

The stemming algorithm employed in this program is the PorterStemming algorithm which employs some fundamental rules for each term. Stemming algorithm relies on heuristics checks for each term, to remove derivational
affixes

- removal of suffixes and prefixes:
    - `sses` -> `ss`
    - `ies` -> `i`
    - `ss` -> `ss`
    - `s` -> ``

### Index

The index, which is a `term: str -> document frequency: int` mapping, is a hash map with key-value lookups.

### Postings List

The postings list is a little more sophisticated, with a dictionary file in invert.py that maps `term: str -> Term Object`. Inside the Term Object, the term, total document frequency, and the postings list are stored. The postings list is a binary search tree, with each node containing the document ID in which the term appears, the number of times the term appears in the given document, and the position of the term within the document.

### Result

After the invert program has finally run, the index and terms_dict are pickled and will be used in test.py

## Test.py

The Test program will allow users to enter a simple query input of a term, perform a lookup, check if the term exists, and then output the term and its context. The input to test.py will be the two pickle files outputted in the output/ folder.

The given input files are processed, and the data structures are rebuilt from the pickle file. After this, the program will prompt the user for an input term. Given the input term, it checks if it exists; if so, it continues; otherwise, it repeats the input prompt.

Once the term has been retrieved, the user is then prompted again for input, this time for a document ID that contains the term. Once the user provides the document ID, it will return a context of 10 terms, including five terms before and five terms after the first position of the given term.

When the user types in the term ZZEND, the program will stop.

## Running the Program

```shell

>>>  python invert.py --i cacm/cacm.all --o output/output.txt --stopwords --stemming
>>>  python test.py -i output/index.pkl.gz output/postings.pkl.gz

```

## Requirements

```shell

>>>  pip install nltk
```