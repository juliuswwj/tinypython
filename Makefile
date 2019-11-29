
all: build/tpc

run: build/tpc
	./build/tpc

test: build/test
	./build/test

build/test: $(wildcard core/*.c) build/_mgen.c
	gcc -g -std=c99 -o build/test core/main.c build/_mgen.c $(wildcard mc/*.c) -lm 

build/tpc: $(wildcard core/*.c) build/_mgen.c
	gcc -std=c99 -o build/tpc -O2 core/main.c build/_mgen.c $(wildcard mc/*.c) -lm 

build/_mgen.c: $(wildcard mc/*.c) tpc/tokenize.py tpc/parse.py tpc/encode.py tpc/py2bc.py $(wildcard mpy/*.py)
	python tpc/mgen.py $^ >$@


clean:
	-rm build/*
