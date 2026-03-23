# นำเข้า serializers จาก Django REST Framework
# Serializer ทำหน้าที่ 2 อย่าง:
# 1. แปลงข้อมูลจาก Model (Python object) → JSON เพื่อส่งกลับให้ Frontend
# 2. ตรวจสอบ (validate) ข้อมูลที่ Frontend ส่งมาว่าถูกต้องหรือไม่
from rest_framework import serializers


class NoteSerializer(serializers.Serializer):
    # id - ใช้ read_only=True เพราะ id ถูกสร้างอัตโนมัติโดยฐานข้อมูล ไม่ต้องส่งมาจาก Frontend
    id = serializers.IntegerField(read_only=True)

    # title - ข้อความสั้น กำหนดความยาวสูงสุด 200 ตัวอักษร (ต้องกรอก ห้ามว่าง)
    title = serializers.CharField(max_length=200)

    # body - ข้อความยาว
    # allow_blank=True หมายถึง อนุญาตให้ส่งค่าว่าง "" ได้
    # default="" หมายถึง ถ้าไม่ได้ส่งค่ามา จะใช้ค่าว่างเป็นค่าเริ่มต้น
    body = serializers.CharField(allow_blank=True, default="")

    # is_done - ค่า True/False บอกว่าโน้ตนี้ทำเสร็จแล้วหรือยัง
    # default=False หมายถึง ถ้าไม่ได้ส่งค่ามา จะตั้งเป็น False (ยังไม่เสร็จ)
    is_done = serializers.BooleanField(default=False)

    # created_at, updated_at - ใช้ read_only=True เพราะถูกสร้างอัตโนมัติโดย Django
    # Frontend ไม่สามารถแก้ไขค่าเหล่านี้ได้ แต่จะได้รับค่ากลับมาเมื่อดูข้อมูล
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
