from random import randint
from c21_Implement_the_MT19937_Mersenne_Twister_RNG import MT19937
from time import time

current_time = int(time())

def crack_seed(rng_output):
	for seed in range(current_time, current_time-1000, -1):
		rng = MT19937(seed)
		if(rng.uint32() == rng_output):
			return seed

current_time += randint(40, 1000)
rng = MT19937(current_time)
rng_output = rng.uint32()

print("seed : %d" % current_time)

current_time += randint(40, 1000)
seed = crack_seed(rng_output)

print("seed : %d" % seed)