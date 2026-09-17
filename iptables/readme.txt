iptables [-t 表名] <命令选项> [链名] [规则编号] [-i/o 网卡名称] [-p 协议类型] [-s 源IP/网段] [--sport 源端口] [-d 目标IP/网段] [--dport 目标端口] -j <动作>

-t filter nat mangle raw

| ‌-A‌ | ‌Append‌：在指定链的‌末尾‌追加一条规则 | iptables -A INPUT ... |
| ‌-I‌ | ‌Insert‌：在指定链的‌头部‌（或指定行号）插入一条规则 | iptables -I INPUT 1 ... |
| ‌-D‌ | ‌Delete‌：删除指定链中的某条规则 | iptables -D INPUT 1 |
| ‌-F‌ | ‌Flush‌：清空指定链或表中所有规则 | iptables -F INPUT |
| ‌-L‌ | ‌List‌：列出指定链或表中所有规则 | iptables -L INPUT |
| ‌-P‌ | ‌Policy‌：设置指定链的‌默认策略‌ | iptables -P INPUT DROP |
| ‌-X‌ | ‌Delete Chain‌：删除用户自定义的空链 | iptables -X MY_CHAIN |
| ‌-Z‌ | ‌Zero‌：清零指定链或表的计数器 | iptables -Z INPUT |

| 选项 | 含义 | 说明 |
| --- | --- | --- |
| ‌-p‌ | 协议 | 匹配协议类型，如 tcp, udp, icmp |
| ‌-s‌ | 源地址 | 匹配源 IP 或网段，如 192.168.1.0/24；加 ! 表示取反 |
| ‌-d‌ | 目标地址 | 匹配目标 IP 或网段 |
| ‌-i‌ | 入站网卡 | 匹配数据从哪个网卡‌进入‌（如 eth0），常用于 PREROUTING/INPUT |
| ‌-o‌ | 出站网卡 | 匹配数据从哪个网卡‌流出‌（如 eth1），常用于 POSTROUTING/OUTPUT |
| ‌--sport‌ | 源端口 | 匹配源端口号或范围（需配合 -p tcp/udp） |
| ‌--dport‌ | 目标端口 | 匹配目标端口号或范围（需配合 -p tcp/udp） |
| ‌-m state‌ | 连接状态 | 配合 --state 使用，如 NEW, ESTABLISHED, RELATED |

-j
<200c>ACCEPT‌：允许数据包通过。
‌DROP‌：直接丢弃数据包，不返回任何信息（静默丢弃）。
‌REJECT‌：拒绝数据包，并向发送方返回错误响应（如 ICMP 不可达）。
‌SNAT‌：源地址转换（用于 nat 表 POSTROUTING 链）。
‌DNAT‌：目标地址转换（用于 nat 表 PREROUTING 链）。
‌MASQUERADE‌：IP 伪装（动态 SNAT，适用于拨号等动态 IP 场景）。
‌LOG‌：记录日志到系统日志文件。
‌RETURN‌：返回上一级链继续匹配。



1. 基础匹配条件
这些选项无需加载额外模块即可直接使用。

表格
选项	含义	说明与示例
‌-p‌	协议	指定传输层协议。
常用值：tcp, udp, icmp, all。
示例：-p tcp
‌-s‌	源地址	匹配数据包的源 IP 地址或网段。
支持取反 ! -s。
示例：-s 192.168.1.0/24
‌-d‌	目标地址	匹配数据包的目标 IP 地址或网段。
支持取反 ! -d。
示例：-d 10.0.0.1
‌-i‌	入站接口	匹配数据包从哪个网络接口‌进入‌。
仅适用于 PREROUTING、INPUT、FORWARD 链。
示例：-i eth0
‌-o‌	出站接口	匹配数据包从哪个网络接口‌流出‌。
仅适用于 OUTPUT、FORWARD、POSTROUTING 链。
示例：-o eth1
2. 端口匹配条件
使用端口匹配时必须配合 -p tcp 或 -p udp 使用。

表格
选项	含义	说明与示例
‌--sport‌	源端口	匹配数据包的源端口号或范围。
示例：--sport 1024:65535
‌--dport‌	目标端口	匹配数据包的目标端口号或范围。
示例：--dport 80 或 --dport 8000:9000
3. 扩展匹配条件（需 -m 模块）
通过 -m 选项加载特定模块，可以实现更复杂的匹配逻辑。

A. 连接状态匹配 (state 或 conntrack)
用于识别数据包属于哪个连接阶段，常用于放行回包。

‌命令格式‌：-m state --state <状态> 或 -m conntrack --ctstate <状态>
‌常见状态值‌：
NEW：新建立的连接。
ESTABLISHED：已建立的连接（双向通信中）。
RELATED：与已有连接相关的连接（如 FTP 数据通道）。
INVALID：无效或无法识别的数据包。
‌示例‌：
bash
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
B. 多端口匹配 (multiport)
用于一次性匹配多个不连续的端口，避免编写多条规则。

‌命令格式‌：-m multiport --dports <端口列表> 或 --sports
‌示例‌：
bash
# 同时放行 80, 443, 8080 端口
iptables -A INPUT -p tcp -m multiport --dports 80,443,8080 -j ACCEPT
C. IP 范围匹配 (iprange)
用于匹配连续的 IP 地址范围，比子网掩码更灵活。

‌命令格式‌：-m iprange --src-range <起始IP>-<结束IP>
‌示例‌：
bash
iptables -A INPUT -m iprange --src-range 192.168.1.100-192.168.1.200 -j DROP
D. 限制速率匹配 (limit)
用于限制匹配规则的数据包速率，常用于防止 DoS 攻击或日志泛滥。

‌命令格式‌：-m limit --limit <速率>
‌示例‌：
bash
# 限制每秒最多匹配 5 个包，突发上限 10 个
iptables -A INPUT -p icmp -m limit --limit 5/s --limit-burst 10 -j ACCEPT
E. MAC 地址匹配 (mac)
基于源 MAC 地址进行匹配，仅在局域网内有效。

‌命令格式‌：-m mac --mac-source <MAC地址>
‌示例‌：
bash
iptables -A INPUT -m mac --mac-source 00:11:22:33:44:55 -j ACCEPT
F. 字符串匹配 (string)
匹配数据包负载中的特定字符串内容。

‌命令格式‌：-m string --algo <算法> --string "<字符串>"
‌示例‌：
bash
# 丢弃包含 "evil" 字符串的数据包
iptables -A INPUT -m string --algo bm --string "evil" -j DROP
G. 时间匹配 (time)
根据时间段匹配数据包。

‌命令格式‌：-m time --timestart <开始时间> --timestop <结束时间>
‌示例‌：
bash
# 仅在工作时间 9:00-18:00 允许访问
iptables -A INPUT -p tcp --dport 80 -m time --timestart 09:00 --timestop 18:00 -j ACCEPT
4. 匹配条件的组合与取反
‌组合使用‌：一条规则可以包含多个匹配条件，它们之间是“与”（AND）的关系。只有所有条件都满足，规则才生效。
示例：-p tcp -s 192.168.1.0/24 --dport 80 表示来自该网段且访问 80 端口的 TCP 包。
‌取反操作‌：在大多数匹配选项前加 ! 表示“非”。
示例：! -s 192.168.1.1 表示源 IP ‌不是‌ 192.168.1.1 的所有数据包。
