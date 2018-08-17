# Open vSwitch Mechanism Driver

## Table of Contents

*   [Provider Network](#provider-network)
    *   [Prerequisites](#prerequisites)
    *   [Architecture](#architecture)
    *   [Network Traffic Flow](#network-traffic-flow)
*   [Self Service Network](#self-service-network)
    *   [Prerequisites](#prerequisites-1)
    *   [Architecture](#architecture-1)
    *   [Network Traffic Flow](#network-traffic-flow-1)

## Provider Network

### Prerequisites

Yêu cầu tối thiểu của một mạng provider với OpenVSwitch bao gồm:

*   Một node controller với các thành phần sau:
    *   Hai card mạng: management và provider
    *   OpenStack Neutron server service và ML2 plugin
*   Hai compute nodes với các thành phần:
    *   Hai card mạng: management và provider
    *   OpenStack Neutron Open vSwitch (OVS) layer2 agent, DHCP agent, metadata agent và các gói phụ thuộc

### Architecture

**Kiến trúc tổng quát một mạng provider sử dụng Open vSwitch**

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-provider-overview.png)

Mô hình này tương tự mạng provider với linux bridge, tuy nhiên thay thế cho một linux bridge agent duy nhất, ở đây instances kết nối với interface vật lý thông qua một firewall agent và một ovs agent. Hình vẽ dưới đây chỉ rõ bản chất của các agents trên compute node và cách thức kết nối từng thành phần:

**Các thành phần và kết nối**

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-provider-compconn1.png)

Như vậy, một instance kết nối tới mạng vật lý qua các thành phần trung gian như sau:

*   Một linux bridge đóng vai trò là tường lửa kiểm soát lưu lượng vào ra instance
*   Một OVS intergration bridge - điểm kết hợp: Tất cả lưu lượng vào ra các instances khác nhau cùng nằm trên compute host đều đi qua bridge này, các instances thuộc các mạng khác nhau kết nối tới những cổng khác nhau
*   Một OVS provider bridge: Kết nối intergration bridge tới interface vật lý, thực hiện kiểm tra, thêm và gỡ VLAN ID trước khi chuyển gói tin qua lại giữa chúng

**Trường hợp hai instances thuộc hai mạng khác nhau cùng nằm trên compute host**

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-provider-compconn2.png)

### Network Traffic Flow

**Kịch bản 1: North-south**

*   Một instance nằm trên compute node 1 sử dụng provider node 1
*   Instance cần gửi gói tin đến một host trên Internet

![](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-provider-flowns1.png)

Quá trình di chuyển của gói tin thông qua các bước:

*   Trên compute node:
    *   Interface (1) trên instance chuyển gói tin qua security group trên linux bridge tới intergration bridge tại cổng (5)
    *   intergration bridge gắn VLAN ID nội bộ cho gói tin 
    *   intergration bridge chuyển gói tin đến provider bridge, hai bridge này giao tiếp với nhau qua **`patch port`** (6) và (7)
    *   provider bridge gỡ bỏ địa chỉ VLAN nội bộ và gán địa chỉ VLAN 101 cho gói tin , sau đó chuyển tiếp nó tới hệ thống mạng vật lý
*   Trên hệ thống mạng vật lý:
    *   Gói tin được xử lý giống hệt như đối với mạng provider sử dụng linux bridge

*Chú ý:* 
*   provider bridge là nơi diễn ra quá trình "dịch" VLAN, gói tin di chuyển giữa instance và provider bridge sử dụng một địa chỉ VLAN nội bộ, ngược lại khi ở bên ngoài hệ thống mạng vật lý, nó lại được định vị dựa vào một địa chỉ VLAN ngoài (WHY?)
*   Kết nối giữa các linux bridge thông thường là kết nối **`veth`**, vậy tại sao kết nối giữa hai OVS bridges lại thông qua cặp **`patch port`**? Câu trả lời là **`patch port`** đem lại hiệu năng cao hơn và có tính năng duy trì kết nối khi OVS được khởi động lại (lưu lượng giữa các instance không bị ngắt trong quá trình khởi động lại OVS). Điều này có được là bởi **`patch port`** chỉ đóng vai trò nhận và truyển tiếp dữ liệu giữa hai vport, không có các cơ chế lưu lại hay thay đổi tuyến đối với lưu lượng qua nó. Nhược điểm của nó là ta không thể bắt các gói tin chuyển qua **`patch port`** như đối với **`veth`** thông thường với các công cụ như **`tcpdump`**
*   Gói tin trả lời đi theo chiều ngược lại

**Kịch bản 2: East-west scenario 1**

*   Instance 1 nằm trên compute node 1 và sử dụng provider network 1
*   Instance 2 nằm trên compute node 2 và sử dụng provider network 1
*   Instance 1 muốn gửi gói tin đến cho instance 2

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-provider-flowew1.png)

Trên mỗi instance, quá trình xử lý gói tin tương tự như kịch bản 1.

Trên hệ thống mạng vật lý, gói tin được xử lý tương tự như kịch bản 2 như đã trình bày trong kịch bản 2 provider network sử dụng linux bridge

**Kịch bản 3: East-west scenario 2**

*   Instance 1 nằm trên compute node 1 và sử dụng provider network 1
*   Instance 2 nằm trên compute node 1 và sử dụng provider network 2
*   Instance 1 muốn gửi gói tin đến cho instance 2

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-provider-flowew2.png)

Quá trình di chuyển gói tin tương tự như kịch bản 3 của provider network sử dụng linux bridge. Điểm khác biệt là tại OVS intergration bridge trên node compute, gói tin chuyển đến các cổng khác nhau sẽ được chuyển tiếp tới linux bridge tương ứng, trong khi đối với mạng sử dụng linux bridge, thao tác lựa định vị VLAN được thực hiện trên một interface vật lý

## Self Service Network

### Prerequisites

*   Thêm một network node cho mạng provider đã cấu hình ở trên, node này chứa các thành phần sau:
    *   Ba network interfaces: management, provider và overlay
    *   OVS L2 agent, L3 agent và các gói phụ thuộc
*   Thay đổi compute node:
    *   Thêm một network interface: overlay

### Architecture

**Kiến trúc tổng quát**

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-selfservice-overview.png)

*Nhận xét*: 

*   Mô hình này tương tự với mô hình self-service sử dụng linux bridge, điểm khác nhau là các bridge được quản lý bởi các OpenvSwitch agent
*   Mạng provider vẫn giao tiếp với mạng vật lý thông qua provider bridge, còn mạng self-service giao tiếp với mạng overlay thông qua tunnel bridge

### Network Traffic Flow

**Kịch bản 1: North-South Scenario**

*   Instance nằm trên compute node 1 sử dụng mạng self-service 1
*   Instance cần gửi gói tin đến một host trên Internet

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-selfservice-flowns1.png)

Quá trình di chuyển của gói tin diễn ra theo các bước:

*   Trên Compute Node:
    *   Interface (1) trên instance gửi gói tin đến port (5) trên intergration bridge thông qua **`iptable`** nằm trên linux bridge
    *   Intergration bridge thêm internal VLAN ID vào cho packet, sau đó nó chuyển ID này thành một internal tunnel ID
    *   Intergration bridge chuyển gói tin đến tunnel bridge thông qua patch port
    *   Tunnel bridge đóng gói gói tin với VNI 101 và gửi đến interface vật lý (9), interface này giao tiếp với hạ tầng mạng overlay phía dưới
*   Trên hệ thống mạng vật lý
    *   Gói tin không được gửi đến địa chỉ đích nằm trên cùng VXLAN nên nó được gửi tới network node để xử lý
*   Trên Network Node:
    *   Gói tin được chuyển tới tunnel bridge (12)
    *   Tunnel bridge gỡ VNI ra khỏi gói tin, gắn vào internal tunnel ID cho nó, sau đó lại chuyển tunnel ID thành một internal VLAN ID tương ứng rồi chuyển nó cho intergration bridge thông qua patch port
    *   Intergration bridge gỡ bỏ VLAN và chuyển gói tin cho self-service network interface trên router. 
    *   Router sử dụng NAT dịch địa chỉ IP cục bộ thành địa chỉ IP công cộng và chuyển tiếp gói tin đến cổng gắn với provider network trên intergration bridge
    *   Intergration bridge gắn VLAN ID nội bộ cho gói tin rồi gửi tới provider bridge
    *   Provider bridge thay VLAN ID nội bộ thành VLAN ID 101 và gửi gói tin ra mạng provider
*   Trên mạng provider: Gói tin di chuyển như trình bày phần mạng provider trong tài liệu này

*Gói tin trả lời di chuyển theo chiều ngược lại*

**Kịch bản 2: East-west 1**

*   Instance 1 nằm trên compute node 1 và sử dụng self-service network 1
*   Instance 2 nằm trên compute node 2 và sử dụng self-service network 1
*   Instance 1 muốn gửi gói tin đến cho instance 2

![](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-selfservice-flowew1.png)

Quá trình di chuyển của gói tin:

*   Trên các compute nodes: Gói tin gửi từ instance 1 và gửi đến instance 2 giống như đã trình bày trong kịch bản 1
*   Trên hệ thống mạng overlay trung gian: Do hai gói tin thuộc cùng VXLAN nên các switch trên mạng overlay có thể chuyển tiếp gói tin từ compute node 1 đến compute node 2 mà không cần thông qua network node

**Kịch bản 3: East-west 2**

*   Instance 1 nằm trên compute node 1 và sử dụng self-service network 1
*   Instance 2 nằm trên compute node 1 và sử dụng self-service network 2
*   Instance 1 muốn gửi gói tin đến cho instance 2

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-ovs-selfservice-flowew2.png)

Quá trình di chuyển của gói tin:

*   Trên compute node:
    *   Gói tin gửi đi từ instance 1 và gửi đến instance 2 giống như đã trình bày trong kịch bản 1
    *   Do hai instance cùng nằm trên compute node nên compute node phải xử lý cả lưu lượng đi ra và đi vào instance
    *   Intergration bridge đóng vai trò định vị linux bridge nào tương ứng với instance 2 để gửi gói tin đến nó

*   Trên mạng overlay:
    *   Mạng overlay chuyển tiếp gói tin gửi từ instance 1 đến cho network node xử lý (vì chúng thuộc hai VXLAN khác nhau), sau đó chuyển tiếp gói tin từ network node đến cho instance 2 nằm trên compute node

*   Trên network node:
    *   Quá trình xử lý gói tin tương tự như kịch bản 3 của mạng self-service sử dụng linux bridge, điểm khác biệt ở chỗ các gói tin thuộc các mạng VXLAN khác nhau đều đi qua và được xử lý bởi một tunnel bridge



