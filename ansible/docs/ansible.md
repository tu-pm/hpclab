
# Ansible Documentation
> Tài liệu này giới thiệu về Ansible, cách thức cài đặt cũng như cách sử dụng các tính năng cơ bản của nó thông qua các công cụ dòng lệnh. 
## Tổng quan
Ansible là một công cụ tự động hóa hoàn toàn các hoạt động cung cấp tài nguyên tính toán đám mây, quản lý các thao tác cấu hình, triển khai ứng dụng và quản lý nội dịch vụ.

Một cách cơ bản, Ansible thực hiện cài đặt hoặc cấu hình dịch vụ trên máy chủ từ xa bằng cách mở một kết nối SSH tới server, thực thi các thủ tục cài đặt cần thiết trên server rồi đóng kết nối. Tất cả các thao tác này được thực hiện một cách tự động thông qua một kịch bản (playbook) được định nghĩa trước.

Các tính chất cơ bản của Ansible bao gồm:
- Đơn giản, dễ sử dụng
- Tin cậy, độ bảo mật cao
- *Không sử dụng agent*: Không cần cài đặt agents trên remote servers, giảm tối thiểu chi phí cài đặt và bảo trì
- Modules đa dạng: Hỗ trợ hơn 400 modules, là những chương trình con mà ansible hỗ trợ thực thi trên server, thực hiện những nhiệm vụ cơ bản như quản lý file, quản lý dịch vụ hay cài đặt packages

## Các khái niệm cơ bản


### Manage Your Inventory in Simple Text Files

Theo mặc định, Ansible mô tả những machines mà nó quản lý sử dụng một file `*.ini` đơn giản gom chúng chung vào một nhóm. Để có thể thêm một machine mới, ta chỉ việc thêm chúng vào file này. Các dữ liệu từ nguồn khác như EC2, RACKspace hay OpenStack cũng có thể được kéo về sử dụng dynamic inventory.

## Cài đặt và cấu hình

### Yêu cầu 
- Control node: Chạy các hệ điều hành Linux/Unix phổ biến, có cài đặt Python 2.7 hoặc 3.5+, và có khả năng kết nối tới các máy chủ được quản lý (managed nodes)
- Managed nodes: Có cài đặt OpenSSH server, Python 2.7 hoặc 3.5+

*Chú ý*: Hiện tại, ansible vẫn sử dụng Python 2.7 theo mặc định. Để yêu cầu Ansible sử dụng Python 3, ta cần thêm cấu hình `ansible_python_interpreter` trong file inventory

### Cài đặt
Cách thức cài đặt ansible trên các phiên bản hệ điều hành khác nhau được cập nhật trong tài liệu [này]([https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html))

### Cấu hình
#### Configuration Files
Đường dẫn file cấu hình của Ansible thường nằm tại các địa chỉ:
- `./ansible.cfg`
- `~/ansible.cfg`
- `/etc/ansible/ansible.cfg`

#### Environmental Configuration
Có thể cấu hình Ansible sử dụng biến môi trường `ANSIBLE_CONFIG` để ghi đè các cấu hình trong file.

#### Command Line Options
Một vài cấu hình có thể được ghi đè thông qua câu lệnh `ansible` hoặc `ansible-playbook`

## Getting Started

### Remote Connection Information

Trong một vài trường hợp hiếm gặp khi thiết bị từ xa không hỗ trợ SFTP, ta có thể cấu hình Ansible sử dụng SCP mode thay thế.

Khi giao tiếp với các máy từ xa, Ansible mặc định sử dụng SSH keys. Nếu muốn sử dụng mật khẩu, ta cần thêm các option như `--ask-pass` hay `--ask-become-pass` để nhập mật khẩu để truy cập remote machine.

### Basic Operations

*   Trước hết, hãy lưu các host đã biết trong file `/etc/ansible/hosts`:

    ```bash
    echo '192.168.122.123' >> /etc/ansible/hosts
    ```

*   Ping đến tất cả các host:

    ```bash
    ansible all -m ping
    ```

*   Hoặc ping đến một người dùng cụ thể:

    ```bash
    ansible all -m ping -u tupham
    ```

*   Chạy một command từ các hosts:

    ```bash
    ansible all -a 'echo "hello there"'
    ```

*   Chạy command từ host hiện tại, chỉ thị `-e` là extra variables:

    ```bash
    ansible localhost -m ping -e 'ansible_python_interpreter="usr/bin/env/python"'
    ```

##  Working with Inventory

Ansible có thể làm việc cùng lúc với nhiều hệ thống từ xa với điều kiện chúng được liệt kê trong danh sách Ansible inventory tại vị trí `/etc/ansible/hosts`.

Không những thế, Ansible còn có thể sử dụng nhiều inventoy files cùng lúc hoặc thậm chí là pull về các dynamic inventory từ nhiều nguồn khác nhau với các định dạng khác nhau (YAML, ini, etc).

Nội dung phần này chỉ ra các thành phần của một ansible inventory file, với khuôn dạng mặc định là INI. Bạn có thể xem nội dung tương tự với khuôn dạng file YAML tại [đây](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)

### Hosts and Groups

*   Group là tập hợp của nhiều host trong cùng một hệ thống, khai báo group dưới dạng một section theo cú pháp:

        # [GROUP_NAME]
        [webservers]
            ...

*   Dưới mỗi groupsection là danh sách các hosts, mỗi host nằm trên một dòng, cú pháp khai báo như sau:

        # HOST_NAME[:ALTERNATIVE_SSH_PORT]
        mail.example.com
        web.example.com:12345

*   Tạo host alias:

        # ALIAS_NAME ansible_port=ALTERNATIVE_SSH_PORT ansible_host=IP_ADDR
        jumper ansible_port=5555 ansible_host=192.168.2.2

*   Chỉ định người dùng cụ thể để SSH đến:
	```
	# HOSTNAME ansible_user=USER_NAME
	192.168.122.123 ansible_user=tupham
	```
*   Liệt kê hostname theo pattern:

        www[01:50].example.com
        db-[a:f].example.com

*   Sử dụng kết nối local thay vì SSH (chạy ansible trên máy trạm):

        localhost ansible_connection=localhost

### Host Variables

*   Định nghĩa biến cho host:

        # HOST_NAME var1=value1 var2=value2 ...
        host1 http_port=80 maxRequestPerChild=808

### Group Variables

*   Biến cũng có thể được định nghĩa cho group

        #[GROUP_NAME]
        ...

        # [GROUP_NAME:vars]
        # var1=value1
        # var2=value2

        [atlanta]
        host1
        host2

        [atlanta:vars]
        ntp_server=ntp.atlanta.example.com
        proxy=proxy.atlanta.example.com

### Groups of Groups

*   Sử dụng hậu tố `:children` để định nghĩa group chứa một hay nhiều group khác:

        [atlanta]
        host1
        host2

        [rayleigh]
        host3
        host4

        [southest:children]
        atlanta
        rayleigh

*   Một vài tính chất:
    *   Host thuộc group con thì thuộc group cha
    *   Biến của group con ghi đè biến cùng tên trong group cha
    *   Group có thể có nhiều cha hoặc con, nhưng không để cây phả hệ có chu trình
    *   Host cũng có thể thuộc nhiều group khác nhau, nhưng chỉ có một thể hiện duy nhất, trộn lẫn thông số của các group mà nó thuộc về

### Default Groups

Có hai group mặc định là `all` và `ungrouped`. `all` chứa tất cả các host, `ungrouped` chứa tất cả các host không có group nào khác ngoài `all`. 
=> Mọi hosts đều thuộc ít nhất 02 groups.

### Some Conventions
*   Không lưu biến trong inventory files
*   Danh sách biến của mỗi group hay host nên chứa trong các file riêng biệt, theo định dạng YAML hay JSON:

        # inventory file
        /etc/ansible/hosts

        # variable files
        /etc/ansible/group_vars/rayleigh
        /etc/ansible/group_vars/webservers
        /etc/ansible/host_vars/foosballs

*   Ansible sẽ tự động tìm đến các file variable (nếu có) theo convention này
*   Ta còn có thể chia nhỏ variable files thành nhiều file con, Ansible có thể tự động tìm và đọc hết tất cả các file này:

        /etc/ansible/group_vars/rayleigh/db_settings
        /etc/ansible/group_vars/rayleigh/cluster_settings

*   *Chú ý:* Các thư mục như `group_vars/` hay `host_vars/` có thể nằm trong cả thư mục inventory hoặc thư mục playbook. Trong trường hợp đó, các biến khai báo trong thư mục playbook sẽ ghi đè các biến khai báo trong thư mục inventory

### Merging Variables

Các biến trùng tên định nghĩa ở mức tổng quát sẽ bị ghi đè bởi mức cụ thể hơn theo thứ tự:

    all group -> parent group -> child group -> host

### Ansible Variables

Danh sách các biến điều khiển cho các hoạt động của ansible nằm ở [đây](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters)

## Working with Command Line Tools

`ansible` và `ansible-playbook` là hai lệnh phổ biến được sử dụng trong ansible, bên cạnh đó còn nhiều lệnh hữu ích khác được liệt kê dưới đây:

Command  |  Description
--  |  --
ansible  |  Cho phép định nghĩa và chạy các 'playbook' tasks trên các hosts khác nhau
ansible-config  |  Quản lý các thao tác cấu hình cho ansible từ dòng lệnh với các hành động như `view`, `list`, `dump`
ansible-consolde  |  Chạy các ad-hoc tasks trên một inventory
ansible-doc  |  In doc của một ansible module nào đó
ansible-inventory  |  Dump thông tin ansible inventory
ansible-playbook  |  Công cụ chạy ansible playbook trên một hệ thống gồm nhiều nút
ansible-pull  |  Chuyển ansible về trạng thái pull - Copy trạng thái của node được quản lý về node hiện tại
ansible-vault  |  Công cụ mã hóa của ansible

## Using Adhoc Commands

Ad-hoc commands là các công cụ giúp ta thực thi những tasks đơn giản một cách tại chỗ trên dòng lệnh mà không cần định nghĩa trong các file playbooks. Dưới đây là một vài trường hợp thường dùng adhoc commands:

### Các thủ tục cơ bản

- Chạy thủ tục trong nhiều luồng (mỗi luồng chạy trên một host) sử dụng chỉ thị `-f` :
	```
	 # reboot all hosts 10 at a time
	 ansible all -a 'reboot' -f 10 
	```
- Chạy module sử dụng chỉ thị `-m`:
	```
	# ping all hosts
	ansible all -m ping
	```
- Chạy thủ tục một cách bất đồng bộ sử dụng chỉ thị `-B`, chỉ định thời gian định kỳ in ra kết quả chỉ thị `-P`:
	```
	# prediocally reading log file each 10 seconds
	ansible all -m command -a "tailf /var/log/somefile.log" -B -P 10
	```
-  Chạy một shell command trên servers:
	```
	# Print terminal emulator
	ansible all -m shell -a 'echo $TERM'
	```	
### Quản lý files

-  Copy file tới remote hosts sử dụng module `copy`:
	```
	ansible all -m copy -a "src=/root/.bashrc dest=/root/.bashrc"
	```
*   Thay đổi quyền cho files sử dụng module `file`:
	```
	ansible all -m file -a "path=/tmp/abc mode=600 owner=tupham group=developers"
	```
*   Xóa file sử dụng module `file`:
	```
	ansible all -m file -a "path=/tmp/abc state=absent"
	```
### Quản lý Packages

*   Dùng `yum` hay `apt` để quản lý các gói phần mềm trên remote hosts
	```
	# Install latest version of mysql server
	ansible all -m apt -a "name=mysql-server"
	```
*   Kiểm tra package đang ở phiên bản mới nhất:
	```
	ansible all -m apt -a "name=vim state=latest"
	```
*   Kiểm tra package có ở phiên bản chỉ định không:
	```
	ansible all -m apt -a "name=acme-1.5 state=present"
	```
*   ...
### Deploying From Source Control

*   Triển khai một ứng dụng trực tiếp một git repo bằng module `git`:
	```
	ansible all -m git -a "repo=<git-repo> dest=<placement> version=HEAD"
	```
### Quản lý dịch vụ
*   Khởi động dịch vụ:
	```
	ansible all -m service -a "name=httpd state=started"
	```
*   Khởi động lại dịch vụ:
	```
	ansible all -m service -a "name=httpd state=restarted"
	```
*   Ngừng dịch vụ:
	```
	ansible all -m service -a "name=httpd state=stopped"
	```

## Working with Playbooks

Playbooks là ngôn ngữ cấu hình, triển khai và điều phối hệ thống từ xa của Ansible. Mỗi tài liệu playbook định nghĩa ra một danh sách các thủ tục sẽ lần lượt được thực thi trên server. Cách thức định nghĩa và quy trình triển khai ansible playbooks được giới thiệu trong tài liệu [này](./playbook.md)
