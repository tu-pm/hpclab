# Problem Resolving

**#1: Disable KVM service and switch to VirtualBox, then switch back**

Khi ta sử dụng lệnh `docker-machine create` để tạo máy ảo, công cụ mặc định được sử dụng là VirtualBox. Tuy nhiên, VirtualBox không thể cùng tồn tại với KVM, bởi vậy ta cần phải tạm thời "tắt" KVM khi làm việc với `docker-machine`.

*   Ngừng hoạt động KVM và chuyển sang VirtualBox:

    /sbin/rmmod kvm_intel && /sbin/rmmod kvm && /etc/init.d/vboxdrv start

*   Nạp lại KVM

    /etc/init.d/vboxdrv stop && /sbin/insmod /lib/modules/`uname -r`/kernel/arch/x86/kvm/kvm.ko  && /sbin/insmod /lib/modules/`uname -r`/kernel/arch/x86/kvm/kvm-intel.ko

*Chú ý*

*   Các lệnh trên phải được chạy dưới quyền root
*   Phải shutdown tất cả các máy ảo KVM trước

**#2: Docker 'swarm leave' stucks on host**


**#3: Worker in status "Down" after reboot**
