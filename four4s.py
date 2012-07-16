from math import sqrt
import re

nonfactnum = re.compile("4*\.4+")

def can_apply(op1, val):
    if op1 == 'fact':
        m = nonfactnum.search(val)
        if m != None:
            return False
    return True

fact_tbl = {1:1}

def fact(n):
    if fact_tbl.has_key(n): return fact_tbl[n]

    if n-int(n) != 0: raise ValueError("invalid arg for fact: " + str(n))
    if n > 50: raise ValueError("invalid arg for fact: " + str(n)) 
    fact_tbl[n] = n * fact(n-1)
    return fact_tbl[n]

def mysqrt(n):
    if n < 0: raise ValueError("invalid arg for sqrt: " + str(n))
    return sqrt(n)


def get_score(e):
    plus_count  = 0
    minus_count = 0
    div_count = 0
    mult_count = 0
    fact_count = 1

unary_ops = [ 'fact', 'mysqrt']
binary_ops= ['+', '*', '/', '-']


def opcount(e):
    c = 0
    for x in e:
        if x in binary_ops: c += 1
    return c

B = {}

for n in range(1, 5):
    B[n] = []
    t = reduce(lambda x,y:x+y, ["4" for x in range(1,n+1)], "")
    print t
    for pos in range(0, n+1):
        B[n].append(t[0:pos] + "." + t[pos:])

for bk in B.keys():
    print bk, "--->"
    for bn in B[bk]:
        print "\t", bn


U1 = {}
U = {}

for n in range(1, 5):
    U[n] = []
    for bn in B[n]:
        U[n].append(bn)

for n in range(1, 5):
    U1[n] = []
    for op1 in unary_ops:
        for bn in B[n]:
            if can_apply(op1, bn): 
                U1[n].append(op1 + "(" + bn + ")")
                U[n].append(op1 + "(" + bn + ")")

"""
for n in range(1, 5):
    for op1 in unary_ops:
        for u1 in U1[n]:
            if can_apply(op1, u1): 
                U[n].append(op1 + "(" + u1 + ")")
"""

for uk in U.keys():
    print uk, "--->"
    for un in U[uk]:
        print "\t", un

S={}

for n in range(1, 5):
    S[0,n] = []
    for un in U[n]:
        S[0, n].append(un)

S1_base = {}
for n in range(2, 5):
    S1_base[n] = []
    for k1 in range(1, n):
        k2 = n-k1
        for op2 in binary_ops:
            for s0k1 in S[0, k1]:
                for s0k2 in S[0, k2]:
                    S1_base[n].append(s0k1 + op2 + s0k2)
                    #S1_base[n].append("(" + s0k1 + op2 + s0k2 + ")")

for n in range(2, 5):
    S[1,n] = [b for b in S1_base[n]]
    for b in S1_base[n]:
        for op1 in unary_ops:
            if can_apply(op1, b):
                S[1,n].append(op1 + "(" + b + ")")


Si_base = {}

for x in S1_base.keys():
    Si_base[1, x] = S1_base[x]

for i in range(2, 4):
    for n in range(i+1, 5):
        Si_base[i, n] = []
        for m in range(0, i):
            for k1 in range(m+1, i):
                k2 = n - k1
                if k2 > i-1-m:
                    for op2 in binary_ops:
                        for smk1 in S[m, k1]:
                            for smk2 in Si_base[i-1-m, k2]:
                                Si_base[i,n].append(smk1 + op2 + smk2)
                                
                                #Si_base[i,n].append("(" + smk1 + op2 + smk2 + ")")
                                opcount1 = opcount(smk1)
                                opcount2 = opcount(smk2)
                                if opcount1 > 0 and opcount2 > 0:
                                    Si_base[i,n].append("(" + smk1 + ")" + op2 + smk2)
                                    Si_base[i,n].append("(" + smk1 + ")" + op2 + "(" + smk2 + ")")
                                    Si_base[i,n].append(smk1 + op2 + "(" + smk2 + ")")
                                elif opcount1 == 0:
                                    Si_base[i,n].append("(" + smk1 + ")" + op2 + smk2)
                                elif opcount2 ==0:
                                    Si_base[i,n].append(smk1 + op2 + "(" + smk2 + ")")
                                

for i in range(2, 4):
    for n in range(i+1, 5):
        S[i, n] = [b for b in Si_base[i, n]]
        for b in Si_base[i,n]:
            for op1 in unary_ops:
                if can_apply(op1, b): S[i,n].append(op1 + "(" + b + ")")

#print "Printing S..."

#for sk in S.keys():
#    print sk, "--->"
#    for sn in S[sk]:
#        print "\t", sn

exprs=[]

for opc in range(0, 4):
    for s in S[opc, 4]:
        exprs.append(s)

todo = [x for x in range(1, 51)]

print todo
results = {}

for expr in exprs:
    print "................", expr
    try:
        x  = eval(expr)
        v=int(x)
        if x-v != 0: continue

        if v in todo: del(todo[v])
        if v not in results.keys():
            results[v] = []
        results[v].append(expr)
        #print expr, "=", v
    except:
        continue

    if len(todo) == 0: break

for k in range(1, 51):
    if results.has_key(k):
        print k, "--->"
        for e in results[k]:
            print "\t", e
