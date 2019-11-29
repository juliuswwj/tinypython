#ifndef TP_COMPILER
#define TP_COMPILER 1
#endif

#include "tp.h"
#include "list.c"
#include "dict.c"
#include "misc.c"
#include "string.c"
#include "builtins.c"
#include "gc.c"
#include "ops.c"
#include "vm.c"

extern void mgen_init(TP, int argc, char* argv[]);

int main(int argc, char *argv[]) {
    char* entry = argv[0];
    tp_vm *tp = tp_init();

    tp_builtins(tp);
    mgen_init(tp, argc, argv);

    // get program name
    while(1){
        char* p = strchr(entry, '/');
        if(!p) break;
        entry = p + 1;
    }
    tp_ez_call(tp, "main", entry, tp_None);
    tp_deinit(tp);
    return(0);
}
