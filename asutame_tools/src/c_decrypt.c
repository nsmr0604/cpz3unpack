
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <Python.h>

unsigned char originalKey[] = {0x5E , 0x4A , 0x0D , 0x4D , 0xE1 , 0xF3 , 0xAB , 0xB3 ,
                0x6D , 0x33 , 0x37 , 0x3C , 0xF3 , 0xF5 , 0xC3 , 0x86,
                 0x89 , 0x9B , 0x4F , 0x7D , 0x11 , 0xDE , 0xD7 , 0x58 ,
                 0x8D , 0x77 , 0x67 , 0x63 , 0x29 , 0x46 , 0xF3 , 0xA5 ,
                 0xB5 , 0xA4 , 0x7F , 0x06 , 0x42 , 0xE7 , 0x0A , 0xED ,
                 0xCC , 0x50 , 0x94 , 0xB1 , 0x5A , 0x4A , 0x20 , 0xE7 ,
                 0xF5 , 0x04 , 0xAF , 0xD9 , 0x7F , 0x68 , 0x3B , 0x5D ,
                 0xFD , 0xA6 , 0xC7 , 0xC1 , 0x89 , 0x22 , 0x50 , 0xFC};

int mygetc(unsigned char** input){
	unsigned char r=**input;
	(*input)++;
	return r;
}

void myputc(int r, unsigned char** input){
	**input = r;
	(*input)++;
}

inline unsigned char rol8(unsigned char num,unsigned char count) {
    return (num << count) | (num >> (0x08 - count));
}
inline unsigned char ror8(unsigned char num,unsigned char count) {
    return (num >> count) | (num << (0x08 - count));
}
inline unsigned int rol32(unsigned int num,unsigned int count) {
    return (num << count) | (num >> (0x20 - count));
}
inline unsigned int ror32(unsigned int num,unsigned int count) {
    return (num >> count) | (num << (0x20 - count));
}

static PyObject * 
encrypt(PyObject *self, PyObject *args, PyObject *keywds)    /* Just the reverse of Encode(). */
{
    unsigned char *buf = "";
    Py_ssize_t  strlength = 0;
    unsigned int length = 0;

    static char *kwlist[] = {"buf", "offset", "length", "delta", "keyMask", NULL};
    
    unsigned long keyMask;
    unsigned int delta;
    unsigned int offset;
    
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#iiik", kwlist, 
                                     &buf, &strlength, &offset, &length, &delta, &keyMask))
        return NULL; 

//    printf("%u\n",length);
    unsigned int eax, ebx, ecx, edx, rolcl, ebp;
    unsigned char al, bl, cl, dl;

    unsigned int padding = length & 0x03;

    unsigned char key[] = {0x5E , 0x4A , 0x0D , 0x4D , 0xE1 , 0xF3 , 0xAB , 0xB3 ,
                    0x6D , 0x33 , 0x37 , 0x3C , 0xF3 , 0xF5 , 0xC3 , 0x86,
                     0x89 , 0x9B , 0x4F , 0x7D , 0x11 , 0xDE , 0xD7 , 0x58 ,
                     0x8D , 0x77 , 0x67 , 0x63 , 0x29 , 0x46 , 0xF3 , 0xA5 ,
                     0xB5 , 0xA4 , 0x7F , 0x06 , 0x42 , 0xE7 , 0x0A , 0xED ,
                     0xCC , 0x50 , 0x94 , 0xB1 , 0x5A , 0x4A , 0x20 , 0xE7 ,
                     0xF5 , 0x04 , 0xAF , 0xD9 , 0x7F , 0x68 , 0x3B , 0x5D ,
                     0xFD , 0xA6 , 0xC7 , 0xC1 , 0x89 , 0x22 , 0x50 , 0xFC};
    
    int i = 0;
    for (i=0; i < 16; i++) {
    	unsigned int tmp = *((unsigned int *)(originalKey + (i * 4)));
        tmp = (tmp + (unsigned long)keyMask) & 0xFFFFFFFF;
        *((unsigned int *)(key+i*4)) = tmp;
    }
    eax = keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax ^ 0xFFFFFFFD;
    eax = eax & 0x0F;
    rolcl = eax + 8;
    
    i = offset;
    
    
    while(1){
    	unsigned int keyIndex = (i + delta) & 0x3F;
        
        ebp = *((unsigned int *)(buf+i));
        ebp = ror32(ebp, rolcl);
        ebp -= 0x6E58A5C2;
        ebp = ebp ^ (*((unsigned int *)(key+keyIndex)));
        
        *((unsigned int *)(buf+i)) = ebp;
        
        i = i + 4;
        if (i >= length - 3)
            break;
    }
    //处理尾部
    int j = i;
    while (padding > 0) {
    	unsigned int keyIndex = (j + delta) & 0x3F;
        
        eax = (*((unsigned int *)(key+keyIndex)));
        ecx = padding * 4;
        eax = eax >> (ecx & 0x0f);
        j = j + 4;
        i = i + 1;
        al = eax & 0x0ff;
        
        dl = buf[i - 1];
        dl = dl - 0x52;
        buf[i - 1] = al ^ dl;
        
//        printf("%u\n",al ^ dl);
        
        padding = padding - 1;
    }

    
    PyObject *result = Py_BuildValue("s#", buf, strlength);


    return result;
}

static PyObject * 
decrypt(PyObject *self, PyObject *args, PyObject *keywds)    /* Just the reverse of Encode(). */
{
    unsigned char *buf = "";
    Py_ssize_t  strlength = 0;
    unsigned int length = 0;

    static char *kwlist[] = {"buf", "offset", "length", "delta", "keyMask", NULL};
    
    unsigned long keyMask;
    unsigned int delta;
    unsigned int offset;
    
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#iiik", kwlist, 
                                     &buf, &strlength, &offset, &length, &delta, &keyMask))
        return NULL; 

//    printf("%u\n",length);
    unsigned int eax, ebx, ecx, edx, rolcl, ebp;
    unsigned char al, bl, cl, dl;

    unsigned int padding = length & 0x03;

    unsigned char key[] = {0x5E , 0x4A , 0x0D , 0x4D , 0xE1 , 0xF3 , 0xAB , 0xB3 ,
                    0x6D , 0x33 , 0x37 , 0x3C , 0xF3 , 0xF5 , 0xC3 , 0x86,
                     0x89 , 0x9B , 0x4F , 0x7D , 0x11 , 0xDE , 0xD7 , 0x58 ,
                     0x8D , 0x77 , 0x67 , 0x63 , 0x29 , 0x46 , 0xF3 , 0xA5 ,
                     0xB5 , 0xA4 , 0x7F , 0x06 , 0x42 , 0xE7 , 0x0A , 0xED ,
                     0xCC , 0x50 , 0x94 , 0xB1 , 0x5A , 0x4A , 0x20 , 0xE7 ,
                     0xF5 , 0x04 , 0xAF , 0xD9 , 0x7F , 0x68 , 0x3B , 0x5D ,
                     0xFD , 0xA6 , 0xC7 , 0xC1 , 0x89 , 0x22 , 0x50 , 0xFC};
    
    int i = 0;
    for (i=0; i < 16; i++) {
    	unsigned int tmp = *((unsigned int *)(originalKey + (i * 4)));
        tmp = (tmp + (unsigned long)keyMask) & 0xFFFFFFFF;
        *((unsigned int *)(key+i*4)) = tmp;
    }
    eax = keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax >> 4;
    eax = eax ^ keyMask;
    eax = eax ^ 0xFFFFFFFD;
    eax = eax & 0x0F;
    rolcl = eax + 8;
    
    i = offset;
    
    
    while(1){
    	unsigned int keyIndex = (i + delta) & 0x3F;
        
        ebp = *((unsigned int *)(buf+i));
        ebp = ebp ^ (*((unsigned int *)(key+keyIndex)));
        ebp += 0x6E58A5C2;
        ebp = rol32(ebp, rolcl);
        
        *((unsigned int *)(buf+i)) = ebp;
        
        i = i + 4;
        if (i >= length - 3)
            break;
    }
    //处理尾部
    int j = i;
    while (padding > 0) {
    	unsigned int keyIndex = (j + delta) & 0x3F;
        
        eax = (*((unsigned int *)(key+keyIndex)));
        ecx = padding * 4;
        eax = eax >> (ecx & 0x0f);
        j = j + 4;
        i = i + 1;
        al = eax & 0xff;
        al = al ^ buf[i - 1];
        al = al + 0x52;
        padding = padding - 1;
        buf[i - 1] = al;
    }

    
    PyObject *result = Py_BuildValue("s#", buf, strlength);


    return result;
}

static PyObject * 
decryptPs2(PyObject *self, PyObject *args, PyObject *keywds)    /* Just the reverse of Encode(). */
{

    unsigned char *inputBuf = "";
    int length = 0;

    static char *kwlist[] = {"buf", "key", NULL};
    
    int key;
    
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#i", kwlist, 
                                     &inputBuf, &length, &key))
        return NULL; 
    
    int eax, ebx, ecx, edx;
    unsigned char al, bl, cl, dl;
    
    ecx = key;
    eax = ecx;
    eax >>= 0x14;
    edx = eax %5;
    eax = eax / 5;
    eax = ecx;
    eax >>= 0x18;
    ecx >>= 3;
    al = eax & 0xff;
    cl = ecx & 0xff;
    al += cl;
    dl = edx & 0xff;
    dl++;
    ecx = dl;
    cl = ecx & 0xff;
    
    int i = 0;
    for (i = 0; i < length; i++) {
    	dl = inputBuf[i];
    	dl = dl - 0x7c;
    	dl = dl ^ al;
    	dl = ror8(dl, cl);
    	inputBuf[i] = dl;
    }
    

    
    PyObject *result = Py_BuildValue("s#", inputBuf, length);


    return result;
}

static PyObject * 
encryptPs2(PyObject *self, PyObject *args, PyObject *keywds)    /* Just the reverse of Encode(). */
{

    unsigned char *inputBuf = "";
    int length = 0;

    static char *kwlist[] = {"buf", "key", NULL};
    
    int key;
    
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#i", kwlist, 
                                     &inputBuf, &length, &key))
        return NULL; 
    
    int eax, ebx, ecx, edx;
    unsigned char al, bl, cl, dl;
    
    ecx = key;
    eax = ecx;
    eax >>= 0x14;
    edx = eax %5;
    eax = eax / 5;
    eax = ecx;
    eax >>= 0x18;
    ecx >>= 3;
    al = eax & 0xff;
    cl = ecx & 0xff;
    al += cl;
    dl = edx & 0xff;
    dl++;
    ecx = dl;
    cl = ecx & 0xff;
    
    int i = 0;
    for (i = 0; i < length; i++) {
    	dl = inputBuf[i];
    	dl = rol8(dl, cl);
    	dl = dl ^ al;
    	dl = dl + 0x7c;
    	inputBuf[i] = dl;
    }
    

    
    PyObject *result = Py_BuildValue("s#", inputBuf, length);


    return result;
}

/* registration table  */
static struct PyMethodDef c_decrypt_methods[] = {
	    {"encrypt", (PyCFunction)encrypt, METH_VARARGS|METH_KEYWORDS, NULL},       /* method name, C func ptr, always-tuple */
	    {"encryptPs2", (PyCFunction)encryptPs2, METH_VARARGS|METH_KEYWORDS, NULL},       /* method name, C func ptr, always-tuple */
	    {"decrypt", (PyCFunction)decrypt, METH_VARARGS|METH_KEYWORDS, NULL},       /* method name, C func ptr, always-tuple */
	    {"decryptPs2", (PyCFunction)decryptPs2, METH_VARARGS|METH_KEYWORDS, NULL},       /* method name, C func ptr, always-tuple */
	    {NULL,NULL,0,NULL}                  /* end of table marker */
};

/* module initializer */
PyMODINIT_FUNC initc_decrypt( )                       /* called on first import */
{                                      /* name matters if loaded dynamically */
    (void) Py_InitModule("c_decrypt", c_decrypt_methods);   /* mod name, table ptr */
}