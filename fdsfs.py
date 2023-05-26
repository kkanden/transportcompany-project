name = 'Alice'


def example():
    # 👇️ mark global
    global name

    print(name)

    name = 'Bob'


example()  # 👉️ 'Alice'
example()  # 👉️ 'Bob'