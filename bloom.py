import sys, math, dill, mmh3, argparse
import numpy as np

class bloom:

    def __init__(self, fpr, n):
        self.fpr, self.n = fpr, n
        self.m = int(-n*math.log(self.fpr)//(math.log(2))**2)
        self.k = math.ceil((self.m/self.n)*math.log(2))
        self.hashes = [self.__hash_fn__(i) for i in range(self.k)]
        self.bvec = np.zeros(self.m)

    def __insert_all__(self, f):
        for line in f:
            key = line.strip()
            self.insert(key)

    def insert(self, key):
        for i in [h(key) % self.m for h in self.hashes]:
                self.bvec[i] = 1

    def __hash_fn__(self, seed):
        def f(key):
            return mmh3.hash(key, seed, signed=False)
        return f

    def query(self, key):
        for h in self.hashes:
            if self.bvec[h(key) % self.m] == 0:
                return "N"
        return "Y"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bloom Filter Implementation')
    for flag in ['-k', '-f', '-n', '-o']:
        parser.add_argument(flag)
    args = parser.parse_args()
    bf = bloom(float(args.f), int(args.n))
    with open(args.k, 'r') as f:
            bf.__insert_all__(f)
    dill.dump(bf, open(args.o, 'wb'))


