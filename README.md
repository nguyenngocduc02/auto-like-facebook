# Auto click like
Tự động click nút like dựa vào danh sách có sẵn trong file txt

## _Yêu cầu bắt buộc: Máy tính có cài đặt Firefox và đã đăng nhập Facebook trên Firefox_

## Cài đặt

Tạo Python virtual environment cho project Python
```bash
python -m venv ./venv
```
Chạy virtual environment bằng CMD Windows
```bash
.\venv\Scripts\activate.bat
```
Install các package cần thiết
```bash
pip install -r requirements.txt
```
Tìm profile của Firefox bằng cách dùng about:profiles, sau đó copy vào dòng 111
Copy các link vào file facebook_links.txt rồi chạy code
```bash
python main.py
```
## _Với các lần chạy sau, chỉ cần thay đổi nội dung trong file facebook_links.txt, sau đó chạy file bat._

