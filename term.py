from postings import PostingsList


class Term:
    def __init__(self, term, frequency=0, postings=None):
        self.term = term
        self.frequency = frequency
        self.postings = postings if postings is not None else PostingsList()

    def add_occurrence(self, document_id, position=None):
        self.frequency += 1
        self.postings.insert(document_id, position)

    def get_occurence(self, document_id):
        self.postings.__getitem__(document_id)

    def grab_frequency(self):
        return self.frequency

    def grab_postings(self):
        return self.postings

    def __str__(self):
        return f"Term({self.term}, Frequency: {self.frequency}, Postings: {self.postings.inorder_with_positions()})"
