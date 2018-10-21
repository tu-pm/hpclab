# Ansible Documentation

## Overview

Ansible là một công cụ tự động hóa hoàn toàn các hoạt động cung cấp tài nguyên tính toán đám mây, quản lý các thao tác cấu hình, triển khai ứng dụng và quản lý nội dịch vụ.

Được thiết kế để hỗ trợ mô hình triển khai đa pha, Ansible mô hình hóa hạ tầng công nghệ thông tin bằng cách mô tả cách thức các hệ thống dưới góc nhìn tổng quan, thay vì xem xét từng hệ thống một cách riêng lẻ.

Ansible có thể dễ dàng được triển khai bằng cách sử dụng ngôn ngữ YAML để mô tả các công việc tự động hóa.

Phần này giới thiệu về những đặc trưng cơ bản nhất của Ansible.

### Efficient Architecture

Ansible hoạt động bằng cách kết nối các nodes và đẩy vào chúng các chương trình nhỏ có tên "Ansible modules". Các chương trình này là các mẫu tài nguyên để xây dựng trạng thái mong muốn của cả hệ thống. Ansible sau đó thực thi các modules này (thông qua SSH) và gỡ bỏ nó sau khi hoàn thành.

Thư viện của các modules này có thể nằm trên bất kỳ đâu mà không cần đến một server, daemon hay CSDL nào. Thông thường, bạn chỉ cần thao tác trên terminal, trên một chương trình soạn thảo và một hệ thống version control là đủ.

### SSH Keys

SSH keys là phương thức bảo mật được ưa chuộng bởi Ansible. Module "authorized_key" giúp người dùng quản lý được các machine nào được truy cập host nào. Bên cạnh SSH, các phương thức như kerberos và các hệ thống quản lý danh tính khác cũng có thể được sử dụng.

### Manage Your Inventory in Simple Text Files

Theo mặc định, Ansible mô tả những machines mà nó quản lý sử dụng một file `*.ini` đơn giản gom chúng chung vào một nhóm. Để có thể thêm một machine mới, ta chỉ việc thêm chúng vào file này. Các dữ liệu từ nguồn khác như EC2, RACKspace hay OpenStack cũng có thể được kéo về sử dụng dynamic inventory.

## Installation, Upgrade and Configuration

### Installation

Ansible hoạt động sử dụng SSH, tức là ta có thể cài đặt nó trên một máy và dùng nó điều khiển cả một hệ thống khác từ xa thông qua SSH. Các phiên bản hiện tại của Ansible có thể hoạt động trên bất kỳ máy nào có cài đặt Python (2.6, 2.7 hoặc >= 3.5). Trên nút điều khiển, ta cần có một phương thức để giao tiếp thông qua ssh, theo mặc định nó có thể là `sftp` hoặc `scp`.

Chú ý, trình thông dịch mặc định được sử dụng bởi ansible là `/usr/bin/python`. Nếu một hệ thống chỉ sử dụng python3, ta có thể gặp phải lỗi giống như sau:

    "module_stdout": "/bin/sh: /usr/bin/python: No such file or directory\r\n"

-> Ta cần sửa thao số `ansible_python_interpreter` trỏ vào thư mục `/usr/bin/python3` để sử dụng trình thông dịch python3.

#### Installing the Control Machine

Trên Ubuntu:

    ```bash
    $ sudo apt-get update
    $ sudo apt-get install software-properties-common
    $ sudo apt-add-repository ppa:ansible/ansible
    $ sudo apt-get update
    $ sudo apt-get install ansible
    ```
### Configuring Ansible

#### Configuration Files

Các thao tác cài đặt Ansible có thể được thay đổi thông qua một file cấu hình (`ansible.cfg`). Sau khi cài đặt ansible, file cấu hình mới nhất của nó có thể được đặt trong thư mục `/etc/ansible` với định dạng `.rpmnew`.

#### Environmental Configuration

Ansible cũng cho phép cấu hình các cài đặt sử dụng các biến môi trường. Nếu các biến này được đặt, chúng sẽ override các cài đặt có sẵn.

#### Command Line Options

Ta cũng có thể thay đổi cấu hình cài đặt thông qua hệ thống dòng lệnh

## Getting Started

### Remote Connection Information

Trong một vài trường hợp hiếm gặp khi thiết bị từ xa không hỗ trợ SFTP, ta có thể cấu hình Ansible sử dụng SCP mode thay thế.

Khi giao tiếp với các máy từ xa, Ansible mặc định sử dụng SSH keys. Nếu muốn sử dụng mật khẩu, ta cần thêm các option như `--ask-pass` hay `--ask-become-pass` để lấy mật khẩu và mật khẩu root truy cập remote machine.

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

       # HOSTNAME ansible_user=USER_NAME
        192.168.122.123 ansible_user=tupham

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

-> Tất cả các host đều thuộc ít nhất 2 group

### Some Conventions

*   Không chứa biến trong inventory files
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

Các biến trùng tên định nghĩa ở mức trừu tượng hơn sẽ bị ghi đè bởi mức cụ thể hơn theo thứ tự:

    all group-> parent group -> child group -> host

### Ansible Variables

Danh sách các biến điều khiển quá trình hoạt động của ansible nằm ở [đây](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#list-of-behavioral-inventory-parameters)

### Non SSH Connection Types

Bên cạnh SSH, Ansible còn quản lý hoạt động của hosts theo các kiểu giao tiếp sau:

*   local: Quản lý thao tác trên chính nút kiểm soát
*   docker: Quản lý các Docker containers sử dụng Docker client cục bộ

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

Ad-hoc Commands là công cụ giúp ta thực thi những tasks đơn giản một cách tại chỗ mà không cần lưu lại.

Các mục dưới đây đề cập đến các ca sử dụng mà ad-hoc commands có thể xử lý rất tốt.

### Paralellism and Shell Commands

*   Thực hiện một tác vụ nào đó trên tất cả các host trong một group với số tiến trình song song ( = số host cùng lúc chạy tác vụ) chỉ định:

        # ansible GROUP_NAME -a 'COMMAND' -f N_PROCESSES
        ansible atlanta -a 'reboot' -f 10 #reboot all hosts in atlanta group 10 at a time

*   Các chỉ thị liên quan tới user trên remote host:
    *   `-u foo`: Chạy lệnh với tư cách của người dùng `foo`, tương đương với lệnh `sudo -u foo`
    *   `--become-user`: Trở thành người dùng `foo` trước khi chạy câu lệnh, tương đương với lệnh `su - foo`
    *   `--ask-become-pass`: Hiển thị ô nhập mật khẩu (nếu cần), sử dụng kèm với chỉ thị `--become-user`
    *   `--become`: Trở thành root, tương tự `su -`

*   Chạy một ansible module:
    *   Dùng chỉ thị `-m` để chỉ ra module nào cần chạy, mặc định là `command`

        ansible atlanta -m ping

    *   `shell` vs `command` module
        *   Cùng dùng để chạy lệnh trên remote hosts
        *   `shell` hỗ trợ các cú pháp như piping hay chuyển hướng, các cú pháp shell-like, command thì không

### File Transfer

*   Copy một file cục bộ tới các remote hosts với module `copy`:

        ansible atlanta -m copy -a "src=<source_file> dest=<destination>"

*   Thay đổi quyền đối với files bằng module `file`:

        ansible atlanta -m file -a "dest=/tmp/abc mode=600 owner=tupham group=developers"

*   Module `file` cũng dùng để tạo mới hay xóa file trên remote hosts

### Managing Packages

*   Dùng `yum` hay `apt` để quản lý các gói phần mềm trên remote hosts

*   Kiểm tra package đang ở phiên bản mới nhất:

        ansible atlanta -m apt -a "name=vim state=lastest"

*   Kiểm tra package có ở phiên bản chỉ định không:

        ansible atlanta -m apt -a "name=acme-1.5 state=present"

*   ...

### Deploying From Source Control

*   Triển khai một ứng dụng trực tiếp một git repo bằng module `git`:

        ansible atlanta -m git -a "repo=<git-repo> dest=<placement> version=HEAD"

### Managing Services

*   Quản lý một dịch vụ nào đó trên remote hosts bằng module `service`

*   Chạy một dịch vụ nào đó:

        ansible atlanta -m service -a "name=httpd state=started"

*   Khởi động lại dịch vụ:

        ansible atlanta -m service -a "name=httpd state=restarted"

*   Ngừng dịch vụ:

        ansible atlanta -m service -a "name=httpd state=stopped"

### Time Limited Background Operation

*   Có thể chỉ định một lệnh chạy bất đồng bộ trên background:

*   Dùng chỉ thị `-B <timeout>` để yêu cầu một lệnh chạy ngầm với khoảng thời gian tối đa là `timeout`:

        ansible all -B 3600 -a "some command here..."

*   Dùng chỉ thị `-P n_secs` để kiểm tra trạng thái lệnh chạy ngầm sau `n_secs` giây

        ansible all -B 3600 -P 60 -a "some command here"

*   Cũng có thể kiểm tra trạng thái lệnh bằng module `async_status`

### Gathering Facts:

*   Lấy về facts (các thông tin định nghĩa playbook) cho các hosts:

        ansible all -m setup

## Working with Playbooks

Playbooks là ngôn ngữ cấu hình, triển khai và điều phối hệ thống từ xa của Ansible. Nó có thể được dùng để mô tả các chính sách mà hệ thống từ xa phải đảm bảo hoặc là các bước trong một quy trình IT nào đó.

Tìm hiểu về Playbook là tìm hiểu một ngôn ngữ hoàn toàn mới với nhiều cú pháp và quy trình khác nhau, bởi vậy nội dung này sẽ được viết trong một tài liệu hoàn toàn mới.
