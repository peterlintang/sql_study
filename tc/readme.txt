1. 全局通用选项 (Global Options)
这些选项位于 tc 命令之后，用于控制命令的行为和输出格式。

表格
短选项	长选项	说明
-s	-statistics	‌显示统计信息‌。配合 show 使用，显示发送/接收的字节数、包数、丢包数等。例如：tc -s qdisc show。
-d	-details	显示更详细的配置信息。
-r	-raw	以原始数值显示，不进行单位换算（如显示字节而非 Kbit/Mbit）。
-b	-batch	从文件中批量读取并执行命令。例如：tc -b script.txt，常用于持久化配置。
-n	-numeric	不解析主机名、端口名或协议名，直接显示数字 IP 和端口。
-f	-force	强制执行，忽略某些非致命错误。
-j	-json	以 JSON 格式输出结果，便于脚本解析。
-p	-pretty	美化 JSON 输出格式。
-N	-netns	在指定的网络命名空间（Network Namespace）中执行命令。
2. 核心操作对象 (Objects)
tc 主要操作以下三种对象，它们构成了流量控制的层级结构：

A. qdisc (Queueing Discipline, 排队规则)
决定数据包如何排队、调度和丢弃。每个网络接口至少有一个根 qdisc。

‌常用命令‌: add, change, replace, delete, show, link.
‌常见类型‌:
pfifo_fast: 默认队列，基于 TOS 优先级，无类。
tbf (Token Bucket Filter): 令牌桶过滤器，用于精确限速（Shaping）。
htb (Hierarchical Token Bucket): 分层令牌桶，支持复杂的带宽分配和借用。
netem (Network Emulator): 网络模拟器，用于模拟延迟、丢包、抖动。
sfq (Stochastic Fairness Queueing): 随机公平队列。
fq_codel: 公平队列 + 主动队列管理，降低延迟。
ingress: 入口队列，仅支持过滤和丢弃（Policing）。
B. class (类别)
仅在“有类” qdisc（如 HTB、CBQ）下使用。用于将带宽划分为不同的层级。

‌常用命令‌: add, change, replace, delete, show.
‌关键参数‌:
parent: 父节点 ID（如 1:1）。
classid: 类的唯一标识（如 1:10）。
rate: ‌保证带宽‌（Commit Information Rate）。
ceil: ‌最大带宽‌（Peak Information Rate），可借用的上限。
prio: 优先级（数值越小优先级越高）。
C. filter (过滤器)
用于匹配数据包特征（如 IP、端口、MAC），并将其引导至特定的 class。

‌常用命令‌: add, change, replace, delete, show.
‌关键参数‌:
protocol: 协议类型（如 ip, ipv6, all）。
prio: 过滤器优先级。
match: 匹配条件（取决于过滤器类型，如 u32, fw, flower）。
flowid: 匹配成功后指向的 Class ID。
‌常见类型‌:
u32: 通用匹配器，最灵活，可匹配任意头部字段。
fw: 基于 iptables/nftables 的 MARK 标记进行分类。
flower: 现代高性能过滤器，支持硬件卸载。
3. 常用参数详解 (Parameters by Qdisc Type)
HTB (分层令牌桶) 参数
表格
参数	说明	示例
rate	保证带宽，该类能获得的最低带宽。	rate 10mbit
ceil	最大带宽，该类能借用的最高带宽上限。	ceil 100mbit
burst	令牌桶大小，允许突发传输的数据量。	burst 15kb
cburst	类别突发大小，通常与 burst 类似。	cburst 15kb
prio	调度优先级。当带宽不足时，高优先级类优先发送。	prio 1
quantum	每次调度发送的最大字节数。通常由 r2q 自动计算。	quantum 1500
TBF (令牌桶过滤器) 参数
表格
参数	说明	示例
rate	长期平均速率限制。	rate 10mbit
burst	令牌桶容量，决定突发能力。	burst 32kb
latency	数据包在队列中等待令牌的最大时间。超过此时间可能丢包。	latency 50ms
mpu	最小包单元。小于此大小的包按此大小计算令牌消耗。	mpu 64
NetEm (网络模拟) 参数
表格
参数	说明	示例
delay	模拟延迟。可指定抖动和相关性。	delay 100ms 10ms
loss	模拟丢包率。	loss 1%
duplicate	模拟数据包重复率。	duplicate 0.1%
corrupt	模拟数据包损坏率。	corrupt 0.01%
reorder	模拟数据包乱序。	reorder 5%
U32 过滤器匹配参数
表格
参数	说明	示例
match	匹配数据包特定偏移量的值。格式：match <value>/<mask> at <offset>	match ip dport 80 0xffff
flowid	匹配成功后，将数据包导向指定的 class。	flowid 1:10
action	执行特定动作，如 drop (丢弃), mirred (镜像/重定向)。	action drop
