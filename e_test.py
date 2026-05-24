import numpy as np
import heapq
import sys
import time

# ========== 强制刷新输出 ==========
def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

# ========== 参数 ==========
FLOORS = 100
ELEVATORS = 2
SIM_TIME = 3600
ARRIVAL_RATE = 0.2
MEAN_DST, STD_DST = 65, 15
LOW_DST_THRESHOLD = 30
MAX_WAIT_LOW = 60.0
ALPHA = 15.0
CAPACITY = 15

TIME_PER_FLOOR = 1.0
DOOR_OPEN_CLOSE = 3.0

# ========== 乘客生成（向量化，避免死循环） ==========
def generate_passengers():
    # 泊松过程
    n = int(ARRIVAL_RATE * SIM_TIME * 1.2)
    intervals = np.random.exponential(1.0 / ARRIVAL_RATE, n)
    arrival_times = np.cumsum(intervals)
    arrival_times = arrival_times[arrival_times <= SIM_TIME]
    # 生成目的楼层（截断正态）
    dsts = np.random.normal(MEAN_DST, STD_DST, len(arrival_times))
    dsts = np.clip(np.round(dsts), 1, FLOORS).astype(int)
    # 避免起始=目的
    for i in range(len(dsts)):
        if dsts[i] == 1:
            dsts[i] = 2
    passengers = [(arrival_times[i], 1, dsts[i]) for i in range(len(arrival_times))]
    return passengers

# ========== 电梯类 ==========
class Elevator:
    __slots__ = ('idx', 'floor', 'direction', 'stops', 'onboard', 'idle_floor', 'total_passengers', 'total_travel_time')
    def __init__(self, idx, idle_floor):
        self.idx = idx
        self.floor = 1.0
        self.direction = 0
        self.stops = []          # 计划停靠的楼层
        self.onboard = []        # (dst, board_time)
        self.idle_floor = idle_floor
        self.total_passengers = 0
        self.total_travel_time = 0.0

# ========== 调度器基类 ==========
class Scheduler:
    def __init__(self, elevators):
        self.elev = elevators
        self.clock = 0.0
        self.events = []           # (time, type, data)
        self.passengers = []       # (arrival, src, dst)
        self.waiting = []          # (arrival, src, dst, idx)
        self.pstates = {}          # idx -> dict
        self.stats = {'all': [], 'low_dst': [], 'high_dst': []}
        self.event_counter = 0

    def add_passenger(self, arrival, src, dst):
        idx = len(self.passengers)
        self.passengers.append((arrival, src, dst))
        self.pstates[idx] = {'arrival': arrival, 'src': src, 'dst': dst,
                             'elev': None, 'board_time': None}
        heapq.heappush(self.events, (arrival, 'arrival', idx))

    def _next_stop(self, e):
        if not e.stops:
            return None
        return min(e.stops, key=lambda f: abs(f - e.floor))

    def schedule_elevator(self, e):
        nxt = self._next_stop(e)
        if nxt is None:
            # 空闲时移动到空闲层
            if abs(e.floor - e.idle_floor) > 0.1:
                e.stops.append(e.idle_floor)
                nxt = e.idle_floor
            else:
                e.direction = 0
                return
        if nxt > e.floor:
            e.direction = 1
        elif nxt < e.floor:
            e.direction = -1
        else:
            e.direction = 0
        travel = abs(nxt - e.floor) * TIME_PER_FLOOR
        heapq.heappush(self.events, (self.clock + travel, 'arrive', (e.idx, nxt)))

    def on_arrive(self, e_idx, floor):
        e = self.elev[e_idx]
        e.floor = float(floor)

        # 开门
        self.clock += DOOR_OPEN_CLOSE / 2.0

        # 下车
        new_onboard = []
        for dst, bt in e.onboard:
            if dst == floor:
                travel = self.clock - bt
                e.total_travel_time += travel
            else:
                new_onboard.append((dst, bt))
        e.onboard = new_onboard

        # 上车（容量限制）
        to_board = [idx for idx, st in self.pstates.items()
                    if st['elev'] == e.idx and st['board_time'] is None and st['src'] == floor]
        to_board.sort(key=lambda idx: self.pstates[idx]['arrival'])
        for idx in to_board:
            if len(e.onboard) >= CAPACITY:
                break
            st = self.pstates[idx]
            wait = self.clock - st['arrival']
            self.stats['all'].append(wait)
            if st['dst'] <= LOW_DST_THRESHOLD:
                self.stats['low_dst'].append(wait)
            else:
                self.stats['high_dst'].append(wait)
            st['board_time'] = self.clock
            e.onboard.append((st['dst'], self.clock))
            e.total_passengers += 1
            if st['dst'] not in e.stops:
                e.stops.append(st['dst'])

        # 移除当前停靠
        if floor in e.stops:
            e.stops.remove(floor)

        # 关门
        self.clock += DOOR_OPEN_CLOSE / 2.0

        # 继续移动
        self.schedule_elevator(e)

    def on_arrival(self, idx):
        arrival, src, dst = self.passengers[idx]
        self.waiting.append((arrival, src, dst, idx))
        self.dispatch()

    def dispatch(self):
        assigned = True
        while assigned:
            assigned = False
            for i, (arr, src, dst, idx) in enumerate(self.waiting):
                chosen = self.select_elevator(src, dst)
                if chosen is not None:
                    self.pstates[idx]['elev'] = chosen.idx
                    if src not in chosen.stops:
                        chosen.stops.append(src)
                    if chosen.direction == 0 and len(chosen.stops) == 1:
                        self.schedule_elevator(chosen)
                    self.waiting.pop(i)
                    assigned = True
                    break

    def select_elevator(self, src, dst):
        raise NotImplementedError

    def run(self, passengers):
        print_flush("  添加乘客事件...")
        for p in passengers:
            self.add_passenger(*p)
        print_flush(f"  共 {len(passengers)} 个乘客，开始事件循环...")

        last_print = 0
        while self.events:
            t, typ, data = heapq.heappop(self.events)
            if t < self.clock:
                continue
            self.clock = t
            self.event_counter += 1

            if self.event_counter - last_print >= 1000:
                boarded = sum(1 for st in self.pstates.values() if st['board_time'] is not None)
                print_flush(f"    事件 {self.event_counter}: 时间={self.clock:.1f}s, 已登梯={boarded}/{len(self.passengers)}")
                last_print = self.event_counter

            if typ == 'arrival':
                self.on_arrival(data)
            else:
                self.on_arrive(*data)

        # 未登梯乘客（理论不应有，但防御）
        for st in self.pstates.values():
            if st['board_time'] is None:
                wait = self.clock - st['arrival']
                self.stats['all'].append(wait)
                if st['dst'] <= LOW_DST_THRESHOLD:
                    self.stats['low_dst'].append(wait)
                else:
                    self.stats['high_dst'].append(wait)

        return self.stats

# ========== Naive 调度 ==========
class NaiveScheduler(Scheduler):
    def __init__(self, elevators):
        for e in elevators:
            e.idle_floor = 1
        super().__init__(elevators)

    def select_elevator(self, src, dst):
        best = None
        best_score = float('inf')
        for e in self.elev:
            dist = abs(e.floor - src)
            penalty = len(e.stops) * 10
            est = dist * TIME_PER_FLOOR + penalty
            if e.direction != 0:
                if (e.direction == 1 and src < e.floor) or (e.direction == -1 and src > e.floor):
                    est += 20
            if est < best_score:
                best_score = est
                best = e
        return best

# ========== Proposed 调度 ==========
class ProposedScheduler(Scheduler):
    def __init__(self, elevators):
        elevators[0].idle_floor = 65
        elevators[1].idle_floor = 1
        super().__init__(elevators)

    def dispatch(self):
        # 强制干预：低目的地超时乘客
        urgent_idx = None
        for i, (arr, src, dst, idx) in enumerate(self.waiting):
            if dst <= LOW_DST_THRESHOLD and (self.clock - arr) > MAX_WAIT_LOW:
                urgent_idx = i
                break
        if urgent_idx is not None:
            arr, src, dst, idx = self.waiting.pop(urgent_idx)
            best_e = min(self.elev, key=lambda e: abs(e.floor - src))
            self.pstates[idx]['elev'] = best_e.idx
            if src not in best_e.stops:
                best_e.stops.append(src)
            if best_e.direction == 0 and len(best_e.stops) == 1:
                self.schedule_elevator(best_e)
        super().dispatch()

    def select_elevator(self, src, dst):
        is_low = dst <= LOW_DST_THRESHOLD
        best = None
        best_score = float('inf')
        for e in self.elev:
            dist = abs(e.floor - src)
            penalty = len(e.stops) * 10
            est = dist * TIME_PER_FLOOR + penalty
            if e.direction != 0:
                if (e.direction == 1 and src < e.floor) or (e.direction == -1 and src > e.floor):
                    est += 20
            fairness = ALPHA / dst if is_low else 0
            bias = 0
            if e.idx == 0:   # E1 高区梯
                if is_low:
                    bias = 30
            else:            # E2 低区梯
                if not is_low and dst > 50:
                    bias = 15
            score = est - fairness + bias
            if score < best_score:
                best_score = score
                best = e
        return best

# ========== 运行 ==========
def run_simulation(scheduler_class, name, passengers):
    print_flush(f"\n启动 {name} 调度器...")
    elevs = [Elevator(0, 1), Elevator(1, 1)]
    sched = scheduler_class(elevs)
    start = time.time()
    stats = sched.run(passengers)
    elapsed = time.time() - start
    print_flush(f"{name} 调度完成，耗时 {elapsed:.1f} 秒")
    return stats

if __name__ == "__main__":
    np.random.seed(42)
    print_flush("生成乘客（上行高峰，起始=1，目的楼层正态65±15）...")
    passengers = generate_passengers()
    print_flush(f"实际乘客数: {len(passengers)}")

    naive_stats = run_simulation(NaiveScheduler, "Naive", passengers)
    proposed_stats = run_simulation(ProposedScheduler, "Proposed", passengers)

    def print_stats(name, stats):
        all_w = stats['all']
        low_w = stats['low_dst']
        high_w = stats['high_dst']
        print_flush(f"\n=== {name} ===")
        print_flush(f"服务乘客数: {len(all_w)}")
        if not all_w:
            return
        print_flush(f"平均等待: {np.mean(all_w):.2f}秒, 最大: {np.max(all_w):.2f}秒")
        if low_w:
            print_flush(f"低目的地(≤{LOW_DST_THRESHOLD})乘客数: {len(low_w)}")
            print_flush(f"  平均等待: {np.mean(low_w):.2f}秒, 最大: {np.max(low_w):.2f}秒")
        if high_w:
            print_flush(f"高目的地(>{LOW_DST_THRESHOLD})乘客数: {len(high_w)}")
            print_flush(f"  平均等待: {np.mean(high_w):.2f}秒, 最大: {np.max(high_w):.2f}秒")

    print_stats("Naive (对称效率)", naive_stats)
    print_stats("Proposed (非对称+强制干预)", proposed_stats)