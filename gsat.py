import random

MAX_FLIPS = 0
MAX_TRIES = 1000

split_pattern=' '

def random_T_assign(num):
	tmp_L = {}
	for i in xrange(1, num+1):
		tmp_L[i] = random.choice([False, True])

	return tmp_L

def test_sat(T_assign, fd):
	fd.seek(0)
	fd.readline()
	res = True

	#start to real test
	while True:
		line = fd.readline()
		if line == "" or res == False:
			break

		line_list = line.split(split_pattern)
		i = 0
		c_res = False
		while True:
			if c_res or line_list[i] == "" or i == line_list.__len__() - 1:
				break

			key = int(line_list[i])
			if key < 0:
				c_res = c_res or (not T_assign[-key])
			else:
				c_res = c_res or T_assign[key]

			i = i + 1

		res = res and c_res

	return res

def get_candidate(T_assign, fd):
	maxIncrease = 0
	res = 0

	for i in xrange(1, len(T_assign)+1):
		#flip and record...
		T_assign[i] = not T_assign[i]
		

def T_update(T, candidate):
	pass

def GSAT():
	fd = file('queens.cnf', 'r')
	line = fd.readline()
	line_list = line.split(split_pattern)
	
	var = (int)(line_list[2])
	MAX_FLIPS = var*5
	clauses = (int)(line_list[3])

	for i in xrange(1, MAX_TRIES+1):
		T = random_T_assign(var)
		for j in xrange(1, MAX_FLIPS+1):
			if test_sat(T, fd):
				print T
				return

			p = get_candidate(T, fd)
			T_update(T, p)

	print "no solution"
	fd.close()

#GSAT()
