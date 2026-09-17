#!/bin/bash
#在ens33上创建一个root qdisc，默认走classid 10
sudo tc qdisc add dev ens33 root handle 1: htb default 10
#创建根类，限制带宽100mbit
sudo tc class add dev ens33 parent 1: classid 1:1 htb rate 100mbit ceil 100mbit
#创建默认子类，保证带宽10mbit/s，最大带宽100mbit/s，优先级2，低于优先级1
sudo tc class add dev ens33 parent 1:1 classid 1:10 htb rate 10mbit ceil 100mbit prio 2
#创建默认子类，保证带宽10mbit/s，最大带宽100mbit/s，优先级1，
sudo tc class add dev ens33 parent 1:1 classid 1:20 htb rate 10mbit ceil 100mbit prio 1
#创建过滤器，挂在根队列下，端口80 tcp/udp数据包走1:20子类处理
sudo tc filter add dev ens33 protocol ip parent 1:0 prio 1 u32 match ip dport 80 0xffff flowid 1:20
#显示class详细信息
#tc -s class show dev ens33
#删除gen队列
#sudo tc qdisc del dev ens33 root
