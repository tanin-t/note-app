# 📝 Note App — เรียน Vue.js ด้วยการสร้างแอปจดบันทึก

Tutorial สำหรับเรียนรู้ Vue.js ตั้งแต่เริ่มต้น โดยค่อยๆ สร้าง Note App ที่ใช้งานได้จริง เชื่อมต่อกับ Backend Django REST API

## 🎯 เหมาะสำหรับใคร

- นักเรียนที่รู้ HTML, CSS, JavaScript พื้นฐานแล้ว
- ต้องการเรียนรู้ Vue.js แบบ step-by-step
- อยากสร้างเว็บแอปที่เชื่อมต่อ Backend จริง

## 🛠️ Tech Stack

| ส่วน | เทคโนโลยี | เวอร์ชัน |
|------|-----------|---------|
| Frontend | Vue.js + Vite | Vue 3 |
| UI Library | Vuetify | 3.x |
| Backend | Django + Django REST Framework | Django 6.x |
| ฐานข้อมูล | SQLite | - |
| Package Manager | npm (Frontend), uv (Backend) | - |

## 📁 โครงสร้างโปรเจกต์

```
note-app/
├── tutorial/               ← 📚 บทเรียนทั้งหมด (Markdown)
│   ├── tutorial.md         ← สารบัญ + แผนที่การเรียนรู้
│   ├── lesson-1-xxx.md     ← บทเรียนแต่ละบท
│   └── _lesson-template.md ← Template สำหรับสร้างบทเรียนใหม่
├── frontend/               ← 🟢 Vue.js Frontend (สร้างในบทที่ 1)
├── backend/                ← 🐍 Django REST API (พร้อมใช้งาน)
│   ├── core/               ← การตั้งค่า Django
│   ├── notes/              ← App สำหรับจัดการโน้ต
│   │   ├── models.py       ← โครงสร้างข้อมูล Note
│   │   ├── serializers.py  ← แปลงข้อมูล JSON ↔ Python
│   │   ├── views.py        ← API endpoints
│   │   └── urls.py         ← เส้นทาง URL
│   ├── db.sqlite3          ← ฐานข้อมูล
│   └── manage.py           ← คำสั่งจัดการ Django
└── README.md               ← ไฟล์นี้
```

## 📚 สารบัญบทเรียน

| บท | หัวข้อ | สิ่งที่เรียนรู้ |
|----|--------|----------------|
| 1 | สร้างโปรเจกต์ Vue.js ด้วย Vite | Vite, โครงสร้างโปรเจกต์, Component, HMR |
| 2 | Counter App ด้วย Options API | data(), methods, event handling |
| 3 | ทำความเข้าใจ Error ใน Vue.js | อ่าน error, DevTools, debug |
| 4 | Multi-page App ด้วย Vue Router | Routing, หน้า CRUD |
| 5 | ทดสอบ API ด้วย Postman | REST API, HTTP methods |
| 6 | สร้าง Note (Create) | Form, HTTP request, validation |
| 7 | แสดงรายการ Note (Read) | Table, search |
| 8 | แก้ไข Note (Update) | Edit form, route params |
| 9 | ลบ Note (Delete) | Confirm dialog |
| 10 | ตกแต่ง UI ด้วย Vuetify | Material Design, UI components |

👉 เริ่มเรียนที่ [สารบัญบทเรียน](./tutorial/tutorial.md)

## 🚀 เริ่มต้นใช้งาน

### สิ่งที่ต้องติดตั้ง

- [Node.js](https://nodejs.org/) เวอร์ชัน 18+
- [Python](https://www.python.org/) เวอร์ชัน 3.14+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Git](https://git-scm.com/)

### รัน Backend (Django)

```bash
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Backend จะทำงานที่ `http://localhost:8000`

### API Endpoints

| Method | URL | คำอธิบาย |
|--------|-----|----------|
| `GET` | `/api/notes/` | ดึงรายการโน้ตทั้งหมด |
| `GET` | `/api/notes/?search=คำค้นหา` | ค้นหาโน้ตตาม title |
| `POST` | `/api/notes/create/` | สร้างโน้ตใหม่ |
| `GET` | `/api/notes/{id}/` | ดึงข้อมูลโน้ตตาม id |
| `PUT` | `/api/notes/{id}/update/` | แก้ไขโน้ต |
| `DELETE` | `/api/notes/{id}/delete/` | ลบโน้ต |

### ตัวอย่าง Request Body (สร้าง/แก้ไขโน้ต)

```json
{
  "title": "ซื้อของ",
  "body": "ไข่ นม ขนมปัง",
  "is_done": false
}
```

## 📖 วิธีเรียน

1. **อ่านบทเรียน** — เปิดไฟล์ใน `tutorial/` ตามลำดับ
2. **ทำตามขั้นตอน** — พิมพ์โค้ดเอง (อย่า copy-paste!)
3. **ทำ Checkpoint ✅** — ตรวจสอบตัวเองทุกจุด
4. **ลอง Challenge 🏋️** — ทำโจทย์ท้ายบทเพื่อเข้าใจลึกขึ้น
5. **ตามไม่ทัน?** — ใช้ branch สำเร็จ: `git checkout lesson-X-completed`
