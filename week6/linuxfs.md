# Linux Disk and File System Management

## File System Terminologies

### File Systems

**File system types**:
    *   Linux native: `ext3`, `ext4`, `squashfs`, `btrfs`
    *   Windows: `ntfs`, `fat`
    *   MacOS: `hfs`, `hfs+`
    *   IBM: `JFS`
    *   SGI: `xfs`

### Partitions

*   Partition là phân vùng vật lý chứa file system. Mỗi file system được chứa trong một partition và mỗi partition cũng chỉ chứa một file system (đối với linux thuần)
*   Các loại partitions:
    *   Primary Partition: Trực tiếp chứa không gian trên ổ cứng xác định bởi sector đầu và cuối của nó. Nó còn chứa các file boot của hệ điều hành hoặc thông tin cấu hình của người dùng.
    *   Extended Partition: Là phân vùng chứa các phân vùng khác, thường là các logical partitions. Nó chỉ quản lý các thông tin của các partitions khác mà không chứa file boot cho hệ điều hành như primary partitions.
    *   Logical Partition: Nằm trong extended partition, thường nhằm mục đích lưu trữ file system độc lập của người dùng. Swap space là một dạng logical partition
    *   Linux LVM Partition: Chứa các filesystems được tạo ra trên ổ đĩa ảo. LVM (Logical Volume Management) là một tính năng của Linux giúp tạo ra tại chỗ các ổ đĩa ảo trên các phân vùng vật lý. Một ổ đĩa ảo là tập hợp các ổ đĩa vật lý nằm trên nhiều partitions khác nhau được gom nhóm bởi LVM và được dùng để định nghĩa ra các file system
*   Ví dụ: `root(/)`, `/home` và `/tmp` file systems thường được tách biệt với nhau trong các partition riêng
*   Có tất cả 4 primary partitions và 1 extended partition trong một hệ thống Linux

### Mount Point

*   Mount point chỉ đơn giản là file bắt đầu cho một file system (thường là file rỗng)

![mount-points](https://prod-edxapp.edx-cdn.org/assets/courseware/v1/90eea9eba0b63783a8bcf2b85ae8a9e3/asset-v1:LinuxFoundationX+LFS101x+1T2017+type@asset+block/LFS01_ch08_screen06.jpg)

*   Mounting là thao tác gắn mount point cho một file system. Mount point được gắn cho file system có thể là bất kì node nào trên cây thư mục.

### Network File System

NFS là hệ thống file phân tán thường được sử dụng nhất đối với servers.

### Backing up Files

`rsync` là một tiện ích mạnh mẽ giúp đồng bộ hóa dữ liệu giữa hai thư mục trên cùng một máy hay giữa hai máy khác nhau.

## Linux Commands for Working with File Systems

*   **`fdisk`** - Tạo, sửa, xóa partitions
*   **`df`** - Hiển thị tất cả filesystems đã được mount trong hệ thống file của Linux và điểm mount của chúng
*  **`mount & umount`** - Mount/Unmount một file system
*   **mkfs** - Tạo và format một file system
*   File **`/etc/fstab`**: Chứa thông tin của các partition và được đọc tại boot time giúp mount các partitions trên hệ thống. Partition được xác định bởi UUID duy nhất hoặc nhãn (label)

## Create and Configure New Volumes for VM Instances

*   Trên host:
    *   Tạo ổ đĩa mới:
        ```bash
        # virsh vol-create-as default VOL_NAME SIZE --format qcow2
        ``` 
    *   Gắn ổ đĩa cho instance:
        ```bash
        # virsh attach-disk VM_NAME \
        --source /var/lib/libvirt/images/VOL_NAME.qcow2 \
        --target PARTITION_NAME
        --persistent
        ```
    *   Chú ý: Linux cho phép tồn tại tối đa 16 partition trên một hard disk, tên của partition được đặt theo quy ước: **`sdxn`** cho `SATA`, `SCSI` hoặc `PATA` drive và **`vdxn`** cho các ổ đĩa ảo trên các máy ảo KVM, trong đó **`x`** là một kí tự alphabet và **`n`** là một chữ số thập phân.
*   Trên VM:
    *   Tạo partition trên ổ đĩa:
        ```bash
        # fdisk /dev/PARTITION_NAME
        ```
    *   Chọn `n` để thêm một partition, lần lượt thực hiện các thao tác theo yêu cầu để khởi tạo partition. Chọn `w` để lưu thay đổi.
    *   Tạo file system trên partition:
        ```bash
        # mkfs --type ext4 /dev/PARTITION_NAME
        ``
    *   Tạo thư mục mount:
        ```bash
        # mkdir MOUNT_DIR
        ```
    *   Mount file system vừa tạo với thư mục mount:
        ```bash
        # mount /dev/PARTITION_NAME MOUNT_DIR
        ```
    *   Thay đổi thông tin trong file `/etc/fstab/` để lưu thay đổi khi reboot:
        ```bash
        /dev/PARTITION_NAME   MOUNT_DIR defaults    0   0
        ```

**DONE!!**
