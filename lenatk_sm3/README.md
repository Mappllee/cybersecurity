- *implement length extension attack for SM3, SHA256, etc*


- **A.代码说明**

我们对SM3进行长度扩展攻击



```python
            
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
```


- **B.运行指导**


![image](https://user-images.githubusercontent.com/105535337/181878991-8add9ffa-4511-4e3a-baaf-6eab3481a01f.png)


首先我们确定消息，然后确定扩展，根据消息及扩展长度进行填充，最后实现长度扩展攻击。




- **C.运行截图**


![image](https://user-images.githubusercontent.com/105535337/181879019-9bf8e10f-86c0-431d-9098-4cbe7a69c760.png)


可以看到，我们对于任意的消息及扩展均实现攻击。
