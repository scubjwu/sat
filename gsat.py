import random
import cnf

MAX_FLIPS = 0
MAX_TRIES = 1000
origin_sn = 0

split_pattern = cnf.split_pattern

def random_T_assign(num):
	tmp_L = {}
	for i in xrange(1, num+1):
		tmp_L[i] = random.choice([False, True])

	return tmp_L

def cal_sn(T_assign, fd):
	sn = 0
	fd.seek(0)
	fd.readline()

	while True:
		line = fd.readline()
		if line == "":
			break

		line_list = line.split(split_pattern)
		i = 0
		c_res = False

		while True:
			if c_res or line_list[i] == "" or i == line_list.__len__() - 1:
				if c_res:
					sn = sn + 1
				break

			key = int(line_list[i])
			if key < 0:
				c_res = c_res or (not T_assign[-key])
			else:
				c_res = c_res or T_assign[key]

			i = i + 1
	
	return sn

def pre_test(T_assign, fd):
	origin_sn = cal_sn(T_assign, fd)

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
	res = -1

	for i in xrange(1, len(T_assign)+1):
		#flip and record...
		T_assign[i] = not T_assign[i]
		candidate_sn = cal_sn(T_assign, fd)
		changes = candidate_sn - origin_sn
		if changes > maxIncrease:
			maxIncrease = changes
			res = i

		T_assign[i] = not T_assign[i]
		
	return res

def GSAT():
	fd = file(cnf.cnf_file, 'r')
	line = fd.readline()
	line_list = line.split(split_pattern)
	
	var = (int)(line_list[2])
	MAX_FLIPS = var*5
	clauses = (int)(line_list[3])

	for i in xrange(1, MAX_TRIES+1):
		T = random_T_assign(var)
		pre_test(T, fd)
		pc = 0
		for j in xrange(1, MAX_FLIPS+1):
			if test_sat(T, fd):
				print "flips: %d, tries: %d" % (j, i)
				print "get one solution: ", T
				return

			tmp = get_candidate(T, fd)
			if tmp == -1 or pc == tmp:
				break
			#update T
			pc = tmp
			T[pc] = not T[pc]

	print "no solution"
	fd.close()

#GSAT()
cnf.test()
GSAT()
