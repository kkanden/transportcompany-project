class Stack:
    def __init__(self):
        self.items = []

    # O(1)
    def is_empty(self):
        return self.items == []

    # O(1)
    def push(self, item):
        self.items.append(item)

    # O(1)
    def pop(self):
        return self.items.pop()

    # O(1)
    def peek(self):
        return self.items[-1]

    # O(1)
    def size(self):
        return len(self.items)

    def __iter__(self):
        while not self.is_empty():
            yield self.pop()


if __name__ == "__main__":
    s = Stack() # s -> []
    print(s.is_empty())
    s.push(4) # s -> [4]
    s.push("pies") # s -> [4, 'pies']
    print(s.peek())
    s.push(True) # s -> [4, 'pies', True]
    print(s.size())
    print(s.is_empty())
    s.push(8.4) # s -> [4, 'pies', True, 8.4]
    print(s.pop()) # s -> [4, 'pies', True]
    print(s.pop()) # s -> [4, 'pies']
    print(s.size())
