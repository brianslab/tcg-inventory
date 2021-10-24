import re

def getTcgpCards (order):
    cardNames = []
    cardQtys = []
    with open(order,"r") as f:
        for line in f:
            entries = re.sub('\s+', ' ', line).split(" - ")
            cardNames.append(entries[2])
            cardQtys.append(entries[0][:1])

    f.close()
    return cardNames, cardQtys

def getDecklistCards (decklist):
    cardNames = []
    cardQtys = []
    with open(decklist, "r") as f:
        for line in f:
            cardNames.append(line.rstrip('\n')[2:])
            cardQtys.append(line[0])

    f.close()
    return cardNames, cardQtys