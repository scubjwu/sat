from os.path import exists
import fileinput

N = 0
cnf_file = "queens.cnf"
clauses = 0
split_pattern = ", "

def check_file_exist(name):
	if exists(cnf_file):
		print "file %s exists...Are you sure to replace [Y/N]" % (cnf_file)
		tmp = raw_input()
		if tmp == 'Y' or tmp == 'y':
			return 0
		elif tmp == 'N' or tmp == 'n':
			return 1
		else:
			print "Enter Y/N please"
			return -1
	else:
		return 0

def get_file_name(prompt):
	print "The cnf file name for %s problem:" % (prompt)
	tmp = raw_input()
	global cnf_file
	if tmp != "":
		cnf_file = tmp
	
	while True:
		tmp = check_file_exist(cnf_file)
		if tmp != -1:
			break

	return tmp	# 0: get file name ok; 1: try to get the file name again

def get_N_queens_value():
	print "The value of N for N queens problem:"
	global N
	N = int(raw_input())
	if N < 4:
		print "The value of N should be larger than 4"
		return 1
	return 0

def queens_cnf_input():
	while get_N_queens_value():
		pass
	
	while get_file_name("N queens"):
		pass

	print "CNF file '%s' for %d-queens problem" % (cnf_file, N)

def cnf_create(func):
	return func()

def implication2clause(fd, array, m):
	global clauses

	for i in range(0, m-1):
		for j in range(i+1, m):
			fd.write(str(-array[i]) + ', ')
			fd.write(str(-array[j]) + ', 0\n')
			clauses += 1

def EqualOne_CNF_write(fd, array, num):
	global clauses

	fd.write(repr(array).strip('[]') + ', 0\n')
	clauses += 1
	implication2clause(fd, array, num)

def LessEqualOne_CNF_write(fd, array, num):
	implication2clause(fd, array, num)

def insert_cnf_head(var):
	for line in fileinput.input(cnf_file, inplace=1):
		if fileinput.isfirstline():
			print "p" + split_pattern + " cnf" + split_pattern \
				+ str(var) + split_pattern + str(clauses)
			
		print line.rstrip()

def N_queens_cnf_create():
	cnf_fd = file(cnf_file, 'w')
	cnf_item1 = [0]*N
	cnf_item2 = [0]*N

	for row in range(0, N):
		i = 0
		for col in range(0, N):
			cnf_item1[i] = row*N + col + 1
			cnf_item2[i] = col*N + row + 1
			i += 1

		EqualOne_CNF_write(cnf_fd, cnf_item1, N)
		EqualOne_CNF_write(cnf_fd, cnf_item2, N)

	
	for row in range(0, N-1):
		i = 0
		for col in range(0, N-row):
			cnf_item1[i] = col*N + (row + col) + 1
			cnf_item2[i] = col*N + (N - 1 - row - col) + 1
			i += 1

		LessEqualOne_CNF_write(cnf_fd, cnf_item1, N-row)
		LessEqualOne_CNF_write(cnf_fd, cnf_item2, N-row)

	for row in range(1, N-1):
		i = 0
		for col in range(0, N-row):
			cnf_item1[i] = (col + row)*N + col + 1
			cnf_item2[i] = (col + row)*N + (N - 1 - col) + 1
			i += 1

		LessEqualOne_CNF_write(cnf_fd, cnf_item1, N-row)
		LessEqualOne_CNF_write(cnf_fd, cnf_item2, N-row)

	cnf_fd.close()

	insert_cnf_head(N*N)
	print "done..."  
	return 0

def test():
	queens_cnf_input()
	cnf_create(N_queens_cnf_create)

if __name__ == "__main__":
	test()
