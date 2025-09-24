class Document:
    """
    Class representing a document with metadata
    """

    def __init__(self, document_id, title, text, publication_date, authors, n, x):
        """
        Initialize a Document object
        """
        self.document_id = document_id
        self.title = title
        self.text = text
        self.publication_date = publication_date
        self.authors = authors
        self.n = n
        self.x = x

    def word_count(self):
        """
        Get the word count of the document text
        :return: Word count
        """
        return len(self.text.split())

    def check_text_empty(self):
        """
        Check if the document text is empty
        :return: True if text is empty, False otherwise
        """
        return len(self.text.strip()) == 0

    def __str__(self):
        if not self.check_text_empty():
            return f"Document ID: {self.document_id}, Title: {self.title}, Text: {self.text}, Publication Date: {self.publication_date}, Authors: {self.authors}, N: {self.n}, X: {self.x}"
        return self.text

    def __repr__(self):
        if not self.check_text_empty():
            return f"Document({self.document_id} | Title: {self.title} | Text: {self.text} | Publication Date: {self.publication_date} | Authors: {self.authors} | N: {self.n} | X: {self.x})"
        return f"Document({self.document_id} | Title: {self.title} | Publication Date: {self.publication_date} | Authors: {self.authors} | N: {self.n} | X: {self.x})"
