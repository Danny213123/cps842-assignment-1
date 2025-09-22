#   You need to write the second program test to test your inverting program. The inputs to the program are the two files generated from the previous program invert.
#   It then keeps asking user to type in a single term. If the term is in one of the documents in the collection, the program should display the document frequency
#   and all the documents which contain this term, for each document, it should display the document ID, the title, the term frequency, all the positions the term occurs
#   in that document, and a summary of the document highlighting the first occurrence of this term with 10 terms in its context. When user types in the term ZZEND,
#   the program will stop (this requirement is valid only when your program doesn't have a graphical interface). Each time, when user types in a valid term, the program
#   should also output the time from getting the user input to outputting the results. Finally, when the program stops, the average value
#   for above-mentioned time should also be displayed.

import argparse
import gzip
import pickle
import sys
import time
from pathlib import Path

from postings import PostingsList
from term import Term

global terms_dict
terms_dict: dict[str, Term] = {}

global index
index: dict[str, int] = {}


def read_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        nargs=2,
        metavar=("DICT", "POSTINGS"),
        required=True,
        help="Dictionary and Postings files",
    )
    args = parser.parse_args()
    dict_path, postings_path = args.input

    # validate paths
    if not dict_path.is_file():
        parser.error(f"Dictionary file {dict_path} does not exist or is not a file.")
    if not postings_path.is_file():
        parser.error(f"Postings file {postings_path} does not exist or is not a file.")

    return dict_path, postings_path


def load_postings(path: Path) -> dict:
    global terms_dict

    with gzip.open(path, "rb") as f:
        snapshot: dict[str, dict] = pickle.load(f)

    terms_dict = {}
    for term, payload in snapshot.items():
        t = Term(term, frequency=0)
        for doc_id, tf, positions in payload["postings"]:
            if positions:
                for p in positions:
                    t.add_occurrence(doc_id, p)
            else:
                for _ in range(tf):
                    t.add_occurrence(doc_id, None)
        terms_dict[term] = t
    return terms_dict

def lookup(user_input: str) -> Term | None:
    global terms_dict
    global index

    start = time.time()

    if user_input in terms_dict:
        term_obj = terms_dict[user_input]
        print(f"Term: {term_obj.__str__()}")
        end = time.time()
        elapsed = end - start
        print(f"Time taken to lookup term '{user_input}': {elapsed:.6f} seconds")
        return term_obj
    else:
        print(f"Term '{user_input}' not found in the index.")
        return None
    
if __name__ == "__main__":
    dict_path, postings_path = read_cli()
    print(f"Dictionary file: {dict_path}")
    print(f"Postings file: {postings_path}")

    terms_dict = load_postings(postings_path)
    print(f"Loaded {len(terms_dict)} terms from postings.")

    for term, term_obj in terms_dict.items():
        print(term_obj)

    while True:
        user_input = input("Enter a term to look up: ")
        if user_input == "ZZEND":
            print("Exiting program.")
            break
        elif user_input != None:
            lookup(user_input)
    # Further processing can be done here, such as loading the dictionary and postings
    # and performing searches or other operations.
