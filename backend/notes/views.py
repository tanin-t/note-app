# นำเข้า decorator สำหรับสร้าง API view แบบ function
# @api_view ทำให้ function ธรรมดากลายเป็น API endpoint ที่รับ HTTP request ได้
from rest_framework.decorators import api_view

# Response ใช้สำหรับส่งข้อมูลกลับไปให้ Frontend ในรูปแบบ JSON
from rest_framework.response import Response

# status มีค่าคงที่ของ HTTP status code เช่น 200, 201, 400, 404
from rest_framework import status

from .models import Note
from .serializers import NoteSerializer


# ==========================================
# ดึงรายการโน้ตทั้งหมด + ค้นหาตาม title
# GET /api/notes/
# GET /api/notes/?search=คำค้นหา
# ==========================================
@api_view(["GET"])
def note_list(request):
    # ดึงโน้ตทั้งหมดจากฐานข้อมูล
    notes = Note.objects.all()

    # รับค่า query parameter "search" จาก URL เช่น ?search=hello
    # ถ้าไม่มีจะได้ค่าว่าง ""
    search = request.query_params.get("search", "")
    if search:
        # กรองเฉพาะโน้ตที่ title มีคำค้นหาอยู่ (ไม่สนตัวพิมพ์ใหญ่-เล็ก)
        # icontains = case-Insensitive contains
        notes = notes.filter(title__icontains=search)

    # แปลง queryset เป็น JSON ด้วย Serializer
    # many=True บอกว่าเรากำลังแปลงข้อมูลหลายรายการ (list)
    serializer = NoteSerializer(notes, many=True)

    # ส่งข้อมูล JSON กลับไป (status 200 OK เป็นค่าเริ่มต้น)
    return Response(serializer.data)


# ==========================================
# สร้างโน้ตใหม่
# POST /api/notes/create/
# ตัวอย่าง body: {"title": "ซื้อของ", "body": "ไข่ นม ขนมปัง"}
# ==========================================
@api_view(["POST"])
def note_create(request):
    # ส่งข้อมูลจาก request body เข้า Serializer เพื่อตรวจสอบ (validate)
    serializer = NoteSerializer(data=request.data)

    # เช็คว่าข้อมูลถูกต้องตามกฎที่กำหนดใน Serializer หรือไม่
    if serializer.is_valid():
        # ถ้าข้อมูลถูกต้อง สร้างโน้ตใหม่ในฐานข้อมูล
        note = Note.objects.create(
            title=serializer.validated_data["title"],
            body=serializer.validated_data["body"],
            is_done=serializer.validated_data["is_done"],
        )

        # ส่งข้อมูลโน้ตที่สร้างแล้วกลับไป พร้อม status 201 (Created)
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

    # ถ้าข้อมูลไม่ถูกต้อง ส่ง error กลับไป พร้อม status 400 (Bad Request)
    # เช่น {"title": ["This field is required."]}
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# ดึงข้อมูลโน้ตตาม id
# GET /api/notes/1/
# ==========================================
@api_view(["GET"])
def note_detail(request, pk):
    # pk (primary key) คือ id ของโน้ตที่ต้องการดู ได้มาจาก URL เช่น /api/notes/1/
    try:
        # ค้นหาโน้ตจาก id ในฐานข้อมูล
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        # ถ้าไม่พบโน้ต ส่ง error 404 (Not Found) กลับไป
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # แปลงโน้ตเป็น JSON แล้วส่งกลับ
    serializer = NoteSerializer(note)
    return Response(serializer.data)


# ==========================================
# แก้ไขโน้ต
# PUT /api/notes/1/update/
# ตัวอย่าง body: {"title": "ซื้อของ (แก้ไข)", "body": "ไข่ นม ขนมปัง เนย"}
# ==========================================
@api_view(["PUT"])
def note_update(request, pk):
    # หาโน้ตที่ต้องการแก้ไขจาก id
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # ตรวจสอบข้อมูลใหม่ที่ส่งมา
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        # อัปเดตค่าแต่ละ field ของโน้ตด้วยข้อมูลใหม่
        note.title = serializer.validated_data["title"]
        note.body = serializer.validated_data["body"]
        note.is_done = serializer.validated_data["is_done"]

        # บันทึกการเปลี่ยนแปลงลงฐานข้อมูล
        note.save()

        # ส่งข้อมูลโน้ตที่แก้ไขแล้วกลับไป
        return Response(NoteSerializer(note).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# ลบโน้ต
# DELETE /api/notes/1/delete/
# ==========================================
@api_view(["DELETE"])
def note_delete(request, pk):
    # หาโน้ตที่ต้องการลบจาก id
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # ลบโน้ตออกจากฐานข้อมูล
    note.delete()

    # ส่ง status 204 (No Content) กลับไป หมายถึง ลบสำเร็จ ไม่มีข้อมูลส่งกลับ
    return Response(status=status.HTTP_204_NO_CONTENT)
