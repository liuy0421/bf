import sys, math, dill, mmh3, argparse
import numpy as np

class bbloom:

    def __init__(self, fpr, n):
        self.cache_size = 512 # emulate cache behavior
        self.fpr, self.n = fpr, n
        self.m = int(-n*math.log(self.fpr)//(math.log(2))**2)
        self.b = math.ceil(self.m/self.cache_size)
        self.k = math.ceil((self.m/self.n)*math.log(2))
        self.hashes = [self.__hash_fn__(i) for i in range(self.k)]
        self.choose = self.__hash_fn__(self.k)
        self.bvec = np.zeros((self.b, self.cache_size))
        if self.b == 1:
            self.size = self.m
        else:
            self.size = self.cache_size

    def __insert_all__(self, f):
        for line in f:
            key = line.strip()
            self.insert(key)

    def insert(self, key):
        block = self.bvec[self.choose(key) % self.b]
        for i in [h(key) % self.size for h in self.hashes]:
                block[i] = 1

    def __hash_fn__(self, seed):
        def f(key):
            return mmh3.hash(key, seed, signed=False)
        return f

    def query(self, key):
        block = self.bvec[self.choose(key) % self.b]
        for h in self.hashes:
            if block[h(key) % self.size] == 0:
                return "N"
        return "Y"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Blocked Bloom Filter Implementation')
    for flag in ['-k', '-f', '-n', '-o']:
        parser.add_argument(flag)
    args = parser.parse_args()
    bf = bbloom(float(args.f), int(args.n))
    with open(args.k, 'r') as f:
            bf.__insert_all__(f)
    dill.dump(bf, open(args.o, 'wb'))


