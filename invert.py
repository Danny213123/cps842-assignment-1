import argparse
import sys
from pathlib import Path
from typing import List, Optional

import nltk
from nltk.tokenize import word_tokenize

from document import Document

nltk.download("punkt_tab")

global index
index: dict[str, int]


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


def tokenize(text: str) -> List[str]:
    return word_tokenize(text)


def normalize(text: str) -> str:
    # Lowercase and strip whitespace
    return text.strip().lower()


def grab_terms(doc: Document) -> dict[str, List[str]]:
    # grab terms from a specific document
    terms = []
    for term in tokenize(doc.text):
        terms.append(normalize(term))
    return terms


def grab_terms_from_all_documents(Documents: List[Document]) -> None | List[str]:
    global index
    index = {}

    with open(f"debug/docs_terms_debug.txt", "w") as f:
        for doc in Documents:
            doc_terms = grab_terms(doc)

            f.write(
                f"Document ID: {doc.document_id}\n"
                f"Title: {doc.title}\n"
                f"Text: {doc.text}\n"
                f"Terms: {sorted(doc_terms)}\n\n"
            )

            # count terms in global index
            for term in doc_terms:
                if term == "grammatical":
                    print(f"Found 'grammatical' in Document ID {doc.document_id}")
                if term in index:
                    index[term] += 1
                else:
                    index[term] = 1
    return list(index.keys())


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
    args = read_cli()

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


if __name__ == "__main__":
    main()
