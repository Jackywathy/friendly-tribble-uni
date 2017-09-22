from queue import PriorityQueue
class Point(object):
    def __init__(self, x, y, facing, dir, steps=1, before=None, ):
        self.x = x
        self.y = y
        self.steps = steps
        self.facing = facing
        self.before = before
        self.dir = dir

    def __lt__(self, other):
        return self.steps < other.steps
    def __gt__(self, other):
        return self.steps > other.steps
    def __str__(self):
        return "{{{}, {}), s:{}, f:{}, d:{}}}".format(self.x,self.y,self.steps, self.facing, self.dir)
    def __repr__(self):
        return str(self)
    def equal(self, other):
        return other.x == self.x and self.y == other.y
    def cord(self):
        return self.x, self.y

def get_points(x, y, direction):
    if direction == 'u':
        return [Point(x-1, y, 'l',"L"),Point (x+1, y, 'r', "R")]
    elif direction == 'd':
        return [Point(x-1, y, 'l', "R"), Point(x+1, y, 'r', "L")]
    elif direction == 'l':
        return [Point(x, y+1, 'u', "R"),Point (x, y-1, 'd', "L")]
    elif direction == 'r':
        return [Point(x, y+1, 'u', "L"), Point(x, y-1, 'd', "R")]





pq = PriorityQueue()
seen = set()
pq.put(Point(0,0, 'u', None))
seen.add((0,0))
with open('snakein.txt') as f:
    x,y = map(int, f.readline().split())
    end = Point(x, y, 'u', None)
before = {}


while pq:
    curr= pq.get_nowait()
    #print("got value:", curr)
    if end.equal(curr):
        #print(curr.steps)
        break

    before[curr] = curr.before


    z = get_points(curr.x, curr.y, curr.facing)

    for p in z:
        cord = (p.x, p.y)
        if cord not in seen:
            p.steps = curr.steps + 1
            p.before = curr
            seen.add(cord)
            pq.put(p)
            #print("added {}".format(p))
            #time.sleep(0.5)


out = []
while curr:
    out.append(curr)
    curr = curr.before
with open('snakeout.txt','w') as f:
    f.write("".join(i.dir for i in reversed(out) if i.dir is not None))