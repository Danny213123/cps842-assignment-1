class Document:
    def __init__(self, document_id, title, text, publication_date, authors, n, x):
        self.document_id = document_id
        self.title = title
        self.text = text
        self.publication_date = publication_date
        self.authors = authors
        self.n = n
        self.x = x

    def word_count(self):
        return len(self.text.split())

    def check_text_empty(self):
        return len(self.text.strip()) == 0

    def __str__(self):
        return self.text

    def __repr__(self):
        if not self.check_text_empty():
            return f"Document({self.document_id} | Title: {self.title} | Text: {self.text} | Publication Date: {self.publication_date} | Authors: {self.authors} | N: {self.n} | X: {self.x})"
        return f"Document({self.document_id} | Title: {self.title} | Publication Date: {self.publication_date} | Authors: {self.authors} | N: {self.n} | X: {self.x})"
