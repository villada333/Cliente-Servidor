# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:44:54 2019

@author: villa
"""

import zmq


context=zmq.Context()
s=context.socket(zmq.REQ)
s.connect("tcp://localhost:5556")
while True:
    m=input()
    s.send_string(m)
    r=s.recv_string()
    print (r)