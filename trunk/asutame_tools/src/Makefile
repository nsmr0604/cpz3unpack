#############################################################
# Compile hello.c into a shareable object file on Cygwin,
# to be loaded dynamically when first imported by Python.
#############################################################

PYLIB = /usr/bin
PYINC = /usr/include/python2.6

CC = /usr/bin/gcc

all: c_lzss.dll c_decrypt.dll

c_lzss.dll: c_lzss.c
		$(CC) -Os c_lzss.c -g -I$(PYINC) -shared -L$(PYLIB) -lpython2.6 -o c_lzss.dll
		
c_decrypt.dll: c_decrypt.c
		$(CC) -Os c_decrypt.c -masm=intel -g -I$(PYINC) -shared -L$(PYLIB) -lpython2.6 -o c_decrypt.dll

clean:
		rm -f c_lzss.dll
		rm -f c_decrypt.dll