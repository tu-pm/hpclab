# Using OpenDaylight SDN Controller in Mininet

## Setting up

-   Sử dụng 2 máy ảo, 1 chạy mininet và 1 cài OpenDaylight
-   Cài đặt Mininet: Import image của Mininet vào VirtualBox và khởi động
-   Cài đặt OpenDaylight:
    -   Tạo máy ảo `OpenDaylight` bằng VirtualBox với tối thiểu 2GB RAM và 2 nhân CPU
    -   Cấu hình thêm một adapter sử dụng host-only network cho máy ảo vừa được tạo ra
    -   Cài đặt và cấu hình JRE 8:
        ```bash
        $ sudo apt update && sudo apt install openjdk-8-jre
        $ echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc && source ~/.bashrc
        ```
    -   Cài đặt OpenDaylight: Tải file nén trên trang chủ Opendaylight, giải nén và khởi động `karaf`:
        ```bash
        $ ./bin/karaf
        ```
    -   Cài đặt các yêu cầu tối thiểu cùng với công cụ giao diện của OpenDaylight trong cửa sổ `karaf`:
        ```bash
        > feature:install odl-restconf odl-l2switch-switch odl-mdsal-apidocs odl-dlux-all
        ```

sudo mn --custom ~/mininet/custom/routing.py --topo mytopo --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=192.168.56.102
