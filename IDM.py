import numpy as np
import math
import matplotlib.pyplot as plt

# 时间定义
timeinterval = 1
totaltime = 100
t = np.linspace(0, totaltime, int(totaltime/timeinterval)+1)

# IDM模型参数定义（高速情况）
a = 1
b = 1.5
s0 = 2
v0 = 120/3.6
T = 1
delta = 4

# 前车加速度定义
a_leading = np.zeros(int(totaltime/timeinterval)+1)
for i in range(1,int(2/timeinterval)+1):
    a_leading[int(20/timeinterval)+i] = -2
    a_leading[int(40/timeinterval)+i] = 2

# 前车速度
v_leading = np.zeros(int(totaltime/timeinterval)+1,dtype=float)
v_leading[0] = 20 # 前车初速度
for i in range(0, int(totaltime/timeinterval)):
    v_leading[i+1] = v_leading[i] + a_leading[i] * timeinterval # 计算速度公式

# 前车轨迹
x_leading = np.zeros(int(totaltime/timeinterval)+1,dtype=float)
x_leading[0] = 28 # 0s时前车位置
for i in range(0, int(totaltime/timeinterval)):
    # 计算距离公式
    x_leading[i+1] = x_leading[i] + v_leading[i] * timeinterval + 0.5 * a_leading[i] * timeinterval * timeinterval

# 后车计算参数定义
x_following = np.zeros(int(totaltime/timeinterval)+1,dtype=float)
s = np.zeros(int(totaltime/timeinterval)+1,dtype=float)
s_safe = np.zeros(int(totaltime/timeinterval)+1,dtype=float)
a_following = np.zeros(int(totaltime/timeinterval)+1,dtype=float)
v_following = np.zeros(int(totaltime/timeinterval)+1,dtype=float)
v_following[0] = 20

# 后车各项参数计算
for i in range(0, int(totaltime/timeinterval)):
    # 计算两车的间距
    s[i] = x_leading[i] - x_following[i]
    # 计算后车安全距离
    s_safe[i] = s0 + max(0, v_following[i]*T+v_following[i]*(v_following[i]-v_leading[i])/(2*math.sqrt(a*b)))
    # 计算后车加速度
    a_following[i] = a * (1-math.pow(v_following[i]/v0, delta)-math.pow(s_safe[i]/s[i], 2))
    # 计算后车速度
    v_following[i+1] = v_following[i] + a_following[i] * timeinterval
    # 计算后车轨迹
    x_following[i+1] = x_following[i] + v_following[i]*timeinterval + 0.5*a_following[i]*timeinterval*timeinterval

# 补足最后时刻两车的间距
s[int(totaltime/timeinterval)] = x_leading[int(totaltime/timeinterval)] - x_following[int(totaltime/timeinterval)]

# 作图输出结果
# 字体
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(12)

# 两车行驶轨迹
plt.subplot(221)
plt.plot(t, x_leading, label="前车")
plt.plot(t, x_following, label="后车")
plt.xlim(0, 110)
plt.ylim(0, 2000)
plt.xlabel("时间（s）")
plt.ylabel("行驶距离（m）")
plt.legend(loc="upper left")
plt.title("两车行驶轨迹")

# 两车加减速度
plt.subplot(222)
plt.plot(t, a_leading, label="前车")
plt.plot(t, a_following, label="后车")
plt.xlim(0, 110)
plt.xlabel("时间（s）")
plt.ylabel("加速度（m/s2）")
plt.legend(loc="upper right")
plt.title("两车加减速度")

# 两车间距
plt.subplot(212)
plt.plot(t, s)
plt.xlim(0, 110)
plt.ylim(0, 30)
plt.xlabel("时间（s）")
plt.ylabel("间距（m）")
plt.title("两车间距")

plt.tight_layout()
plt.suptitle("IDM(" + str(timeinterval) + "s)")
plt.savefig("IDM模型输出结果（时间间隔为" + str(timeinterval) + "s）.png")
plt.show()
