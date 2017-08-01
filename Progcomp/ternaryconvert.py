word = "#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklm#nopqrstuvwxyz0123456789 !\"$%&'()*,-.:?@"
out = []
exit = False
lockout = [["**"] for x in range(4)]
print(lockout)
with open("input.txt") as f:
	f.readline()
	for row in f:
		break_now = False

		if exit:
			break
		row = row.rstrip()
		# split row into 4 sub rows
		# 0,1,2,3
		rows = [row[i*2:i*2+2] for i in range(4)]
		rows = reversed(rows)

		# comleted base 3 string
		int_str = ""
		if rows == lockout:
			print("LOCKOUT!")
			exit = True
			break

		for i in rows:
			if i == "X.":
				int_str += "0"
			elif i == ".X":
				int_str += "1"
			elif i == "..":
				int_str += "2"
			else:
				out.append("#")
				break_now = True
				break

		if break_now:
			break

		out.append((word[int(int_str, 3)]))
print("".join(out))
