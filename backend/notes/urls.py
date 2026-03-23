# กำหนดเส้นทาง URL สำหรับ API ของโน้ต
# ไฟล์นี้เชื่อม URL กับ view function ว่า URL ไหนจะเรียก function ไหน
from django.urls import path

from . import views

# urlpatterns คือ list ของเส้นทาง URL ทั้งหมดใน app นี้
# path() รับ 3 ค่า:
#   1. URL pattern - เส้นทาง URL
#   2. view function - function ที่จะถูกเรียกเมื่อมี request เข้ามาที่ URL นี้
#   3. name - ชื่อของ URL ใช้อ้างอิงภายใน Django
urlpatterns = [
    # GET /api/notes/           → ดึงรายการโน้ตทั้งหมด (รองรับ ?search=คำค้นหา)
    path("notes/", views.note_list, name="note-list"),

    # POST /api/notes/create/   → สร้างโน้ตใหม่
    path("notes/create/", views.note_create, name="note-create"),

    # GET /api/notes/1/         → ดึงข้อมูลโน้ต id=1
    # <int:pk> หมายถึง รับตัวเลขจาก URL แล้วส่งเป็น parameter ชื่อ pk ให้ view function
    path("notes/<int:pk>/", views.note_detail, name="note-detail"),

    # PUT /api/notes/1/update/  → แก้ไขโน้ต id=1
    path("notes/<int:pk>/update/", views.note_update, name="note-update"),

    # DELETE /api/notes/1/delete/ → ลบโน้ต id=1
    path("notes/<int:pk>/delete/", views.note_delete, name="note-delete"),
]
