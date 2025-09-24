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
    """
    Read command line arguments
    """
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


def load_index(path: Path) -> dict:
    """
    Load index from the pickle gzip file
    :param path: Path to the gzip file
    :return: Dictionary of terms and their frequencies
    """
    global index

    with gzip.open(path, "rb") as f:
        index = pickle.load(f)
    return index


def load_postings(path: Path) -> dict:
    """
    Load postings from the pickle gzip file
    :param path: Path to the gzip file
    :return: Dictionary of Term objects
    """
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
    """
    Look up a term in the index and return its Term object if found
    :param user_input: Term to look up
    :return: Term object if found, None otherwise
    """
    global terms_dict
    global index

    start = time.time()

    # check if term is in index
    if user_input in terms_dict:
        term_obj = terms_dict[user_input]
        print(f"Term: {term_obj.__str__()}")
        end = time.time()
        duration = end - start
        print(f"Time taken to lookup term '{user_input}': {duration:.6f} seconds")
        return term_obj
    else:
        print(f"Term '{user_input}' not found in the index.")
        return None


def get_common_occurrences(
    document_id: int, positions: list[int], n: int
) -> list[dict]:
    """
    Look up terms that have the same document ID and within n/2 positions before and after the given position

    :param document_id: Document ID to look up
    :param positions: List of positions where the term occurs in the document
    :param n: Number of terms to retrieve around the position
    :return: List of terms that occur in the same document within the specified range
    """
    global terms_dict

    common_terms = []

    # find all terms that have the same document ID
    for term, term_obj in terms_dict.items():
        node_document = (
            term_obj.postings.__getitem__(document_id)
            if document_id in term_obj.postings
            else None
        )
        if node_document:
            common_terms.append(term)

    # sort terms by position in the document
    common_terms = sorted(
        common_terms,
        key=lambda term: (
            terms_dict[term].postings.grab_positions(document_id)[0]
            if terms_dict[term].postings.grab_positions(document_id)
            else float("inf")
        ),
    )

    # start position is the maximum between 0 and the first position - n, which ensures no out of bounds issue
    # end position is the minimum between the length and current position + n,
    # for the same reason
    print(f"Common terms in document {document_id}: {common_terms}")
    start_pos = max(0, positions[0] - n)
    end_pos = min(positions[0] + n, len(common_terms))
    for term in common_terms[start_pos:end_pos]:
        print(f"Term: {term.__str__()}")

    return common_terms


def main():
    """
    You need to write the second program test to test your inverting program. The inputs to the program are the two files generated from the previous program invert.
    It then keeps asking user to type in a single term. If the term is in one of the documents in the collection, the program should display the document frequency
    and all the documents which contain this term, for each document, it should display the document ID, the title, the term frequency, all the positions the term occurs
    in that document, and a summary of the document highlighting the first occurrence of this term with 10 terms in its context. When user types in the term ZZEND,
    the program will stop (this requirement is valid only when your program doesn't have a graphical interface). Each time, when user types in a valid term, the program
    should also output the time from getting the user input to outputting the results. Finally, when the program stops, the average value
    for above-mentioned time should also be displayed.
    """

    dict_path, postings_path = read_cli()
    print(f"Dictionary file: {dict_path}")
    print(f"Postings file: {postings_path}")

    start = time.time()

    terms_dict = load_postings(postings_path)
    print(f"Loaded {len(terms_dict)} terms from postings.")

    #   for term, term_obj in terms_dict.items():
    #       print(term_obj)

    end = time.time()
    duration = end - start

    print(f"Time taken to load postings: '{duration:.6f}' seconds")

    start = time.time()

    index = load_index(dict_path)
    print(f"Loaded {len(index)} terms from dictionary.")

    end = time.time()
    duration = end - start

    print(f"Time taken to load dictionary: '{duration:.6f}' seconds")

    while True:
        user_input = input("Enter a term to look up: ")

        # exit condition
        if user_input == "ZZEND":
            print("Exiting program.")
            break

        # if user input is not empty, look up term
        elif user_input is not None:
            user_term = lookup(user_input)
            try:
                if user_term is not None:
                    user_input = input(
                        "Enter a specific document ID to look up the location of this term: "
                    )
                    if user_input is not None and user_term is not None:
                        try:
                            retrieve_start = time.time()
                            try:
                                user_term_posting = user_term.get_occurrence(
                                    int(user_input)
                                )
                            except TypeError:
                                user_term_posting = None
                            except KeyError:
                                user_term_posting = None
                            if user_term_posting is None:
                                print(
                                    f"Document ID '{user_input}' not found for term '{user_input}'."
                                )
                            else:
                                print(user_term_posting)
                                get_common_occurrences(
                                    int(user_input), user_term_posting["positions"], 5
                                )
                            retrieve_end = time.time()
                            retrieve_duration = retrieve_end - retrieve_start
                            print(
                                f"Time taken to retrieve postings for document ID '{user_input}': {retrieve_duration:.6f} seconds"
                            )
                        except TypeError:
                            print("Invalid Input")
            except EOFError:
                print("No input received. Exiting.")
                break
            except ValueError:
                print("Invalid Input")
                continue


if __name__ == "__main__":
    main()
