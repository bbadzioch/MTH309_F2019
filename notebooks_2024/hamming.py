import matplotlib.pyplot as plt
import numpy as np
import random
from IPython.display import HTML, display
import requests

def add_noise(msg, p):
    msg = np.array(msg, dtype ='uint8')
    noisy = np.logical_xor(msg, np.random.rand(msg.size) < p)
    return list(np.array(noisy, dtype='uint8'))
    
def hamming_encode(msg):
    msg = np.array(msg, dtype ='uint8')
    if msg.size %4 != 0:
        print("Array length must be divisible by 4.\nThe array entered has length {}.".format(msg.size))
        return []
    he = np.vstack((np.eye(4,dtype='uint8'), np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1]],dtype='uint8')))
    he_r, he_c = he.shape
    msg = msg.reshape(msg.size//he_c, he_c).T
    encoded = np.dot(he, msg) % 2
    return list(encoded.T.ravel())
 
def hamming_decode(msg):
    msg = np.array(msg, dtype ='uint8')
    hd = np.array([[0,1,1,1,1,0,0],[1,0,1,1,0,1,0],[1,1,0,1,0,0,1]],dtype='uint8')
    hd_r, hd_c = hd.shape
    msg = msg.reshape(msg.size//hd_c, hd_c).T
    raw = np.dot(hd, msg) %2
    decoded = []
    e = np.hstack((np.zeros((hd_c,1), dtype='uint8'), np.eye(hd_c, dtype='uint8')))
    hde = np.hstack((np.zeros((hd_r,1), dtype='uint8'), hd))
    for i in range(msg.shape[1]):
        for j in range(hde.shape[1]):
            if np.array_equal(raw[:,i], hde[:, j]):
                msg[:, i] = (msg[:, i] + e[:, j]) %2
                break
        decoded.extend(list(msg[:4, i]))
    
    return list(np.array(decoded, dtype='uint8'))
 
def recover_from_coded(msg):
    r = []
    for i in range(0,msg.size,7):
        r.extend(msg[i:i+4])
    return np.array(r, dtype='uint8')


def text2bits(s):
    return list(np.unpackbits(np.array([ord(c) for c in s], dtype='uint8')))


def bits2text(b):
    return ''.join([chr(x) for x in np.packbits(np.array(b, dtype='uint8'))])

def color_print(no_corr, corr, p):
    s1 = r'''<style type="text/css"> 
            #wrap {width:900px; margin:  30px 0 0 0;} 
            #left_col {float:left;width:440px;}
            #right_col {float:right;width:440px;}
            #pout {padding: 20px 20px 20px 20px; background-color:black; color:gray; font-family:monospace; font-size:11pt; line-height: 120%;}
            </style>
            '''
    
    s2 = r'<div id="wrap"><div id="left_col"><b>without error correction (p={})</b>'.format(p)
    s3 = r'</div><div id="right_col"><b>with error correction (p={})</b>'.format(p)
    s4 = r'</div></div>'
    
    printout1 = ''
    for m, c in no_corr:
        if m:
            printout1 += c
        else:
            printout1 += '<span style="background-color:FireBrick;">' + c + '</span>'
    printout1 = '<p id="pout">' + printout1 + '</p>'
    
    printout2 = ''
    for m, c in corr:
        if m:
            printout2 += c
        else:
            printout2 += '<span style="background-color:FireBrick;">' + c + '</span>'
    printout2 = '<p id="pout">' + printout2 + '</p>'
    display(HTML(s1 + s2 + printout1 + s3 + printout2 + s4))


    
def text_compare(text, p):
    t_arr = np.array([ord(c) for c in text], dtype = 'uint8')
    bit_arr = np.unpackbits(t_arr)
    encoded = np.array(hamming_encode(bit_arr), dtype='uint8')
    noisy = np.array(add_noise(encoded, p), dtype='uint8')
    
    no_corr = recover_from_coded(noisy)
    ss1 = ''.join([chr(c) for c in np.packbits(no_corr)])
    text1 = [ (c==d, d) for c, d in zip(text, ss1)]

    corr = np.array(hamming_decode(noisy), dtype='uint8')
    ss2 = ''.join([chr(c) for c in np.packbits(corr)])
    text2 = [ (c==d, d) for c, d in zip(text, ss2)]
    
    color_print(text1, text2, p)
