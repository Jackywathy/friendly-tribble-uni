with open("cocoin.txt") as f:
    z = f.readlines()
    p1 = list(map(int, z[0].rstrip().split()))
    p2 = list(map(int, z[1].rstrip().split()))

# x1, x2, distance
if p1[0] != 0:
    am = p1[0]
    p1[0] -= am
    p2[0] -= am

if p1[1] != 0:
    am = p1[1]
    p1[1] -= am
    p2[1] -= am

#print(p1, p2)

z = p1[2] - p2[2] + p2[0]**2 + p2[1]**2
# D - E + x^2 + y^2

b = 2*z * p2[1]
a = 4*(p2[1]**2) + 4*(p2[0]**2)
c = z*z- 4*p1[2]*p1[2]*p2[0]*p2[0]

#print(a,b,c)


with open("cocoout.txt", 'w') as f:
    if p2[2] 
        f.write('yes')
    else:
        f.write('no')
