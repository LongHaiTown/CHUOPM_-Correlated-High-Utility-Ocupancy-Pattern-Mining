transactions = [ ('a', 'b', 'c'), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('a', 'b', 'c', 'd'), ]
for trans in transactions :
    for item in trans:
        print(item)
    