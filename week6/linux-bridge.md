# Linux Bridge Mechanism Driver

## Table of Contents

*   [Provider Network](#provider-network)
    *   [Prerequisites](#prerequisites)
    *   [Architecture](#architecture)
    *   [Network Traffic Flow](#network-traffic-flow)
    *   [Example Configuration](#example-configuration)
*   [Selfservice Network](#selfservice-network)
    *   [Prerequisites:](#prerequisites-1)
    *   [Architecture](#architecture-1)
    *   [Network Traffic Flow](#network-traffic-flow-1)
    *   [Example Configuration](#example-configuration-1)
*   [High Availability Using VRRP](#high-availability-using-vrrp)
    *   [Prerequisites](#prerequisites-2)
    *   [Architecture](#architecture-2)
    *   [Network Traffic Flow](#network-traffic-flow-2)

## Provider Network

Kiến trúc mạng provider network sử dụng linux bridge của OpenStack tạo ra kết nối tầng 2 giữa các instances và hạ tầng mạng vật lý sử dụng cơ chế VLAN tagging. Mỗi OpenStack project có thể chứa tối đa 01 mạng flat (untagged) và 4095 mạng VLAN thuộc loại provider network.

### Prerequisites

Yêu cầu phần cứng tối thiểu để cài đặt mạng provider:

*   Một node controller với các cài đặt:
    *   Hai network interfaces: management và provider
    *   Dịch vụ OpenStack server và ML2 plugin
*   Hai compute nodes với các cài đặt:
    *   Hai network interfaces: management và provider
    *   Các **`neutron`** agents: linux bridge, DHCP, metadata và các thành phần phụ thuộc

### Architecture

**Tổng quan kiến trúc Provider Network sử dụng Linux Bridge**

![linux-bridge-overview](https://docs.openstack.org/neutron/latest/_images/deploy-lb-provider-overview.png)

*Chú thích:*
*   Management network quản lý giao tiếp giữa các thành phần trong cả hệ thống OpenStack, Provider Network quản lý giao tiếp giữa các instances với nhau hoặc với môi trường bên ngoài.
*   Mỗi instance gắn với một bridge trên linux bridge agent, tương tự đối với các agent khác tham gia vào mạng provider (như dhcp agent)

**Mô phỏng cấu hình linux bridge trên một compute node sử dụng mạng provider**

![linux-bridge-provider](https://docs.openstack.org/neutron/latest/_images/deploy-lb-provider-compconn1.png)

*Chú thích:*
*   Mạng VLAN của instance này có ID là 1, ngầm hiểu là mạng flat
*   **`iptables`** là cơ chế tường lửa mà security group cấu hình trên linux bridge nhằm quản lý lưu lượng cho instance 1
*   Như đã nói, mỗi instance gắn với một linux bridge, chúng giao tiếp với nhau qua một liên kết ảo **`veth`** với hai điểm đầu cuối cũng là hai **`virtual tap`** (Terminal Access Point)
*   Mỗi Compute node có một interface vật lý cho mạng provider, các instances chia sẻ chung interface này khi giao tiếp với bên ngoài.

**Compute Node với 2 instance thuộc 2 mạng VLAN khác nhau:**

![two-vlans-linux-bridge](https://docs.openstack.org/neutron/pike/_images/deploy-lb-provider-compconn2.png)

*Chú thích:*
*   Các instances chia sẻ chung một physical interface
*   Gói tin từ các instances được định tuyến dựa trên VLAN ID của nó (dưới góc nhìn của virtual network)

### Network Traffic Flow

Các mục dưới đây mô tả dòng chảy lưu lượng trong mạng trong các kịch bản khác nhau, hai khái niệm kịch bản được sử dụng là:

*   North-South scenario: Lưu lượng giữa instance và môi trường mạng ngoài như Internet
*   East-West scenario: Lưu lượng giữa các instances cùng hoặc khác VLAN networks

**Kịch bản 1: North-South scenario**

*   Một instance nằm trên compute node 1 và sử dụng mạng provider 1
*   Instance cần gửi dữ liệu ra môi trường mạng Internet

![kich ban 1](https://docs.openstack.org/neutron/pike/_images/deploy-lb-provider-flowns1.png)

Gói tin di chuyển trong mạng theo các bước:

1.  Trên compute node 1:
    1.  Instance gửi gói tin tới bridge qua liên kết ảo **`veth`**
    1.  SG (3) trên bridge quyết định xem gói tin có được phép truyền qua hay không
    1.  Cổng VLAN sub-interface (4) chuyển gói tin đến interface vật lý (5)
1.  Trên hệ thống mạng vật lý:
    1.  Interface (5) thêm VLAN ID cho gói tin là 101 và chuyển đến cho switch (6)
    1.  Switch gỡ VLAN ID, biết gói tin thuộc mạng VLAN 101, kiểm tra tiếp địa chỉ MAC của gói tin là địa chỉ của router (do gói tin cần được gửi tới bên ngoài nên MAC đích là của router) nên chuyển gói tin tới luôn cho router
    1.  Router thực hiện định tuyến cho gói tin, xác định nút kế tiếp trong mạng ngoài cho gói tin, chuyển gói tin tới cổng ra phù hợp
    1.  Switch chuyển tiếp gói tin ra môi trường bên ngoài

*Gói tin trả về từ mạng ngoài được gửi tới instance 1 theo chiều ngược lại*

**Kịch bản 2: East-West scenario 1**

*   Instance 1 nằm trên compute node 1, sử dụng mạng provider 1
*   Instance 2 nằm trên compute node 2, sử dụng mạng provider 1
*   Instance 1 muốn gửi gói tin đến instance 2

![kich ban 2](https://docs.openstack.org/neutron/pike/_images/deploy-lb-provider-flowew1.png)

Gói tin di chuyển trong mạng theo các bước:

1.  Trên compute node 1

    1.  Instance 1 gửi gói tin tới bridge qua liên kết ảo **`veth`**
    1.  SG (3) trên bridge quyết định xem gói tin có được phép truyền qua hay không
    1.  Cổng VLAN sub-interface (4) chuyển gói tin đến interface vật lý (5)

1.  Trên mạng vật lý
    1.  Interface (5) thêm VLAN ID cho gói tin là 101 và chuyển đến cho switch (6)
    1.  Switch đọc tiêu đề VLAN, xác định được gói tin chuyển giữa hai host cùng VLAN, bèn chuyển gói tin đến luôn với compute node 2
*   Trên compute node 2
    1.  Đọc gói tin theo chiều ngược lại với chiều chuyển gói tin đi của compute node 1

*Gói tin trả lời từ instance 2 về tới instance 1 theo chiều ngược lại*

**Kịch bản 3: East-West scenario 2**

*   Instance 1 nằm trên compute node 1 sử dụng mạng provider 1
*   Instance 2 nằm trên compute node 1 sử dụng mạng provider 2
*   Instance 1 muốn chuyển gói tin đến instance 2

![kich ban 3](https://docs.openstack.org/neutron/pike/_images/deploy-lb-provider-flowew2.png)

Gói tin di chuyển trong mạng theo các bước:

1.  Trên compute node 1
    1.  Instance 1 gửi gói tin tới bridge qua liên kết ảo **`veth`**
    1.  SG (3) trên bridge quyết định xem gói tin có được phép truyền qua hay không
    1.  Cổng VLAN sub-interface (4) chuyển gói tin đến interface vật lý (5)
1.  Trên mạng vật lý
    1.  Interface (5) thêm VLAN ID cho gói tin là 101 và chuyển đến cho switch (6)
    1.  Switch đọc tiêu đề VLAN, xác định được gói tin được gửi ra địa chỉ MAC nằm ngoài VLAN 101, bèn gỡ tiêu đề VLAN và chuyển tới cho router xử lý
    1.  Router xác định được địa chỉ IP đích nằm trong mạng provider 2, định tuyến gói tin đến địa chỉ IP đích của instance 2 và gửi tới cổng ra phù hợp
    1.  Switch nhận gói tin, dựa vào bảng ARP xác định được địa chỉ MAC đích của gói tin thuộc mạng VLAN 102, gắn tiêu đề VLAN và chuyển đến interface (12), cũng chính là interface (5) vì hai instance nằm trên một copute node và dùng chung interface này
1.  Trở về compute node 1
    1.  Interface gỡ bỏ VLAN ID, chuyển gói tin cho linux bridge (13) gắn với instance 2
    1.  Instance 2 nhận gói tin theo chiều ngược với chiều gửi

*Gói tin trả lời từ instance 2 về instance 1 di chuyển theo chiều ngược lại*

### Example Configuration

Xem hướng dẫn cấu hình tại [đây](https://docs.openstack.org/neutron/pike/admin/deploy-lb-provider.html#example-configuration)

----

## Selfservice Network

Khắc phục hạn chế của provider network sử dụng mạng VLAN, self-service network với cơ chế VXLAN hỗ trợ số lượng mạng ảo lớn hơn rất nhiều. Dưới đây là kiến trúc mạng và cách thức cấu hình mạng self-service với OpenStack sử dụng cơ chế VXLAN.

### Prerequisites:

Thêm vào dự án triển khai provider network các thành phần sau:

*   Một network node với các thành phần: 
    *   Ba card mạng: management, provider và overlay
    *   Các **`neutron`** agents: linux bridge layer-2 agent, layer-3 agent và các thành phần phụ thuộc
*   Thêm vào compute node:
    *   Một card mạng: overlay

### Architecture

**Tổng quan kiến trúc Self-service Network sử dụng Linux Bridge**

![selfservice overview](https://docs.openstack.org/neutron/pike/_images/deploy-lb-selfservice-overview.png)

*Chú thích:*
*   Màu đỏ đại diện cho management network của dự án OpenStack
*   Màu cam đại diện cho mạng provider network đã cấu hình ở phần trước
*   Màu xanh lam đại diện cho mạng self-service đang cài đặt, mạng này chạy trên một mạng overlay VXLAN đại diện bởi màu nâu

**Vai trò của Network Node**

Network node trong mạng self-service đóng vai trò như một router định tuyến lưu lượng giữa các instances nằm trên các mạng self-service khác nhau cũng như giữa mạng self-service với mạng ngoài.

Các thành phần của network node:

*   Linux bridges:
    *   Mỗi bridge giao tiếp với một mạng VXLAN hoặc VLAN xác định, đóng vai trò vận chuyển gói tin giữa router và overlay network (physical networks)
*   Một router
    *   Được gắn nhiều cổng khác nhau, mỗi cổng là một gateway giao tiếp với một mạng provider hoặc self-service
    *   Được cài đặt các giao thức NAT nhằm dịch địa chỉ giữa các host từ mạng này sang mạng khác

**Các  thành phần và kết nối của mạng self-service**

![selfservice component and conectivity](https://docs.openstack.org/neutron/pike/_images/deploy-lb-selfservice-compconn1.png)

*Chú thích:*
*   Các cổng giao tiếp VXLAN kết nối đến các interface trên một mạng VXLAN overlay, trong khi các cổng giao tiếp VLAN kết nối trực tiếp tới mạng Ethernet vật lý

### Network Traffic Flow

**Kịch bản 1: North-south scenario**

Với các instance có địa chỉ IPv4 tĩnh, network node thực hiện ánh xạ SNAT trên các host trong một mạng self-service để giao tiếp với bên ngoài. Giả sử có một instance nằm trên compute node 1 sử dụng mạng self-service 1 muốn gửi gói tin tới mạng ngoài.

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-lb-selfservice-flowns1.png)

Quá trình chuyển tiếp gói tin diễn ra như sau:

1.  Trên compute node
    1.  Instance (1) chuyển gói tin đến overlay interface (4) thông qua linux bridge gắn với nó
    1.  Interface (4) gắn VXLAN ID (VNI) 101 vào gói tin và chuyển nó cho interface vật lý (5)
1.  Trên mạng overlay
    1.  Interface 5 chuyển tiếp gói tin VXLAN trên mạng overlay, gói tin có địa chỉ đích nằm ngoài mạng VXLAN nên nó được chuyển tới cho network node
    1.  Network node nhận gói tin tại overlay interface (7), chuyển gói tin đến cho bridge giao tiếp với mạng VXLAN 101
1.  Trên Network Node:
    1.  Gói tin được gỡ VNI, chuyển đến cho router trên network node thông qua bridge agent giao tiếp với VXLAN 101
    1.  Trên router, địa chỉ IPv4 nguồn được dịch ra địa chỉ Ipv4 của router trên mạng provider, sau đó gói tin được chuyển qua gateway interface trên mạng provider (11)
    1.  Gói tin được chuyển từ router qua linux bridge giao tiếp với VLAN 101 trên Network node đến interface vật lý (14)
1.  Trên mạng vật lý:
    1.  Interface (14) thêm vào VLAN ID 101 cho gói tin (chỉ thị gói tin là flat) và forward gói tin trên mạng provider
    1.  Gói tin lúc này được xử lý trên mạng provider như các kịch bản đã xét đến trong phần [provider network](#provider-network)

*Gói tin trả lời từ mạng provider hoặc từ Internet gửi về instance di chuyển theo chiều ngược lại*

**Kịch bản 2: East-west scenario 1**

*   Instance 1 nằm trên compute node 1 và sử dụng network node 1
*   Instance 2 nằm trên compute node 2 và sử dụng network node 1
*   Instance 1 muốn gửi gói tin đến cho instance 2

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-lb-selfservice-flowew1.png)

Quá trình chuyển tiếp gói tin diễn ra giống hệt như hai gói tin nằm trên cùng mạng provider, điểm khác biệt là môi trường chuyển tiếp gói tin giữa hai instance là mạng overlay.

**Kịch bản 3: East-west scenario 2**

*   Instance 1 nằm trên compute node 1 và sử dụng network node 1
*   Instance 2 nằm trên compute node 1 và sử dụng network node 2
*   Instance 1 muốn gửi gói tin đến cho instance 2

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-lb-selfservice-flowew2.png)

Quá trình chuyển tiếp gói tin cũng tương tự như kịch bản 3 của provider network

*Tổng kết: Network traffic trong mạng self-service tương tự như mạng provider, chỉ có một vài điểm khác biệt đáng chú ý:*
*   Hạ tầng mạng vận chuyển gói tin giữa hai instance trong mạng self-service là mạng VXLAN overlay
*   Quá trình đóng và gỡ thẻ VXLAN nằm trên linux bridge, khác với quá trình đóng gỡ thẻ VLAN nằm trên interface vật lý
*   Network node với virtual router và bridges đóng vai trò định tuyến gói tin trong mạng VXLAN, thông thường có sự hỗ trợ của các giao thức NAT giúp các host thuộc các loại mạng khác nhau

### Example Configuration

Xem hướng dẫn cấu hình mạng self-service tại [đây](https://docs.openstack.org/neutron/pike/admin/deploy-lb-selfservice.html#example-configuration)

## High Availability Using VRRP

Phần này đề cập đến việc mở rộng mô hình mạng self-service với cơ chế khả dụng cao (high availability) sử dụng giao thức Virtual Router Redundancy Protocol (VRRP) thông qua agent **`keepalived`**  giúp chống chịu lỗi cho quá trình định tuyến trong mạng self-service.

Cấu hình tối thiểu yêu cầu của mô hình này là ít nhất 2 node network, 1 node master được sử dụng chính và 1 node backup.

Trong kịch bản hoạt động thông thường, **`keepalived`** trên master router định kì gửi một gói tin *heartbeat* thông qua một mạng ẩn kết nối tất cả các VRRP router trên cùng một project. Theo mặc định, mạng này sử dụng giá trị đầu tiên trong tùy chọn `tenant_network_types` trong file `ml2_conf.ini`. Nếu muốn thêm các tùy chọn kiểm soát cao hơn, người dùng có thể định nghĩa thêm loại mạng self-service và tên mạng vật lý sử dụng cho mạng này với hai options `l3_ha_network_type` và `l3_ha_network_name` trong file `neutron.conf`.

Nếu **`keepalived`** trên router backup không còn nhận được gói tin *heartbeat* nữa, nó sẽ cho rằng router master bị lỗi và cấu hình cho router backup trở thành master bằng cách cấu hình lại các địa chỉ IP trên các interfaces nằm trong `qrouter` namespace. Nếu có nhiều backup router trên cùng một hệ thống, router được lựa chọn theo thứ tự ưu tiên, sau đó là theo địa chỉ IP (cao nhất).

Sự gián đoạn trong quá trình chuyển gói tin *heartbeat* giữa các nút mạng thường là do lỗi interface trên mạng self-service hoặc mạng vật lý. Việc khởi động lại hoặc ngưng hoạt động L3 agent không ảnh hưởng đến hoạt động của **`keepalived`**.

Bên cạnh đó, hãy cân nhắc các cơ chế HA sau cho môi trường hoạt động thực tế:

*   Phân tán master instance trên các router nằm trên các network nodes khác nhau nhằm giảm xung đột xảy ra trên một network node
*   Chỉ hỗ trợ mạng self-service sử dụng router. Các mạng provider hoạt động tại tầng 2 trên hạ tầng vật lý chỉ sử dụng cho mục đích redundancy

### Prerequisites

Thêm một node network vào mạng self-service với các thành phần:
*   Ba network interfaces: management, provider và overlay
*   OpenStack  netwroking L2 agent, L3 agent và các package phụ thuộc

### Architecture

Kiến trúc tổng quát của mạng self-service có hỗ trợ high availability:

![lb-ss-ha](https://docs.openstack.org/neutron/pike/_images/deploy-lb-ha-vrrp-overview.png)

Trong sơ đồ này, hai node network có cấu trúc giống nhau và cách thức kết nối đến hệ thống mạng vật lý như nhau. Dưới đây là mô hình thành phần và kết nối với một mạng untagged và một mạng self-service:

![alt text](https://docs.openstack.org/neutron/pike/_images/deploy-lb-ha-vrrp-compconn1.png)

Master router được cấu hình trên network node 1, backup router được cấu hình trên network node 2.

### Network Traffic Flow

Quá trình luân chuyển của lưu lượng trong mạng diễn ra hệt như một mạng self service thông thường.
