# OpenDaylight Controller

## Overview

-   Đặc điểm: Java-based, model-driven
-   Các công nghệ:
    -   **OSGI** : Framework backend
    -   **Karaf**: Cung cấp giao diện dòng lệnh dùng để cài đặt các packages
    -   **YANG** : Ngôn ngữ data modeling dùng để mô hình hóa các thông số cấu hình và trạng thái
-   Các hệ thống con:
    -   **Config**: Framework dùng để kích hoạt, quản lý phụ thuộc và cấu hình
    -   **MD-SAL**: Công cụ dùng để gửi và lưu trữ dữ liệu
    -   **MD-SAL Clustering**: Hỗ trợ tính năng phân cụm cho MD-SAL 
-   Hỗ trợ truy cập từ bên ngoài:
    -   **NETCONF**: XML API 
    -   **RESTCONF**: HTTP REST API

## RESTCONF API

### Overview

-   Hỗ trợ các thao tác cơ bản: **GET**, **PUT**, **POST**, **DELETE** và **OPTIONS**
-   Cấu trúc request và response có thể là [XML](http://tools.ietf.org/html/rfc6020) hoặc [JSON](http://tools.ietf.org/html/draft-lhotka-netmod-yang-json-02)
-   

