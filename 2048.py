# coding=utf-8
import random
import copy
import sys,tty,termios

class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class game(object):

	def __init__(self):
		self.init_table()

	def init_table(self):
		# self.array = [[0 for i in range(4)] for j in range(4)]  
		self.array = [[0]*4 for j in range(4)]  
		ran_pos = random.sample(range(16), 2)
		self.array[ran_pos[0]//4][ran_pos[0]%4] = self.array[ran_pos[1]//4][ran_pos[1]%4] = 2		

	def display(self):

		a = ("┌", "├", "├", "├", "└")
		b = ("┬", "┼", "┼", "┼", "┴")
		c = ("┐", "┤", "┤", "┤", "┘")
		for i in range(4):
			print(a[i] + ("─" * 5 + b[i]) * 3 + ("─" * 5 + c[i]))
			for j in range(4):
				print("│%4s" % (self.array[i][j] if self.array[i][j] else ' '), end=' ')
			print("│")
		print(a[4] + ("─" * 5 + b[4]) * 3 + ("─" * 5 + c[4]))

	def judge(self):
		total = sum(l.count(0) for l in self.array)
		if total != 0:
			return True
		for i in range(4): 
			for j in range(4):
				if i < 3 and self.array[i][j] == self.array[i + 1][j]:
					return True
				if j < 3 and self.array[i][j] == self.array[i][j + 1]:
					return True
		print("Gameover!")
		return False

	def update(self):
		ran_pos = []
		ran_num = [2,4]
		for i in range(4):
			for j in range(4):
				if self.array[i][j] == 0:
				   ran_pos.append(4*i + j)
		if len(ran_pos) > 0:
			k = random.choice(ran_pos)
			n = random.choice(ran_num)
			self.array[k//4][k%4] = n

	def move_up(self):
		visit = []
		for j in range(4):
			for i in range(1,4):
				for k in range(i,0,-1):
					if self.array[k-1][j] == 0:
						self.array[k-1][j] = self.array[k][j]
						self.array[k][j] = 0
					elif self.array[k-1][j] == self.array[k][j] and (4 *(k-1) + j) not in visit and (4*k + j) not in visit:
						self.array[k-1][j] *= 2
						self.array[k][j] = 0
						visit.append(4*(k) + j)
						visit.append(4*(k-1) + j)

	def move_down(self):
		visit = []
		for j in range(4):
			for i in range(3, 0, -1):
				for k in range(0,i):
				   if self.array[k+1][j] == 0:
					  	self.array[k+1][j] = self.array[k][j]
					  	self.array[k][j] = 0
				   elif self.array[k+1][j] == self.array[k][j] and (4 *(k+1) + j) not in visit and (4*k + j) not in visit:
					  	self.array[k+1][j] *= 2
					  	self.array[k][j] = 0  	
					  	visit.append(4*(k) + j)
					  	visit.append(4*(k+1) + j)

	def move_left(self):
		visit = []
		for i in range(4):
			for j in range(1, 4):
				for k in range(j,0,-1):
					if self.array[i][k-1] == 0 :
						self.array[i][k-1] = self.array[i][k]
						self.array[i][k] = 0
					elif self.array[i][k-1] == self.array[i][k] and 4 * i + k - 1 not in visit and 4 * i + k not in visit:
						self.array[i][k-1] *= 2
						self.array[i][k] = 0 	
						visit.append(4 * i + k)
						visit.append(4 * i + k - 1)

	
	def move_right(self):
		visit = []
		for i in range(4):
			for j in range(3, 0, -1):
				for k in range(j):
				   if self.array[i][k+1]  == 0:
					  	self.array[i][k+1] = self.array[i][k]
					  	self.array[i][k] = 0
				   elif self.array[i][k] == self.array[i][k+1] and 4 * i + k + 1 not in visit and 4 * i + k not in visit:
					  	self.array[i][k+1] *= 2
					  	self.array[i][k] = 0	
					  	visit.append(4*i + k + 1)
					  	visit.append(4*i + k)

	def run(self):
		try:
			print('usage: up, down, left, right to move, qqq to exit')
			getch = _Getch()
			self.display()
			while self.judge():
				movement = {'\x1b[A':self.move_up, '\x1b[B':self.move_down, '\x1b[C':self.move_right, '\x1b[D':self.move_left}
				action = getch()
				temp = copy.deepcopy(self.array)
				action = movement.get(action, None)
				print('usage: up, down, left, right to move, qqq to exit')
				if action:
					action()
					if temp != self.array:
						self.update()
						temp = copy.deepcopy(self.array)
						self.display()
					else:
						self.display()
				else:
					print('bye')
					sys.exit()
		except KeyboardInterrupt:
			print('bye')
			sys.exit()


if __name__ == '__main__':
	obj = game()
	obj.run()