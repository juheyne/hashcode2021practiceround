import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()
print(args.file)

with open(args.file) as f:
    read_data = f.read()
