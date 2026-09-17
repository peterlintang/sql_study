# 创建名为 cpu-limit-demo 的控制组目录
mkdir -p /sys/fs/cgroup/cpu-limit-demo

# 50% cpu usage for all processes in this group
echo "50000 100000" | tee /sys/fs/cgroup/cpu-limit-demo/cpu.max

# add process to group, can add multiple process
echo 96307 | tee /sys/fs/cgroup/cpu-limit-demo/cgroup.procs

# remove process from group, move it to upper group
echo 96307 | tee /sys/fs/cgroup/cgroup.procs

# remove cgroup
rmdir /sys/fs/cgroup/cpu-limit-demo

/******************************************************************/
1. 核心管理文件
这些文件用于管理 Cgroup 的层级结构、进程归属以及控制器启用状态。

表格
文件名	作用详解
cgroup.procs‌	‌进程列表文件‌。
• ‌读‌：列出当前 Cgroup 中所有线程组领导者的 PID。
• ‌写‌：将指定 PID 的进程（及其所有线程）移动到此 Cgroup。这是将进程加入或移出限制组的主要入口。
cgroup.subtree_control‌	‌子树控制器开关‌。
• ‌读/写‌：决定当前 Cgroup 的子节点可以启用哪些资源控制器（如 +cpu +memory）。只有在此文件中启用的控制器，子 Cgroup 才能使用对应的限制文件（如 cpu.max）。
• ‌注意‌：根 Cgroup 通常由 systemd 管理，手动修改需谨慎。
cgroup.controllers‌	‌可用控制器列表‌。
• ‌只读‌显示当前 Cgroup 支持且已启用的控制器名称（如 cpu memory io pids）。如果某个控制器未在此列出，则无法在该层级或其子层级中使用相关资源限制。
cgroup.freeze‌	‌冻结状态控制‌。
• ‌写‌：写入 1 冻结该 Cgroup 内所有进程（暂停执行，不消耗 CPU）；写入 0 恢复执行。
• ‌读‌：查看当前冻结状态（0 或 1）。
cgroup.type‌	‌Cgroup 类型标识‌。
• ‌只读‌：显示当前 Cgroup 的类型，通常为 domain（普通域，可包含进程）或 threaded（线程域，用于更细粒度的线程调度）。
2. CPU 资源控制与统计
涉及 CPU 时间片、权重和亲和性。

表格
文件名	作用详解
cpu.max‌	‌CPU 硬限制‌。
• ‌格式‌：<quota> <period>（单位微秒）。
• ‌作用‌：限制该组进程在给定周期内可使用的最大 CPU 时间。例如 50000 100000 表示每 100ms 最多使用 50ms CPU（即单核 50%）。若设为 max 100000 则表示无限制。
cpu.weight‌	‌CPU 权重调度‌。
• ‌范围‌：1-10000（默认 100）。
• ‌作用‌：当多个 Cgroup 竞争空闲 CPU 资源时，按权重比例分配时间片。权重越高，获得的 CPU 时间越多。
cpu.stat‌	‌CPU 使用统计‌。
• ‌只读‌：显示详细的 CPU 使用情况，包括用户态时间、内核态时间、被节流（throttled）的次数和时间等。
cpuset.cpus‌	‌CPU 亲和性限制‌。
• ‌作用‌：指定该组进程只能在哪些 CPU 核心上运行（如 0-3 表示仅限前 4 个核心）。需启用 cpuset 控制器。
cpuset.mems‌	‌内存节点限制‌。
• ‌作用‌：指定该组进程只能使用哪些 NUMA 内存节点。需启用 cpuset 控制器。
3. 内存资源控制与统计
涉及物理内存、Swap 和大页内存。

表格
文件名	作用详解
memory.max‌	‌内存硬上限‌。
• ‌作用‌：限制该组可使用的最大物理内存+Swap 总量。超过此限制将触发 OOM Killer 杀死进程。支持单位如 1G, 512M。设为 max 表示无限制。
memory.swap.max‌	‌Swap 使用上限‌。
• ‌作用‌：限制该组可使用的 Swap 空间大小。设为 0 可禁止使用 Swap，强制仅使用物理内存。
memory.high‌	‌内存软上限（节流阈值）‌。
• ‌作用‌：当内存使用超过此值时，内核会尝试异步回收内存并节流进程的内存分配速度，但不会立即杀死进程。用于防止突发内存占用影响系统稳定性。
memory.low‌	‌内存保护下限‌。
• ‌作用‌：只要内存使用低于此值，内核通常会避免对该组进行内存回收（除非系统极度缺内存）。用于保护关键服务不被换出。
memory.current‌	‌当前内存用量‌。
• ‌只读‌：显示当前已使用的物理内存总量（单位字节）。
memory.stat‌	‌详细内存统计‌。
• ‌只读‌：提供细分数据，如匿名页（anon）、文件缓存（file）、滑动窗口（slab）、活跃/非活跃页面等详细信息。
memory.events‌	‌内存事件计数‌。
• ‌只读‌：记录 OOM 杀死次数、高水位线突破次数等事件的发生频率。
4. I/O 资源控制与统计
涉及磁盘读写带宽和 IOPS。

表格
文件名	作用详解
io.max‌	‌I/O 硬限制‌。
• ‌格式‌：<major>:<minor> rbps=<bytes> wbps=<bytes> riops=<count> wiops=<count>。
• ‌作用‌：限制特定块设备的读写带宽（Bytes/sec）和每秒操作次数（IOPS）。
io.weight‌	‌I/O 权重‌。
• ‌作用‌：类似 CPU weight，决定在多个 Cgroup 竞争磁盘 IO 时的相对优先级。
io.stat‌	‌I/O 使用统计‌。
• ‌只读‌：显示每个块设备的读写字节数、操作次数、合并次数等详细指标。
5. 其他资源控制器
表格
文件名	作用详解
pids.max‌	‌进程数硬限制‌。
• ‌作用‌：限制该 Cgroup 内允许存在的最大进程/线程总数。防止“Fork 炸弹”导致系统崩溃。设为 max 表示无限制。
pids.current‌	‌当前进程数‌。
• ‌只读‌：显示当前 Cgroup 内的进程/线程总数。
hugetlb.<pagesize>.max‌	‌大页内存限制‌。
• ‌作用‌：限制特定大小（如 2MB, 1GB）的大页内存使用量。例如 hugetlb.2MB.max。
rdma.max‌	‌RDMA 资源限制‌。
• ‌作用‌：限制远程直接内存访问（RDMA）资源的分配，如 HCA handles 和 MR 数量。
💡 操作示例
1. 查看当前限制：‌

bash
cat /sys/fs/cgroup/my-group/cpu.max
cat /sys/fs/cgroup/my-group/memory.max
2. 设置限制：‌

bash
# 限制 CPU 为单核的 50%
echo "50000 100000" > /sys/fs/cgroup/my-group/cpu.max

# 限制内存为 512MB
echo "536870912" > /sys/fs/cgroup/my-group/memory.max
3. 查看实时统计：‌

bash
cat /sys/fs/cgroup/my-group/memory.current
cat /sys/fs/cgroup/my-group/cpu.stat
⚠️ 注意事项
权限‌：大多数文件需要 root 权限才能写入。
控制器启用‌：如果某些文件（如 cpu.max）不存在，可能是因为父级 Cgroup 的 cgroup.subtree_control 中未启用对应的控制器（如 +cpu）。
单位‌：注意不同文件的单位差异，CPU 时间为微秒（us），内存通常为字节（Bytes），I/O 带宽为 Bytes/sec。
Systemd 集成‌：在现代 Linux 发行版中，建议通过 systemd 服务单元文件（如 CPUQuota=, MemoryMax=）来管理这些参数，而不是直接操作文件系统，以避免配置冲突。
