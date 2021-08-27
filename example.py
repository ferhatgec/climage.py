data = ''

with open('example.climg', 'r') as file:
    import climage

    for line in file:
        data += line

    x = climage.climage()
    x.parse(data)
    x.generate()
