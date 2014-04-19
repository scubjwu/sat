import random
import cnf
import math

MAX_FLIPS = 0
MAX_TRIES = 1000
CONTENT = []

num_flips = 0.
num_tries = 0.
solution = {}

split_pattern = cnf.split_pattern

def random_T_assign(num):
	tmp_L = {}
	for i in xrange(1, num+1):
		tmp_L[i] = random.choice([False, True])

	return tmp_L

def new_random_T_assign(num):
	tmp_L = {}
	step = int(math.sqrt(num))
	for i in xrange(1, num+1, step):
		p = random.randrange(i, i+step)
		for j in xrange(i, i+step):
			if j == p:
				tmp_L[j] = True
			else:
				tmp_L[j] = False

	return tmp_L

def cal_sn(T_assign):
	sn = 0

	for i in xrange(1, len(CONTENT)):
		c_res = False
		len_c = len(CONTENT[i]) - 1
		for j in xrange(0, len_c):
			key = int(CONTENT[i][j])
			if key < 0:
				c_res = c_res or (not T_assign[-key])
			else:
				c_res = c_res or T_assign[key]

			if c_res:
				sn = sn + 1
				break

	
	return sn

def test_sat(T_assign):
	res = True

	for i in xrange(1, len(CONTENT)):
		if res == False:
			break

		c_res = False
		len_c = len(CONTENT[i]) - 1
		for j in xrange(0, len_c):
			key = int(CONTENT[i][j])
			if key < 0:
				c_res = c_res or (not T_assign[-key])
			else:
				c_res = c_res or T_assign[key]

			if c_res:
				break

		res = res and c_res

	return res

def get_candidate(T_assign):
	maxIncrease = 0
	res = -1

	for i in xrange(1, len(T_assign)+1):
		#flip and record...
		T_assign[i] = not T_assign[i]
		candidate_sn = cal_sn(T_assign)
		if candidate_sn > maxIncrease:
			maxIncrease = candidate_sn
			res = i

		T_assign[i] = not T_assign[i]
		
	return res

def handle_cnf():
	global CONTENT

	fd = file(cnf.cnf_file, "r")
	lines = fd.readlines()
	fd.close()
	
	n = len(lines)
	CONTENT = [0]*n
	for i in xrange(0, n):
		CONTENT[i] = lines[i].split(split_pattern)

def GSAT():
	handle_cnf();
	
	var = (int)(CONTENT[0][2])
	MAX_FLIPS = var*5
	clauses = (int)(CONTENT[0][3])

	for i in xrange(1, MAX_TRIES+1):
		T = new_random_T_assign(var)
	#	T = random_T_assign(var)
		pc = 0
		for j in xrange(1, MAX_FLIPS+1):
			if test_sat(T):
				global solution, num_flips, num_tries
				num_flips = num_flips + j
				num_tries = num_tries + i
				solution = T.copy()
				return

			tmp = get_candidate(T)
			if tmp == -1 or pc == tmp:
				break
			#update T
			pc = tmp
			T[pc] = not T[pc]


#GSAT()
if __name__ == "__main__":
	from timeit import Timer
	test_n = 10
	cnf.test()
	T = Timer("GSAT()", "from __main__ import GSAT")
	print "running time: ", T.timeit(test_n)
	if solution == {}:
		print "no solution"
	else:
		print "get one solution: ", solution

	print "flips: %f, tries: %f" % (num_flips/test_n, num_tries/test_n)
#	import profile
#	profile.run("GSAT()")
