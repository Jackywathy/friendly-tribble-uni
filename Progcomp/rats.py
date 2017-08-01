
def revFunc(i):
    return int("".join(reversed((str(i)))))

def rev_sort(i, check, count):
    if i > 10**12:
        return []

    # i is int of number,
    rev = revFunc(i)
    # sorts and reerses string
    sort = int("".join(sorted(str(i+rev))))

    if sort in check:
        return check[check.index(sort):]
    else:
        check.append(sort)
        return rev_sort(sort, check, count+1)

dict_array = {}
#
# continas
# (period, smallest_element of cycle) : [number of occurences, (rest of elements)


for i in range(1, 10000):

    check = []
    cycle = tuple(rev_sort(i, check, 1))
    if not cycle:
        continue

    period = len(cycle)
    smallest = min(cycle)

    if (period, smallest) in dict_array:
        dict_array[(period, smallest)][0] += 1
    else:
        # not in dictionary, add new entry
        dict_array[(period, smallest)] = [1, cycle]

for i in sorted(dict_array):
    period, smallest = i
    occurs, rest = dict_array[i]
    print("Period: {}, occurs {} times, cycle: {}".format(period, occurs, " ".join(map(str, rest))))


#print(rev_sort(180, []))

