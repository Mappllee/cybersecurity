#sm3

vi = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
 
t = [0x79cc4519, 0x7a879d8a]
MAX = 2**32

def Int2Bin(a, k):
    res = list(bin(a)[2:])
    for i in range(k-len(res)):
        res.insert(0, '0')
    return ''.join(res)

def LoopLeftShift(a, k):
    res = list(Int2Bin(a, 32))
    for i in range(k):
        temp = res.pop(0)
        res.append(temp)
    return int(''.join(res), 2)
 

def fillFunction(message):
    message =  bin(int(message, 16))[2:]
    for i in range(4):
        if (len(message)%4 == 0):
            break
        else:
            message = '0'+message
    length = len(message)
    k = 448 - (length+1)%512
    if (k < 0):     #k是满足等式的最小非负整数
        k += 512
    addMessage = '1' + '0'*k + Int2Bin(length, 64)
    message += addMessage
    return message
 
def IterFunction(message):
    n = int(len(message)/512)
    v = []
    v.append(Int2Bin(vi, 256))
    for i in range(n):
        w, w1 = msgExten(message[512*i:512*(i+1)])
        temp = CF(v[i], message[512*i:512*(i+1)], w, w1)
        temp = Int2Bin(temp, 256)
        v.append(temp)
    return v[n]

def Group(m):
    n = len(m) / 128
    M = []
    for i in range(int(n)):
        M.append(m[0 + 128 * i:128 + 128 * i])
    return M
def Expand(M, n):
    W = []
    W_ = []
    for j in range(16):
        W.append(int(M[n][0 + 8 * j:8 + 8 * j], 16))
    for j in range(16, 68):
        W.append(P1(W[j - 16] ^ W[j - 9] ^ LoopLeftShift(W[j - 3], 15)) ^ LoopLeftShift(W[j - 13], 7) ^ W[j - 6])
    for j in range(64):
        W_.append(W[j] ^ W[j + 4])
    Wstr = ''
    W_str = ''
    for x in W:
        Wstr += (hex(x)[2:] + ' ')
    for x in W_:
        W_str += (hex(x)[2:] + ' ')
    return W, W_
def msgExten(b):
    w = []
    w1 = []
    for i in range(16):
        temp = b[i*32:(i+1)*32]
        w.append(int(temp, 2))
    for j in range(16, 68, 1):
        factor1 = LoopLeftShift(w[j-3], 15)
        factor2 = LoopLeftShift(w[j-13], 7)
        factor3 = P1(w[j-16]^w[j-9]^factor1)
        factor4 = factor3^factor2^w[j-6]
        w.append(factor4)
    for j in range(64):
        factor1 = w[j]^w[j+4]
        w1.append(factor1)
    return w, w1

def P0(X):
    return X^LoopLeftShift(X, 9)^LoopLeftShift(X, 17)
def P1(X):
    return X^LoopLeftShift(X, 15)^LoopLeftShift(X, 23)
def T(j):
    if j <= 15:
        return t[0]
    else:
        return t[1]
def FF(X, Y, Z, j):
    if j <= 15:
        return X^Y^Z
    else:
        return (X&Y)|(X&Z)|(Y&Z)
def GG(X, Y, Z, j):
    if j <= 15:
        return X^Y^Z
    else:
        return (X&Y)|(un(X)&Z)


def un(a):
    a = Int2Bin(a, 32)
    b = ''
    for i in a:
        if i == '0':
            b += '1'
        else:
            b+= '0'
    return int(b, 2)
def C1F(V, M, i):
    A, B, C, D, E, F, G, H = V[i]
    W, W_ = Expand(M, i)
    for j in range(64):
        SS1 = LoopLeftShift((LoopLeftShift(A, 12) + E + LoopLeftShift(T(j), j % 32)) % (2 ** 32), 7)
        SS2 = SS1 ^ LoopLeftShift(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W_[j]) % (2 ** 32)
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) % (2 ** 32)
        D = C
        C = LoopLeftShift(B, 9)
        B = A
        A = TT1
        H = G
        G = LoopLeftShift(F, 19)
        F = E
        E = P0(TT2)
    a, b, c, d, e, f, g, h = V[i]
    V_ = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]
    return V_
def CF(vi, bi, w, w1):
    A = []
    for i in range(8):
        temp = vi[32*i:32*(i+1)]
        A.append(int(temp, 2))
    for j in range(64):
        factor1 = LoopLeftShift(A[0], 12)
        factor2 = LoopLeftShift(T(j), j%32)
        SS1 = LoopLeftShift((factor1+A[4]+factor2)%MAX, 7)
        factor3 = LoopLeftShift(A[0], 12)
        SS2 = SS1^factor3
        TT1 = (FF(A[0], A[1], A[2], j) + A[3] + SS2 + w1[j])%MAX
        TT2 = (GG(A[4], A[5], A[6], j) + A[7] + SS1 + w[j])%MAX
        A[3] = A[2]
        A[2] = LoopLeftShift(A[1], 9)
        A[1] = A[0]
        A[0] = TT1
        A[7] = A[6]
        A[6] = LoopLeftShift(A[5], 19)
        A[5] = A[4]
        A[4] = P0(TT2)
    temp = Int2Bin(A[0], 32)+Int2Bin(A[1], 32)+Int2Bin(A[2], 32)+\
    Int2Bin(A[3], 32)+Int2Bin(A[4], 32)+Int2Bin(A[5], 32)+\
    Int2Bin(A[6], 32)+Int2Bin(A[7], 32)
    temp = int(temp, 2)
    return temp^int(vi, 2)

def SM3(message):
    m = fillFunction(message)  # 填充消息

    Vn = IterFunction(m)  # 迭代
    return hex(int(Vn,2))[2:]
def len_ext_atk(msg, ext, n):
    h_m = SM3(msg)              # H(m)
    Hm = []
    for i in range(8):
        Hm.append(int(h_m[i*8:i*8+8], 16))
    len_e = hex((n + len(ext))*4)[2:]   # 总消息长度
    len_e = (16 - len(len_e)) * '0' + len_e
    ext = ext + '8'
    if len(ext) % 128 > 112:
        ext = ext + '0' * (128 - len(ext) % 128 + 112) + len_e
    else:
        ext = ext + '0' * (112 - len(ext) % 128) + len_e
    ext_g = Group(ext)      # 数据分组
    n_g = len(ext_g)            # 分组个数
    V = [Hm]
    for i in range(n_g):
        V.append(C1F(V, ext_g, i))
    res = ''
    for x in V[n_g]:
        res += hex(x)[2:]
    return res

if __name__ == '__main__':
    message = '123456'     # 消息
    extend = '789'         # 扩展
    if len(message) % 128 < 112:
        n = (int(len(message) / 128) + 1) * 128  
    else:
        n = (int(len(message) / 128) + 2) * 128  
    len_m = hex(len(message)*4)[2:]
    len_m = (16 - len(len_m)) * '0' + len_m  # 消息长度
    pad = n - len(message) - 16 - 1              
    new_m = message + '8' + pad*'0' + len_m + extend    
    res_new = SM3(new_m)
    res = len_ext_atk(message, extend, n)
    print("new msghash:", res_new)
    print("lenatk_res:", res)
    if res_new == res:
        print("success!")
    else:
        print("false!")
