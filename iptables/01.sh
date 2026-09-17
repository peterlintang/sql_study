#!/bin/bash
# 1. 放行本机已建立的连接和相关的连接（关键步骤）
# 这允许本机向外发起请求后，外部返回的数据包能顺利进入本机
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 2. 放行本地回环接口（lo），确保本机内部服务通信正常
iptables -A INPUT -i lo -j ACCEPT

# 3. 【重要】如果你是通过 SSH 远程管理服务器，必须先放行 SSH 端口
# 假设 SSH 端口为 22，请根据你的实际端口修改
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 4. 设置 INPUT 链的默认策略为 DROP
# 这将丢弃所有未匹配上述规则的新入站连接
iptables -P INPUT DROP

