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






/*******************************************/

1. 基本语法结构
bash
tc [ OPTIONS ] object COMMAND [ dev DEV ] [ PARAMS ]
‌OPTIONS‌: 全局选项，控制命令行为（如显示统计信息）。
‌object‌: 操作对象，主要为 qdisc、class、filter。
‌COMMAND‌: 对对象执行的操作，如 add、delete、show。
‌dev DEV‌: 指定网络接口设备名称（如 eth0, ens33）。
‌PARAMS‌: 特定对象和命令所需的参数（如带宽速率、句柄 ID、过滤器规则等）。
2. 三大核心对象的命令格式
A. qdisc (排队规则)
用于定义数据包的排队、调度和丢弃策略。

bash
tc qdisc [ add | change | replace | delete | show ] dev DEV [ parent qdisc-id | root ] [ handle qdisc-id ] qdisc_type [ parameters ]
‌parent qdisc-id | root‌: 指定父节点。root 表示根队列；其他情况指定父 qdisc 的句柄（如 1:）。
‌handle qdisc-id‌: 指定该 qdisc 的唯一标识符（如 1:0）。
‌qdisc_type‌: 队列类型，如 htb, tbf, pfifo_fast, netem, ingress。
‌parameters‌: 该类型特有的参数（如 rate, burst, latency）。
‌示例：‌

bash
# 添加根 HTB 队列
tc qdisc add dev eth0 root handle 1: htb default 10
B. class (类别)
仅在支持分类的 qdisc（如 HTB, CBQ）中使用，用于分层管理带宽。

bash
tc class [ add | change | replace | delete | show ] dev DEV parent qdisc-id classid class-id qdisc_type [ parameters ]
‌parent qdisc-id‌: 父类的句柄（如 1:1）。
‌classid class-id‌: 当前类的唯一标识（如 1:10）。
‌parameters‌: 带宽参数，如 rate (保证带宽), ceil (最大带宽), prio (优先级)。
‌示例：‌

bash
# 添加子类，保证10Mbit，最大100Mbit
tc class add dev eth0 parent 1:1 classid 1:10 htb rate 10mbit ceil 100mbit prio 2
C. filter (过滤器)
用于匹配数据包特征并将其引导至特定的 class 或执行动作。

bash
tc filter [ add | change | replace | delete | show ] dev DEV [ parent qdisc-id | root ] protocol PROTO prio PRIO filter_type [ filter_params ] flowid class-id
‌parent qdisc-id | root‌: 过滤器挂载的父节点。
‌protocol PROTO‌: 匹配的协议，如 ip, ipv6, all。
‌prio PRIO‌: 过滤器优先级，数值越小优先级越高。
‌filter_type‌: 过滤器类型，如 u32, fw, flower, bpf。
‌filter_params‌: 匹配条件（如 IP、端口、MAC）。
‌flowid class-id‌: 匹配成功后指向的目标 Class ID。
‌示例：‌

bash
# 匹配目标端口80的流量，导向类 1:10
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dport 80 0xffff flowid 1:10
3. 常用全局选项 (OPTIONS)
表格
选项	说明
-s	显示统计信息（如发送字节数、丢包数）。常与 show 连用。
-d	显示详细信息。
-r	显示原始数值，不进行单位换算。
-b	从文件批量执行命令（如 tc -b config.txt）。
-n	不解析主机名和端口名，直接显示数字。
-j	以 JSON 格式输出。
4. 完整实战示例
以下是一个完整的 HTB 限速配置流程，展示了各部分格式的组合：

bash
# 1. 清除旧配置
tc qdisc del dev eth0 root 2>/dev/null

# 2. 添加根 qdisc (HTB)
tc qdisc add dev eth0 root handle 1: htb default 10

# 3. 添加根 class (总带宽 100Mbit)
tc class add dev eth0 parent 1: classid 1:1 htb rate 100mbit ceil 100mbit

# 4. 添加默认 class (未匹配流量，限速 10Mbit)
tc class add dev eth0 parent 1:1 classid 1:10 htb rate 10mbit ceil 100mbit prio 2

# 5. 添加高优先级 class (HTTP流量，限速 50Mbit)
tc class add dev eth0 parent 1:1 classid 1:20 htb rate 50mbit ceil 100mbit prio 1

# 6. 添加过滤器 (匹配端口 80 导向 1:20)
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dport 80 0xffff flowid 1:20
注意事项
‌顺序依赖‌：必须先创建父节点（qdisc 或 class），才能创建子节点或挂载过滤器。
‌句柄格式‌：句柄通常格式为 Major:Minor（如 1:10）。根 qdisc 的 Major 号通常自定义，Minor 号为 0；Class 的 Major 号需与父 qdisc 一致。
‌持久化‌：tc 配置重启后失效，建议将命令写入启动脚本或使用 tc -b 加载配置文件。
