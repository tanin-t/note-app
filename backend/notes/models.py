# นำเข้า models จาก Django เพื่อใช้สร้างตารางในฐานข้อมูล
from django.db import models


# สร้าง Model ชื่อ Note สำหรับเก็บข้อมูลโน้ต
# Model คือตัวแทนของตารางในฐานข้อมูล แต่ละ field คือคอลัมน์ในตาราง
class Note(models.Model):
    # ชื่อโน้ต - ใช้ CharField สำหรับข้อความสั้นๆ กำหนดความยาวสูงสุด 200 ตัวอักษร
    title = models.CharField(max_length=200)

    # เนื้อหาโน้ต - ใช้ TextField สำหรับข้อความยาวๆ ไม่จำกัดความยาว
    # blank=True หมายถึง อนุญาตให้ส่งค่าว่างได้
    # default="" หมายถึง ถ้าไม่ได้ส่งค่ามา จะใช้ค่าว่างเป็นค่าเริ่มต้น
    body = models.TextField(blank=True, default="")

    # สถานะว่าทำเสร็จแล้วหรือยัง - ใช้ BooleanField เก็บค่า True/False
    # default=False หมายถึง เมื่อสร้างใหม่จะยังไม่เสร็จ
    is_done = models.BooleanField(default=False)

    # วันที่สร้าง - auto_now_add=True จะบันทึกเวลาอัตโนมัติตอนสร้างครั้งแรก
    created_at = models.DateTimeField(auto_now_add=True)

    # วันที่แก้ไขล่าสุด - auto_now=True จะอัปเดตเวลาอัตโนมัติทุกครั้งที่บันทึก
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # เรียงลำดับโน้ตจากอัปเดตล่าสุดไปเก่าสุด (เครื่องหมาย - หมายถึงเรียงจากมากไปน้อย)
        ordering = ["-updated_at"]

    # __str__ คือ method ที่ Python เรียกเมื่อต้องการแสดงผล object เป็นข้อความ
    # เช่น เมื่อดูใน Admin จะแสดงชื่อ title แทนที่จะแสดง "Note object (1)"
    def __str__(self):
        return self.title
