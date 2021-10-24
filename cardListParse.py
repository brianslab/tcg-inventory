import re

def getTcgpCards (order):
    cardNames = []
    cardQtys = []
    with open(order,"r") as f:
        for line in f:
            entries = re.sub('\s+', ' ', line).split(" - ")
            cardNames.append(entries[2])
            cardQtys.append(entries[0][:1])
    # print(cardNames)
    # print(cardQtys)
    f.close()
    return cardNames, cardQtys

def getDecklistCards (list):
    return