
def _boot_init():
    global FTYPE 
    try:
        f = open('tp.h','r').read()
        FTYPE = 'f'
        if 'double tp_num' in f: FTYPE = 'd'
    except:
        FTYPE = 'd'
_boot_init()

def merge(a,b):
    if isinstance(a,dict):
        for k in b: a[k] = b[k]
    else:
        for k in b: setattr(a,k,b[k])

def number(v):
    if type(v) is str and v[0:2] == '0x':
        v = int(v[2:],16)
    return float(v)

def istype(v,t):
    if t == 'string': return isinstance(v,str)
    elif t == 'list': return (isinstance(v,list) or isinstance(v,tuple))
    elif t == 'dict': return isinstance(v,dict)
    elif t == 'number': return (isinstance(v,float) or isinstance(v,int))
    raise Exception('?')

def fpack(v):
    import struct
    return struct.pack(FTYPE,v)

def _load(fname):
    f = open(fname,'rb')
    r = f.read()
    f.close()
    return r

def _save(fname,v):
    f = open(fname,'wb')
    f.write(v)
    f.close()

import os
os.load = _load
os.save = _save
