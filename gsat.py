import random
import cnf
import math
import profile
from timeit import Timer

#import pdb

class GSAT_TEST:
	def __init__(self):
		gsat_type = raw_input("Select which gsat algorithm to test [1-3]\n[1] GSAT\n[2] GWSAT\n[3] GSAT_TABU\n--->")
		if gsat_type.isdigit() == False:
			print "Please type 1-3 to selct the gsat algorithm for testing..."
			return

		if int(gsat_type) == 1:
			#create the cnf file first
			cnf.test()
			#execute the test
			test = GSAT("GSAT")
			self.run_test(test)
		elif int(gsat_type) == 2:
			cnf.test()
			test = GWSAT("GWSAT")
			self.run_test(test)
		elif int(gsat_type) == 3:
			cnf.test()
			test = GSAT_TABU("GSAT_TABU")
			self.run_test(test)
		else:
			print "unknown method..."

	def run_test(self, obj):
			num = 10
			T = Timer(obj.run)
			print "Algorithm: #######" + obj.method + "#######"
			print "running time: ", T.timeit(num)/num
			if obj.solution == {}:
				print "no solution"
			else:
				print "get one solution: ", obj.solution
				print "flips: %f, tries: %f" % (obj.num_flips/num, obj.num_tries/num)

class GSAT_BASE:
	MAX_FLIPS = 0
	MAX_TRIES = 1000
	CONTENT = []

	num_flips = 0.
	num_tries = 0.

	solution = {}

	split_pattern = cnf.split_pattern

	def __init__(self):
		self.handle_cnf()
		self.var = (int)(self.CONTENT[0][2])
		self.MAX_FLIPS = self.var*5
		self.clauses = (int)(self.CONTENT[0][3])

	def random_T_assign(self, num):
		tmp_L = {}
		for i in xrange(1, num+1):
			tmp_L[i] = random.choice([False, True])

		return tmp_L

	def new_random_T_assign(self, num):
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

	def verify_clause(self, n, T_assign):
		res = False

		for i in xrange(0, len(self.CONTENT[n])-1):
			key = int(self.CONTENT[n][i])
			if key < 0:
				res = res or (not T_assign[-key])
			else:
				res = res or T_assign[key]

			if res:
				break
		
		return res

	def cal_sn(self, T_assign, pos):
		sn = 0

		for i in xrange(1, len(self.CONTENT)):
		#	pdb.set_trace()
			if (not str(pos) in self.CONTENT[i]) and (not str(-pos) in self.CONTENT[i]):
				continue

			if self.verify_clause(i, T_assign):
				continue
			
			T_assign[pos] = not T_assign[pos]

			if self.verify_clause(i, T_assign):
				sn = sn + 1

			T_assign[pos] = not T_assign[pos]

		return sn

	def test_sat(self, T_assign):
		res = True

		for i in xrange(1, len(self.CONTENT)):
			res = res and self.verify_clause(i, T_assign)
			if res == False:
		#		global unsat_clause
		#		unsat_clause = i
				break;

		return res

	def get_candidate(self, T_assign):
		maxIncrease = 0
		res = -1

		for i in xrange(1, len(T_assign)+1):
			#flip and record...
			candidate_sn = self.cal_sn(T_assign, i)
			if candidate_sn > maxIncrease:
				maxIncrease = candidate_sn
				res = i

		return res

	def handle_cnf(self):
		fd = file(cnf.cnf_file, "r")
		lines = fd.readlines()
		fd.close()
		
		n = len(lines)
		self.CONTENT = [0]*n
		for i in xrange(0, n):
			self.CONTENT[i] = lines[i].split(self.split_pattern)

	def run(self):
		pass
	
##########################################################################################################
class GSAT(GSAT_BASE):
	def __init__(self, method):
		GSAT_BASE.__init__(self)
		self.method = method

	def run(self):
		for i in xrange(1, self.MAX_TRIES+1):
			T = self.new_random_T_assign(self.var)
		#	T = random_T_assign(var)
			pc = 0
			for j in xrange(1, self.MAX_FLIPS+1):
				if self.test_sat(T):
					self.num_flips = self.num_flips + j
					self.num_tries = self.num_tries + i
					self.solution = T.copy()
					return

				tmp = self.get_candidate(T)
				if tmp == -1 or pc == tmp:
					break
				
				#update T
				pc = tmp
				T[pc] = not T[pc]

############################################################################################################
class GWSAT(GSAT_BASE):
	def __init__(self, method):
		GSAT_BASE.__init__(self)
		self.method = method
		self.RW_P = 0.15
		self.unsat_clause = 0
		
	def test_sat(self, T_assign):
		res = True

		for i in xrange(1, len(self.CONTENT)):
			res = res and self.verify_clause(i, T_assign)
			if res == False:
				self.unsat_clause = i
				break;

		return res
		
	def get_candidate_rw(self):
		pos = random.randrange(0, len(self.CONTENT[self.unsat_clause])-1)
		tmp = math.fabs(int(self.CONTENT[self.unsat_clause][pos]))
		return tmp
		
	def run(self):
		for i in xrange(1, self.MAX_TRIES+1):
			T = self.new_random_T_assign(self.var)
		#	T = random_T_assign(var)
			pc = 0
			for j in xrange(1, self.MAX_FLIPS+1):
				if self.test_sat(T):
					self.num_flips = self.num_flips + j
					self.num_tries = self.num_tries + i
					self.solution = T.copy()
					return

				if random.random() > self.RW_P:
					tmp = self.get_candidate(T)
				else:
					tmp = self.get_candidate_rw()

				if tmp == -1 or tmp == pc:
					break;

				#update T
				pc = tmp
				T[pc] = not T[pc]
				
#################################################################################################################		

class GSAT_TABU(GSAT_BASE):
	def __init__(self, method):
		GSAT_BASE.__init__(self)
		self.method = method
		self.tabu_list_len = (int)(0.01875 * self.var + 2.8125)
		self.tabu_list = []
	
	def get_tabu_candidate(self, T_assign):
		res = -1
		tabu_mem = {}

		for i in xrange(1, len(T_assign)+1):
			candidate_sn = self.cal_sn(T_assign, i)
			tabu_mem[i] = self.cal_sn(T_assign, i)
		
		#sort tabu_mem
		tabu_candidate = sorted(tabu_mem.items(), key=lambda  e:e[1], reverse=True)
		#get the best candidate based on tabu list
	#	pdb.set_trace()
		for candidate in tabu_candidate:
			if self.tabu_list[candidate[0]-1] == 0:
				res = candidate[0]
				break

		return res
		
	def run(self):
		for i in xrange(1, self.MAX_TRIES+1):
			T = self.new_random_T_assign(self.var)
		#	T = random_T_assign(var)
			pc = 0
			self.tabu_list = [0]*self.var #init tabu list for every try
			for j in xrange(1, self.MAX_FLIPS+1):
				if self.test_sat(T):
					self.num_flips = self.num_flips + j
					self.num_tries = self.num_tries + i
					self.solution = T.copy()
					return

				tmp = self.get_tabu_candidate(T)
				if tmp == -1:
					break
				
				#update T
				pc = tmp
				T[pc] = not T[pc]

				#update tabu list
				for t in xrange(self.var):
					if t == pc-1:
						self.tabu_list[t] = self.tabu_list_len
					elif self.tabu_list[t] == 0:
						continue
					else:
						self.tabu_list[t] = self.tabu_list[t] - 1
################################################################################################################		

if __name__ == "__main__":
	t = GSAT_TEST()
#	profile.run("GWSAT()")

