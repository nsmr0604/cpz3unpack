from array import array
a=array('B', [10, 254, 145, 145])
b=array('B', [10, 254, 145, 145])
a[0:0+4]=b
print a