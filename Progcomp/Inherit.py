people = {}
parents = {}
id = 0
with open("inherit.txt") as f:
    start = None
    # remove lnu
    f.readline()
    for line in f:
        line = line.rstrip()
        dead = False
        data = line.split()
        current, children = data[0][:-1], data[1:]
        # remove colon
        if current.endswith("x"):
            dead = True
            current = current[:-1]
        elif current.endswith("*"):
            start = current[:-1]
            current = current[:-1]

        people[current] = [children, dead]
        for i in children:
            parents[i] = current
'''
for i in people:
    print(i, people[i])'''
import collections
females = collections.defaultdict(list)
males = []

seen = set()



def bfs(current, children, dead, moveup, layer):
    seen.add(current)
    if current.startswith("M"):
        if not dead:
            males.append(current)
    else:
        females[layer].append(current)

    for child in children:
        if child in seen:
            continue
        if child.startswith("M"):
            bfs(child, people[child][0], people[child][1], False, layer+1)
        else:
            bfs(child, [], True, False, layer+1)

    if moveup:
        if current != "M0":
            bfs(parents[current], people[parents[current]][0], people[parents[current]][1], True, layer+1)


bfs(start, people[start][0], people[start][1], True, 0)

print(" ".join(males), end=" ")
for i in sorted(females):
    print("+".join(females[i]), end= " ")

