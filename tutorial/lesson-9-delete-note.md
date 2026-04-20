# บทที่ 9: ลบ Note — ยืนยันก่อนลบผ่าน API

> 📍 **บทที่ 9 / 10** ━━━━━━━━━━ `[█████████░]`

| ⬅️ [บทที่ 8: แก้ไข Note](./lesson-8-edit-note.md) | [สารบัญ](./tutorial.md) | [บทที่ 10: Vuetify ➡️](./lesson-10-vuetify.md) |
|:---|:---:|---:|

---

## 🎯 เป้าหมาย

ในบทนี้เราจะ:
- ดึงข้อมูล Note มาแสดง **ก่อนลบ** เพื่อให้ผู้ใช้ยืนยัน
- ส่ง **DELETE request** ไป Backend เพื่อลบข้อมูล
- เข้าใจ **HTTP Status 204 No Content** — response ที่ไม่มี body
- จัดการ **loading state**, **error handling** และ **404 Not Found**
- เข้าใจว่าทำไมต้องมี **หน้ายืนยันก่อนลบ** (Confirm before delete)
- ครบ **CRUD** ทั้ง 4 ปฏิบัติการ! 🎉

> 🎮 **Fun Fact:** ในบทที่ 4 หน้าลบ Note แสดงแค่ "Note #1" ซึ่งผู้ใช้ไม่รู้ว่ากำลังจะลบอะไร
> ในบทนี้เราจะดึง**ชื่อ Note จริง**มาแสดง เพื่อให้ผู้ใช้แน่ใจก่อนลบ! 🛡️

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

- ทำบทที่ 8 เสร็จแล้ว (แก้ไข Note ผ่านหน้าเว็บได้)
- มี **2 Terminal** ทำงาน:
  1. Terminal 1: `npm run dev` (Vue.js — port 5173)
  2. Terminal 2: `uv run python manage.py runserver` (Django — port 8000)
- มี Note อย่างน้อย 2-3 รายการในฐานข้อมูล (เพื่อทดสอบลบ)

> 💡 **ถ้ายังไม่ได้ทำบทก่อนหน้า** สามารถเริ่มจาก branch สำเร็จได้:
> ```bash
> git checkout lesson-8-completed
> ```

---

## 🧠 ทำความเข้าใจก่อนเริ่ม

### ทำไมต้องมีหน้ายืนยันก่อนลบ?

ลองจินตนาการ: ถ้ากดปุ่ม "ลบ" แล้ว**ลบทันทีโดยไม่ถาม** จะเกิดอะไร?

```
❌ กดลบผิด → ข้อมูลหายถาวร → ไม่สามารถกู้คืนได้ 😱
```

วิธีที่ดีคือ **ถามยืนยันก่อน:**

```
✅ กดลบ → เห็นชื่อ Note ที่จะลบ → กดยืนยัน → ลบสำเร็จ
                                  → กดยกเลิก → ไม่ลบ (ปลอดภัย!)
```

> 💡 **เปรียบเทียบ:**
>
> | ลบทันที (ไม่ดี) | ยืนยันก่อนลบ (ดี) |
> |----------------|-------------------|
> | กดปุ่ม → ลบเลย! | กดปุ่ม → ถาม "แน่ใจนะ?" → ลบ |
> | เหมือนทิ้งของลงถังขยะทันที | เหมือนถามก่อน "จะทิ้งจริงเหรอ?" |
> | ผิดพลาดง่าย 😰 | ปลอดภัยกว่า 🛡️ |

---

### DELETE Request

ในบทนี้เราจะใช้ HTTP method **DELETE** ซึ่งเป็นตัวสุดท้ายของ CRUD:

> 💡 **CRUD ครบทั้ง 4:**
>
> | ปฏิบัติการ | HTTP Method | URL | บทที่เรียน |
> |-----------|------------|-----|----------|
> | **C**reate (สร้าง) | POST | `/api/notes/create/` | บทที่ 6 |
> | **R**ead (อ่าน) | GET | `/api/notes/` | บทที่ 7 |
> | **U**pdate (แก้ไข) | PUT | `/api/notes/5/update/` | บทที่ 8 |
> | **D**elete (ลบ) | DELETE | `/api/notes/5/delete/` | **บทนี้!** |

---

### HTTP Status 204 No Content

เมื่อลบสำเร็จ Backend จะตอบ Status **204 No Content** — หมายความว่า:

```
"ลบสำเร็จแล้ว ไม่มีข้อมูลส่งกลับ"
```

> 💡 **เปรียบเทียบ Status Code:**
>
> | Status | ความหมาย | ตัวอย่าง |
> |--------|----------|---------|
> | 200 OK | สำเร็จ — มีข้อมูลส่งกลับ | GET, PUT → ได้ JSON กลับ |
> | 201 Created | สร้างสำเร็จ — มีข้อมูลส่งกลับ | POST → ได้ Note ที่สร้าง |
> | **204 No Content** | **สำเร็จ — ไม่มีข้อมูลส่งกลับ** | **DELETE → ลบแล้ว ไม่มีอะไร** |
> | 400 Bad Request | ข้อมูลไม่ถูกต้อง | ส่ง title ว่าง |
> | 404 Not Found | ไม่พบข้อมูล | ขอ Note ID ที่ไม่มี |
>
> **สำคัญ:** เมื่อได้ 204 **ห้ามเรียก `response.json()`** เพราะไม่มี body!
>
> ```js
> // ❌ ผิด — 204 ไม่มี body → error!
> const data = await response.json()
>
> // ✅ ถูก — ตรวจ status แล้ว redirect เลย
> if (response.ok) {
>   this.$router.push('/notes')
> }
> ```

---

## 📝 ขั้นตอน

---

## ส่วนที่ 1: ดึงข้อมูล Note มาแสดงก่อนลบ

### ขั้นตอนที่ 1: ทดสอบ DELETE API ใน Postman ก่อน

ก่อนเขียนโค้ด ลองลบ Note ผ่าน Postman ก่อน:

**สร้าง Note ทิ้ง (เพื่อทดสอบลบ):**

`POST http://localhost:8000/api/notes/create/`

Body (raw JSON):
```json
{
  "title": "สร้างเพื่อทดสอบลบ",
  "body": "จะลบ Note นี้ทิ้ง"
}
```

จดจำ `id` ที่ได้ (สมมติเป็น `10`)

**ลอง DELETE:**

`DELETE http://localhost:8000/api/notes/10/delete/`

ผลลัพธ์:
- Status: `204 No Content`
- Body: ว่าง (ไม่มีข้อมูลส่งกลับ)

**ตรวจสอบว่าลบจริง:**

`GET http://localhost:8000/api/notes/10/`

ผลลัพธ์:
```json
{
  "detail": "Not found."
}
```
Status: `404 Not Found` — ยืนยันว่าลบแล้วจริง!

> 💡 **สังเกต:**
>
> | จุดสังเกต | รายละเอียด |
> |-----------|-----------|
> | Method = **DELETE** | ไม่ต้องส่ง body |
> | Status **204** | สำเร็จ ไม่มี body กลับมา |
> | GET หลังลบ → **404** | ยืนยันว่าลบจากฐานข้อมูลแล้ว |

#### ✅ ตรวจสอบ
- [ ] สร้าง Note ทดสอบใน Postman
- [ ] DELETE Note นั้น → ได้ Status 204
- [ ] GET Note เดิม → ได้ 404 (ลบแล้วจริง)

---

### ขั้นตอนที่ 2: แก้ไข NoteDelete.vue — ดึงข้อมูลมาแสดงก่อนลบ

ในบทที่ 4 หน้าลบแสดงแค่ "Note #1" ซึ่งผู้ใช้ไม่รู้ว่ากำลังจะลบ Note อะไร

เราจะแก้ให้ดึงข้อมูลจาก API มาแสดง **ชื่อ Note จริง** ก่อนลบ

เปิดไฟล์ `src/views/NoteDelete.vue` แล้ว**แก้ไขเป็นโค้ดนี้ทั้งหมด:**

```vue
<script>
export default {
  data() {
    return {
      noteId: null,
      note: null,
      loading: false,
      error: ''
    }
  },

  async created() {
    this.noteId = this.$route.params.id
    await this.fetchNote()
  },

  methods: {
    async fetchNote() {
      this.loading = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/')

        if (response.ok) {
          this.note = await response.json()
        } else {
          this.error = 'ไม่พบ Note #' + this.noteId
        }
      } catch (err) {
        this.error = 'ไม่สามารถเชื่อมต่อ Backend ได้'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>🗑️ ยืนยันการลบ</h1>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลดข้อมูล...</p>

    <!-- Error -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- ข้อมูล Note + ปุ่มยืนยัน -->
    <div v-else-if="note">
      <p>คุณต้องการลบ Note นี้ใช่หรือไม่?</p>

      <table border="1" cellpadding="8" style="border-collapse: collapse; margin: 16px 0;">
        <tr>
          <th>หัวข้อ</th>
          <td>{{ note.title }}</td>
        </tr>
        <tr>
          <th>เนื้อหา</th>
          <td>{{ note.body || '(ไม่มีเนื้อหา)' }}</td>
        </tr>
        <tr>
          <th>สถานะ</th>
          <td>{{ note.is_done ? '✅ เสร็จแล้ว' : '⬜ ยังไม่เสร็จ' }}</td>
        </tr>
      </table>

      <p style="color: red;">⚠️ การลบไม่สามารถกู้คืนได้!</p>

      <button @click="confirmDelete">🗑️ ยืนยันลบ</button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </div>
  </div>
</template>
```

> 💡 **สิ่งที่เปลี่ยนจากบทที่ 4:**
>
> | ก่อน (บทที่ 4) | หลัง (บทที่ 9) |
> |----------------|----------------|
> | แสดง "Note #1" (ไม่รู้ว่าลบอะไร) | แสดง**ชื่อจริง**ของ Note |
> | `created()` — อ่านแค่ ID | `async created()` — ดึงข้อมูลจาก API |
> | ไม่มี loading / error | มี loading + error + 404 handling |
> | ไม่มีรายละเอียด Note | แสดงตารางข้อมูล Note ก่อนลบ |
>
> **อธิบายโค้ด:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `note: null` | เก็บข้อมูล Note ทั้ง object (ไม่แยก field เหมือน NoteEdit) |
> | `this.note = await response.json()` | เก็บข้อมูลทั้งก้อน |
> | `v-else-if="note"` | แสดงเมื่อมีข้อมูล Note (ไม่ใช่ null) |
> | `note.body \|\| '(ไม่มีเนื้อหา)'` | ถ้า body ว่าง แสดง "(ไม่มีเนื้อหา)" แทน |
>
> 🤔 **ทำไมเก็บเป็น `note` object ไม่แยก title, body เหมือน NoteEdit?**
>
> | NoteEdit (บทที่ 8) | NoteDelete (บทที่ 9) |
> |--------------------|---------------------|
> | แยก `title`, `body`, `is_done` | เก็บเป็น `note` ก้อนเดียว |
> | เพราะต้อง **แก้ไข** ทีละ field ด้วย `v-model` | เพราะแค่ **แสดง** ข้อมูล ไม่ต้องแก้ |
> | `v-model="title"` ต้องเป็นตัวแปรใน data | `{{ note.title }}` อ่านค่าอย่างเดียว |

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteDelete.vue` ตามโค้ดด้านบน
- [ ] เปิดหน้ารายการ → กด **🗑️ ลบ** ของ Note ใดก็ได้
- [ ] เห็นชื่อ Note จริง + เนื้อหา + สถานะ ในตาราง
- [ ] เปิด `/notes/99999/delete` → เห็น error "ไม่พบ Note"

---

### ขั้นตอนที่ 3: ทดสอบหน้ายืนยันลบ

**ทดสอบที่ 1 — เปิดหน้าลบ Note ที่มีอยู่:**
1. เปิดหน้า `/notes` → กด **🗑️ ลบ** ของ Note ใดก็ได้
2. เห็นตารางแสดงข้อมูล Note: หัวข้อ, เนื้อหา, สถานะ
3. เห็นข้อความเตือน "⚠️ การลบไม่สามารถกู้คืนได้!"

**ทดสอบที่ 2 — กดยกเลิก:**
1. กดลิงก์ **❌ ยกเลิก**
2. กลับไปหน้ารายการ → Note ยังอยู่ (ไม่ถูกลบ)

**ทดสอบที่ 3 — เปิดหน้าลบ Note ที่ไม่มี:**
1. พิมพ์ URL ตรง: `http://localhost:5173/notes/99999/delete`
2. ควรเห็น: "❌ ไม่พบ Note #99999"

#### ✅ ตรวจสอบ
- [ ] Note ที่มีอยู่ → เห็นข้อมูล Note ครบ
- [ ] กดยกเลิก → กลับหน้ารายการ (Note ไม่ถูกลบ)
- [ ] Note ที่ไม่มี → เห็น error "ไม่พบ Note"

---

## ส่วนที่ 2: ส่ง DELETE Request

### ขั้นตอนที่ 4: เพิ่ม confirmDelete — ส่ง DELETE request

ตอนนี้หน้ายืนยันลบแสดงข้อมูลได้แล้ว แต่กดปุ่ม "🗑️ ยืนยันลบ" ยังไม่ทำอะไร

แก้ไข `src/views/NoteDelete.vue` เป็น**เวอร์ชันสมบูรณ์:**

```vue
<script>
export default {
  data() {
    return {
      noteId: null,
      note: null,
      loading: false,
      deleting: false,
      error: ''
    }
  },

  async created() {
    this.noteId = this.$route.params.id
    await this.fetchNote()
  },

  methods: {
    async fetchNote() {
      this.loading = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/')

        if (response.ok) {
          this.note = await response.json()
        } else {
          this.error = 'ไม่พบ Note #' + this.noteId
        }
      } catch (err) {
        this.error = 'ไม่สามารถเชื่อมต่อ Backend ได้'
      } finally {
        this.loading = false
      }
    },

    async confirmDelete() {
      this.deleting = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/delete/', {
          method: 'DELETE'
        })

        if (response.ok) {
          this.$router.push('/notes')
        } else {
          this.error = 'ไม่สามารถลบ Note ได้'
        }
      } catch (err) {
        alert('ไม่สามารถเชื่อมต่อ Backend ได้ — ตรวจสอบว่า Django server ทำงานอยู่')
      } finally {
        this.deleting = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>🗑️ ยืนยันการลบ</h1>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลดข้อมูล...</p>

    <!-- Error -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- ข้อมูล Note + ปุ่มยืนยัน -->
    <div v-else-if="note">
      <p>คุณต้องการลบ Note นี้ใช่หรือไม่?</p>

      <table border="1" cellpadding="8" style="border-collapse: collapse; margin: 16px 0;">
        <tr>
          <th>หัวข้อ</th>
          <td>{{ note.title }}</td>
        </tr>
        <tr>
          <th>เนื้อหา</th>
          <td>{{ note.body || '(ไม่มีเนื้อหา)' }}</td>
        </tr>
        <tr>
          <th>สถานะ</th>
          <td>{{ note.is_done ? '✅ เสร็จแล้ว' : '⬜ ยังไม่เสร็จ' }}</td>
        </tr>
      </table>

      <p style="color: red;">⚠️ การลบไม่สามารถกู้คืนได้!</p>

      <button @click="confirmDelete" :disabled="deleting" style="background-color: #ff4444; color: white; border: none; padding: 8px 16px; cursor: pointer;">
        {{ deleting ? '⏳ กำลังลบ...' : '🗑️ ยืนยันลบ' }}
      </button>
      &nbsp;
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </div>
  </div>
</template>
```

> 💡 **สิ่งที่เพิ่ม:**
>
> | โค้ดที่เพิ่ม | ทำอะไร |
> |-------------|--------|
> | `deleting: false` | สถานะกำลังลบ (แยกจาก `loading` ที่ใช้ตอนดึงข้อมูล) |
> | `method: 'DELETE'` | ใช้ DELETE method — ไม่ต้องส่ง body ใดๆ |
> | `if (response.ok)` | ตรวจว่าลบสำเร็จ (status 204) |
> | `:disabled="deleting"` | ปิดปุ่มขณะลบ ป้องกันกดซ้ำ |
> | `style="background-color: #ff4444; ..."` | ปุ่มสีแดงเตือนว่าเป็นการลบ |
>
> 🤔 **DELETE request ต่างจาก POST/PUT ยังไง?**
>
> | | POST / PUT | DELETE |
> |---|-----------|--------|
> | ต้องส่ง body? | ✅ ต้องส่ง JSON | ❌ ไม่ต้องส่ง |
> | ต้องส่ง headers? | ✅ Content-Type: application/json | ❌ ไม่ต้อง |
> | Response body? | ✅ ได้ JSON กลับ | ❌ ไม่มี (204 No Content) |
>
> ```js
> // POST — ส่ง body + headers
> fetch(url, {
>   method: 'POST',
>   headers: { 'Content-Type': 'application/json' },
>   body: JSON.stringify({ title: '...' })
> })
>
> // DELETE — แค่ระบุ method
> fetch(url, {
>   method: 'DELETE'
> })
> ```
>
> DELETE เรียบง่ายที่สุด! แค่บอก Backend ว่า "ลบ Note นี้" — ไม่ต้องส่งข้อมูลอะไร

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteDelete.vue` เพิ่ม `confirmDelete` + `deleting`
- [ ] กดปุ่ม "🗑️ ยืนยันลบ" → Note ถูกลบ + redirect ไปหน้ารายการ
- [ ] Note ที่ลบหายไปจากรายการจริง

---

### ขั้นตอนที่ 5: ทดสอบการลบ Note

> ⚠️ **ก่อนทดสอบ:** สร้าง Note ใหม่ 2-3 รายการเพื่อใช้ทดสอบลบ (เราจะลบทิ้ง!)

**ทดสอบที่ 1 — ลบ Note สำเร็จ:**
1. เปิดหน้า `/notes` → จดจำจำนวน Note
2. กด **🗑️ ลบ** ของ Note ใดก็ได้
3. เห็นข้อมูล Note → ตรวจว่าใช่ Note ที่ต้องการลบ
4. กดปุ่ม **🗑️ ยืนยันลบ**
5. redirect ไปหน้ารายการ → Note หายไป → จำนวน Note ลดลง 1!

**ทดสอบที่ 2 — กดยกเลิก:**
1. กด **🗑️ ลบ** ของ Note อีกรายการ
2. เห็นข้อมูล Note
3. กดลิงก์ **❌ ยกเลิก**
4. กลับมาหน้ารายการ → Note **ยังอยู่** (ไม่ถูกลบ) ✅

**ทดสอบที่ 3 — ปิด Backend:**
1. ปิด Django server (กด `Ctrl+C` ใน Terminal 2)
2. กด **🗑️ ลบ** ของ Note ใดก็ได้
3. ควรเห็น error: "❌ ไม่สามารถเชื่อมต่อ Backend ได้"
4. **เปิด Django server กลับ!** `uv run python manage.py runserver`

**ทดสอบที่ 4 — เปิด DevTools ดู request:**
1. เปิด DevTools (F12) → แท็บ Network
2. กด **🗑️ ลบ** ของ Note → เห็น **GET** (ดึงข้อมูล)
3. กด **🗑️ ยืนยันลบ** → เห็น **DELETE** request
   - Method: `DELETE`
   - Status: `204`

#### ✅ ตรวจสอบ
- [ ] ลบ Note → redirect → Note หายจากรายการ
- [ ] กดยกเลิก → Note ยังอยู่
- [ ] Backend ปิด → เห็น error
- [ ] DevTools: เห็น GET + DELETE request

---

## ส่วนที่ 3: ทบทวน CRUD ทั้งหมด

### ขั้นตอนที่ 6: ทดสอบ CRUD ครบวงจร

ตอนนี้เราครบ CRUD ทั้ง 4 แล้ว! มาทดสอบทั้งหมดต่อเนื่องกัน:

**ทดสอบ CRUD ครบวงจร:**

1. **Create** — สร้าง Note ใหม่:
   - กด **➕ สร้าง Note ใหม่** → กรอกข้อมูล → กดบันทึก
   - ✅ เห็น Note ใหม่ในรายการ

2. **Read** — ดูรายการ + ค้นหา:
   - ดูรายการ Note ทั้งหมด
   - ลองค้นหาชื่อ Note ที่เพิ่งสร้าง
   - ✅ เห็น Note ที่ค้นหา

3. **Update** — แก้ไข Note ที่เพิ่งสร้าง:
   - กด **✏️ แก้ไข** → แก้ไขหัวข้อ → ติ๊กเสร็จแล้ว → กดบันทึก
   - ✅ เห็นข้อมูลที่แก้ไข + สถานะ ✅

4. **Delete** — ลบ Note:
   - กด **🗑️ ลบ** → ตรวจข้อมูล → กดยืนยันลบ
   - ✅ Note หายจากรายการ

> 🎉 **ยินดีด้วย! คุณสร้าง CRUD App ครบสมบูรณ์แล้ว!**
>
> ```
> ✅ Create — สร้าง Note ผ่านหน้าเว็บ → บันทึกใน Backend
> ✅ Read   — ดึงรายการ + ค้นหา → แสดงในตาราง
> ✅ Update — ดึงข้อมูลเดิม → แก้ไข → อัปเดตใน Backend
> ✅ Delete — แสดงข้อมูลก่อนลบ → ยืนยัน → ลบจาก Backend
> ```

#### ✅ ตรวจสอบ
- [ ] ทำ CRUD ครบ 4 ปฏิบัติการต่อเนื่องกัน
- [ ] ทุกอย่างทำงานถูกต้อง
- [ ] เข้าใจ flow ของแต่ละปฏิบัติการ

---

### ขั้นตอนที่ 7: สรุปโครงสร้างไฟล์และ API

มาดูภาพรวมทั้งหมดที่สร้างมาตั้งแต่บทที่ 4-9:

**ไฟล์ Vue.js:**

```
src/
├── views/
│   ├── NoteList.vue     ← 📋 รายการ (GET /api/notes/)
│   ├── NoteCreate.vue   ← ➕ สร้าง (POST /api/notes/create/)
│   ├── NoteEdit.vue     ← ✏️ แก้ไข (GET + PUT /api/notes/:id/)
│   └── NoteDelete.vue   ← 🗑️ ลบ (GET + DELETE /api/notes/:id/)
├── router/
│   └── index.js         ← เส้นทาง URL ทั้งหมด
├── App.vue              ← Layout หลัก + Navbar
└── main.js              ← จุดเริ่มต้น + ติดตั้ง Router
```

**API Endpoints:**

> 💡 **สรุป API ที่ใช้ทั้งหมด:**
>
> | Method | URL | ใช้ใน | ทำอะไร |
> |--------|-----|-------|--------|
> | GET | `/api/notes/` | NoteList | ดึงรายการ Note ทั้งหมด |
> | GET | `/api/notes/?search=คำค้นหา` | NoteList | ค้นหา Note |
> | POST | `/api/notes/create/` | NoteCreate | สร้าง Note ใหม่ |
> | GET | `/api/notes/:id/` | NoteEdit, NoteDelete | ดึงข้อมูล Note 1 รายการ |
> | PUT | `/api/notes/:id/update/` | NoteEdit | อัปเดต Note |
> | DELETE | `/api/notes/:id/delete/` | NoteDelete | ลบ Note |

#### ✅ ตรวจสอบ
- [ ] เข้าใจโครงสร้างไฟล์ทั้งหมดใน Vue.js
- [ ] เข้าใจว่าแต่ละ component ใช้ API ตัวไหน

---

## สรุปโค้ดทั้งหมดในบทนี้

ไฟล์เดียวที่แก้ไขในบทนี้:

**`src/views/NoteDelete.vue`** (เวอร์ชันสมบูรณ์):

```vue
<script>
export default {
  data() {
    return {
      noteId: null,
      note: null,
      loading: false,
      deleting: false,
      error: ''
    }
  },

  async created() {
    this.noteId = this.$route.params.id
    await this.fetchNote()
  },

  methods: {
    async fetchNote() {
      this.loading = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/')

        if (response.ok) {
          this.note = await response.json()
        } else {
          this.error = 'ไม่พบ Note #' + this.noteId
        }
      } catch (err) {
        this.error = 'ไม่สามารถเชื่อมต่อ Backend ได้'
      } finally {
        this.loading = false
      }
    },

    async confirmDelete() {
      this.deleting = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/delete/', {
          method: 'DELETE'
        })

        if (response.ok) {
          this.$router.push('/notes')
        } else {
          this.error = 'ไม่สามารถลบ Note ได้'
        }
      } catch (err) {
        alert('ไม่สามารถเชื่อมต่อ Backend ได้ — ตรวจสอบว่า Django server ทำงานอยู่')
      } finally {
        this.deleting = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>🗑️ ยืนยันการลบ</h1>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลดข้อมูล...</p>

    <!-- Error -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- ข้อมูล Note + ปุ่มยืนยัน -->
    <div v-else-if="note">
      <p>คุณต้องการลบ Note นี้ใช่หรือไม่?</p>

      <table border="1" cellpadding="8" style="border-collapse: collapse; margin: 16px 0;">
        <tr>
          <th>หัวข้อ</th>
          <td>{{ note.title }}</td>
        </tr>
        <tr>
          <th>เนื้อหา</th>
          <td>{{ note.body || '(ไม่มีเนื้อหา)' }}</td>
        </tr>
        <tr>
          <th>สถานะ</th>
          <td>{{ note.is_done ? '✅ เสร็จแล้ว' : '⬜ ยังไม่เสร็จ' }}</td>
        </tr>
      </table>

      <p style="color: red;">⚠️ การลบไม่สามารถกู้คืนได้!</p>

      <button @click="confirmDelete" :disabled="deleting" style="background-color: #ff4444; color: white; border: none; padding: 8px 16px; cursor: pointer;">
        {{ deleting ? '⏳ กำลังลบ...' : '🗑️ ยืนยันลบ' }}
      </button>
      &nbsp;
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </div>
  </div>
</template>
```

---

## ❌ ปัญหาที่พบบ่อย

### ปัญหา: กดยืนยันลบแล้วได้ error `SyntaxError: Unexpected end of JSON input`

**สาเหตุ:** เรียก `response.json()` หลัง DELETE — แต่ 204 No Content ไม่มี body!

**วิธีแก้:**
```js
// ❌ ผิด — 204 ไม่มี body → json() error!
const data = await response.json()

// ✅ ถูก — ตรวจ response.ok แล้ว redirect เลย
if (response.ok) {
  this.$router.push('/notes')
}
```

---

### ปัญหา: กดยืนยันลบแล้วได้ `405 Method Not Allowed`

**สาเหตุ:** URL ผิดหรือ method ผิด

**วิธีแก้:**
```js
// ❌ ผิด — URL ไม่มี /delete/
fetch('http://localhost:8000/api/notes/1/', { method: 'DELETE' })

// ✅ ถูก — URL มี /delete/
fetch('http://localhost:8000/api/notes/1/delete/', { method: 'DELETE' })
```

---

### ปัญหา: ลบสำเร็จแต่กลับมาหน้ารายการ Note ยังอยู่

**สาเหตุ:** อาจเป็น browser cache หรือ `NoteList.vue` ไม่ได้ดึงข้อมูลใหม่

**วิธีแก้:**
1. เปิด DevTools → ติ๊ก **Disable cache**
2. ตรวจว่า `NoteList.vue` มี `mounted()` ที่เรียก `fetchNotes()` — ทุกครั้งที่เปิดหน้าจะดึงข้อมูลใหม่

> 💡 ปกติถ้า `mounted()` ทำงานทุกครั้งที่เข้าหน้า Note จะลบหายทันที
> ถ้าไม่หาย ให้ลอง **Refresh** หน้า (F5)

---

### ปัญหา: เปิดหน้าลบแล้วฟอร์มว่าง ไม่มีข้อมูล Note

**สาเหตุ:** อาจลืมเรียก `fetchNote()` ใน `created()`

**วิธีแก้:**
```js
// ❌ ผิด — ไม่ได้ดึงข้อมูล
created() {
  this.noteId = this.$route.params.id
}

// ✅ ถูก — ดึงข้อมูลจาก API
async created() {
  this.noteId = this.$route.params.id
  await this.fetchNote()
}
```

---

## 🏋️ ลองทำเอง (Challenge)

### ⭐ ระดับง่าย
เพิ่ม **ลิงก์ "✏️ แก้ไขแทน"** ในหน้ายืนยันลบ — ถ้าผู้ใช้เข้ามาหน้าลบแต่อยากแก้ไขแทน:
- เพิ่ม `<router-link :to="'/notes/' + noteId + '/edit'">✏️ แก้ไขแทน</router-link>` ก่อนปุ่มยกเลิก
- ให้ผู้ใช้มีตัวเลือกมากขึ้น

### ⭐⭐ ระดับปานกลาง
เพิ่ม **ลบจากหน้ารายการโดยตรง** (Quick Delete) — โดยไม่ต้องไปหน้ายืนยัน:
- เพิ่มปุ่ม "🗑️ ลบเลย" ใน `NoteList.vue` ถัดจากลิงก์ "🗑️ ลบ" เดิม
- กดแล้วใช้ `confirm('ต้องการลบ Note "..." หรือไม่?')` ถามก่อน
- ถ้าตอบ OK → ส่ง DELETE request → เรียก `fetchNotes()` ดึงข้อมูลใหม่

### ⭐⭐⭐ ระดับยาก
ทำ **Soft Delete** — ลบแล้วแสดง **"กู้คืน" (Undo)** ชั่วคราว:
- หลังลบสำเร็จ ไม่ redirect ทันที แต่แสดงข้อความ "ลบ Note สำเร็จ" พร้อมปุ่ม "↩️ กู้คืน"
- ใช้ `setTimeout` 5 วินาที ถ้าไม่กดกู้คืน → redirect ไปหน้ารายการ
- ถ้ากดกู้คืน → สร้าง Note ใหม่ด้วย POST (ใช้ข้อมูลที่เก็บไว้ใน `this.note`)

<details>
<summary>💡 คำใบ้ระดับง่าย</summary>

เพิ่มใน template ก่อน `<router-link to="/notes">`:
```html
<router-link :to="'/notes/' + noteId + '/edit'">✏️ แก้ไขแทน</router-link>
&nbsp;
```

`:to` ต้องใช้ dynamic binding (มี `:`) เพราะมีตัวแปร `noteId`

</details>

<details>
<summary>💡 คำใบ้ระดับปานกลาง</summary>

เพิ่ม method ใน `NoteList.vue`:

```js
async quickDelete(note) {
  const confirmed = confirm('ต้องการลบ Note "' + note.title + '" หรือไม่?')

  if (!confirmed) return

  try {
    const response = await fetch('http://localhost:8000/api/notes/' + note.id + '/delete/', {
      method: 'DELETE'
    })

    if (response.ok) {
      await this.fetchNotes()   // ดึงข้อมูลใหม่
    }
  } catch (err) {
    alert('ไม่สามารถลบ Note ได้')
  }
}
```

ใน template เพิ่มปุ่ม:
```html
<button @click="quickDelete(note)" style="color: red; cursor: pointer;">🗑️ ลบเลย</button>
```

**ข้อดี:** ลบได้เร็ว — ไม่ต้องเปลี่ยนหน้า
**ข้อเสีย:** เห็นข้อมูลน้อยกว่าหน้ายืนยัน

</details>

<details>
<summary>💡 คำใบ้ระดับยาก</summary>

เพิ่มตัวแปรใน `data()`:

```js
deleted: false,
undoTimeout: null
```

แก้ `confirmDelete()`:

```js
async confirmDelete() {
  this.deleting = true

  try {
    const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/delete/', {
      method: 'DELETE'
    })

    if (response.ok) {
      this.deleted = true

      // ตั้ง timer 5 วินาที → redirect
      this.undoTimeout = setTimeout(() => {
        this.$router.push('/notes')
      }, 5000)
    }
  } catch (err) {
    alert('ไม่สามารถลบ Note ได้')
  } finally {
    this.deleting = false
  }
}
```

เพิ่ม method กู้คืน:

```js
async undoDelete() {
  clearTimeout(this.undoTimeout)

  try {
    const response = await fetch('http://localhost:8000/api/notes/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: this.note.title,
        body: this.note.body,
        is_done: this.note.is_done
      })
    })

    if (response.ok) {
      this.$router.push('/notes')
    }
  } catch (err) {
    alert('ไม่สามารถกู้คืน Note ได้')
  }
}
```

เพิ่มใน template:

```html
<div v-if="deleted" style="background: #e8f5e9; padding: 16px; border-radius: 8px; margin-top: 16px;">
  <p>✅ ลบ Note "{{ note.title }}" สำเร็จ!</p>
  <p>จะกลับไปหน้ารายการใน 5 วินาที...</p>
  <button @click="undoDelete">↩️ กู้คืน</button>
</div>
```

**หมายเหตุ:** นี่เป็น "Soft Undo" ที่สร้าง Note ใหม่ (ID จะเปลี่ยน) ไม่ใช่การกู้คืนจริง
การทำ Soft Delete จริงๆ ต้องเพิ่ม field `is_deleted` ที่ Backend

</details>

---

## 📖 คำศัพท์ที่เรียนรู้ในบทนี้

| คำศัพท์ | ความหมาย | เปรียบเทียบ |
|---------|----------|-------------|
| DELETE | HTTP method สำหรับลบข้อมูล | เหมือนโยนเอกสารทิ้งถังขยะ |
| 204 No Content | Status ที่บอกว่าสำเร็จ แต่ไม่มีข้อมูลส่งกลับ | เหมือนคนส่งของบอก "ส่งแล้ว" โดยไม่ให้ใบเสร็จ |
| Confirm Dialog | การถามยืนยันก่อนทำ action ที่ไม่สามารถย้อนกลับ | เหมือนป้าย "แน่ใจนะ? จะทิ้งจริงเหรอ?" |
| CRUD | Create, Read, Update, Delete — 4 ปฏิบัติการพื้นฐานกับข้อมูล | เหมือนสมุดที่: เขียน, อ่าน, แก้, ลบ |
| Destructive Action | การกระทำที่ไม่สามารถย้อนกลับได้ (เช่น ลบข้อมูล) | เหมือนฉีกกระดาษทิ้ง — เอากลับยาก |

---

## สรุปสิ่งที่ได้เรียนรู้ ✅

| หัวข้อ | สิ่งที่เรียนรู้ |
|--------|----------------|
| Confirm Before Delete | แสดงข้อมูล Note ก่อนลบ เพื่อให้ผู้ใช้ตรวจสอบ |
| DELETE Request | ส่ง DELETE request ไป Backend — ไม่ต้องส่ง body, ไม่ต้องส่ง headers |
| 204 No Content | Status ที่บอกว่าลบสำเร็จ — **ห้ามเรียก response.json()** |
| loading vs deleting | แยกสถานะ "กำลังโหลดข้อมูล" กับ "กำลังลบ" |
| CRUD ครบ! | Create (POST) → Read (GET) → Update (PUT) → Delete (DELETE) |
| UX Best Practice | ใช้ปุ่มสีแดงสำหรับ destructive action + แสดง warning ก่อนลบ |
| Object vs Fields | เก็บข้อมูลเป็น object ก้อนเดียว (แสดงอย่างเดียว) vs แยก fields (ต้องแก้ไข) |

---

> ➡️ **บทถัดไป:** [บทที่ 10: ใช้ Vuetify ตกแต่ง UI](./lesson-10-vuetify.md)
