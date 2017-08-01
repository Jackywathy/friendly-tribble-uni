nums = [1,2,3,-100,3]
all_max = 0
current_max = 0

for i in nums:
	current_max = max(current_max+i, 0)
	all_max = max(current_max, all_max)

print(all_max)