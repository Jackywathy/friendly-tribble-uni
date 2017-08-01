num_problem = int(input())
alpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
for i in range(num_problem):
    line = list(input())
    num_mem = int(line[0])
    original = alpha[num_mem:]
    print(original)