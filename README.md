# ECMH

1、原理解释：

（1）哈希函数使用SHA256函数，椭圆曲线使用标准secp256k1曲线参数：

![image](https://user-images.githubusercontent.com/108848022/182010042-99a19ad7-996a-40d7-b9fe-8535a85bb5bd.png)

（2）def calculate_p_q(x,y)：表示椭圆曲线上的加法

![image](https://user-images.githubusercontent.com/108848022/182010055-f679bf9d-6a4d-41ca-8cd4-a047121f930a.png)

（3）def calculate_np(x, y, k)：表示椭圆曲线上的点乘

![image](https://user-images.githubusercontent.com/108848022/182010062-4854f367-7138-4c36-9093-7561661a550f.png)

（4）shanks算法参考文献为：https://blog.csdn.net/weixin_44617902/article/details/112785051

2、ECMH原理：

![image](https://user-images.githubusercontent.com/108848022/182010135-94dfa747-a778-44d2-a557-dcb613b90a68.png)

（1）ECMH体系表示：将哈希后的数映射到椭圆曲线上，例如针对字符串‘2022’进行哈希，哈希后的值改为10进制后作为横坐标，看是否能映射到椭圆曲线上。若此哈希值在椭圆曲线上有解，则通过二次剩余将其求出。

（2）若能将hash值映射到椭圆曲线上，即可得到对应的横纵坐标，即为单个元素进行ECMH的输出结果。

（3）若有多个hash值，则分别映射到椭圆曲线，得到多个对应的横纵坐标（如果无法映射则跳过不予考虑），最终将所有横纵坐标相加（利用calculate_p_q函数）即可得到多个元素ECMH的输出结果。

3、结果截图：

（1）单个数进行ECMH之后的结果为：

![image](https://user-images.githubusercontent.com/108848022/182010110-ab4e7503-3462-4a64-8eed-d6de082e5b3a.png)

（2）多个数进行ECMH之后的结果为：

![image](https://user-images.githubusercontent.com/108848022/182010120-e3980e6b-429e-47fe-afd1-a8451d2d91b7.png)

