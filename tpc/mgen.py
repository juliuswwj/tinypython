import sys, py2bc


lext=[]
lset=[]
linit=[]

def parse_c(fname, name):
    global lext, linit
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if line.endswith('{'):
                line = line[:-1].strip()
            if ('tp_%s_init' % name) in line and 'TP' in line and line.startswith('void'):
                lext.append(line + ';')
                if 'argv' in line: 
                    lset.append('tp_%s_init(tp, argc, argv);' % name)
                else:
                    lset.append('tp_%s_init(tp);' % name)

def parse_py(fname, name):
    global lext, lset, linit

    with open(fname, 'r') as f:
        txt = f.read()
    
    bc = map(lambda x: '%3d' % ord(x), py2bc.xcompile(txt, fname))
    lext.append('static unsigned char bc_%s[] = {' % name)
    while len(bc) > 0:
        if len(bc) > 16:
            bs = ', '.join(bc[:16]) + ','
            bc = bc[16:]
        else:
            bs = ','.join(bc)
            bc = ''
        lext.append('    ' + bs)
    lext.append('};')
    
    lset.append('tp_import(tp, 0, "%s", bc_%s, sizeof(bc_%s));' % (name, name, name))
    for line in txt.split('\n'):
        line = line.strip()
        if line.startswith('def') and '_init()' in line:
            linit.append('tp_ez_call(tp,"%s","_init",tp_None);' % name)



for fname in sys.argv[1:]:
    name = fname.split('/')[-1].split('.')[0]
    if fname.endswith('.c'):
        parse_c(fname, name)
    elif fname.endswith('.py'):
        parse_py(fname, name)
    else:
        continue


print '// generate by mgen.py'
print '#include "../core/tp.h"'
for v in lext: print v
print 'void mgen_init(TP, int argc, char* argv[]) {'
for v in lset: print '   ', v
for v in linit: print '   ', v
print '}'
