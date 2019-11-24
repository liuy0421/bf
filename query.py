import dill, sys, mmh3, argparse
from bloom import bloom

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bloom Filter Implementation')
    for flag in ['-i', '-q']:
        parser.add_argument(flag)
    args = parser.parse_args()
    bf = dill.load(open(args.i, 'rb'))
    with open(args.q, 'r') as f:
        for line in f:
            q = line.strip()
            print("{}:{}".format(q, bf.query(q)))