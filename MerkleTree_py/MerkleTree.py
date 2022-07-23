import math
import hashlib
from hashlib import sha256
import random
import sys
import string


def create_merkletree(data):
    depth = math.ceil(math.log2(len(data)) + 1)  # merkle tree深度
    mktree = [[sha256(i.encode()).hexdigest() for i in data]]  # merkle tree的第0层(倒置)
    for i in range(depth - 1):
        len_lay = len(mktree[i])  # 第i层消息块个数
        mkt_lay = [sha256(mktree[i][j * 2].encode() + mktree[i][j * 2 + 1].encode()).hexdigest() for j in
                   range(int(len_lay / 2))]  # merkle tree的第i+1层
        if len_lay % 2 != 0:
            mkt_lay.append(mktree[i][-1])  # 若块数为奇数，则最后一个块直接放入下一层
        mktree.append(mkt_lay)
    return mktree

def create_message(length):
    res = []
    for i in range(length):
        block = [random.choice(string.digits + string.ascii_letters) for i in range(5)]  # 一个消息块长为5
        res.append(''.join(block))
    return res
def verify_node(message,merkletree): 
    message_hash = (hashlib.sha256(message.encode())).hexdigest() 
    try:
        place_message = merkletree[0].index(message_hash) 
    except:
        print("消息不在树中")
    
    depth = len(merkletree) #二叉树深度
    proof = [] #审核节点
    for i in range(depth - 1): 
        if place_message % 2 == 0: 
            if place_message != len(merkletree[i]) - 1:                 proof.append(['0',merkletree[i][place_message + 1]])
        else: 
            proof.append([merkletree[i][place_message - 1],'0'])
        place_message = math.floor(place_message / 2)
        
    return proof

def proof(message,proof_node,root):
    message_hash = (hashlib.sha256(message.encode())).hexdigest() #将消息进行hash用于验证
    for i in proof_node:
        if i[0] == '0':    
            message_hash = hashlib.sha256(message_hash.encode() + i[1].encode()).hexdigest()
        else:
            message_hash = hashlib.sha256(i[0].encode() + message_hash.encode()).hexdigest()
    if message_hash == root:
        print("验证通过")
    else:
        print("验证失败")

   

print("#------------------------------------------------------------#")

message_2 = create_message(100000)
tree_2 = create_merkletree(message_2)
print("已经生成100000节点的树")

place = random.randint(0,99999)
print("选取随机消息:")
print("位置:",place)
print("消息:",message_2[place])


print("#------------------------------------------------------------#")
print("从最低到根节点的路径：")
proof_node = verify_node(message_2[place],tree_2)
for i in proof_node:
    print(i)
print("#------------------------------------------------------------#")
print("使用proof nodes去验证消息：")

proof(message_2[place],proof_node,tree_2[-1][0])
