import pwn
import base64
import sys

def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def find_quadratic_residue(arr, p):
    def find_quadratic_residues(a, p):
        return [x for x in range(1, p) if x**2 % p == a]

    for a in arr:
        res = find_quadratic_residues(a, p)
        if len(res) > 0:
            return min(res), a
    raise Exception("No quadratic residue found")

def legendre_symbol(p, ints):
    def leg(a, p):
        return pow(a, (p - 1) // 2, p)

    def findSquare(a, p):
        return pow(a, (p + 1) // 4, p)

    for x in ints:
        if leg(x, p) == 1:
            return findSquare(x, p)

def chinese_theorem():
    for x in range(1, 936):
        if x % 5 == 2 and x % 11 == 3 and x % 17 == 5:
            return x;
    raise Exception()

def decrypt_flag(a, p, encFlag):
    flag = ""
    for n in encFlag:
        if pow(n,(p-1)//2,p)==1:
            flag += '1'
        else:
            flag += '0'
    flag
    ls = [chr(int(flag[i:i+8],2)) for i in range(0,len(flag),8)]
    result = ""
    for i in ls:
        result += i
    return result

print(gcd(66528, 52920))
print(gcd_extended(26513, 32321))
print(find_quadratic_residue([14, 6, 11], 29))
print(legendre_symbol())
print(chinese_theorem())
print(decrypt_flag(288260533169915, 1007621497415251, encFlag))
