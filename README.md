# Toolshop Automation – Nhóm HHK

[![CI](https://github.com/LuuThiAnhHuyen/toolshop-automation-nhomHHK/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/LuuThiAnhHuyen/toolshop-automation-nhomHHK/actions/workflows/ci.yml)

Bộ kiểm thử tự động cho Toolshop, sử dụng Python, pytest và Playwright.

## Chạy kiểm thử

Sao chép file cấu hình mẫu, sau đó cài thư viện và trình duyệt Playwright:

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
pytest -v
```

Chạy riêng feature BDD:

```bash
pytest tests/bdd -v
```

## Kết quả CI

<!-- Bổ sung docs/screenshots/ci-green.png sau khi workflow CI của nhóm chạy xanh cả 3 trình duyệt trên main. -->

## Trace Viewer

![Trace Viewer hiển thị bước kiểm thử bị lỗi](docs/screenshots/trace-viewer.png)
