# Ansible Playbook Documentation

Playbooks là ngôn ngữ cấu hình, triển khai và điều phối hệ thống từ xa của Ansible. Nó có thể được dùng để mô tả các chính sách yêu cầu đối với hệ thống từ xa hay các bước trong một quy trình IT nào đó.

Tài liệu này tập trung giới thiệu về cú pháp, cách dùng và một số ví dụ của Playbook.

## Intro to Playbook

### Playbook Language Example

Playbooks được thể hiện bằng cú pháp YAML.

Mỗi playbook chứa một danh sách gồm nhiều 'plays'. Mỗi `play` có chức năng kết nối một tập các hosts với các vai trò định trước, thao tác này được thể hiện trong các "tasks". Mỗi `task` là một lời gọi đến một ansible module.

Dưới đây là ví dụ về một playbook chỉ chứa một `play`:

```yaml
---
- hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  remote_user: root
  tasks:
  - name: ensure apache is at the latest version
    yum:
      name: httpd
      state: latest
  - name: write the apache config file
    template:
      src: /srv/httpd.j2
      dest: /etc/httpd.conf
    notify:
    - restart apache
  - name: ensure apache is running
    service:
      name: httpd
      state: started
  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
```

Giải thích: Play này thực hiện trên các hosts nằm trong group `webservers` dưới quyền người dùng `root`, bao gồm các 3 tasks:

*   Tải httpd bằng module `yum`
*   Tạo apche config file bằng module `template`
*   Khởi động apache
*   Khởi động lại apache

Playbook cũng có thể có nhiều `play`:

```yaml
---
- hosts: webservers
  remote_user: root

  tasks:
  - name: ensure apache is at the latest version
    yum:
      name: httpd
      state: latest
  - name: write the apache config file
    template:
      src: /srv/httpd.j2
      dest: /etc/httpd.conf

- hosts: databases
  remote_user: root

  tasks:
  - name: ensure postgresql is at the latest version
    yum:
      name: postgresql
      state: latest
  - name: ensure that postgresql is started
    service:
      name: postgresql
      state: started
```
### Basics

#### Hosts and Users

*   Chọn các máy trạm và người dùng để chạy một play:

    ```yaml
    ---
    - hosts: webservers
      remote_user: root
    ```
*   Ta cũng có thể xác định user trong tasks, hoặc chạy play dưới quyền người dùng khác (với các chỉ thị `become`, `become_user`, `become_method`, ...)

*   Xác định thứ tự chạy play giữa các hosts:

    ```yaml
    - hosts: all
      order: sorted
      gather_facts: False
      tasks:
        - debug:
            var: inventory_hostname
    ```
*   order = {sorted, reverse_sorted (theo tên), inventory, reverse_inventory (theo thứ tự định nghĩa trong file inventory), shuffle (ngẫu nhiên)}

#### Tasks List

Mỗi play gồm một danh sách các tasks. Các tasks được thực thi lần lượt theo thứ tự trên tất cả các máy trong danh sách `hosts`. Khi thực thi playbook, nếu như một máy nào đó failed với một task nào đó, nó sẽ bị loại ra khỏi vòng lặp thao tác.

Mỗi task có mục đích là thực thi một module nào đó với các tham số cụ thể. Các tham số này có thể được truyền trực tiếp hoặc truyền từ danh sách biến định nghĩa trước.

Các module là **indempotent**, nếu ta đã chạy một module nào đó và đạt được trạng thái mong muốn rồi thì yêu cầu chạy lại nó với danh sách tham số cũ sẽ không được thực hiện.

Mỗi task nên có một tên cụ thể. Tên này được được hiển thị ra trong output của playbook. Bởi thế, nên đặt tên dễ hiểu và mô tả chính xác công việc mà task thực hiện.

Mỗi `task` có một module, mỗi module chứa các tham số dưới dạng dict, duy chỉ có `shell` và `command` là có thể có tham số chứa trong một list.

Sử dụng biến đã định nghĩa trong mục `vars`:

```yaml
tasks:
  - name: create a virtual host file for {{ vhost }}
    template:
      src: somefile.j2
      dest: /etc/httpd/conf.d/{{ vhost }}
```

#### Handlers

Sử dụng lênh `notify` tại cuối mỗi khối `task` để chỉ ra hành động mà chỉ được thực hiện một lần duy nhất, ngay cả khi hành động đấy được yêu cầu cùng lúc bởi nhiều tasks khác nhau. Ví dụ:

```yaml
- name: template configuration file
  template:
    src: template.j2
    dest: /etc/foo.conf
  notify:
     - restart memcached
     - restart apache
```

Những hành động trong `notify` được gọi là các `handlers`. Các `handlers` được định nghĩa trong section `handlers` trong playbook giống như cách định nghĩa các tasks. Handlers chỉ chạy một lần sau khi tất cả các tasks trong plays hòan tất, ngay cả khi nó được notify nhiều lần. Dưới đây là định nghĩa của các handlers được notify trong ví dụ trên:

```yaml
handlers:
    - name: restart memcached
      service:
        name: memcached
        state: restarted
    - name: restart apache
      service:
        name: apache
        state: restarted
```

Kể từ Ansible 2.2, `handlers` có thể "lắng nghe" một `topic` nào đó, các `tasks` notify một `topic` cũng đồng thời notify các handlers lắng nghe luôn:

```yaml
handlers:
    - name: restart memcached
      service:
        name: memcached
        state: restarted
      listen: "restart web services"
    - name: restart apache
      service:
        name: apache
        state:restarted
      listen: "restart web services"

tasks:
    - name: restart everything
      command: echo "this task will restart the web services"
      notify: "restart web services"
```
Cách làm này khiến cho việc trigger nhiều handlers cùng lúc và quản lý chúng trở nên dễ dàng hơn.

#### Executing A Playbook

Thực thi một playbook với số lượng tiến trình song song xác định:

    ansible-playbook playbook.yaml -f 10

#### Tips and Tricks

*   Kiểm tra cú pháp của tài liệu ansible:

        ansible-playbook <name> --syntax-check

## Creating Reusable Playbooks

### Roles

`Role` là cách thức để tự động load các file `vars`, `tasks` và `handlers` dựa trên một cấu trúc file định sẵn. Gom nhóm các nội dung này bằng các `roles` còn giúp cho việc chia sẻ `role` dễ dàng hơn.

#### Role Directory Structure

Ví dụ về cấu trúc của một project:

```yaml
site.yml
webservers.yml
fooservers.yml
roles/
   common/
     tasks/
     handlers/
     files/
     templates/
     vars/
     defaults/
     meta/
   webservers/
     tasks/
     defaults/
     meta/
```

