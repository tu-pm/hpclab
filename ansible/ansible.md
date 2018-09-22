# Ansible Documentation

## Overview

Ansible là một công cụ tự động hóa hoàn toàn các hoạt động cung cấp tài nguyên tính toán đám mây, quản lý các thao tác cấu hình, triển khai ứng dụng và quản lý nội dịch vụ.

Được thiết kế để hỗ trợ mô hình triển khai đa pha, Ansible mô hình hóa hạ tầng công nghệ thông tin bằng cách mô tả cách thức các hệ thống tương quan với nhau, thay vì xem xét từng hệ thống một cách riêng lẻ.

Ansible có thể dễ dàng được triển khai, nó sử dụng ngôn ngữ YAML dùng để mô tả các công việc tự động hóa theo một cách gần ngôn ngữ tự nhiên nhất.

Phần này giới thiệu về những đặc trưng cơ bản nhất của Ansible.

### Efficient Architecture

Ansible hoạt động bằng cách kết nối các nodes và đẩy vào chúng các chương trình nhỏ có tên "Ansible modules". Các chương trình này là các mẫu tài nguyên để xây dựng trạng thái mong muốn của cả hệ thống. Ansible sau đó thực thi các modules này (thông qua SSH) và gỡ bỏ nó sau khi hoàn thành.

Thư viện của các modules này có thể nằm trên bất kỳ module nào mà không cần servers, daemons hay CSDL nào. Thông thường, bạn chỉ cần thao tác trên terminal, trên một chương trình soạn thảo và một hệ thống version control là đủ.

### SSH Keys

SSH keys là phương thức bảo mật được ưa chuộng hơn bởi Ansible. Module "authorized_key" giúp người dùng quản lý được các machine nào được truy cập host nào. Bên cạnh SSH, các phương thức như kerberos và các hệ thống quản lý danh tính khác cũng có thể được sử dụng.

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

Các thao tác cài đặt Ansible có thể được thay đổi thông qua một file cấu hình (`ansible.cfg`). Sau khi cài đặt ansible, file cấu hình mới nhất của nó có thể được đặt trong thư mục `etc/ansible` với định dạng `.rpmnew`.

#### Environmental Configuration

Ansible cũng cho phép cấu hình các cài đặt sử dụng các biến môi trường. Nếu các biến này được đặt, chúng sẽ override các cài đặt có sẵn.

#### Command Line Options

Ta cũng có thể thay đổi cấu hình cài đặt thông qua hệ thống dòng lệnh

## Getting Started

### Remote Connection Information

Trong một vài trường hợp hiếm gặp khi thiết bị từ xa không hỗ trợ SFTP, ta có thể cấu hình Ansible sử dụng SCP mode thay thế.

Khi giao tiếp với các máy từ xa, Ansible mặc định sử dụng SSH keys. Nếu muốn sử dụng mật khẩu, ta cần thêm các option như `--ask-pass` hay `--ask-become-pass` để lấy mật khẩu và mật khẩu root truy cập remote machine.

### Basic Operations

*   Trước hết, hãy lưu các host đã biết trong file `/etc/ansible/hosts`. 
