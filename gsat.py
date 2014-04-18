import random
import cnf

MAX_FLIPS = 0
MAX_TRIES = 1000
CONTENT=[]

split_pattern = cnf.split_pattern

def random_T_assign(num):
	tmp_L = {}
	for i in xrange(1, num+1):
		tmp_L[i] = random.choice([False, True])

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
		T = random_T_assign(var)
		pc = 0
		for j in xrange(1, MAX_FLIPS+1):
			if test_sat(T):
				print "flips: %d, tries: %d" % (j, i)
				print "get one solution: ", T
				return

			tmp = get_candidate(T)
			if tmp == -1 or pc == tmp:
				break
			#update T
			pc = tmp
			T[pc] = not T[pc]

	print "no solution"

#GSAT()
if __name__ == "__main__":
	cnf.test()
	GSAT()
