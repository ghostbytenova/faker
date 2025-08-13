# faker
Python Faker module for generating realistic fake user data — names, usernames, emails, birthdays, and more. Supports Vietnamese language and customizable formats.

# Hướng dẫn sử dụng Module Faker

## 1. Giới thiệu
Module `Faker` được sử dụng để sinh dữ liệu giả lập như tên, họ, ngày sinh, username, email,... phục vụ cho mục đích test hoặc tạo dữ liệu mẫu.

## 2. Cài đặt
```bash
pip install unidecode
```
Đảm bảo bạn đã có cấu trúc thư mục dữ liệu:
```
data/
  vietnamese/
    firstnames.txt
    all.txt
    boy.txt
    girl.txt
```

## 3. Cách sử dụng cơ bản

### 3.1. Import và khởi tạo
```python
from faker_module import Faker

faker = Faker(lang="vietnamese", gender="all")
```

### 3.2. Lấy tên và họ
```python
first_name = faker.first_name()
last_name = faker.last_name()
full_name = faker.fullname()
```

### 3.3. Sinh username
```python
username = faker.username()
```

### 3.4. Sinh email
```python
email = faker.email(server="gmail.com")
```

### 3.5. Sinh ngày sinh
```python
birthday = faker.birthday(min=1990, max=2005)
print(birthday.format("dd/mm/yyyy"))
```

## 4. Sinh toàn bộ thông tin
```python
info = Faker.generateInformation()
print(info.fullName, info.username, info.birthday)
```

## 5. Ví dụ nâng cao

### 5.1. Tuỳ chỉnh định dạng ngày sinh
```python
faker = Faker()
dob = faker.birthday(min=1995, max=2005)
print(dob.format("dd-mm-yyyy"))   # 05-07-1999
print(dob.format("d/m/yy"))       # 5/7/99
print(dob.format("yyyy.mm.dd"))   # 1999.07.05
```

### 5.2. Sinh username kèm hậu tố số hoặc chữ
```python
faker = Faker()
print(faker.username(sep="_", ext=int, range_ext=(100, 999)))   # nguyen_hoang_472
print(faker.username(sep="", ext=str, range_ext=6))             # tranthaoAbX9kP
```

### 5.3. Sinh nhiều thông tin và xuất ra JSON
```python
import json

users = [Faker.generateInformation() for _ in range(5)]
print(json.dumps([u.__dict__ for u in users], ensure_ascii=False, indent=2))
```

### 5.4. Loại bỏ dấu tiếng Việt
```python
faker = Faker(lang="vietnamese", gender="all")
print(faker.fullname(unsigned=True))   # Nguyen Van Nam
```
