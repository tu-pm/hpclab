# Network Configuration

## Table of Contents

1. [Ethernet Interfaces](#ethernet-interfaces)
    1. [Identify Ethernet Interfaces](#identify-ethernet-interfaces)
    1. [Ethernet Interface Logical Names](#ethernet-interface-logical-names)
    1. [Ethernet Interface Settings](#ethernet-interface-settings)
1. [IP Addressing](#ip-addressing)
    1. [Temporary IP Address Assignment](#temporary-ip-address-assignment)
    1. [Dynamic IP Address Assignment (DHCP Client)](#dynamic-ip-address-assignment-dhcp-client)
    1. [Static IP Address Assignment](#static-ip-address-assignment)
    1. [Loopback Interface](#loopback-interface)
1. [Name Resolution](#name-resolution)
    1. [DNS Client Configuration](#dns-client-configuration)
    1. [Static Hostnames](#static-hostnames)
    1. [Name Service Switch Configuration](#name-service-switch-configuration)
1. [Bridging](#bridging)

## Ethernet Interfaces

### Identify Ethernet Interfaces

*   Xem các thông tin cơ bản của tất cả network interface

```bash
tupham@Tubuntu:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp7s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN group default qlen 1000
    link/ether 20:47:47:14:4c:55 brd ff:ff:ff:ff:ff:ff
3: wlp6s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether e4:f8:9c:1d:33:96 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.5/24 brd 192.168.1.255 scope global dynamic wlp6s0
       valid_lft 81768sec preferred_lft 81768sec
    inet6 fe80::439e:9bbe:9011:fcb3/64 scope link 
       valid_lft forever preferred_lft forever

```

*   Xem chi tiết hơn bằng lệnh `lshw`:

```bash
tupham@Tubuntu:~$ sudo lshw -class network
  *-network
       description: Wireless interface
       product: Wireless 3160
       vendor: Intel Corporation
       physical id: 0
       bus info: pci@0000:06:00.0
       logical name: wlp6s0
       version: 83
       serial: e4:f8:9c:1d:33:96
       width: 64 bits
       clock: 33MHz
       capabilities: pm msi pciexpress bus_master cap_list ethernet physical wireless
       configuration: broadcast=yes driver=iwlwifi driverversion=4.15.0-24-generic firmware=17.948900127.0 ip=192.168.1.5 latency=0 link=yes multicast=yes wireless=IEEE 802.11
       resources: irq:45 memory:f7d00000-f7d01fff

```

### Ethernet Interface Logical Names
### Ethernet Interface Settings

## IP Addressing

### Temporary IP Address Assignment
### Dynamic IP Address Assignment (DHCP Client)
### Static IP Address Assignment
### Loopback Interface

## Name Resolution

### DNS Client Configuration
### Static Hostnames
### Name Service Switch Configuration

## Bridging


