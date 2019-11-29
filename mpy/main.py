import sys

def agent():
    print(sys.version)
    print(str(sys.argv))

def test():
    import math
    print(math.pi)
    print('%s . %s' % (sys.version, '12'))
