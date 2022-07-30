- *Impl Merkle Tree following RFC6962*


- **A.代码说明**



![121](https://user-images.githubusercontent.com/105535337/181878030-7446a920-5062-4dd2-a5e5-94e03fdefcaa.png)


代码为Python，我们参考了RFC6962，对于每个数据块都找到对应的路径来判断数据，根据上图所示结构，实现时从下往上实现即可，当块为奇数时需要特殊处理

其中代码已经标记了注释


- **B.运行指导**


![image](https://user-images.githubusercontent.com/105535337/181878162-9abb2a88-537a-42f0-be22-d759eb1528d5.png)


首先我们生成100000个节点的树，然后选取随机消息进行验证，并且输出从最低到根节点的路径，最后使用proof node去验证。


- **C.运行截图**


![image](https://user-images.githubusercontent.com/105535337/181878210-cfe98178-d488-4f6d-ae31-fb8196882f65.png)
