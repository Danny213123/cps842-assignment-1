import argparse
import sys
from pathlib import Path
from typing import List, Optional

import nltk
from nltk.tokenize import word_tokenize

from document import Document
from term import Term

nltk.download("punkt_tab")

global index
index: dict[str, int]

global terms_dict
terms_dict: dict[str, Term] = {}


def read_documents(file_path: Path) -> List[Document]:

    if not file_path.exists():
        print(f"Error: {file_path} does not exist.", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Reading document(s) from {file_path}")

    # declare current document state
    document_id: Optional[int] = None
    pointer: Optional[str] = None  # one of {"T","W","B","A","N","X"} or None

    title_parts: List[str] = []
    text_parts: List[str] = []
    date_parts: List[str] = []
    authors: List[str] = []
    n_parts: List[str] = []
    x_parts: List[str] = []

    documents: List[Document] = []

    def flush_current():
        nonlocal document_id, title_parts, text_parts, date_parts, authors, n_parts, x_parts
        if document_id is None:
            return
        doc = Document(
            document_id,
            " ".join(title_parts).strip(),
            " ".join(text_parts).strip(),
            " ".join(date_parts).strip(),
            [a.strip() for a in authors if a.strip()],
            n_parts[:],
            x_parts[:],
        )
        documents.append(doc)

        # reset
        document_id = None
        title_parts.clear()
        text_parts.clear()
        date_parts.clear()
        authors.clear()
        n_parts.clear()
        x_parts.clear()

    with open(file_path, "r", encoding="utf-8") as file:
        for raw in file:
            line = raw.rstrip("\n").replace("\t", " ")

            if not line:
                if pointer == "T":
                    title_parts.append("")
                elif pointer == "W":
                    text_parts.append("")
                elif pointer == "B":
                    date_parts.append("")
                elif pointer == "A":
                    authors.append("")
                elif pointer == "N":
                    n_parts.append("")
                elif pointer == "X":
                    x_parts.append("")
                continue

            if line.startswith(".I"):
                flush_current()
                parts = line.split()
                if len(parts) < 2 or not parts[1].isdigit():
                    print(f"[ERROR]: Invalid Document ID line: {line}", file=sys.stderr)
                    sys.exit(1)
                document_id = int(parts[1])
                pointer = None
                continue

            if line in (".T", ".W", ".B", ".A", ".N", ".X"):
                pointer = line[1]
                continue

            if pointer == "T":
                title_parts.append(line)
            elif pointer == "W":
                text_parts.append(line)
            elif pointer == "B":
                date_parts.append(line)
            elif pointer == "A":
                authors.append(line)
            elif pointer == "N":
                n_parts.append(line)
            elif pointer == "X":
                x_parts.append(line)
            else:
                pass

    if document_id is not None:
        flush_current()
    else:
        if not documents:
            print(f"[ERROR]: No documents found in {file_path}", file=sys.stderr)
            sys.exit(1)

    return documents


def write_documents(file_path: Path, documents: List[Document]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(doc.__repr__() + "\n")


def write_terms(file_path: Path, terms: List[str]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        for term in terms:
            f.write(term + "\n")


def write_text(file_path: Path, text: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


def write_index(file_path: Path, index: dict[str, int]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        for term, count in index.items():
            f.write(f"{term}: {count}\n")


def write_postings_list(file_path: Path, term: str, postings_list: List[int]) -> None:

    # make sure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Postings list for term '{term}':\n")
        for doc_id in postings_list:
            f.write(f"{doc_id}\n")


def tokenize(text: str) -> List[str]:
    return word_tokenize(text)


def normalize(text: str) -> str:
    # Remove punctuation
    text = "".join(char for char in text if char.isalnum() or char.isspace())

    # only keep non-numeric characters
    text = "".join(char for char in text if not char.isdigit())

    # check for empty string
    if not text.strip():
        return ""

    # Lowercase and strip whitespace
    return text.strip().lower()


def grab_terms(doc: Document) -> dict[str, List[str]]:
    # grab terms from a specific document
    terms = []
    for term in tokenize(doc.text):
        terms.append(normalize(term))
    #   for term in tokenize(doc.title):
    #       terms.append(normalize(term))
    return terms


def grab_terms_from_all_documents(Documents: List[Document]) -> None | List[str]:
    global index, terms_dict
    index = {}
    terms_dict = {}

    debug_path = Path("debug/docs_terms_debug.txt")
    debug_path.parent.mkdir(parents=True, exist_ok=True)

    with debug_path.open("w", encoding="utf-8") as f:
        for doc in Documents:
            doc_terms = grab_terms(doc)

            f.write(
                f"Document ID: {doc.document_id}\n"
                f"Title: {doc.title}\n"
                f"Text: {doc.text}\n"
                f"Terms: {sorted(doc_terms)}\n\n"
            )

            position_pointer = 0

            # count terms in global index
            for term in doc_terms:
                position_pointer += 1
                # check if term_obj already exists
                term_obj = terms_dict.get(term)
                if term_obj is None:
                    term_obj = Term(term)
                else:
                    pass
                if term == "grammatical":
                    print(
                        f"Found 'grammatical' in Document ID {doc.document_id} at position {position_pointer}"
                    )
                if term in index:
                    index[term] += 1
                    term_obj.add_occurrence(doc.document_id, position_pointer)
                else:
                    index[term] = 1
                    term_obj.add_occurrence(doc.document_id, position_pointer)
                terms_dict[term] = term_obj
    return list(index.keys())


def grab_postings_list(term: Term) -> List[int]:
    postings = term.grab_postings()
    return [doc_id for doc_id, tf in postings.inorder()]


def indexer(terms: List[str], docs: List[Document]) -> dict[str, int]:
    global index

    return index


def read_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cli",
        description="CPS842: Information Retrieval and Web Search - Assignment 1",
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to cacm.all file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to output file (all Document objects, one per line)",
    )
    parser.add_argument(
        "--stopwords",
        action="store_true",
        help="Remove stopwords (flag only; not applied in this minimal parser)",
    )
    return parser.parse_args()


def main():
    global index, terms_dict

    args = read_cli()

    # make sure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    docs = read_documents(args.input)

    write_documents(args.output, docs)
    print(f"\nParsed {len(docs)} documents -> {args.output}")

    terms = grab_terms_from_all_documents(docs)
    print(f"Extracted {len(terms)} unique terms.")

    index = indexer(terms, docs)
    print(f"Created index with {len(index)} unique terms.")
    index_output_path = args.output.parent / "index.txt"
    write_index(index_output_path, index)

    terms_output_path = args.output.parent / "terms.txt"
    write_terms(terms_output_path, sorted(terms))

    text_output_path = args.output.parent / "all_text.txt"
    all_text = "\n".join(doc.text for doc in docs)
    write_text(text_output_path, all_text)

    # print postings list for a specific term
    specific_term = terms_dict.get("grammatical")
    if specific_term is None:
        print("Term 'grammatical' not found in terms dictionary.")
        return
    postings_list = grab_postings_list(specific_term)
    print(f"Postings list for term '{specific_term}': {postings_list}")
    postings_output_path = args.output.parent / f"postings_grammatical.txt"
    write_postings_list(postings_output_path, specific_term, postings_list)


if __name__ == "__main__":
    main()
