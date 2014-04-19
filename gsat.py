import random
import cnf
import math
import profile
from timeit import Timer

#import pdb

MAX_FLIPS = 0
MAX_TRIES = 1000
CONTENT = []

num_flips = 0.
num_tries = 0.
RW_P = 0.15
unsat_clause = 0
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

def verify_clause(n, T_assign):
	res = False

	for i in xrange(0, len(CONTENT[n])-1):
		key = int(CONTENT[n][i])
		if key < 0:
			res = res or (not T_assign[-key])
		else:
			res = res or T_assign[key]

		if res:
			break
	
	return res

def cal_sn(T_assign, pos):
	sn = 0

	for i in xrange(1, len(CONTENT)):
	#	pdb.set_trace()
		if (not str(pos) in CONTENT[i]) and (not str(-pos) in CONTENT[i]):
			continue

		if verify_clause(i, T_assign):
			continue
		
		T_assign[pos] = not T_assign[pos]

		if verify_clause(i, T_assign):
			sn = sn + 1

		T_assign[pos] = not T_assign[pos]

	return sn

def test_sat(T_assign):
	res = True

	for i in xrange(1, len(CONTENT)):
		res = res and verify_clause(i, T_assign)
		if res == False:
			global unsat_clause
			unsat_clause = i
			break;

	return res

def get_candidate(T_assign):
	maxIncrease = 0
	res = -1

	for i in xrange(1, len(T_assign)+1):
		#flip and record...
		candidate_sn = cal_sn(T_assign, i)
		if candidate_sn > maxIncrease:
			maxIncrease = candidate_sn
			res = i

	return res

def get_candidate_rw():
	pos = random.randrange(0, len(CONTENT[unsat_clause])-1)
	tmp = math.fabs(int(CONTENT[unsat_clause][pos]))
	return tmp

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

def GWSAT():
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

			if random.random() > RW_P:
				tmp = get_candidate(T)
			else:
				tmp = get_candidate_rw()

			if tmp == -1 or tmp == pc:
				break;

			#update T
			pc = tmp
			T[pc] = not T[pc]

def test():
	test_n = 10
	T = Timer("GWSAT()", "from __main__ import GWSAT")
	print "running time: ", T.timeit(test_n)/test_n
	if solution == {}:
		print "no solution"
	else:
		print "get one solution: ", solution
		print "flips: %f, tries: %f" % (num_flips/test_n, num_tries/test_n)

if __name__ == "__main__":
	cnf.test()
	test()
#	profile.run("GWSAT()")

