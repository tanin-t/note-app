# บทที่ 8: แก้ไข Note — อัปเดตข้อมูลผ่าน API

> 📍 **บทที่ 8 / 10** ━━━━━━━━━━ `[████████░░]`

| ⬅️ [บทที่ 7: แสดงรายการ Note](./lesson-7-list-note.md) | [สารบัญ](./tutorial.md) | [บทที่ 9: ลบ Note ➡️](./lesson-9-delete-note.md) |
|:---|:---:|---:|

---

## 🎯 เป้าหมาย

ในบทนี้เราจะ:
- ดึงข้อมูล Note เดิมจาก **API** มาแสดงในฟอร์ม (Pre-fill form)
- เรียนรู้ **`created()` Lifecycle Hook** สำหรับดึงข้อมูลก่อน render
- ส่ง **PUT request** ไป Backend เพื่ออัปเดตข้อมูล
- เพิ่ม **checkbox `is_done`** ให้เปลี่ยนสถานะได้
- จัดการ **loading state**, **error handling** และ **404 Not Found**
- เข้าใจความแตกต่างระหว่าง **POST** (สร้าง) กับ **PUT** (แก้ไข)

> 🎮 **Fun Fact:** ในบทที่ 4 หน้าแก้ไข Note ใช้**ข้อมูลจำลอง** — `title = 'ตัวอย่างหัวข้อ Note #1'`
> ในบทนี้เราจะดึงข้อมูล **จริง** จาก Backend มาแสดงในฟอร์ม แล้วส่งกลับไปอัปเดตได้! 🎉

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

- ทำบทที่ 7 เสร็จแล้ว (หน้ารายการ Note ดึงข้อมูลจาก API ได้)
- มี **2 Terminal** ทำงาน:
  1. Terminal 1: `npm run dev` (Vue.js — port 5173)
  2. Terminal 2: `uv run python manage.py runserver` (Django — port 8000)
- มี Note อย่างน้อย 1-2 รายการในฐานข้อมูล

> 💡 **ถ้ายังไม่ได้ทำบทก่อนหน้า** สามารถเริ่มจาก branch สำเร็จได้:
> ```bash
> git checkout lesson-7-completed
> ```

---

## 🧠 ทำความเข้าใจก่อนเริ่ม

### POST vs PUT — สร้างใหม่ vs แก้ไขของเดิม

ในบทที่ 6 เราส่ง **POST** ไป Backend เพื่อ **สร้าง** Note ใหม่
ในบทนี้เราจะส่ง **PUT** เพื่อ **แก้ไข** Note ที่มีอยู่แล้ว

> 💡 **เปรียบเทียบ POST กับ PUT:**
>
> | | POST (สร้าง) | PUT (แก้ไข) |
> |---|------------|-----------|
> | ใช้เมื่อ | สร้างข้อมูลใหม่ | อัปเดตข้อมูลที่มีอยู่ |
> | ต้องรู้ ID ไหม? | ❌ ไม่ต้อง (Backend สร้างให้) | ✅ ต้องรู้ (ระบุใน URL) |
> | URL | `/api/notes/create/` | `/api/notes/5/update/` |
> | เปรียบเทียบ | เขียนหน้าใหม่ในสมุด ✏️ | ลบแล้วเขียนทับหน้าเดิม 📝 |

---

### ขั้นตอนการแก้ไข Note

การแก้ไข Note ต้องทำ **2 ขั้นตอน:**

```
ขั้นตอนที่ 1: ดึงข้อมูลเดิม (GET)
   เปิดหน้าแก้ไข → ดึง Note จาก API → แสดงในฟอร์ม

ขั้นตอนที่ 2: ส่งข้อมูลใหม่ (PUT)
   ผู้ใช้แก้ไขข้อมูล → กดบันทึก → ส่งไป Backend → อัปเดตในฐานข้อมูล
```

> 💡 **เปรียบเทียบกับการสร้าง Note:**
>
> | สร้าง Note (บทที่ 6) | แก้ไข Note (บทที่ 8) |
> |---------------------|---------------------|
> | เปิดฟอร์มว่าง | เปิดฟอร์มที่มีข้อมูลเดิม |
> | ใช้ 1 API (POST create) | ใช้ 2 API (GET detail + PUT update) |
> | เหมือนกรอกใบสมัครใหม่ | เหมือนแก้ไขใบสมัครที่กรอกไว้แล้ว |

---

## 📝 ขั้นตอน

---

## ส่วนที่ 1: ดึงข้อมูล Note เดิมมาแสดง

### ขั้นตอนที่ 1: ดู API ดึงข้อมูล Note ตาม ID

ก่อนเขียนโค้ด มาดูก่อนว่า API ส่งอะไรกลับมา:

เปิด **Postman** แล้ว `GET http://localhost:8000/api/notes/1/`

> ⚠️ เปลี่ยน `1` เป็น ID ของ Note ที่มีอยู่จริงในฐานข้อมูล

ตัวอย่างผลลัพธ์:
```json
{
  "id": 1,
  "title": "ซื้อของ",
  "body": "ไข่ นม ขนมปัง",
  "is_done": false,
  "created_at": "2025-01-15T09:00:00Z",
  "updated_at": "2025-01-15T09:00:00Z"
}
```

> 💡 **สังเกต:**
>
> | จุดสังเกต | รายละเอียด |
> |-----------|-----------|
> | ผลลัพธ์เป็น **Object** `{...}` | เพราะเป็นข้อมูล 1 รายการ (ไม่ใช่ Array) |
> | มี `id`, `title`, `body`, `is_done` | ข้อมูลครบทุก field ที่ต้องแสดงในฟอร์ม |
> | URL มี ID: `/notes/1/` | ระบุว่าจะดู Note ตัวไหน |

**ทดสอบเพิ่ม — ลอง GET ID ที่ไม่มี:**

```
GET http://localhost:8000/api/notes/99999/
```

ผลลัพธ์:
```json
{
  "detail": "Not found."
}
```
Status: `404 Not Found`

> 💡 Backend ตอบ **404** เมื่อไม่พบ Note — เราจะจัดการกรณีนี้ด้วย!

#### ✅ ตรวจสอบ
- [ ] GET `/api/notes/1/` ใน Postman → ได้ข้อมูล Note 1 รายการ
- [ ] GET `/api/notes/99999/` → ได้ 404 Not Found
- [ ] เข้าใจโครงสร้าง JSON ของ Note รายการเดียว

---

### ขั้นตอนที่ 2: ดู API อัปเดต Note

ต่อไปดู API สำหรับอัปเดต:

เปิด **Postman** แล้ว `PUT http://localhost:8000/api/notes/1/update/`

Body (raw JSON):
```json
{
  "title": "ซื้อของ (แก้ไขจาก Postman)",
  "body": "ไข่ นม ขนมปัง เนย",
  "is_done": true
}
```

ตัวอย่างผลลัพธ์:
```json
{
  "id": 1,
  "title": "ซื้อของ (แก้ไขจาก Postman)",
  "body": "ไข่ นม ขนมปัง เนย",
  "is_done": true,
  "created_at": "2025-01-15T09:00:00Z",
  "updated_at": "2025-01-15T14:30:00Z"
}
```

> 💡 **สังเกต:**
>
> | จุดสังเกต | รายละเอียด |
> |-----------|-----------|
> | Method = **PUT** | ไม่ใช่ POST (PUT = แก้ไข) |
> | URL = `/notes/1/update/` | ต้องระบุ ID ของ Note ที่จะแก้ |
> | ต้องส่ง **ทุก field** | title, body, is_done — ถ้าไม่ส่ง field ไหน จะ error |
> | `updated_at` เปลี่ยน | เวลาอัปเดตเปลี่ยนอัตโนมัติ |
> | `created_at` ไม่เปลี่ยน | เวลาสร้างยังเหมือนเดิม |

#### ✅ ตรวจสอบ
- [ ] PUT `/api/notes/1/update/` ใน Postman → อัปเดตสำเร็จ
- [ ] `updated_at` เปลี่ยนเป็นเวลาใหม่
- [ ] GET `/api/notes/1/` ตรวจว่าข้อมูลเปลี่ยนจริง

---

### ขั้นตอนที่ 3: แก้ไข NoteEdit.vue — ดึงข้อมูลเดิมมาแสดง

เปิดไฟล์ `src/views/NoteEdit.vue` แล้ว**แก้ไขเป็นโค้ดนี้ทั้งหมด:**

```vue
<script>
export default {
  data() {
    return {
      noteId: null,
      title: '',
      body: '',
      is_done: false,
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
          const data = await response.json()
          this.title = data.title
          this.body = data.body
          this.is_done = data.is_done
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
    <h1>✏️ แก้ไข Note #{{ noteId }}</h1>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลดข้อมูล...</p>

    <!-- Error -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- ฟอร์มแก้ไข -->
    <form v-else @submit.prevent="submitForm">
      <div>
        <label>หัวข้อ:</label><br />
        <input v-model="title" type="text" placeholder="ใส่หัวข้อ" />
      </div>
      <br />
      <div>
        <label>เนื้อหา:</label><br />
        <textarea v-model="body" placeholder="ใส่เนื้อหา" rows="5"></textarea>
      </div>
      <br />
      <div>
        <label>
          <input type="checkbox" v-model="is_done" />
          เสร็จแล้ว
        </label>
      </div>
      <br />
      <button type="submit">💾 บันทึก</button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

> 💡 **สิ่งที่เปลี่ยนจากบทที่ 4:**
>
> | ก่อน (บทที่ 4) | หลัง (บทที่ 8) |
> |----------------|----------------|
> | `created()` — กำหนดข้อมูลจำลอง | `async created()` — ดึงจาก API จริง |
> | `this.title = 'ตัวอย่างหัวข้อ...'` | `this.title = data.title` (จาก API) |
> | ไม่มี `is_done` | มี checkbox `is_done` |
> | ไม่มี loading / error | มี loading + error handling |
>
> **อธิบายโค้ดทีละบรรทัด:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `async created()` | ทำงานเมื่อ component ถูกสร้าง — ดึงข้อมูลทันที |
> | `this.$route.params.id` | อ่าน ID จาก URL เช่น `/notes/5/edit` → `id = "5"` |
> | `fetch('.../' + this.noteId + '/')` | GET ข้อมูล Note ตาม ID |
> | `this.title = data.title` | เอาข้อมูลจาก API มาใส่ในตัวแปร → ฟอร์มแสดงข้อมูลเดิม |
> | `v-else @submit.prevent` | แสดงฟอร์มเมื่อไม่ loading และไม่มี error |
>
> 🤔 **ทำไมใช้ `created()` แทน `mounted()` ในกรณีนี้?**
>
> ทั้งสองใช้ได้! แต่ `created()` ทำงาน**เร็วกว่า** (ก่อน render) ซึ่งเหมาะกับการดึงข้อมูลมาแสดงในฟอร์ม
>
> | Hook | เหมาะกับ |
> |------|---------|
> | `created()` | ดึงข้อมูลมาใส่ตัวแปร (ไม่ต้องจัดการ DOM) |
> | `mounted()` | ดึงข้อมูล + อาจต้องจัดการ DOM (เช่น focus input) |

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteEdit.vue` ตามโค้ดด้านบน
- [ ] เปิด `http://localhost:5173/notes/1/edit` (เปลี่ยน 1 เป็น ID ที่มีจริง)
- [ ] ฟอร์มแสดง **ข้อมูลเดิม** ของ Note (title, body, is_done)
- [ ] เปิด `/notes/99999/edit` → เห็น error "ไม่พบ Note"

---

### ขั้นตอนที่ 4: ทดสอบการดึงข้อมูล

**ทดสอบที่ 1 — เปิดหน้าแก้ไข Note ที่มีอยู่:**
1. เปิดหน้า `/notes` → กด **✏️ แก้ไข** ของ Note ใดก็ได้
2. ฟอร์มควรแสดงข้อมูลเดิมของ Note นั้น (หัวข้อ, เนื้อหา, สถานะ)

**ทดสอบที่ 2 — เปิดหน้าแก้ไข Note ที่ไม่มี:**
1. พิมพ์ URL ตรง: `http://localhost:5173/notes/99999/edit`
2. ควรเห็น: "❌ ไม่พบ Note #99999"

**ทดสอบที่ 3 — ปิด Backend:**
1. ปิด Django server (กด `Ctrl+C` ใน Terminal 2)
2. เปิดหน้าแก้ไข Note ใดก็ได้
3. ควรเห็น: "❌ ไม่สามารถเชื่อมต่อ Backend ได้"
4. **เปิด Django server กลับ!** `uv run python manage.py runserver`

#### ✅ ตรวจสอบ
- [ ] Note ที่มีอยู่ → ฟอร์มแสดงข้อมูลเดิม
- [ ] Note ที่ไม่มี → เห็น error "ไม่พบ Note"
- [ ] Backend ปิด → เห็น error "ไม่สามารถเชื่อมต่อ"

---

## ส่วนที่ 2: ส่งข้อมูลที่แก้ไขไป Backend

### ขั้นตอนที่ 5: เพิ่ม submitForm — ส่ง PUT request

ตอนนี้ฟอร์มดึงข้อมูลเดิมมาแสดงได้แล้ว แต่กดปุ่มบันทึกยังไม่ทำอะไร

เพิ่ม method `submitForm` ใน `methods:` (ต่อท้าย `fetchNote`)

แก้ไข `src/views/NoteEdit.vue`:

```vue
<script>
export default {
  data() {
    return {
      noteId: null,
      title: '',
      body: '',
      is_done: false,
      loading: false,
      saving: false,
      error: '',
      errors: {}
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
          const data = await response.json()
          this.title = data.title
          this.body = data.body
          this.is_done = data.is_done
        } else {
          this.error = 'ไม่พบ Note #' + this.noteId
        }
      } catch (err) {
        this.error = 'ไม่สามารถเชื่อมต่อ Backend ได้'
      } finally {
        this.loading = false
      }
    },

    async submitForm() {
      this.errors = {}
      this.saving = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/update/', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.title,
            body: this.body,
            is_done: this.is_done
          })
        })

        if (response.ok) {
          this.$router.push('/notes')
        } else {
          const data = await response.json()
          this.errors = data
        }
      } catch (err) {
        alert('ไม่สามารถเชื่อมต่อ Backend ได้ — ตรวจสอบว่า Django server ทำงานอยู่')
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>✏️ แก้ไข Note #{{ noteId }}</h1>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลดข้อมูล...</p>

    <!-- Error (ดึงข้อมูลไม่ได้) -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- ฟอร์มแก้ไข -->
    <form v-else @submit.prevent="submitForm">
      <div>
        <label>หัวข้อ:</label><br />
        <input v-model="title" type="text" placeholder="ใส่หัวข้อ" />
        <p v-if="errors.title" style="color: red;">{{ errors.title[0] }}</p>
      </div>
      <br />
      <div>
        <label>เนื้อหา:</label><br />
        <textarea v-model="body" placeholder="ใส่เนื้อหา" rows="5"></textarea>
        <p v-if="errors.body" style="color: red;">{{ errors.body[0] }}</p>
      </div>
      <br />
      <div>
        <label>
          <input type="checkbox" v-model="is_done" />
          เสร็จแล้ว
        </label>
      </div>
      <br />
      <button type="submit" :disabled="saving">
        {{ saving ? '⏳ กำลังบันทึก...' : '💾 บันทึก' }}
      </button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

> 💡 **สิ่งที่เพิ่ม:**
>
> | โค้ดที่เพิ่ม | ทำอะไร |
> |-------------|--------|
> | `saving: false` | สถานะกำลังบันทึก (แยกจาก `loading` ที่ใช้ตอนดึงข้อมูล) |
> | `errors: {}` | เก็บ validation error จาก Backend |
> | `method: 'PUT'` | ใช้ PUT แทน POST เพราะเป็นการแก้ไข |
> | `'/notes/' + this.noteId + '/update/'` | URL รวม ID ของ Note ที่จะแก้ |
> | `is_done: this.is_done` | ส่งสถานะ checkbox ไปด้วย |
> | `v-if="errors.title"` | แสดง validation error ใต้ช่อง input |
> | `:disabled="saving"` | ปิดปุ่มขณะบันทึก ป้องกันกดซ้ำ |
>
> 🤔 **ทำไมแยก `loading` กับ `saving`?**
>
> | ตัวแปร | ใช้เมื่อ | ผลลัพธ์ |
> |--------|---------|---------|
> | `loading` | กำลัง**ดึงข้อมูล**เดิม (GET) | ซ่อนฟอร์ม แสดง "กำลังโหลด" |
> | `saving` | กำลัง**บันทึก**ข้อมูลใหม่ (PUT) | ปิดปุ่ม แสดง "กำลังบันทึก" |
>
> ถ้าใช้ตัวแปรเดียวกัน เวลากดบันทึก ฟอร์มจะหายไป (เพราะ `v-if="loading"` จะซ่อนฟอร์ม)

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteEdit.vue` เพิ่ม `submitForm` + `saving` + `errors`
- [ ] เปิดหน้าแก้ไข Note → แก้ไขข้อมูล → กดบันทึก → redirect ไปหน้ารายการ
- [ ] ข้อมูลในหน้ารายการเปลี่ยนตามที่แก้ไข

---

### ขั้นตอนที่ 6: ทดสอบการแก้ไข Note

**ทดสอบที่ 1 — แก้ไขหัวข้อและเนื้อหา:**
1. เปิดหน้า `/notes` → กด **✏️ แก้ไข** ของ Note ใดก็ได้
2. แก้ไขหัวข้อ เช่น เพิ่ม " (แก้ไขแล้ว)" ต่อท้าย
3. แก้ไขเนื้อหา
4. กดปุ่ม **💾 บันทึก**
5. ควร redirect ไปหน้า `/notes` → เห็นข้อมูลที่แก้ไข

**ทดสอบที่ 2 — เปลี่ยนสถานะ is_done:**
1. เปิดหน้าแก้ไข Note ที่ยังไม่เสร็จ (⬜)
2. ติ๊ก ☑️ **เสร็จแล้ว**
3. กดบันทึก
4. กลับมาหน้ารายการ → สถานะควรเปลี่ยนเป็น ✅

**ทดสอบที่ 3 — ส่งหัวข้อว่าง:**
1. เปิดหน้าแก้ไข Note
2. ลบหัวข้อให้ว่าง
3. กดบันทึก
4. ควรเห็น error สีแดง: "This field may not be blank."

**ทดสอบที่ 4 — เปิด DevTools Network:**
1. เปิด DevTools (F12) → แท็บ Network
2. เปิดหน้าแก้ไข Note → เห็น **GET** request ดึงข้อมูล
3. แก้ไขข้อมูลแล้วกดบันทึก → เห็น **PUT** request อัปเดตข้อมูล

#### ✅ ตรวจสอบ
- [ ] แก้ไข title + body → บันทึกสำเร็จ → ข้อมูลเปลี่ยน
- [ ] เปลี่ยน is_done → บันทึก → สถานะเปลี่ยนในหน้ารายการ
- [ ] ส่งหัวข้อว่าง → เห็น validation error
- [ ] DevTools: เห็น GET (ดึงข้อมูล) + PUT (อัปเดต) request

---

## ส่วนที่ 3: ทำความเข้าใจ Flow ทั้งหมด

### ขั้นตอนที่ 7: Flow การแก้ไข Note ตั้งแต่ต้นจนจบ

มาดู flow ทั้งหมดว่าเกิดอะไรบ้าง:

```
1. ผู้ใช้กด "✏️ แก้ไข" ในหน้ารายการ
   → Vue Router เปลี่ยน URL เป็น /notes/5/edit

2. NoteEdit.vue ถูกสร้าง → created() ทำงาน
   → อ่าน ID จาก URL: this.$route.params.id = "5"
   → เรียก fetchNote()

3. fetchNote() ส่ง GET /api/notes/5/
   → Backend ส่งข้อมูล Note กลับมา
   → ใส่ข้อมูลลง title, body, is_done → ฟอร์มแสดงข้อมูลเดิม

4. ผู้ใช้แก้ไขข้อมูลในฟอร์ม
   → v-model อัปเดตตัวแปรอัตโนมัติ

5. ผู้ใช้กด "💾 บันทึก" → submitForm() ทำงาน
   → ส่ง PUT /api/notes/5/update/ พร้อมข้อมูลใหม่

6. Backend อัปเดตฐานข้อมูล → ตอบ 200 OK
   → Vue redirect ไปหน้ารายการ → เห็นข้อมูลที่แก้ไข!
```

> 💡 **เปรียบเทียบกับชีวิตจริง:**
>
> | ขั้นตอน | เปรียบเทียบ |
> |---------|------------|
> | กด ✏️ แก้ไข | เปิดไฟล์เอกสารเดิม |
> | GET ข้อมูล | อ่านเนื้อหาเดิมในเอกสาร |
> | แก้ไขในฟอร์ม | พิมพ์แก้ไขเนื้อหา |
> | กด 💾 บันทึก | กด Save ไฟล์ |
> | redirect กลับ | ปิดไฟล์แล้วกลับไปดูรายการ |

#### ✅ ตรวจสอบ
- [ ] เข้าใจ flow ทั้งหมดตั้งแต่กดแก้ไขจนบันทึกสำเร็จ
- [ ] เข้าใจว่าใช้ 2 API: GET (ดึงข้อมูล) + PUT (อัปเดต)

---

### ขั้นตอนที่ 8: เปรียบเทียบ NoteCreate กับ NoteEdit

มาดูความเหมือนและความต่างระหว่าง 2 component:

> 💡 **เปรียบเทียบ NoteCreate.vue กับ NoteEdit.vue:**
>
> | | NoteCreate (บทที่ 6) | NoteEdit (บทที่ 8) |
> |---|---------------------|---------------------|
> | **หน้าที่** | สร้าง Note ใหม่ | แก้ไข Note ที่มีอยู่ |
> | **ฟอร์มเริ่มต้น** | ว่างเปล่า | มีข้อมูลเดิม |
> | **Lifecycle Hook** | ไม่มี | `created()` ดึงข้อมูลก่อน |
> | **HTTP Method** | POST | PUT |
> | **URL** | `/api/notes/create/` | `/api/notes/5/update/` |
> | **ต้องรู้ ID** | ❌ | ✅ (จาก URL params) |
> | **ส่ง is_done** | ไม่ส่ง (ใช้ default) | ส่ง (อาจเปลี่ยนค่า) |
> | **Loading** | มีแค่ `loading` (ตอนบันทึก) | มี `loading` (ดึงข้อมูล) + `saving` (บันทึก) |

#### ✅ ตรวจสอบ
- [ ] เข้าใจว่า NoteCreate กับ NoteEdit ต่างกันอย่างไร
- [ ] เข้าใจว่า NoteEdit ต้องใช้ 2 API (GET + PUT)

---

## สรุปโค้ดทั้งหมดในบทนี้

ไฟล์เดียวที่แก้ไขในบทนี้:

**`src/views/NoteEdit.vue`** (เวอร์ชันสมบูรณ์):

```vue
<script>
export default {
  data() {
    return {
      noteId: null,
      title: '',
      body: '',
      is_done: false,
      loading: false,
      saving: false,
      error: '',
      errors: {}
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
          const data = await response.json()
          this.title = data.title
          this.body = data.body
          this.is_done = data.is_done
        } else {
          this.error = 'ไม่พบ Note #' + this.noteId
        }
      } catch (err) {
        this.error = 'ไม่สามารถเชื่อมต่อ Backend ได้'
      } finally {
        this.loading = false
      }
    },

    async submitForm() {
      this.errors = {}
      this.saving = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/' + this.noteId + '/update/', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.title,
            body: this.body,
            is_done: this.is_done
          })
        })

        if (response.ok) {
          this.$router.push('/notes')
        } else {
          const data = await response.json()
          this.errors = data
        }
      } catch (err) {
        alert('ไม่สามารถเชื่อมต่อ Backend ได้ — ตรวจสอบว่า Django server ทำงานอยู่')
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>✏️ แก้ไข Note #{{ noteId }}</h1>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลดข้อมูล...</p>

    <!-- Error (ดึงข้อมูลไม่ได้) -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- ฟอร์มแก้ไข -->
    <form v-else @submit.prevent="submitForm">
      <div>
        <label>หัวข้อ:</label><br />
        <input v-model="title" type="text" placeholder="ใส่หัวข้อ" />
        <p v-if="errors.title" style="color: red;">{{ errors.title[0] }}</p>
      </div>
      <br />
      <div>
        <label>เนื้อหา:</label><br />
        <textarea v-model="body" placeholder="ใส่เนื้อหา" rows="5"></textarea>
        <p v-if="errors.body" style="color: red;">{{ errors.body[0] }}</p>
      </div>
      <br />
      <div>
        <label>
          <input type="checkbox" v-model="is_done" />
          เสร็จแล้ว
        </label>
      </div>
      <br />
      <button type="submit" :disabled="saving">
        {{ saving ? '⏳ กำลังบันทึก...' : '💾 บันทึก' }}
      </button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

---

## ❌ ปัญหาที่พบบ่อย

### ปัญหา: เปิดหน้าแก้ไขแล้วฟอร์มว่าง ไม่มีข้อมูลเดิม

**สาเหตุ:** อาจลืมเรียก `fetchNote()` ใน `created()` หรือลืม `await`

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

### ปัญหา: กดบันทึกแล้วได้ error `405 Method Not Allowed`

**สาเหตุ:** ใช้ method ผิด (POST แทน PUT) หรือ URL ผิด

**วิธีแก้:**
```js
// ❌ ผิด — ใช้ POST (สำหรับสร้าง)
fetch('http://localhost:8000/api/notes/1/update/', {
  method: 'POST',
  ...
})

// ✅ ถูก — ใช้ PUT (สำหรับแก้ไข)
fetch('http://localhost:8000/api/notes/1/update/', {
  method: 'PUT',
  ...
})
```

---

### ปัญหา: กดบันทึกแล้วได้ error `400 Bad Request` แม้กรอกข้อมูลครบ

**สาเหตุ:** อาจลืมส่ง `is_done` ไปด้วย — Backend ต้องการทุก field

**วิธีแก้:**
```js
// ❌ ผิด — ส่งไม่ครบ
body: JSON.stringify({
  title: this.title,
  body: this.body
})

// ✅ ถูก — ส่งครบทุก field
body: JSON.stringify({
  title: this.title,
  body: this.body,
  is_done: this.is_done
})
```

---

### ปัญหา: เปิดหน้าแก้ไข Note ที่ไม่มี แต่ไม่เห็น error

**สาเหตุ:** อาจตรวจแค่ `catch` แต่ไม่ตรวจ `response.ok`

**วิธีแก้:**
```js
// ❌ ผิด — ไม่ตรวจ response status
const data = await response.json()
this.title = data.title

// ✅ ถูก — ตรวจ response.ok ก่อน
if (response.ok) {
  const data = await response.json()
  this.title = data.title
} else {
  this.error = 'ไม่พบ Note #' + this.noteId
}
```

---

### ปัญหา: แก้ไข Note แล้วกลับมาหน้ารายการ ข้อมูลยังเป็นเดิม

**สาเหตุ:** อาจเป็นเพราะ browser cache

**วิธีแก้:**
1. เปิด DevTools (F12) → แท็บ Network
2. ติ๊ก ☑️ **Disable cache**
3. Refresh หน้ารายการอีกครั้ง

หรือตรวจว่า PUT request สำเร็จจริง (status 200) ใน DevTools Network

---

## 🏋️ ลองทำเอง (Challenge)

### ⭐ ระดับง่าย
เพิ่ม **ลิงก์ "⬅️ กลับ"** ที่ด้านบนของฟอร์ม แทนที่จะมีแค่ปุ่ม "❌ ยกเลิก" ด้านล่าง:
- เพิ่ม `<router-link to="/notes">⬅️ กลับไปรายการ</router-link>` ก่อน `<h1>`
- ทำให้ผู้ใช้กลับไปหน้ารายการได้ง่ายขึ้น

### ⭐⭐ ระดับปานกลาง
เพิ่ม **แสดงวันที่ created_at และ updated_at** ในหน้าแก้ไข:
- เพิ่ม `created_at: ''` และ `updated_at: ''` ใน `data()`
- เก็บค่าจาก API: `this.created_at = data.created_at`
- ใช้ `formatDate()` method จากบทที่ 7 แสดงวันที่
- แสดงไว้ใต้หัวข้อ: "สร้างเมื่อ: 15 ม.ค. 2568 | แก้ไขล่าสุด: 15 ม.ค. 2568 14:30"

### ⭐⭐⭐ ระดับยาก
ทำ **Confirm before leaving** — ถ้าผู้ใช้แก้ไขข้อมูลแล้วยังไม่บันทึก แต่จะออกจากหน้า ให้ถามก่อน:
- เพิ่มตัวแปร `isDirty: false` ใน data
- ใช้ `watch` ดูค่า `title`, `body`, `is_done` — ถ้าเปลี่ยนให้ `isDirty = true`
- ใช้ `beforeRouteLeave` navigation guard ของ Vue Router
- ถ้า `isDirty = true` → `confirm('คุณมีการเปลี่ยนแปลงที่ยังไม่บันทึก ต้องการออกจากหน้านี้?')`

<details>
<summary>💡 คำใบ้ระดับง่าย</summary>

เพิ่มในส่วน template ก่อน `<h1>`:
```html
<router-link to="/notes">⬅️ กลับไปรายการ</router-link>
```

แค่นี้เลย! `<router-link>` สร้างลิงก์ที่ไม่ reload หน้า

</details>

<details>
<summary>💡 คำใบ้ระดับปานกลาง</summary>

เพิ่มใน `data()`:
```js
created_at: '',
updated_at: ''
```

ใน `fetchNote()` หลังจากเก็บ title, body, is_done แล้ว:
```js
this.created_at = data.created_at
this.updated_at = data.updated_at
```

เพิ่ม method `formatDate()` (copy จากบทที่ 7):
```js
formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
```

แสดงใน template (ระหว่าง `<h1>` กับ `<form>`):
```html
<p style="color: gray;" v-if="created_at">
  📅 สร้างเมื่อ: {{ formatDate(created_at) }} | แก้ไขล่าสุด: {{ formatDate(updated_at) }}
</p>
```

</details>

<details>
<summary>💡 คำใบ้ระดับยาก</summary>

`beforeRouteLeave` เป็น **Navigation Guard** ของ Vue Router ที่ทำงานก่อนออกจากหน้า:

```js
export default {
  data() {
    return {
      // ... เดิม
      isDirty: false
    }
  },

  watch: {
    title() { this.isDirty = true },
    body() { this.isDirty = true },
    is_done() { this.isDirty = true }
  },

  // Navigation Guard
  beforeRouteLeave(to, from, next) {
    if (this.isDirty) {
      const answer = confirm('คุณมีการเปลี่ยนแปลงที่ยังไม่บันทึก ต้องการออกจากหน้านี้?')
      if (answer) {
        next()       // อนุญาตให้ออก
      } else {
        next(false)  // ยกเลิก — อยู่หน้าเดิม
      }
    } else {
      next()         // ไม่มีการเปลี่ยนแปลง — ออกได้เลย
    }
  },

  methods: {
    // ...

    async submitForm() {
      // ...
      if (response.ok) {
        this.isDirty = false   // รีเซ็ตก่อน redirect
        this.$router.push('/notes')
      }
    }
  }
}
```

**ข้อควรระวัง:** ต้องเซ็ต `isDirty = false` ก่อน `$router.push` ไม่งั้นจะถามทุกครั้งที่บันทึกสำเร็จ!

**ปัญหาเพิ่มเติม:** `watch` จะทำงานตอน `fetchNote()` ใส่ข้อมูลเดิมด้วย ทำให้ `isDirty = true` ทันที
แก้โดยเพิ่ม flag:

```js
async fetchNote() {
  this.loading = true
  try {
    // ...
    if (response.ok) {
      const data = await response.json()
      this.title = data.title
      this.body = data.body
      this.is_done = data.is_done

      // รีเซ็ตหลังใส่ข้อมูลเดิม
      this.$nextTick(() => {
        this.isDirty = false
      })
    }
  }
  // ...
}
```

`this.$nextTick()` รอให้ Vue อัปเดตเสร็จก่อน แล้วค่อยรีเซ็ต `isDirty`

</details>

---

## 📖 คำศัพท์ที่เรียนรู้ในบทนี้

| คำศัพท์ | ความหมาย | เปรียบเทียบ |
|---------|----------|-------------|
| PUT | HTTP method สำหรับอัปเดตข้อมูลทั้งหมด | เหมือนยื่นเอกสารฉบับแก้ไขใหม่ทั้งฉบับ |
| Pre-fill Form | การใส่ข้อมูลเดิมในฟอร์มก่อนให้ผู้ใช้แก้ไข | เหมือนเปิดไฟล์เอกสารเดิม — เห็นเนื้อหาที่เขียนไว้ |
| created() | Lifecycle Hook — ทำงานเมื่อ component ถูกสร้าง (ก่อน render) | เหมือนเชฟเตรียมวัตถุดิบก่อนเปิดร้าน |
| $route.params | ค่าตัวแปรจาก URL เช่น `/notes/5/edit` → `{ id: "5" }` | เหมือนที่อยู่ที่ระบุเลขห้อง — บอกว่าจะไปห้องไหน |
| response.ok | ตรวจว่า HTTP status เป็น 200-299 (สำเร็จ) | เหมือนดูว่าได้รับพัสดุสำเร็จหรือไม่ |
| 404 Not Found | Status code ที่บอกว่าไม่พบข้อมูลที่ขอ | เหมือนไปหาบ้านเลขที่ไม่มีจริง |
| Validation Error | Error ที่ Backend ส่งกลับเมื่อข้อมูลไม่ถูกต้อง | เหมือนเจ้าหน้าที่ส่งแบบฟอร์มคืน เพราะกรอกไม่ครบ |

---

## สรุปสิ่งที่ได้เรียนรู้ ✅

| หัวข้อ | สิ่งที่เรียนรู้ |
|--------|----------------|
| Pre-fill Form | ดึงข้อมูลเดิมจาก API (GET) มาแสดงในฟอร์มก่อนให้แก้ไข |
| PUT Request | ส่ง PUT request พร้อมข้อมูลที่แก้ไขไป Backend — ต้องระบุ ID ใน URL |
| created() vs mounted() | ทั้งสองใช้ดึงข้อมูลได้ — `created()` ทำงานก่อน render, `mounted()` ทำงานหลัง render |
| loading vs saving | แยกสถานะ "กำลังโหลด" กับ "กำลังบันทึก" ไม่ให้สับสน |
| Error Handling | จัดการ 3 กรณี: 404 Not Found, validation error, network error |
| POST vs PUT | POST = สร้างใหม่ (ไม่ต้องรู้ ID), PUT = แก้ไขของเดิม (ต้องรู้ ID) |
| is_done checkbox | ใช้ `<input type="checkbox" v-model="is_done">` เชื่อม checkbox กับตัวแปร boolean |

---

> ➡️ **บทถัดไป:** [บทที่ 9: ลบ Note (Delete)](./lesson-9-delete-note.md)
