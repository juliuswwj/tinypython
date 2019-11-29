import sys, os
if not "tinypy" in sys.version:
    from boot import *

import tokenize,parse,encode

def xcompile(s, fname):
    tokens = tokenize.tokenize(s)
    t = parse.parse(s,tokens)
    r = encode.encode(fname, s, t)
    return r

def ximport(name):
    if name in MODULES:
        return MODULES[name]
    py = name+".py"
    tpc = name+".tpc"
    if os.exists(py):
        if not os.exists(tpc) or os.mtime(py) > os.mtime(tpc):
            s = os.load(py)
            code = xcompile(s,py)
            os.save(tpc,code)
    if not os.exists(tpc): raise
    code = os.load(tpc)
    g = {'__name__':name,'__code__':code}
    g['__dict__'] = g
    MODULES[name] = g
    exec(code,g)
    return g
    
    
def _init():
    BUILTINS['compile'] = xcompile
    BUILTINS['import'] = ximport

def import_fname(fname, name):
    g = {}
    g['__name__'] = name
    MODULES[name] = g
    s = os.load(fname)
    code = _compile(s, fname)
    g['__code__'] = code
    exec(code,g)
    return g
