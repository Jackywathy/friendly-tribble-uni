def get_next(letter, list):
    for i, list_l in enumerate(list):
        if list_l == letter:
            return "+" + str(i+1)
    return "0"


def get_iso(word):
    out = []
    for i, letter in enumerate(word):
        # starts at i=0, needs to be i=1
        out.append(get_next(letter, word[i + 1:]))
    return out

DIFF = "{}, {} have different lengths"
ISO = "{}, {} are isomorphs with repetition pattern {}"
NO_ISO = "{}, {} are not isomorphs"

with open("iso.txt") as f:
    f.readline() # get rid of line number
    for line in f:
        line = line.rstrip()
        word1, word2 = line.split()
        if len(word1) != len(word2):
            # not same length
            print(DIFF.format(word1, word2))
        else:
            # see if it is iso
            if get_iso(word2) == get_iso(word1):
                print(ISO.format(word1, word2, " ".join(get_iso(word1))))
            else:
                print(NO_ISO.format(word1, word2))



