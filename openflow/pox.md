# Learning POX

        Docs: https://noxrepo.github.io/pox-doc/html/

## POX Components

-   Mỗi `component` là một loại controller định nghĩa bởi POX
-   Danh sách components có sẵn: https://noxrepo.github.io/pox-doc/html/#stock-components. 
-   Tự định nghĩa một component:
    -   Tạo ra Python module định nghĩa component trong thư mục `ext/` nằm trong thư mục gốc của pox
    -   Trong module này cần có:
        -   Hàm `launch`: Chỉ ra cách thức sử lý các tham số dòng lệnh được truyền vào khi khởi tạo component
        -   Một lớp định nghĩa component

## POX API

### Các thành phần chính:

-   `pox.core`: Là central point của POX API
-   `pox.lib.address`: Định nghĩa và làm việc với các kiểu địa chỉ mạng 
-   `pox.lib.revent`: Hệ thống sự kiện định nghĩa bởi POX API
-   `pox.lib.packet`: Lớp cơ sở định nghĩa các gói tin gửi bởi các OpenFlow messages
-   `pox.lib.recoco`: Làm việc với luồng
-   `pox.lib.ioworker`: Làm việc với socket

### Đăng ký components với core

-   Các components trong hệ thống cùng đăng ký với một đối tượng `core` duy nhất thông qua phương thức `core.register(NAME, COMPONENT_OBJECT)`
-   Ví dụ:
    ```python
    import pox.core as core

    class MyComponent(object):
        ...

    def launch():
        component = MyComponent(...)
        core.register("foo", component)
    ```
-   Cách khác, sử dụng `registerNew(COMPONENT_CLASS)` giúp đăng ký component duy nhất một lần ngay cả khi nó được khởi tạo nhiều lần, đồng thời tên đăng ký của component chính là tên class:
    ```python
    def launch():
        core.registerNew(MyComponent)
    ```
-   Lúc này, ta có thể truy cập tới component vừa đăng ký từ module khác bằng cú pháp `core.foo` hoặc `core.MyComponent`

### Làm việc với gói tin

-   `pox.lib.packet` hỗ trợ khởi tạo và parse các loại packets khác nhau (VD: ethernet, arp, ipv4, icmp, tcp, udp, dhcp, dns, lldp and vlan)
-   Import module:
    ```python
    import pox.lib.packet as pkt
    ```
-   Các phương thức/thuộc tính:
    -   `.type`: Loại gói tin
    -   `.protocol`: Giao thức gửi gói tin
    -   `.payload`: Nội dung gói tin
    -   `.find(TYPE)`: Trích xuất ra gói tin thuộc loại TYPE được đóng trong gói tin hiện tại
-   Với mỗi loại gói tin, POX hỗ trợ thêm một số các phương thức hữu dụng khác để xử lý chúng. Chi tiết xem tại: https://noxrepo.github.io/pox-doc/html/#id79

## OpenFlow in POX

-   `core.openflow` là central point để đăng ký các OF components
-   Datapath (Switch) ID: Mỗi switch kết nối với controller có một ID duy nhất, gọi là `DPID`. Lấy giá trị này bằng thuộc tính `.dpid` trên đối tượng openflow connection (sẽ đề cập ở dưới).
-   Giao tiếp với Switches:
    -   Một đối tượng connection được sử dụng để giao tiếp giữa controller và switch. Controller giao tiếp với switch thông qua các gói tin OpenFlow, ngược lại, gói tin từ switch gửi tới controller như các *event* và có thể được bắt trên controller thông qua các event handlers 
    -   Có hai cách để thực hiện giao tiếp với switch: Thông qua `Connection` object hoặc thông qua OpenFlow Nexus (`core.openflow`). Phương án thứ nhất phù hợp với giao tiếp 1-1 giữa controller với switch, trong khi phương án thứ 2 phù hợp hơn với giao tiếp 1-nhiều.

### Connection

-   API cho hai loại connection trên được mô tả tại link: https://noxrepo.github.io/pox-doc/html/#id101
-   Trong tài liệu này, ta sẽ chủ yếu làm việc với OpenFlow Nexus

### Events

-   Gói tin gửi từ switch tới controller thông qua một đối tượng `event`. Đối tượng này gồm các thuộc tính quan trọng sau:
    -   `connection`: Đối tượng `Connection` của giao tiếp 
    -   `dpid`: ID của switch
    -   `ofp`: Thông điệp OpenFlow gửi tới controller. Danh sách các loại thông điệp và nội dung của chúng được đề cập đến phía dưới
-   Phương thức xử lý event trong component: `_handle_EVENT_NAME`. Ví dụ: `_handleConnectionUp`, `_handleFlowIn`, ...
-   Các loại event thường được sử dụng được đề cập dưới đây:

#### `ConnectionUp`

-   Xuất hiện khi có kết nối mới tới controller
-   Thuộc tính đặc biệt:
    -   `ofp`: Chứa thêm các thông tin khác như các loại `actions` được hỗ trợ, thông tin về cổng nhận gói tin
-   Handler:
    ```python
    def _handle_ConnectionUp(self, event):
        print("Switch %s has come up" % event.dpid)
    ```

#### `ConnectionDown`

-   Xuất hiện khi kết nối bị ngắt
-   Thuộc tính đặc biệt:
    -   Không có thuộc tính `ofp`
-   Handler:
    ```python
    def _handle_ConnectionDown(self, event):
        print("Switch %s has gone down" % event.dpid)
    ```

#### `PortStatus`

-   Xuất hiện khi controller nhận gói tin `ofp_port_status` báo hiệu thông tin về các cổng có sự thay đổi
-   Thuộc tính đặc biệt:
    -   `added|modified|deleted`: Cổng trên switch mới được thêm vào/sửa đổi/xóa
-   Handler:
    ```python
    def _handle_PortStatus(self, event):
        if event.added:
            action = "added"
        elif event.modified:
            action = "modified"
        else:
            action = "deleted"
        print("Port %s on Switch %s has been %s" % (event.port, event.dpid, action))
    ```

#### `FlowRemoved`

-   Xuất hiện khi controller nhận gói tin `ofp_flow_removed`, báo hiệu một dòng nào đó bị xóa khỏi flow table một cách cố ý hoặc do timeout xảy ra
-   Thuộc tính đặc biệt:
    -   `bool idleTimeout|hardTimeout|timeout|deleted`: Lý do flow bị xóa bỏ

#### Statistics Events

-   Xem tại link: https://noxrepo.github.io/pox-doc/html/#id109

#### FlowIn

-   Xuất hiện khi có gói tin gửi tới controller
-   Thuộc tính đặc biệt:
    -   `int port`: Cổng nhận gói tin 
    -   `bytes data`: Dữ liệu thô 
    -   `packet parsed`: Dữ liệu đã được parsed

#### ErrorIn

-   Xuất hiện khi có thông điệp báo lỗi gửi tới controller
    -   `should_log`: Nên log ra thông điệp báo lỗi hay không 
    -   `asString()`: Format lỗi thành dạng xâu 

### Messages

-   Các đối tượng thông điệp được controller sử dụng để yêu cầu switch thực hiện một công việc nào đó (cập nhật flow table, chuyển tiếp các gói tin, ...)
-   Một số loại thông điệp thường dùng:
    -   `ofp_packet_in`: Thông điệp được gửi tới controller từ switch cùng với sự kiện PacketIn (bản chất là thông điệp `ofp_packet_out` gửi từ một switch khác)
    -   `ofp_packet_out`: Gửi thông điệp từ switch
    -   `ofp_flow_mod`: Cập nhật flow table 
    -   `ofp_stats_request`: Yêu cầu các dữ liệu thống kê từ switches
-   Chi tiết API của các loại message xem tại link: https://noxrepo.github.io/pox-doc/html/#id113

### Matching

-   Các đối tượng `ofp_match` được sử dụng để định nghĩa cách thức so khớp tiêu đề của một thông điệp với các dòng trong flow table
-   Các thuộc tính:
    -   `in_port`: Cổng nhận gói tin
    -   `dl_src`: Địa chỉ ethernet nguồn 
    -   `dl_dst`: Địa chỉ ethernet đích 
    -   `dl_vlan`: VLAN ID 
    -   `dl_vlan_pcp`: VLAN priority 
    -   `dl_type`: Loại ethernet
    -   `nw_tos`: IP TOS/DS bits
    -   `nw_proto`: Giao thức tầng trên của IP
    -   `nw_src`: Địa chỉ IP nguồn 
    -   `nw_dst`: Địa chỉ IP đích 
    -   `tp_src`: Cổng giao vận nguồn
    -   `tp_dst`: Cổng giao vận đích 
-   Các phương thức:
    -   `from_packet(packet, in_port=None, spec_flags=False)`: Định nghĩa đối tượng `match` từ một gói tin 
    -   `clone()`: Tạo bản sao mới
    -   `flip()`: Tạo bản sao mới với thông tin nguồn và đích tráo đổi cho nhau
    -   `show()`: Hiển thị thông tin của đối tượng `match`
    -   `get_nw_src()`: Lấy địa chỉ IP nguồn 
    -   `set_nw_src()`: Gán địa chỉ IP nguồn 
    -   `get_nw_dst()`: Lấy địa chỉ IP đích 
    -   `set_nw_dst()`: Gán địa chỉ IP đích 

### Actions

-   Các đối tượng `actions` được sử dụng để yêu cầu thực hiện các thay đổi nhất định lên một gói tin
-   Các loại actions:
    -   `ofp_action_output`: Chuyển gói tin qua cổng xác định
    -   `ofp_action_enqueue`: Chuyển gói tin qua một hàng đợi xác định 
    -   `ofp_action_vlan_vid`: Gán lại địa chỉ VLAN ID cho một gói tin 
    -   `ofp_action_vlan_pcp`: Thay đổi độ ưu tiên VLAN cho gói tin 
    -   `ofp_action_dl_addr`: Gán địa chỉethernet nguồn và đích cho gói tin 
    -   `ofp_action_nw_addr`: Gán địa chỉ IP nguồn và đích cho gói tin
    -   `ofp_action_nw_tos`: Gán loại dịch vụ (tos) cho gói tin 
    -   `ofp_action_tp_port`: Gán cổng giao vận nguồn và đích cho gói tin 
-   API chi tiết của các loại action xem tại link: https://noxrepo.github.io/pox-doc/html/#id125
