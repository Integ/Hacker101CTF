def setup(seed):
	state = 0
	for i in range(16):
		cur = seed & 3
		seed >>= 2
		state = (state << 4) | ((state & 3) ^ cur)
		state |= cur << 2
	return state

def next(state):
	ret = 0
	for i in range(26):
		ret <<= 1
		ret |= state & 1
		state = (state << 1) ^ (state >> 61)
		state &= 0xFFFFFFFFFFFFFFFF
		state ^= 0xFFFFFFFFFFFFFFFF

		for j in range(0, 64, 4):
			cur = (state >> j) & 0xF
			cur = (cur >> 3) | ((cur >> 2) & 2) | ((cur << 3) & 8) | ((cur << 2) & 4)
			state ^= cur << j

	return ret, state

codes = [53494609, 56755322, 51004373]
seeds = [45581862, 113365951, 188081858, 256095067, 282153298, 346490059, 424882614, 488989743, 549998639, 616433078, 692728011, 758932818, 850298715,
		 920179394, 992798655, 1062908454, 1088169837, 1152021236]
for seed in seeds:
	print('{:08X}'.format(seed))
	state1 = setup(seed)
	code1, state2 = next(state1)
	code2, state3 = next(state2)
	code3, state4 = next(state3)
	code4, state5 = next(state4)
	print([code1, code2, code3, code4])