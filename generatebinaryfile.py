import os
import struct
import random
import sys
f = open('midiccionario.txt','wb')
for i in range(125000):
    for ii in range(1024):
        f.write(struct.pack("=I",random.randint(0,1024)))

f.close()