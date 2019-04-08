from itertools import product
from tqdm import tqdm

def setup(seed):
	state = 0
	for i in range(16):
		cur = seed & 3
		seed >>= 2
		state = (state << 4) | ((state & 3) ^ cur)
		state |= cur << 2
	return state

def next(state, code):
	ret = 0
	for i in range(26):
		if state & 1 == code[i]:
			ret <<= 1
			ret |= state & 1
			state = (state << 1) ^ (state >> 61)
			state &= 0xFFFFFFFFFFFFFFFF
			state ^= 0xFFFFFFFFFFFFFFFF

			for j in range(0, 64, 4):
				cur = (state >> j) & 0xF
				cur = (cur >> 3) | ((cur >> 2) & 2) | ((cur << 3) & 8) | ((cur << 2) & 4)
				state ^= cur << j
		else:
			return False
	print("state:{} --- code:{}".format(state, code))

codes = [53494609, 56755322, 51004373]
code = '{:026b}'.format(codes[0])
code = list(map(int, code))

for state in tqdm(range(2**32)):
	next(setup(state), code)