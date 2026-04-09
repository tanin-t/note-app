# บทที่ 7: แสดงรายการ Note — ดึงข้อมูลจาก API มาแสดง

> 📍 **บทที่ 7 / 10** ━━━━━━━━━━ `[███████░░░]`

| ⬅️ [บทที่ 6: สร้าง Note](./lesson-6-create-note.md) | [สารบัญ](./tutorial.md) | [บทที่ 8: แก้ไข Note ➡️](./lesson-8-edit-note.md) |
|:---|:---:|---:|

---

## 🎯 เป้าหมาย

ในบทนี้เราจะ:
- เข้าใจ **Lifecycle Hook** (`mounted`) — โค้ดที่ทำงานอัตโนมัติเมื่อหน้าเปิด
- ดึงข้อมูล Note จาก **API จริง** มาแทนข้อมูลจำลอง
- แสดงรายการ Note ด้วย **`v-for`** ในตาราง
- เพิ่ม **ฟังก์ชันค้นหา** (search) ที่ส่ง query ไป Backend
- จัดการ **loading state** และ **empty state** ให้ UX ดี
- เข้าใจ **วันที่/เวลา** ที่ Backend ส่งกลับมา

> 🎮 **Fun Fact:** ในบทที่ 4 เราใช้ข้อมูลจำลอง (hardcoded) ไว้ในโค้ด 3 รายการ
> ในบทนี้เราจะลบข้อมูลจำลองทิ้ง แล้วดึงข้อมูล **จริง** จาก Backend มาแสดง! 🎉

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

- ทำบทที่ 6 เสร็จแล้ว (สร้าง Note ผ่านหน้าเว็บได้)
- มี **2 Terminal** ทำงาน:
  1. Terminal 1: `npm run dev` (Vue.js — port 5173)
  2. Terminal 2: `uv run python manage.py runserver` (Django — port 8000)
- มี Note อย่างน้อย 1-2 รายการในฐานข้อมูล (สร้างจากบทที่ 6 หรือ Postman)

> 💡 **ถ้ายังไม่ได้ทำบทก่อนหน้า** สามารถเริ่มจาก branch สำเร็จได้:
> ```bash
> git checkout lesson-6-completed
> ```

---

## 🧠 ทำความเข้าใจก่อนเริ่ม

### ข้อมูลจำลอง vs ข้อมูลจาก API

ในบทที่ 4 เราสร้าง `NoteList.vue` ที่มี **ข้อมูลจำลอง** (hardcoded) ไว้ในโค้ด:

```js
// ❌ ข้อมูลจำลอง — เขียนตายตัวในโค้ด
data() {
  return {
    notes: [
      { id: 1, title: 'ซื้อของ', body: 'ไข่ นม ขนมปัง' },
      { id: 2, title: 'การบ้าน', body: 'ทำแบบฝึกหัดบทที่ 4' },
      { id: 3, title: 'ประชุม', body: 'ประชุมทีมบ่าย 2 โมง' }
    ]
  }
}
```

ในบทนี้เราจะเปลี่ยนมา **ดึงจาก API จริง:**

```js
// ✅ ข้อมูลจาก API — ดึงจาก Backend จริง
data() {
  return {
    notes: []   // เริ่มที่ว่าง แล้วค่อย fetch มาใส่
  }
}
```

> 💡 **เปรียบเทียบ:**
>
> | ข้อมูลจำลอง | ข้อมูลจาก API |
> |-------------|---------------|
> | เขียนตายตัวในโค้ด | ดึงจาก Backend |
> | ข้อมูลไม่เปลี่ยน ไม่ว่า reload กี่ครั้ง | ข้อมูลอัปเดตตามฐานข้อมูลจริง |
> | เหมือนอ่านจากกระดาษ | เหมือนค้นหาใน Google |

---

### mounted() คืออะไร?

`mounted()` คือ **Lifecycle Hook** — ฟังก์ชันที่ Vue เรียกอัตโนมัติเมื่อ component **แสดงบนหน้าจอแล้ว**

```
Component ถูกสร้าง → render HTML → ✅ mounted() ทำงาน!
```

> 💡 **เปรียบเทียบ Lifecycle Hooks:**
>
> | Hook | ทำงานเมื่อไหร่ | ใช้ทำอะไร |
> |------|---------------|----------|
> | `created()` | component ถูกสร้าง (ยังไม่แสดง) | ตั้งค่าตัวแปร, อ่าน route params |
> | `mounted()` | component แสดงบนหน้าจอแล้ว | **ดึงข้อมูลจาก API** |
>
> เปรียบเทียบ:
> - `created()` = เชฟเตรียมวัตถุดิบ (ยังไม่ได้ปรุง)
> - `mounted()` = อาหารเสิร์ฟพร้อมกิน — **ถึงเวลาจัดโต๊ะ (ดึงข้อมูลมาแสดง)**

ทำไมดึงข้อมูลใน `mounted()` แทน `created()`?
- ทั้งสองใช้ได้ แต่ `mounted()` เป็นที่นิยมเพราะ **HTML พร้อมแล้ว** ถ้าต้องการจัดการ DOM ก็ทำได้ทันที

---

## 📝 ขั้นตอน

---

## ส่วนที่ 1: ดึงข้อมูลจาก API

### ขั้นตอนที่ 1: ดูข้อมูลที่ API ส่งกลับก่อน

ก่อนเขียนโค้ด มาดูก่อนว่า API ส่งอะไรกลับมา:

เปิด **Postman** แล้ว `GET http://localhost:8000/api/notes/`

ตัวอย่างผลลัพธ์:
```json
[
  {
    "id": 3,
    "title": "ประชุม",
    "body": "ประชุมทีมบ่าย 2 โมง",
    "is_done": false,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "title": "ซื้อของ",
    "body": "ไข่ นม ขนมปัง",
    "is_done": false,
    "created_at": "2025-01-15T09:00:00Z",
    "updated_at": "2025-01-15T09:00:00Z"
  }
]
```

> 💡 **สังเกต:**
>
> | จุดสังเกต | รายละเอียด |
> |-----------|-----------|
> | ผลลัพธ์เป็น **Array** `[...]` | เพราะเป็นรายการหลายรายการ |
> | เรียงจากอัปเดตล่าสุดก่อน | Backend ตั้ง `ordering = ['-updated_at']` |
> | มี `created_at`, `updated_at` | วันที่ในรูปแบบ ISO 8601 |
> | มี `is_done` | สถานะว่าทำเสร็จแล้วหรือยัง |

#### ✅ ตรวจสอบ
- [ ] เปิด Postman แล้ว GET `/api/notes/` → เห็นรายการ Note
- [ ] เข้าใจโครงสร้าง JSON ที่ Backend ส่งกลับ

---

### ขั้นตอนที่ 2: แก้ไข NoteList.vue — ดึงข้อมูลจาก API

เปิดไฟล์ `src/views/NoteList.vue` แล้ว**แก้ไขเป็นโค้ดนี้ทั้งหมด:**

```vue
<script>
export default {
  data() {
    return {
      notes: []
    }
  },

  async mounted() {
    await this.fetchNotes()
  },

  methods: {
    async fetchNotes() {
      const response = await fetch('http://localhost:8000/api/notes/')
      const data = await response.json()
      this.notes = data
    }
  }
}
</script>

<template>
  <div>
    <h1>📋 รายการ Note ทั้งหมด</h1>

    <router-link to="/notes/create">➕ สร้าง Note ใหม่</router-link>

    <table border="1" cellpadding="8" style="margin-top: 16px; width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>#</th>
          <th>หัวข้อ</th>
          <th>เนื้อหา</th>
          <th>จัดการ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="note in notes" :key="note.id">
          <td>{{ note.id }}</td>
          <td>{{ note.title }}</td>
          <td>{{ note.body }}</td>
          <td>
            <router-link :to="'/notes/' + note.id + '/edit'">✏️ แก้ไข</router-link>
            |
            <router-link :to="'/notes/' + note.id + '/delete'">🗑️ ลบ</router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
```

> 💡 **สิ่งที่เปลี่ยนจากบทที่ 4:**
>
> | ก่อน (บทที่ 4) | หลัง (บทที่ 7) |
> |----------------|----------------|
> | `notes: [{ id: 1, ... }, ...]` — ข้อมูลจำลอง 3 รายการ | `notes: []` — เริ่มที่ว่าง |
> | ไม่มี `mounted()` | มี `async mounted()` เรียก `fetchNotes()` |
> | ไม่มี `methods` | มี `fetchNotes()` ดึงข้อมูลจาก API |
>
> **อธิบายโค้ดทีละบรรทัด:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `notes: []` | เริ่มต้นเป็น array ว่าง — ยังไม่มีข้อมูล |
> | `async mounted()` | ทำงานเมื่อ component แสดงบนหน้าจอ |
> | `await this.fetchNotes()` | เรียก method `fetchNotes()` แล้วรอให้เสร็จ |
> | `fetch('...api/notes/')` | ส่ง GET request ไป Backend (GET เป็นค่าเริ่มต้น ไม่ต้องระบุ method) |
> | `response.json()` | แปลง response เป็น JavaScript array |
> | `this.notes = data` | เก็บข้อมูลไว้ใน `notes` → Vue อัปเดตตารางอัตโนมัติ |
>
> 🤔 **ทำไม GET request ไม่ต้องใส่ `method: 'GET'`?**
>
> เพราะ `fetch()` ใช้ GET เป็น**ค่าเริ่มต้น** อยู่แล้ว:
> ```js
> // ทั้งสองแบบทำเหมือนกัน:
> fetch('http://localhost:8000/api/notes/')               // GET (ค่าเริ่มต้น)
> fetch('http://localhost:8000/api/notes/', { method: 'GET' })  // GET (ระบุชัด)
> ```

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteList.vue` ตามโค้ดด้านบน
- [ ] เปิด `http://localhost:5173/notes` → เห็นรายการ Note จาก API จริง!
- [ ] ข้อมูลตรงกับที่เห็นใน Postman
- [ ] เข้าใจว่า `mounted()` ทำงานอัตโนมัติเมื่อเปิดหน้า

---

### ขั้นตอนที่ 3: ทดสอบว่าข้อมูลมาจาก API จริง

เพื่อพิสูจน์ว่าข้อมูลมาจาก Backend จริง ลองทำดังนี้:

**ทดสอบที่ 1 — สร้าง Note ใหม่แล้วดู:**
1. กด **➕ สร้าง Note ใหม่** → กรอกข้อมูล → กดบันทึก
2. redirect กลับมาหน้า `/notes`
3. ควรเห็น Note ใหม่ที่เพิ่งสร้าง! 🎉

**ทดสอบที่ 2 — สร้างผ่าน Postman แล้วดู:**
1. เปิด Postman → `POST http://localhost:8000/api/notes/create/`
2. Body: `{ "title": "สร้างจาก Postman", "body": "ทดสอบ" }`
3. กลับมาที่เบราว์เซอร์ → **Refresh** หน้า `/notes`
4. ควรเห็น Note จาก Postman ปรากฏ!

> 💡 ไม่ว่าจะสร้างจาก **หน้าเว็บ** หรือ **Postman** ก็เห็นข้อมูลเดียวกัน
> เพราะทั้งสองใช้ **ฐานข้อมูลเดียวกัน!**

#### ✅ ตรวจสอบ
- [ ] สร้าง Note ใหม่ผ่านหน้าเว็บ → เห็นในรายการ
- [ ] สร้าง Note ผ่าน Postman → Refresh แล้วเห็นในรายการ
- [ ] เข้าใจว่าข้อมูลมาจาก Backend ผ่าน API จริง

---

## ส่วนที่ 2: เพิ่ม Loading State และ Error Handling

### ขั้นตอนที่ 4: ปัญหา — หน้าว่างขณะรอข้อมูล

ลอง **refresh** หน้า `/notes` แล้วสังเกตดีๆ:

เมื่อ refresh จะเห็นตารางว่างเปล่า**ชั่วขณะ** ก่อนข้อมูลจะปรากฏ

ทำไม? เพราะ:
```
1. เปิดหน้า → notes = [] (ว่าง) → แสดงตารางว่าง
2. mounted() ทำงาน → เริ่ม fetch API → ...รอ...
3. ได้ข้อมูลแล้ว → notes = [...] → แสดงข้อมูล
```

ช่วง "รอ" (ขั้นตอนที่ 2) ผู้ใช้เห็นตารางว่าง ไม่รู้ว่ากำลังโหลดหรือไม่มีข้อมูลจริง 😕

**วิธีแก้:** เพิ่ม loading state + empty state!

---

### ขั้นตอนที่ 5: เพิ่ม Loading State + Error Handling + Empty State

แก้ไข `src/views/NoteList.vue`:

```vue
<script>
export default {
  data() {
    return {
      notes: [],
      loading: false,
      error: ''
    }
  },

  async mounted() {
    await this.fetchNotes()
  },

  methods: {
    async fetchNotes() {
      this.loading = true
      this.error = ''

      try {
        const response = await fetch('http://localhost:8000/api/notes/')
        const data = await response.json()
        this.notes = data
      } catch (err) {
        this.error = 'ไม่สามารถดึงข้อมูลได้ — ตรวจสอบว่า Backend ทำงานอยู่'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>📋 รายการ Note ทั้งหมด</h1>

    <router-link to="/notes/create">➕ สร้าง Note ใหม่</router-link>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลด...</p>

    <!-- Error -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- Empty state -->
    <p v-else-if="notes.length === 0">📭 ยังไม่มี Note — ลองสร้าง Note ใหม่!</p>

    <!-- ตาราง Note -->
    <table v-else border="1" cellpadding="8" style="margin-top: 16px; width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>#</th>
          <th>หัวข้อ</th>
          <th>เนื้อหา</th>
          <th>จัดการ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="note in notes" :key="note.id">
          <td>{{ note.id }}</td>
          <td>{{ note.title }}</td>
          <td>{{ note.body }}</td>
          <td>
            <router-link :to="'/notes/' + note.id + '/edit'">✏️ แก้ไข</router-link>
            |
            <router-link :to="'/notes/' + note.id + '/delete'">🗑️ ลบ</router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
```

> 💡 **สิ่งที่เพิ่ม:**
>
> | โค้ดที่เพิ่ม | ทำอะไร |
> |-------------|--------|
> | `loading: false` | ตัวแปรบอกว่ากำลังโหลดอยู่หรือไม่ |
> | `error: ''` | ตัวแปรเก็บข้อความ error |
> | `try/catch/finally` | จัดการ error เหมือนบทที่ 6 |
> | `v-if="loading"` | แสดงข้อความ "กำลังโหลด" ขณะรอ API |
> | `v-else-if="error"` | แสดง error ถ้าเชื่อมต่อ Backend ไม่ได้ |
> | `v-else-if="notes.length === 0"` | แสดง "ไม่มี Note" ถ้าข้อมูลว่าง |
> | `v-else` | แสดงตาราง ถ้ามีข้อมูล |
>
> 🤔 **v-if / v-else-if / v-else คืออะไร?**
>
> เหมือน `if / else if / else` ใน JavaScript แต่ใช้ใน HTML:
>
> ```
> ถ้า loading = true        → แสดง "กำลังโหลด"
> ไม่งั้น ถ้ามี error       → แสดง error message
> ไม่งั้น ถ้า notes ว่าง   → แสดง "ไม่มี Note"
> ไม่งั้น                   → แสดงตาราง
> ```
>
> **สำคัญ:** `v-if`, `v-else-if`, `v-else` ต้องอยู่ **ติดกัน** (ไม่มี element อื่นคั่น)

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteList.vue` เพิ่ม loading + error + empty state
- [ ] Refresh หน้า → เห็น "⏳ กำลังโหลด..." ก่อนข้อมูลแสดง
- [ ] ลองปิด Django server → Refresh → เห็น error สีแดง
- [ ] เปิด Django server กลับ → Refresh → ข้อมูลแสดงปกติ

---

### ขั้นตอนที่ 6: ทดสอบแต่ละสถานะ

**ทดสอบที่ 1 — Loading state:**
1. Refresh หน้า `/notes`
2. สังเกตว่าเห็น "⏳ กำลังโหลด..." ก่อนข้อมูลแสดง (อาจเห็นแค่แป๊บเดียว)

**ทดสอบที่ 2 — Error state:**
1. ปิด Django server (กด `Ctrl+C` ใน Terminal 2)
2. Refresh หน้า `/notes`
3. ควรเห็น: "❌ ไม่สามารถดึงข้อมูลได้..."
4. **เปิด Django server กลับ!** `uv run python manage.py runserver`

**ทดสอบที่ 3 — Empty state:**
1. เปิด Postman
2. `GET http://localhost:8000/api/notes/` → ดูว่ามี Note กี่รายการ
3. ลบ Note ทั้งหมดด้วย Postman:
   - `DELETE http://localhost:8000/api/notes/1/delete/`
   - `DELETE http://localhost:8000/api/notes/2/delete/`
   - (ลบจนหมด)
4. Refresh หน้า `/notes` → ควรเห็น: "📭 ยังไม่มี Note — ลองสร้าง Note ใหม่!"
5. สร้าง Note ใหม่ให้หน้ากลับมาปกติ

> 💡 **ทำไมต้องมี Empty State?**
>
> | ไม่มี Empty State | มี Empty State |
> |-------------------|----------------|
> | เห็นตารางว่าง — ไม่แน่ใจว่ากำลังโหลดหรือไม่มีจริง | เห็นข้อความชัดเจนว่า "ไม่มี Note" |
> | ผู้ใช้สับสน 😕 | ผู้ใช้รู้ว่าต้องทำอะไรต่อ ✅ |

#### ✅ ตรวจสอบ
- [ ] Loading: เห็น "กำลังโหลด" ขณะรอ API
- [ ] Error: ปิด Backend → เห็น error สีแดง
- [ ] Empty: ลบ Note ทั้งหมด → เห็น "ยังไม่มี Note"
- [ ] ปกติ: มี Note → เห็นตาราง

---

## ส่วนที่ 3: เพิ่มฟังก์ชันค้นหา (Search)

### ขั้นตอนที่ 7: ดู API ค้นหาใน Postman ก่อน

ก่อนเขียนโค้ด ลองค้นหาใน Postman ก่อน:

```
GET http://localhost:8000/api/notes/?search=ซื้อ
```

ควรได้เฉพาะ Note ที่ title มีคำว่า "ซื้อ"

> 💡 **จำได้ไหม?** จากบทที่ 5 เราทดสอบ `?search=` ใน Postman แล้ว!
>
> Backend รับ query parameter `search` แล้ว **filter เฉพาะ Note ที่มีคำค้นหาในหัวข้อ** (case-insensitive)

#### ✅ ตรวจสอบ
- [ ] ลอง GET `/api/notes/?search=คำค้นหา` ใน Postman → ได้ผลลัพธ์ที่ filter แล้ว

---

### ขั้นตอนที่ 8: เพิ่มช่องค้นหาใน NoteList.vue

แก้ไข `src/views/NoteList.vue` เป็น**เวอร์ชันสมบูรณ์:**

```vue
<script>
export default {
  data() {
    return {
      notes: [],
      loading: false,
      error: '',
      search: ''
    }
  },

  async mounted() {
    await this.fetchNotes()
  },

  methods: {
    async fetchNotes() {
      this.loading = true
      this.error = ''

      try {
        let url = 'http://localhost:8000/api/notes/'

        if (this.search) {
          url = url + '?search=' + this.search
        }

        const response = await fetch(url)
        const data = await response.json()
        this.notes = data
      } catch (err) {
        this.error = 'ไม่สามารถดึงข้อมูลได้ — ตรวจสอบว่า Backend ทำงานอยู่'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>📋 รายการ Note ทั้งหมด</h1>

    <div style="margin-bottom: 16px;">
      <router-link to="/notes/create">➕ สร้าง Note ใหม่</router-link>
    </div>

    <!-- ช่องค้นหา -->
    <div style="margin-bottom: 16px;">
      <input
        v-model="search"
        type="text"
        placeholder="🔍 ค้นหาหัวข้อ..."
        @keyup.enter="fetchNotes()"
      />
      <button @click="fetchNotes()">🔍 ค้นหา</button>
    </div>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลด...</p>

    <!-- Error -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- Empty state -->
    <p v-else-if="notes.length === 0 && search">
      🔍 ไม่พบ Note ที่มีคำว่า "{{ search }}"
    </p>
    <p v-else-if="notes.length === 0">📭 ยังไม่มี Note — ลองสร้าง Note ใหม่!</p>

    <!-- ตาราง Note -->
    <table v-else border="1" cellpadding="8" style="margin-top: 16px; width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>#</th>
          <th>หัวข้อ</th>
          <th>เนื้อหา</th>
          <th>สถานะ</th>
          <th>จัดการ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="note in notes" :key="note.id">
          <td>{{ note.id }}</td>
          <td>{{ note.title }}</td>
          <td>{{ note.body }}</td>
          <td>{{ note.is_done ? '✅' : '⬜' }}</td>
          <td>
            <router-link :to="'/notes/' + note.id + '/edit'">✏️ แก้ไข</router-link>
            |
            <router-link :to="'/notes/' + note.id + '/delete'">🗑️ ลบ</router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- จำนวนรายการ -->
    <p v-if="!loading && !error" style="color: gray; margin-top: 8px;">
      แสดง {{ notes.length }} รายการ
    </p>
  </div>
</template>
```

> 💡 **สิ่งที่เพิ่ม:**
>
> | โค้ดที่เพิ่ม | ทำอะไร |
> |-------------|--------|
> | `search: ''` | ตัวแปรเก็บคำค้นหา |
> | `v-model="search"` | เชื่อม input กับตัวแปร `search` |
> | `@keyup.enter="fetchNotes()"` | กด Enter ในช่องค้นหา → เรียก fetchNotes |
> | `@click="fetchNotes()"` | กดปุ่มค้นหา → เรียก fetchNotes |
> | `url + '?search=' + this.search` | ส่งคำค้นหาไป Backend ผ่าน query parameter |
> | `notes.length === 0 && search` | แยก empty state: ค้นหาแล้วไม่เจอ vs ไม่มี Note เลย |
> | `note.is_done ? '✅' : '⬜'` | แสดงสถานะด้วย emoji |
> | `notes.length` + `รายการ` | แสดงจำนวน Note ทั้งหมด |
>
> 🤔 **`@keyup.enter` คืออะไร?**
>
> เป็น **Event Modifier** ของ Vue — จับเฉพาะเมื่อผู้ใช้กดปุ่ม **Enter**:
>
> | Event | ทำงานเมื่อ |
> |-------|----------|
> | `@keyup` | กดปุ่มอะไรก็ได้ |
> | `@keyup.enter` | กดปุ่ม **Enter** เท่านั้น |
> | `@keyup.escape` | กดปุ่ม **Esc** เท่านั้น |

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteList.vue` เป็นเวอร์ชันสมบูรณ์
- [ ] เห็นช่องค้นหาและปุ่ม 🔍 ค้นหา
- [ ] พิมพ์คำค้นหา + กด Enter → ผลลัพธ์ filter ตามคำค้นหา
- [ ] ลบคำค้นหา + กดค้นหา → แสดง Note ทั้งหมด
- [ ] เห็นจำนวนรายการด้านล่าง

---

### ขั้นตอนที่ 9: ทดสอบฟังก์ชันค้นหา

**ทดสอบที่ 1 — ค้นหาคำที่มี:**
1. สร้าง Note 2-3 รายการ (ถ้ายังไม่มี):
   - "ซื้อของ" / "ไข่ นม ขนมปัง"
   - "การบ้าน" / "ทำแบบฝึกหัด"
   - "ประชุม" / "ประชุมทีมบ่าย 2 โมง"
2. พิมพ์ `ซื้อ` ในช่องค้นหา → กด Enter
3. ควรเห็นเฉพาะ Note "ซื้อของ"
4. แสดง "แสดง 1 รายการ"

**ทดสอบที่ 2 — ค้นหาคำที่ไม่มี:**
1. พิมพ์ `xyz` ในช่องค้นหา → กด Enter
2. ควรเห็น: 🔍 ไม่พบ Note ที่มีคำว่า "xyz"

**ทดสอบที่ 3 — ล้างคำค้นหา:**
1. ลบคำในช่องค้นหาให้ว่าง
2. กดปุ่ม 🔍 ค้นหา
3. ควรเห็น Note ทั้งหมดกลับมา

**ทดสอบที่ 4 — เปิด DevTools Network:**
1. เปิด DevTools (F12) → แท็บ Network
2. พิมพ์ `ซื้อ` แล้วกด Enter
3. จะเห็น request `notes/?search=ซื้อ` ในรายการ
4. ลบคำค้นหาแล้วกด Enter → เห็น request `notes/` (ไม่มี query parameter)

> 💡 **เปิด DevTools Network** เพื่อดูว่า Vue.js ส่ง request อะไรไป Backend จริง!

#### ✅ ตรวจสอบ
- [ ] ค้นหาคำที่มี → เห็นเฉพาะ Note ที่ตรง
- [ ] ค้นหาคำที่ไม่มี → เห็นข้อความ "ไม่พบ"
- [ ] ล้างคำค้นหา → เห็น Note ทั้งหมด
- [ ] DevTools Network → เห็น request ที่มี `?search=` ตามที่พิมพ์

---

## ส่วนที่ 4: ปรับปรุง UX

### ขั้นตอนที่ 10: แสดงวันที่อัปเดตล่าสุด

ข้อมูลจาก API มี `updated_at` เป็นรูปแบบ ISO 8601 เช่น `2025-01-15T10:30:00Z`

เราจะแสดงวันที่ในรูปแบบที่อ่านง่ายโดยใช้ **method** แปลงวันที่:

เพิ่ม method `formatDate` ใน `<script>` (ใน `methods:`):

```js
methods: {
  async fetchNotes() {
    // ... โค้ดเดิม ...
  },

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
}
```

เพิ่มคอลัมน์ "อัปเดตล่าสุด" ในตาราง:

ใน `<thead>` เพิ่มก่อน `<th>จัดการ</th>`:

```html
<th>อัปเดต</th>
```

ใน `<tbody>` เพิ่มก่อน `<td>` ของปุ่มจัดการ:

```html
<td>{{ formatDate(note.updated_at) }}</td>
```

> 💡 **อธิบาย:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `new Date(dateString)` | แปลง string เป็น Date object |
> | `toLocaleDateString('th-TH', {...})` | แสดงวันที่ในรูปแบบไทย |
> | `year: 'numeric'` | แสดงปี เช่น "2568" |
> | `month: 'short'` | แสดงเดือนย่อ เช่น "ม.ค." |
> | `day: 'numeric'` | แสดงวัน เช่น "15" |
> | `hour: '2-digit', minute: '2-digit'` | แสดงเวลา เช่น "10:30" |
>
> ตัวอย่างผลลัพธ์: `15 ม.ค. 2568 10:30`

#### ✅ ตรวจสอบ
- [ ] เพิ่มคอลัมน์ "อัปเดต" ในตาราง
- [ ] เห็นวันที่ในรูปแบบไทยที่อ่านง่าย
- [ ] ลองสร้าง Note ใหม่ → วันที่อัปเดตใหม่

---

## สรุปโค้ดทั้งหมดในบทนี้

ไฟล์เดียวที่แก้ไขในบทนี้:

**`src/views/NoteList.vue`** (เวอร์ชันสมบูรณ์):

```vue
<script>
export default {
  data() {
    return {
      notes: [],
      loading: false,
      error: '',
      search: ''
    }
  },

  async mounted() {
    await this.fetchNotes()
  },

  methods: {
    async fetchNotes() {
      this.loading = true
      this.error = ''

      try {
        let url = 'http://localhost:8000/api/notes/'

        if (this.search) {
          url = url + '?search=' + this.search
        }

        const response = await fetch(url)
        const data = await response.json()
        this.notes = data
      } catch (err) {
        this.error = 'ไม่สามารถดึงข้อมูลได้ — ตรวจสอบว่า Backend ทำงานอยู่'
      } finally {
        this.loading = false
      }
    },

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
  }
}
</script>

<template>
  <div>
    <h1>📋 รายการ Note ทั้งหมด</h1>

    <div style="margin-bottom: 16px;">
      <router-link to="/notes/create">➕ สร้าง Note ใหม่</router-link>
    </div>

    <!-- ช่องค้นหา -->
    <div style="margin-bottom: 16px;">
      <input
        v-model="search"
        type="text"
        placeholder="🔍 ค้นหาหัวข้อ..."
        @keyup.enter="fetchNotes()"
      />
      <button @click="fetchNotes()">🔍 ค้นหา</button>
    </div>

    <!-- Loading -->
    <p v-if="loading">⏳ กำลังโหลด...</p>

    <!-- Error -->
    <p v-else-if="error" style="color: red;">❌ {{ error }}</p>

    <!-- Empty state (ค้นหาแล้วไม่เจอ) -->
    <p v-else-if="notes.length === 0 && search">
      🔍 ไม่พบ Note ที่มีคำว่า "{{ search }}"
    </p>

    <!-- Empty state (ไม่มี Note เลย) -->
    <p v-else-if="notes.length === 0">📭 ยังไม่มี Note — ลองสร้าง Note ใหม่!</p>

    <!-- ตาราง Note -->
    <table v-else border="1" cellpadding="8" style="margin-top: 16px; width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>#</th>
          <th>หัวข้อ</th>
          <th>เนื้อหา</th>
          <th>สถานะ</th>
          <th>อัปเดต</th>
          <th>จัดการ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="note in notes" :key="note.id">
          <td>{{ note.id }}</td>
          <td>{{ note.title }}</td>
          <td>{{ note.body }}</td>
          <td>{{ note.is_done ? '✅' : '⬜' }}</td>
          <td>{{ formatDate(note.updated_at) }}</td>
          <td>
            <router-link :to="'/notes/' + note.id + '/edit'">✏️ แก้ไข</router-link>
            |
            <router-link :to="'/notes/' + note.id + '/delete'">🗑️ ลบ</router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- จำนวนรายการ -->
    <p v-if="!loading && !error" style="color: gray; margin-top: 8px;">
      แสดง {{ notes.length }} รายการ
    </p>
  </div>
</template>
```

---

## ❌ ปัญหาที่พบบ่อย

### ปัญหา: เปิดหน้าแล้วตารางว่าง แม้ Backend ทำงานอยู่

**สาเหตุ:** อาจลืมใส่ `async` หน้า `mounted()` หรือลืม `await` หน้า `this.fetchNotes()`

**วิธีแก้:**
```js
// ❌ ผิด — ไม่รอ fetchNotes เสร็จ
mounted() {
  this.fetchNotes()
}

// ✅ ถูก — รอ fetchNotes เสร็จ
async mounted() {
  await this.fetchNotes()
}
```

> จริงๆ ในกรณีนี้ แม้ไม่มี `async/await` ก็ยังทำงานได้ เพราะ Vue จะ re-render ตามค่าที่เปลี่ยน
> แต่ใส่ `async/await` เป็นนิสัยดี เพราะช่วยให้โค้ดเข้าใจง่ายและจัดการ error ได้ถูกต้อง

---

### ปัญหา: ค้นหาแล้ว URL ไม่เปลี่ยน ทำให้ไม่สามารถแชร์ลิงก์ค้นหา

**สาเหตุ:** เรายังไม่ได้ sync คำค้นหากับ URL

**คำอธิบาย:** ในเวอร์ชันนี้ คำค้นหาเก็บแค่ใน `data()` — ถ้า refresh หน้า คำค้นหาจะหายไป

นี่เป็นพฤติกรรมปกติสำหรับตอนนี้ — ในบทขั้นสูงจะเรียนเรื่องการ sync state กับ URL (Query Parameters)

---

### ปัญหา: เห็นข้อมูลเดิมทุกครั้ง ไม่ update ตามที่สร้างใหม่

**สาเหตุ:** อาจเป็นเพราะ browser cache

**วิธีแก้:**
1. เปิด DevTools (F12) → แท็บ Network
2. ติ๊ก ☑️ **Disable cache**
3. Refresh หน้าอีกครั้ง

---

### ปัญหา: ค้นหาแล้วได้ผลลัพธ์ถูกต้อง แต่ล้างค้นหาแล้ว Note ยังไม่ครบ

**สาเหตุ:** อาจลืมลบคำในช่องค้นหาก่อนกดค้นหา

**วิธีแก้:** ตรวจสอบว่า:
1. ลบคำในช่องค้นหาจนว่างเปล่า
2. กดปุ่ม 🔍 ค้นหา หรือกด Enter
3. ดูใน DevTools Network ว่า URL เป็น `/api/notes/` (ไม่มี `?search=`)

---

### ปัญหา: วันที่แสดงเป็นภาษาอังกฤษ ไม่ใช่ภาษาไทย

**สาเหตุ:** เบราว์เซอร์อาจไม่รองรับ locale `th-TH`

**วิธีแก้:** เปลี่ยนเป็น `en-US` หรือตรวจว่าเบราว์เซอร์รองรับ:
```js
// ถ้าไม่รองรับ th-TH
return date.toLocaleDateString('en-US', { ... })

// หรือใช้รูปแบบกว้างๆ
return date.toLocaleString()
```

---

## 🏋️ ลองทำเอง (Challenge)

### ⭐ ระดับง่าย
เพิ่ม **ปุ่ม Refresh** ถัดจากปุ่มค้นหา เพื่อดึงข้อมูลใหม่โดยไม่ต้อง reload หน้า:
- เพิ่ม `<button @click="fetchNotes()">🔄 Refresh</button>`
- ทดสอบ: สร้าง Note ด้วย Postman → กด Refresh → เห็น Note ใหม่

### ⭐⭐ ระดับปานกลาง
เพิ่ม **ตัวนับจำนวน Note แยกตามสถานะ:**
- แสดง "✅ เสร็จแล้ว: X | ⬜ ยังไม่เสร็จ: Y"
- ใช้ `computed` property:
  ```js
  computed: {
    doneCount() {
      return this.notes.filter(note => note.is_done).length
    },
    pendingCount() {
      return this.notes.filter(note => !note.is_done).length
    }
  }
  ```

### ⭐⭐⭐ ระดับยาก
ทำให้ **ค้นหาแบบ real-time** — พิมพ์แล้วค้นหาอัตโนมัติ (ไม่ต้องกด Enter):
- ใช้ **watch** เพื่อดูค่า `search`:
  ```js
  watch: {
    search() {
      this.fetchNotes()
    }
  }
  ```
- ปัญหา: ถ้าพิมพ์เร็วๆ จะส่ง request ทุกตัวอักษร! ลองหาวิธี **debounce** (ชะลอ) ให้ส่ง request เมื่อหยุดพิมพ์แล้ว 300ms
- คำใบ้: ใช้ `setTimeout` + `clearTimeout`

<details>
<summary>💡 คำใบ้ระดับง่าย</summary>

เพิ่มในส่วน template ถัดจากปุ่มค้นหา:
```html
<button @click="fetchNotes()">🔄 Refresh</button>
```

ปุ่มนี้เรียก `fetchNotes()` เดิม — ดึงข้อมูลจาก API อีกครั้ง

</details>

<details>
<summary>💡 คำใบ้ระดับปานกลาง</summary>

`computed` คือตัวแปรที่ **คำนวณอัตโนมัติ** เมื่อข้อมูลที่ใช้เปลี่ยน:

```js
export default {
  data() { ... },
  computed: {
    doneCount() {
      return this.notes.filter(note => note.is_done).length
    },
    pendingCount() {
      return this.notes.filter(note => !note.is_done).length
    }
  },
  methods: { ... }
}
```

ใน template:
```html
<p>✅ เสร็จแล้ว: {{ doneCount }} | ⬜ ยังไม่เสร็จ: {{ pendingCount }}</p>
```

`filter()` กรอง array เหลือเฉพาะรายการที่ตรงเงื่อนไข แล้ว `.length` นับจำนวน

</details>

<details>
<summary>💡 คำใบ้ระดับยาก</summary>

Debounce คือ "ชะลอ" — รอจนหยุดพิมพ์ก่อนค่อยส่ง request:

```js
data() {
  return {
    // ...
    searchTimeout: null
  }
},

watch: {
  search() {
    // ยกเลิก timeout เก่า (ถ้ามี)
    clearTimeout(this.searchTimeout)

    // ตั้ง timeout ใหม่ — รอ 300ms
    this.searchTimeout = setTimeout(() => {
      this.fetchNotes()
    }, 300)
  }
}
```

**วิธีทำงาน:**
- พิมพ์ตัวอักษรแรก → ตั้ง timer 300ms
- พิมพ์ตัวถัดไป (ภายใน 300ms) → ยกเลิก timer เก่า + ตั้ง timer ใหม่
- หยุดพิมพ์ 300ms → timer หมด → เรียก `fetchNotes()`

ผลลัพธ์: ส่ง request แค่ครั้งเดียวเมื่อหยุดพิมพ์ แทนที่จะส่งทุกตัวอักษร!

</details>

---

## 📖 คำศัพท์ที่เรียนรู้ในบทนี้

| คำศัพท์ | ความหมาย | เปรียบเทียบ |
|---------|----------|-------------|
| mounted() | Lifecycle Hook — ทำงานเมื่อ component แสดงบนหน้าจอ | เหมือนร้านอาหารเปิดประตู — ถึงเวลาเริ่มรับลูกค้า |
| Lifecycle Hook | ฟังก์ชันที่ Vue เรียกอัตโนมัติตามช่วงเวลา | เหมือนนาฬิกาปลุก — ดังอัตโนมัติตามเวลาที่ตั้ง |
| v-if / v-else | แสดง/ซ่อน element ตามเงื่อนไข | เหมือนสวิตช์ไฟ — เปิดเมื่อเงื่อนไขเป็นจริง |
| Loading State | สถานะแสดงว่ากำลังโหลดข้อมูล | เหมือนป้าย "กรุณารอสักครู่" ที่ธนาคาร |
| Empty State | สถานะแสดงว่าไม่มีข้อมูล | เหมือนป้าย "ชั้นว่าง" ในตู้เย็น |
| Query Parameter | ข้อมูลเพิ่มเติมที่ส่งผ่าน URL หลังเครื่องหมาย `?` | เหมือนโน้ตเพิ่มเติมในใบสั่งอาหาร — "ไม่ใส่ผัก" |
| @keyup.enter | Event Modifier — จับเหตุการณ์เฉพาะปุ่ม Enter | เหมือนกริ่งที่ดังเฉพาะเมื่อมีคนกดปุ่มนั้น |
| toLocaleDateString() | แสดงวันที่ตาม locale ของภาษาที่กำหนด | เหมือนแปลปฏิทินเป็นภาษาท้องถิ่น |

---

## สรุปสิ่งที่ได้เรียนรู้ ✅

| หัวข้อ | สิ่งที่เรียนรู้ |
|--------|----------------|
| mounted() | Lifecycle Hook ที่ทำงานเมื่อ component แสดงแล้ว — เหมาะสำหรับดึงข้อมูล |
| fetch GET | ส่ง GET request ดึงข้อมูลจาก API — ไม่ต้องระบุ `method` เพราะเป็นค่าเริ่มต้น |
| v-if / v-else-if / v-else | แสดง content ต่างกันตามสถานะ: loading / error / empty / data |
| Search | ส่งคำค้นหาไป Backend ผ่าน query parameter `?search=` |
| @keyup.enter | จับ event เฉพาะปุ่ม Enter |
| formatDate | แปลงวันที่ ISO 8601 เป็นรูปแบบที่อ่านง่ายด้วย `toLocaleDateString()` |
| UX States | แอปที่ดีต้องจัดการทุกสถานะ: loading, error, empty, data |

---

> ➡️ **บทถัดไป:** [บทที่ 8: แก้ไข Note (Update)](./lesson-8-edit-note.md)
