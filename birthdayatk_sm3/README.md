- *implement the naïve birthday attack of reduced SM3*


- **A.代码说明**

使用生日攻击来寻找碰撞，对L bit长的串进行攻击，则需要进行2^{2/l}次搜索，则可以确定原像空间。



```python
            
def bir_atk(exm):
    num = int(2 ** (exm / 2))     # 求得原像空间的大小
    ans = [-1] * 2**exm       
    for i in range(num):
        temp = int(SM3(str(i))[0:int(exm / 4)], 16)
        if ans[temp] == -1:      #进行判断，当结果不为-1时，返回产生碰撞的消息的16进制值
            ans[temp] = i
        else:
            return hex(temp), i, ans[temp]     #否则，将i赋值给当前碰撞的值。
```


- **B.运行指导**


![image](https://user-images.githubusercontent.com/105535337/181878846-26012be3-d00d-41d4-8c90-ec6e2685ef85.png)


首先我们求得原像空间大小，然后在空间中寻找碰撞




- **C.运行截图**


![image](https://user-images.githubusercontent.com/105535337/181878869-6755d4f3-f026-4b98-854b-9efc54ea7317.png)


多次进行攻击，每次碰撞均成功，可以验证攻击成功。
