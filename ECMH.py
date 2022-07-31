import sys
import math
import time
import hashlib
import binascii
from gmpy2 import invert
from random import randint

#SHA256算法
def hash256(m):
    return hashlib.sha256(m.encode()).hexdigest()

#secp256k1曲线
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
G = [Gx, Gy]

# 椭圆曲线上的加法
def calculate_p_q(x,y):
    x1=x[0]
    y1=x[1]
    x2=y[0]
    y2=y[1]
    if x1 == x2 and y1 == p - y2:
        return False
    if x1 != x2:
        r = ((y2 - y1) * invert(x2 - x1, p)) % p  # get_inverse函数用于求模逆
    else:
        r = (((3 * x1 * x1 + a) % p) * invert(2 * y1, p)) % p

    x = (r * - x1 - x2) % p
    y = (r * (x1 - x) - y1) % p
    return x, y


# 椭圆曲线上的点乘
def calculate_np(x, y, k):
    k = k % p
    k = bin(k)[2:]
    rx, ry = x, y
    for i in range(1, len(k)):
        rx, ry = calculate_p_q(rx, ry, rx, ry)
        if k[i] == '1':
            rx, ry = calculate_p_q(rx, ry, x, y)
    return [rx % p, ry % p]

#shanks算法
def Shanks(n, p):
    def legendre(a, p):
        return pow(a, (p - 1) // 2, p)

    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def ECMH(message):
    while(1):
        e=hash256(message)
        e=int(e,16)
        tmp = (e**3 + a*e + b)%p
        #利用shanks算法求解离散对数问题
        y=Shanks(tmp, p)
        if(y==-1):
            continue
        return tmp, y

def ECMH_(Set):
     t=0
     V=[]
     for i in Set:
          e=hash256(i)
          e=int(e,16)
          tmp = (e ** 3 + a * e + b) % p
          # 若此哈希值在椭圆曲线上有解，则通过二次剩余将其求出
          y = Shanks(tmp, p)
          if (y == -1):
               continue
          V.append([tmp, y])
          t=t+1
     for i in range(1,t):
          ecmh=calculate_p_q(V[0],V[i])
     return ecmh[0],ecmh[1]



message='2022'
x,y=ECMH(message)
print("单个数哈希之后的值为：",x)
print("单个数哈希之后的值为：",y)

set=['2020','2021','2022']
x1,y1=ECMH_(set)
print("多个数哈希之后的值为：",x1)
print("多个数哈希之后的值为：",y1)
