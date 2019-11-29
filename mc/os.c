#include "../core/tp.h"

static tp_obj tp_os_command(TP) {
    char s[TP_CSTR_LEN]; tp_cstr(tp,TP_STR(),s,TP_CSTR_LEN);
    int r = system(s);
    return tp_number(r);
}


static tp_obj tp_os_exists(TP) {
    char fname[TP_CSTR_LEN]; tp_cstr(tp,TP_STR(),fname,TP_CSTR_LEN);
    struct stat stbuf;
    return tp_number(!stat(fname,&stbuf));
}

static tp_obj tp_os_mtime(TP) {
    char fname[TP_CSTR_LEN]; tp_cstr(tp,TP_STR(),fname,TP_CSTR_LEN);
    struct stat stbuf;
    if (!stat(fname,&stbuf)) { return tp_number(stbuf.st_mtime); }
    tp_raise(tp_None,tp_string("(tp_mtime) IOError: ?"));
}



static tp_obj tp_os_save(TP) {
    char fname[256]; tp_cstr(tp,TP_STR(),fname,256);
    tp_obj v = TP_OBJ();
    FILE *f;
    f = fopen(fname,"wb");
    if (!f) { tp_raise(tp_None,tp_string("(tp_os_save) IOError: ?")); }
    fwrite(v.string.val,v.string.len,1,f);
    fclose(f);
    return tp_None;
}

// also used by vm.c
tp_obj tp_os_load(TP) {
    FILE *f;
    long l;
    tp_obj r;
    char *s;
    char fname[256]; tp_cstr(tp,TP_STR(),fname,256);
    struct stat stbuf;
    stat(fname, &stbuf);
    l = stbuf.st_size;
    f = fopen(fname,"rb");
    if (!f) {
        tp_raise(tp_None,tp_string("(tp_os_load) IOError: ?"));
    }
    r = tp_string_t(tp,l);
    s = r.string.info->s;
    l = fread(s,1,l,f);
/*    if (rr !=l) { printf("hmmn: %d %d\n",rr,(int)l); }*/
    fclose(f);
    return tp_track(tp,r);
}



void tp_os_init(TP, int argc, char *argv[]) {
    int i;
    tp_obj os = tp_dict(tp);
    tp_obj args = tp_list(tp);

    tp_set_string(tp, os, "version", "tinypy-scms-1.0");

    tp_set_func(tp, os, "command", tp_os_command);
    tp_set_func(tp, os, "exists", tp_os_exists);
    tp_set_func(tp, os, "mtime", tp_os_mtime);
    tp_set_func(tp, os, "save", tp_os_save);
    tp_set_func(tp, os, "load", tp_os_load);

    for (i=1; i<argc; i++) { _tp_list_append(tp, args.list.val,tp_string(argv[i])); }
    tp_set(tp, os, tp_string("argv"), args);

    tp_set(tp, tp->modules, tp_string("os"), os);
    tp_set(tp, tp->modules, tp_string("sys"), os);
}

