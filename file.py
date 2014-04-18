import fileinput

for line in fileinput.input("test.cnf", inplace=1):
	if fileinput.isfirstline():
		print "add new line here"
	print line.rstrip()
