class Node:
    def __init__(self, document_id, tf=0):
        self.left = None
        self.right = None
        self.document_id = document_id
        self.tf = tf
        self.positions = []  # position pointer within the text


class PostingsBST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, document_id, position=None):
        """Insert an occurrence for `document_id`; record `position` if given."""
        if self.root is None:
            self.root = Node(document_id, tf=1)
            if position is not None:
                self.root.positions.append(position)
            self.size += 1
            return

        cur = self.root
        while True:

            # left if smaller, right if larger
            if document_id == cur.document_id:
                cur.tf += 1
                if position is not None:
                    cur.positions.append(position)
                return
            elif document_id < cur.document_id:
                if cur.left is None:
                    cur.left = Node(document_id, tf=1)
                    if position is not None:
                        cur.left.positions.append(position)
                    self.size += 1
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(document_id, tf=1)
                    if position is not None:
                        cur.right.positions.append(position)
                    self.size += 1
                    return
                cur = cur.right

    def inorder(self):
        result = []
        stack = []
        cur = self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            result.append((cur.document_id, cur.tf))
            cur = cur.right
        return result

    def inorder_with_positions(self):
        result = []
        stack = []
        cur = self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            # copy positions so callers can't mutate internal state accidentally
            result.append((cur.document_id, cur.tf, list(cur.positions)))
            cur = cur.right
        return result

    def __contains__(self, document_id):
        cur = self.root
        while cur:
            if document_id == cur.document_id:
                return True
            cur = cur.left if document_id < cur.document_id else cur.right
        return False

    def __getitem__(self, document_id):
        cur = self.root
        while cur:
            if document_id == cur.document_id:
                return cur.tf
            cur = cur.left if document_id < cur.document_id else cur.right
        raise KeyError(f"Document ID {document_id} not found in postings list.")

    def grab_positions(self, document_id):
        cur = self.root
        while cur:
            if document_id == cur.document_id:
                return list(cur.positions)  # return a copy
            cur = cur.left if document_id < cur.document_id else cur.right
        raise KeyError(f"Document ID {document_id} not found in postings list.")

    def __len__(self):
        return self.size


class PostingsList:
    def __init__(self):
        self.bst = PostingsBST()

    def insert(self, document_id, position=None):
        self.bst.insert(document_id, position)

    def inorder(self):
        return self.bst.inorder()

    def inorder_with_positions(self):
        return self.bst.inorder_with_positions()

    def __contains__(self, document_id):
        return document_id in self.bst

    def __getitem__(self, document_id):
        return self.bst[document_id]

    def grab_positions(self, document_id):
        return self.bst.grab_positions(document_id)

    def __len__(self):
        return len(self.bst)
