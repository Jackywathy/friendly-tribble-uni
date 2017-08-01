import time

with open("nias.txt") as f:
	f.readline()
	for line in f:
		line = line.rstrip()
		dist, ascent = map(float, line.split())
		print("Distance:{:5}km ascent:{:5}m  Naismith time:  {:5}  adjusted time:{:5}".format(dist, ascent, 0 , 0))
