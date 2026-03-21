import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import time

# ================== 模型参数 ==================
Lx, Ly = 80, 80
dx = 1.0
dt = 0.2
T = 10000                    # 延长模拟时间，观察长期行为
nt = int(T/dt)

# 降低初始文明密度
np.random.seed(42)
C = np.random.rand(Lx, Ly) * 0.005   # 清理者初始极低
H = np.random.rand(Lx, Ly) * 0.02    # 隐藏者
N = np.random.rand(Lx, Ly) * 0.05    # 垃圾文明
S = np.ones((Lx, Ly)) * 3.0           # 初始资源提高

# 扩散系数
D_C = 0.7
D_H = 0.1
D_N = 0.2

# 相互作用参数
beta_CH = 0.2                # 捕食效率
p_H_base = 0.25          # 基础被探测概率
alpha_CC = 0.02               # 清理者战争损耗（保持低值）

# 转化参数
tau_N = 0.1
tau_H = 0.09

# 出生率参数（密度制约）
rho_C = 0.08                  # 基础出生率
rho_H = 0.06
rho_N = 0.02
C_capacity = 1.2       # 清理者局部密度上限（用于密度制约）
H_capacity = 0.5
N_capacity = 1.0

mu = 0.02                    # 基础死亡率

# 资源参数
r = 0.15                      # 再生率
K = 6.0                       # 环境承载力
delta = 0.09                   # 文明消耗率
S_min = 4.0                    # 资源压力阈值

# 探测半径
R = 4
x = np.arange(-R, R+1)
y = np.arange(-R, R+1)
X, Y = np.meshgrid(x, y)
mask = (X**2 + Y**2) <= R**2
mask = mask.astype(float)
mask /= mask.sum()

# 技术爆炸参数（大幅降低）
tech_prob = 0.0001 * dt
tech_strength = 1.0

# ================== 辅助函数 ==================
def nonlocal_avg(u):
    return convolve(u, mask, mode='constant', cval=0.0)

def laplacian(u):
    # 五点差分，反射边界通过手动修正简化（用周期近似，但网格较大）
    return (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) +
            np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4*u) / dx**2

# ================== 模拟主循环 ==================
C_total, H_total, N_total = [], [], []
S_avg_list = []
time_points = []

start = time.time()

for n in range(nt):
    C_avg = nonlocal_avg(C)
    H_avg = nonlocal_avg(H)

    # 隐藏者被探测概率（随隐藏者密度略增，但基础值很低）
    p_H = p_H_base * (1 + 0.1 * H_avg)
    p_H = np.clip(p_H, 0, 0.5)   # 上限0.5

    # 捕食与战争
    predation = beta_CH * p_H * H * C_avg
    war = alpha_CC * C * C_avg

    C -= war * dt
    H -= predation * dt

    # 资源压力
    P = np.maximum(0, 1 - S / S_min)

    # 转化
    trans_N_to_C = tau_N * P * N
    trans_H_to_C = tau_H * P * H
    C += (trans_N_to_C + trans_H_to_C) * dt
    N -= trans_N_to_C * dt
    H -= trans_H_to_C * dt

    # 技术爆炸
    tech = np.random.rand(Lx, Ly) < tech_prob
    C += tech * tech_strength * (N + H) * dt
    N -= tech * tech_strength * N * dt
    H -= tech * tech_strength * H * dt

    # 清理收益：捕食转化为资源增加和清理者适度增长（大幅降低）
    resource_gain = predation * dt * 0.5   # 资源增益
    S += resource_gain
    C_gain = predation * dt * 0.2          # 清理者直接增殖收益降低
    C += C_gain

    # 出生率（密度制约）
    fS = S / (S + 1.0)                     # 资源影响因子
    # 密度制约项：(1 - u / capacity)，确保非负
    C_birth = rho_C * C * fS * np.maximum(0, 1 - C / C_capacity)
    H_birth = rho_H * H * fS * np.maximum(0, 1 - H / H_capacity)
    N_birth = rho_N * N * fS * np.maximum(0, 1 - N / N_capacity)
    C += C_birth * dt
    H += H_birth * dt
    N += N_birth * dt

    # 基础死亡率
    C -= mu * C * dt
    H -= mu * H * dt
    N -= mu * N * dt

    # 扩散
    C += D_C * laplacian(C) * dt
    H += D_H * laplacian(H) * dt
    N += D_N * laplacian(N) * dt

    # 非负
    C = np.maximum(C, 0)
    H = np.maximum(H, 0)
    N = np.maximum(N, 0)

    # 资源演化
    S += r * S * (1 - S/K) * dt
    total_pop = C + H + N
    S -= delta * total_pop * dt
    S = np.maximum(S, 0)

    # 记录
    if n % 100 == 0:
        C_total.append(np.sum(C))
        H_total.append(np.sum(H))
        N_total.append(np.sum(N))
        S_avg_list.append(np.mean(S))
        time_points.append(n * dt)

    if n % 2000 == 0:
        print(f"Step {n}, time {n*dt:.0f}, C:{np.sum(C):.1f}, H:{np.sum(H):.1f}, N:{np.sum(N):.1f}, S:{np.mean(S):.2f}")

print(f"Simulation finished in {time.time()-start:.1f}s")

# ================== 绘图 ==================
plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
plt.plot(time_points, C_total, 'r-', label='C')
plt.plot(time_points, H_total, 'b-', label='H')
plt.plot(time_points, N_total, 'g-', label='N')
plt.xlabel('Time')
plt.ylabel('Total population')
plt.legend()
plt.grid(True)
plt.title('Population dynamics')

plt.subplot(2,2,2)
plt.plot(time_points, S_avg_list, 'orange')
plt.xlabel('Time')
plt.ylabel('Average resource S')
plt.grid(True)
plt.title('Resource evolution')

# 最后时刻的空间分布
plt.subplot(2,2,3)
im = plt.imshow(C.T, origin='lower', cmap='Reds', vmin=0, vmax=0.5)
plt.colorbar(im)
plt.title(f'Cleaner C at t={nt*dt:.0f}')

plt.subplot(2,2,4)
im = plt.imshow(H.T, origin='lower', cmap='Blues', vmin=0, vmax=0.5)
plt.colorbar(im)
plt.title(f'Hider H at t={nt*dt:.0f}')

plt.tight_layout()
plt.savefig('dark_forest_v3.png', dpi=150)
plt.show()