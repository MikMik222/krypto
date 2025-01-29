from sympy import *
from math import gcd
from random import randint

def generace():
    p = randprime(10**12, 10**13-1)
    q = randprime(10**12, 10**13-1)
    n = p *q
    fin = (p - 1) * (q - 1)
    opakuj = True
    while opakuj:
        e = randint(2,fin-1)
        if gcd(e, fin)==1:
            opakuj = False
    d = pow(e, -1, fin)
    privatniklic = [n,d]
    
    verejnyklic = [n,e]
    return privatniklic, verejnyklic


def sifrovani(ot, d, n):
    cislaot = []
    counter = 0
    temp = []
    result = []
    for i in ot:
        if counter == 7:
            cislaot.append(temp)
            temp = []
            counter = 0
        b = str(bin(ord(i)))[2:]
        temp.append("0"*(11-len(b))+b)
        counter += 1
    if len(temp)>0:
        cislaot.append(temp)
    binarnicislo = ""
    for i in cislaot:
        for j in i:
            binarnicislo += j

        z = int(binarnicislo,2)
        res = pow(z,d,n)
        result.append(res)
        binarnicislo = ""
    return result

def desifrovani(result, e, n):
    res = []
    temp = []
    for i in result:
        if i.isdigit():
            desdek = pow(int(i),e,n)
            binarnicislo = "0"*(77-len(str(bin(desdek)[2:]))) + str(bin(desdek)[2:])
            for i in range(7):
                cislo = int(binarnicislo[i*11:i*11+11],2)
                if cislo != 0:
                    temp.append(chr(cislo))
            res.append(temp)
            temp = []
        else:
            return "Zadán špatný vstup"
    return res