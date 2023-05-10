[English](README.md)

# Build your own Zerotier

## Introduction

Implement a L2 VPN similar to Zerotier or a Virtual Switch.

It simulates the behavior of a physical switch, providing Ethernet frame exchange services for devices connected to the switch's ports.

The difference is that the ports of this virtual switch can be connected to devices all over the world through the Internet, making them appear to be in the same local area network for the operating system.

## Background Knowledge

### What is Network Switch?

A network switch is networking hardware that connects devices on a computer network by using packet switching to receive and forward data to the destination device.

A network switch is a multiport network bridge that uses MAC addresses to forward data at the data link layer (layer 2) of the OSI model. Some switches can also forward data at the network layer (layer 3) by additionally incorporating routing functionality. Such switches are commonly known as layer-3 switches or multilayer switches.

In this project, we focues on layer-2 switchs, which recognize and forward Ethernet frames. When forwarding packets, switches use a forwarding table to look up the port corresponding to the destination address.

In a switch, the forwarding table is generally called the MAC address table. This table maintains the MAC addresses known in the local network and their corresponding ports. When a switch receives a Ethernet frame, it looks up the port corresponding to the destination MAC address in the forwarding table, and forwards the data frame only to that port, thereby achieving data forwarding within the local area network. If the destination MAC address is not in the table, the switch forwards the Ethernet frame to all ports except the source port so that the target device can respond and update the forwarding table.

In this project, we will write a program called VSwitch as a virtual switch to achieve Ethernet frame exchange function.

### Virtual Network Device: TAP

TAP is a type of virtual network device that can simulate a physical network interface, allowing operating systems and applications to use it like a physical interface. TAP devices are commonly used to create virtual private network (VPN) connections between different computers for secure data transmission over public networks.

The TAP device is implemented in the operating system kernel. It looks like a regular network interface and can be used in applications like a regular physical network card. When packets are sent through the TAP device, they are passed to the TUN/TAP driver in the kernel, which passes the packets to the application. The application can process the packets and pass them to other devices or networks. Similarly, when applications send packets, they are passed to the TUN/TAP driver, which forwards them to the specified target device or network.

In this project, the TAP device is used to connect client computers and the virtual switch, enabling packet forwarding between client computers and the virtual switch.

## System Architecture
- Composed of a server (**VSwitch**) and several clients (**VPort**s)

- The server (**VSwitch**) simulates the behavior of a physical network switch, providing Ethernet frame exchange service for each computers connected to the VSwitch by VPorts.
  - Maintains a MAC table
    |MAC|VPort|
    |--|--|
    11:11:11:11:11:11 | VPort-1
    aa:aa:aa:aa:aa:aa | VPort-a
  - Implements Ethernet frame exchange service based on the MAC table

- The client (**VPort**) simulates the behavior of a physical switch port, responsible for relaying Ethernet frames between the switch and the computer.
  - VPort has two ends.
    - One end is connected to a computer('s linux kernel) through TAP device.
    - The other end is connected to the VSwitch through UDP socket.
  - Responsible for relaying packets between the computer('s linux kernel) and the VSwitch.
    ```
    Computer's Linux Kernel <==[TAP]==> (Ethernet Frame) <==[UDP]==> VServer
    ```
- Architecture Diagram
    ```
        +----------------------------------------------+
        |                   VSwitch                    |
        |                                              |
        |     +----------------+---------------+       |
        |     |            MAC Table           |       |
        |     |--------------------------------+       |
        |     |      MAC       |      VPort    |       |
        |     |--------------------------------+       |
        |     | 11:11:11:11:11 |   VClient-1   |       |
        |     |--------------------------------+       |
        |     | aa:aa:aa:aa:aa |   VClient-a   |       |
        |     +----------------+---------------+       |
        |                                              |
        |           ^                       ^          |
        +-----------|-----------------------|----------+
            +-------|--------+     +--------|-------+
            |       v        |     |        v       |
            | +------------+ |     | +------------+ |
            | | UDP Socket | |     | | UDP Socket | |
            | +------------+ |     | +------------+ |
            |       ^        |     |        ^       |
            |       |        |     |        |       |
            |(Ethernet Frame)|     |(Ethernet Frame)|
            |       |        |     |        |       |
      VPort |       v        |     |        v       | VPort
            | +------------+ |     | +------------+ |
            | | TAP Device | |     | | TAP Device | |
            | +------------+ |     | +------------+ |
            |       ^        |     |        ^       |
            +-------|--------+     +--------|-------+
                    v                       v
      -------------------------   -------------------------
      Computer A's Linux Kernel   Computer B's Linux Kernel

    ```

## Source Code

1. [`vswitch.py`](./vswitch.py): code for **VSwitch**
2. [`vport.c`](./vport.c): code for **VPort**

## How to build
Just run
```
make
```

## How to deploy

### Environment Preparation

- A server with a public IP for runing VSwitch
- At least two clients, which run VPort to connect to VSwitch, constructing a Virtual Private Network
- Assuming the public IP is `SERVER_IP` and the server port is `SERVER_PORT`

### Step 1. Run VSwitch
On the server with public IP:
```
python3 vswitch.py ${SERVER_PORT}
```

### Step 2. Run and Configure VPort on Client-1

- Run VPort
    ```
    sudo ./vport ${SERVER_IP} ${SERVER_PORT}
    ```
- Configure TAP device
    ```
    sudo ip addr add 10.1.1.101/24 dev tapyuan
    sudo ip link set tapyuan up
    ```

### Step 3. Run and Configure VPort on Client-2

- Run VPort
    ```
    sudo ./vport ${SERVER_IP} ${SERVER_PORT}
    ```
- Configure TAP device
    ```
    sudo ip addr add 10.1.1.102/24 dev tapyuan
    sudo ip link set tapyuan up
    ```

### Step 4. Ping Connectivity Test

- Ping client-2 from client-1
    ```
    ping 10.1.1.102
    ```
- Ping client-1 from client-2
    ```
    ping 10.1.1.101
    ```
### Demo Video


https://github.com/peiyuanix/build-your-own-zerotier/assets/11792595/7e4db7a5-88a5-4181-8d5f-dd861e9a040c

