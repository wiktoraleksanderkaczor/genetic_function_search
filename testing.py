from inspect import signature, getmembers
import math
import types

def main():
    mem = getmembers(math)
    func_only = [f[1] for f in mem]
    print(func_only)

if __name__ == "__main__":
    main()