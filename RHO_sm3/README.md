- *implement the Rho method of reduced SM3*


- **A.代码说明**

RHO方法用来进行生日攻击是一种边碰撞边存储的方法，可以提高攻击效率，并且节省空间。

```python
            
  def rho_method(exm):
    num = int(exm/4)                # 因为要转化为16进制位数，所以做切割
    x = hex(random.randint(0, 2**(exm+1)-1))[2:]
    x_a = SM3(x)            
    x_b = SM3(x_a)               # 因为有模n的存在，所以，序列最后一定会陷入循环中
    i = 1
    while x_a[:num] != x_b[:num]:
        i += 1
        x_a = SM3(x_a)             
        x_b = SM3(SM3(x_b))      # 序列中距离为k的两项的差，一定为前面任意距离为k的两项的差的倍数
    x_b = x_a          
    x_a = x            
    for j in range(i):
        if SM3(x_a)[:num] == SM3(x_b)[:num]:
            return SM3(x_a)[:num], x_a, x_b
        else:
            x_a = SM3(x_a)       #序列中任意两数的差，也一定可以转换为相邻两个数的差的倍数。
            x_b = SM3(x_b)
```


- **B.运行指导**


![image](https://user-images.githubusercontent.com/105535337/181878497-6e759aa3-70f1-4a75-9f73-f2cd2c06a60a.png)


首先我们使用8bit来验证攻击的正确性，利用rho方法来找到前8bit的碰撞，则总体碰撞同理。

然后输出两个消息以及对应的hash值，可以看出前8bit是相同的。


- **C.运行截图**


![image](https://user-images.githubusercontent.com/105535337/181878560-5e97595a-8a2b-4562-b165-b810c4876d3d.png)


多次进行攻击，每次碰撞均成功，可以验证攻击成功。
