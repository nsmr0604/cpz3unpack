#############################################################
# Compile hello.c into a shareable object file on Cygwin,
# to be loaded dynamically when first imported by Python.
#############################################################

PYLIB = /usr/bin
PYINC = /usr/include/python2.6

CC = gcc
CFLAGS = -O3 -g -masm=intel -march=core2 -pipe 
LDFLAGS = -s -shared -I$(PYINC) -L$(PYLIB) -lpython2.6 

all: c_lzss.dll c_decrypt.dll

c_lzss.dll: c_lzss.c
		$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) c_lzss.c -o c_lzss.dll
		
c_decrypt.dll: c_decrypt.c
		$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) c_decrypt.c -o c_decrypt.dll

clean:
		rm -f c_lzss.dll
		rm -f c_decrypt.dll