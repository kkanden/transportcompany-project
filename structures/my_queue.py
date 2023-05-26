class Queue:
    # Θ(1)
    def __init__(self):
        self.items = []

    # Θ(1)
    def is_empty(self):
        return self.items == []

    # Θ(n)
    def enqueue(self, item):
        self.items.insert(0, item)

    # Θ(1)
    def dequeue(self):
        return self.items.pop()

    def front(self):
        return self.items[-1]

    # Θ(1)
    def size(self):
        return len(self.items)


