# Vim Tips and Tricks

## Macros

### How to Create Macros

*   Bước 1: Nhấn 'q'
*   Bước 2: Chọn ký tự để lưu macro, vim sẽ bắt đầu quay các thao tác của bạn
*   Bước 3: Thực hiện các thao tác cần làm trên file
*   Bước 4: Nhấn lại 'q' để kết thúc quay, macro sẽ được lưu vào ký tự đã chọn

### Comment a Paragraph

Thực hiện các thao tác dưới đây:

1. Đặt con trỏ văn bản trong paragraph
2. Nhấn tổ hợp **`vip`** để chọn cả đoạn
3. Nhấn **`:`** để thực hiện command
4. Thêm cụm `s/^/#` vào trong command và nhấn enter ('#' là ký tự để comment)

-> Xong.

### Un comment a Paragraph

Thực hiện các thao tác dưới đây:

1. Đặt con trỏ văn bản trong paragraph
2. Nhấn tổ hợp **`vip`** để chọn cả đoạn
3. Nhấn **`:`** để thực hiện command
4. Thêm cụm `s/^#/` vào trong command và nhấn enter ('#' là ký tự để comment)

-> Xong.

