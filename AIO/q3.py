from collections import deque

with open('chimin.txt') as f:
    x = f.readlines()
    w1 = x[1].rstrip()
    w2 = x[2].rstrip()
    out = x[3].rstrip()

cuts = 0
c1 = False
c2 = False
nope = False

cry = False

for i in range(len(w1)):
    l1, l2, curr = w1[i], w2[i], out[i]

    used = False
    # check if any continue the cut
    if c1:
        if l1 == curr:
            used = True
        else:
            c1 = False
    if c2:
        if l2 == curr:
            used = True
        else:
            c2 = False

    if not used:
        # check if it actuall is legit
        if l1 == curr and l2 == curr:
            cuts += 1
            c1, c2 = True, True
        elif l1 == curr:
            c1 = True
            cuts += 1
        elif l2 == curr:
            c2 = True
            cuts += 1
        else:
            nope= True
            break

with open("chimout.txt", 'w') as f:
    f.write("SUCCESS\n" if not nope else "PLAN FOILED\n")
    if not nope:
        f.write(str(cuts-1))