# HỆ THỐNG TIẾP NHẬN VÀ XỬ LÝ YÊU CẦU SINH VIÊN TRÊN ODOO

## 1. Giới thiệu

**Tên đề tài:** Xây dựng hệ thống tiếp nhận và xử lý yêu cầu sinh viên trên nền tảng Odoo.

**Tên module:** `student_request_management`

Hệ thống hỗ trợ sinh viên gửi yêu cầu trực tuyến, đồng thời giúp bộ phận nhà trường tiếp nhận, phân loại, phân công và theo dõi tiến độ xử lý yêu cầu.

### Chức năng chính

- Tiếp nhận yêu cầu sinh viên thông qua biểu mẫu trực tuyến.
- Lưu trữ thông tin sinh viên: mã sinh viên, họ tên, lớp, ngành, email và số điện thoại.
- Quản lý 20 loại yêu cầu sinh viên.
- Tự động tạo dữ liệu yêu cầu trong CRM.
- Phân loại yêu cầu theo phòng ban phụ trách.
- Tự động tính ngày dự kiến hoàn thành theo thời gian xử lý quy định.
- Theo dõi tiến độ qua 5 giai đoạn:
  1. Mới tiếp nhận.
  2. Đã phân loại.
  3. Đang xử lý.
  4. Chờ sinh viên bổ sung.
  5. Hoàn tất.
- Quản lý nội dung cần sinh viên bổ sung và kết quả xử lý.
- Kiểm tra điều kiện trước khi chuyển yêu cầu sang trạng thái hoàn tất.
- Tự động cập nhật trạng thái quá hạn bằng Scheduled Action chạy định kỳ mỗi ngày.

## 2. Công nghệ sử dụng

- Odoo 20.0.
- Python.
- PostgreSQL.
- XML.
- HTML/CSS.
- JavaScript (nếu có trong module).
- Odoo CRM.
- Odoo Website.

## 3. Yêu cầu môi trường

Máy tính cần cài đặt:

- Windows 10 hoặc Windows 11.
- Odoo 20.0.
- PostgreSQL tương thích với phiên bản Odoo.
- Python đi kèm bộ cài Odoo hoặc môi trường Python tương thích.
- Git.

**Lưu ý:** Dự án GitHub chỉ chứa mã nguồn module tùy chỉnh, không bao gồm bộ cài Odoo, PostgreSQL hoặc cơ sở dữ liệu.

## 4. Cài đặt dự án

### Bước 1. Cài đặt Odoo

Cài đặt Odoo 20.0 và PostgreSQL trên máy tính.

Đảm bảo Odoo có thể khởi động và truy cập được qua trình duyệt.

### Bước 2. Tải mã nguồn từ GitHub

Mở PowerShell và chuyển đến thư mục custom addons:

```powershell
cd D:\Odoo\custom_addons
```

Tải dự án:

```powershell
git clone <GITHUB_REPOSITORY_URL>
```

Sau khi tải về, kiểm tra thư mục:

```text
D:\Odoo\custom_addons\student_request_management
```

### Bước 3. Kiểm tra cấu hình Odoo

Mở file cấu hình:

```text
D:\Odoo\server\odoo.conf
```

Đảm bảo cấu hình `addons_path` có chứa thư mục custom addons:

```ini
addons_path = D:\Odoo\server\odoo\addons,D:\Odoo\custom_addons
```

Nếu cấu hình đã có đường dẫn này thì không cần thêm lại.

### Bước 4. Tạo cơ sở dữ liệu

Khởi động Odoo, truy cập:

```text
http://localhost:8069
```

Tạo một cơ sở dữ liệu mới, ví dụ:

```text
student_request_db
```

Thiết lập thông tin quản trị cơ sở dữ liệu theo môi trường cài đặt.

### Bước 5. Cài đặt module

Đăng nhập Odoo bằng tài khoản quản trị.

1. Bật chế độ nhà phát triển.
2. Mở ứng dụng Apps.
3. Chọn Update Apps List.
4. Tìm module `Student Request Management`.
5. Nhấn Install.

Nếu module không xuất hiện, kiểm tra lại `addons_path`, tên thư mục module và file `__manifest__.py`.

## 5. Cập nhật module bằng PowerShell

Khi mã nguồn được cập nhật từ GitHub hoặc có thay đổi trong module, có thể nâng cấp module bằng lệnh:

```powershell
& "D:\Odoo\python\python.exe" "D:\Odoo\server\odoo-bin" -c "D:\Odoo\server\odoo.conf" -d student_request_db -u student_request_management --stop-after-init
```

Thay `student_request_db` bằng tên cơ sở dữ liệu đang sử dụng.

Sau khi nâng cấp thành công, khởi động lại dịch vụ Odoo:

```powershell
Restart-Service -Name odoo-server-20.0 -Force
```

**Lưu ý:** Đường dẫn Python, Odoo, file cấu hình và tên dịch vụ có thể khác tùy máy tính.

## 6. Truy cập hệ thống

Sau khi cài đặt module thành công, truy cập:

**Trang gửi yêu cầu sinh viên:**

```text
http://localhost:8069/student/request
```

**Trang quản lý Odoo:**

```text
http://localhost:8069/web
```

Nhân viên và quản trị viên đăng nhập vào Odoo để quản lý yêu cầu thông qua CRM.

## 7. Kiểm tra chức năng

Sau khi cài đặt, nên kiểm tra lần lượt:

1. Truy cập biểu mẫu gửi yêu cầu sinh viên.
2. Nhập thông tin sinh viên và nội dung yêu cầu.
3. Gửi biểu mẫu và kiểm tra yêu cầu được tạo trong CRM.
4. Kiểm tra thông tin sinh viên, loại yêu cầu và phòng ban phụ trách.
5. Kiểm tra ngày tiếp nhận và ngày dự kiến hoàn thành.
6. Thử chuyển yêu cầu qua các giai đoạn xử lý.
7. Kiểm tra điều kiện bắt buộc khi chuyển sang giai đoạn Hoàn tất.
8. Kiểm tra điều kiện nhập nội dung khi chuyển sang Chờ sinh viên bổ sung.
9. Kiểm tra trường Quá hạn xử lý.
10. Vào Settings → Technical → Automation → Scheduled Actions để kiểm tra tác vụ tự động cập nhật yêu cầu quá hạn.

## 8. Cấu trúc thư mục module

```text
student_request_management/
│
├── __init__.py
├── __manifest__.py
├── README.md
│
├── controllers/
│   ├── __init__.py
│   └── main.py
│
├── models/
│   ├── __init__.py
│   └── crm_lead.py
│
├── views/
│   └── crm_lead_views.xml
│
├── templates/
│   └── student_request_templates.xml
│
└── data/
    └── ir_cron.xml
```

Cấu trúc trên mang tính minh họa. Các thư mục và file khác đang được khai báo trong module cũng cần được giữ nguyên khi tải dự án.

## 9. Lưu ý khi phát triển nhóm

- Mỗi thành viên sử dụng tài khoản Odoo riêng.
- Không chia sẻ mật khẩu quản trị.
- Không chỉnh sửa trực tiếp cùng một file khi thành viên khác đang thực hiện thay đổi.
- Sử dụng Git để quản lý phiên bản mã nguồn.
- Pull mã nguồn mới nhất trước khi bắt đầu công việc.
- Kiểm tra và nâng cấp module trên cơ sở dữ liệu thử nghiệm trước khi áp dụng vào cơ sở dữ liệu chính.
- Không đưa thông tin đăng nhập, dữ liệu sinh viên thật hoặc file cấu hình cá nhân lên GitHub.

## 10. Thông tin dự án

**Tên dự án:** Hệ thống tiếp nhận và xử lý yêu cầu sinh viên trên nền tảng Odoo.

**Module:** `student_request_management`

**Nền tảng:** Odoo 20.0.

**Mục đích:** Hỗ trợ số hóa quy trình tiếp nhận, quản lý và theo dõi quá trình xử lý yêu cầu sinh viên trong môi trường giáo dục.