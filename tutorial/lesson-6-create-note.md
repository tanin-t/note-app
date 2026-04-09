# บทที่ 6: สร้าง Note — เชื่อมต่อ Frontend กับ Backend

> 📍 **บทที่ 6 / 10** ━━━━━━━━━━ `[██████░░░░]`

| ⬅️ [บทที่ 5: Postman](./lesson-5-postman.md) | [สารบัญ](./tutorial.md) | [บทที่ 7: แสดงรายการ Note ➡️](./lesson-7-list-note.md) |
|:---|:---:|---:|

---

## 🎯 เป้าหมาย

ในบทนี้เราจะ:
- เข้าใจวิธี **ส่ง HTTP request จาก JavaScript** ด้วย `fetch()`
- เรียนรู้ **async/await** สำหรับจัดการงานที่ต้องรอ (เช่น รอ API ตอบกลับ)
- เชื่อมต่อ **ฟอร์มสร้าง Note** (จากบทที่ 4) กับ **API จริง** (จากบทที่ 5)
- จัดการ **error จาก API** แล้วแสดงให้ผู้ใช้เห็น
- เพิ่ม **loading state** ให้ผู้ใช้รู้ว่ากำลังบันทึก

> 🎮 **Fun Fact:** ในบทที่ 5 เราใช้ Postman เป็น "รีโมท" กดส่ง request เอง
> ในบทนี้เราจะเขียนโค้ดให้ **Vue.js เป็นรีโมทแทนเรา** — กดปุ่มบนหน้าเว็บ แล้วส่ง request ไป Backend อัตโนมัติ! 🤖

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

- ทำบทที่ 4 และ 5 เสร็จแล้ว
- มี **2 Terminal** ทำงาน:
  1. Terminal 1: `npm run dev` (Vue.js — port 5173)
  2. Terminal 2: `uv run python manage.py runserver` (Django — port 8000)
- เข้าใจ API สร้าง Note: `POST /api/notes/create/` (ทดสอบใน Postman แล้ว)

> 💡 **ถ้ายังไม่ได้ทำบทก่อนหน้า** สามารถเริ่มจาก branch สำเร็จได้:
> ```bash
> git checkout lesson-5-completed
> ```

---

## 🧠 ทำความเข้าใจก่อนเริ่ม

### Postman vs JavaScript

ในบทที่ 5 เราใช้ **Postman** ส่ง request ไป Backend:

```
Postman  ───→  POST /api/notes/create/  ───→  Backend (Django)
         ←───  { "id": 1, "title": "..." }  ←───
```

ในบทนี้เราจะเปลี่ยนมาใช้ **JavaScript (fetch)** ส่ง request แทน:

```
Vue.js (fetch)  ───→  POST /api/notes/create/  ───→  Backend (Django)
                ←───  { "id": 1, "title": "..." }  ←───
```

> 💡 **เปรียบเทียบ:**
>
> | Postman | JavaScript (fetch) |
> |---------|-------------------|
> | เราเป็นคนกด Send | โค้ดส่ง request อัตโนมัติ |
> | เราเลือก Method + URL | โค้ดกำหนด Method + URL |
> | เราพิมพ์ JSON ใน Body | โค้ดสร้าง JSON จากข้อมูลในฟอร์ม |
> | เราอ่านผลลัพธ์เอง | โค้ดจัดการผลลัพธ์แทน |

---

### fetch() คืออะไร?

`fetch()` คือ **ฟังก์ชันของ JavaScript** ที่ส่ง HTTP request ได้ — เหมือน Postman แต่เขียนเป็นโค้ด:

```js
// ตัวอย่าง fetch
const response = await fetch('http://localhost:8000/api/notes/create/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'ซื้อของ', body: 'ไข่ นม ขนมปัง' })
})
```

> 💡 **เทียบกับ Postman:**
>
> | Postman | fetch() |
> |---------|---------|
> | เลือก Method: POST | `method: 'POST'` |
> | เลือก Body → raw → JSON | `headers: { 'Content-Type': 'application/json' }` |
> | พิมพ์ JSON: `{"title":"..."}` | `body: JSON.stringify({title: '...'})` |
> | กด Send | เรียก `fetch()` |
> | ดูผลลัพธ์ด้านล่าง | `const data = await response.json()` |

---

### async/await คืออะไร?

เมื่อส่ง request ไป Backend ต้อง **รอ** Backend ตอบกลับ — อาจใช้เวลาไม่กี่มิลลิวินาที หรือนานหลายวินาที

`async/await` คือวิธีบอก JavaScript ว่า **"รอตรงนี้ก่อน แล้วค่อยทำต่อ"**

```js
// ❌ ไม่มี await — ไม่รอ Backend ตอบ (ได้ Promise แทนข้อมูลจริง)
const response = fetch('http://localhost:8000/api/notes/')

// ✅ มี await — รอ Backend ตอบก่อน แล้วจึงเก็บผลลัพธ์
const response = await fetch('http://localhost:8000/api/notes/')
```

> 💡 **เปรียบเทียบ:**
>
> | ไม่มี await | มี await |
> |-------------|----------|
> | สั่งอาหารแล้ว**เดินออกจากร้านเลย** | สั่งอาหารแล้ว**รอรับอาหาร**ก่อน |
> | ไม่ได้อาหาร! 😱 | ได้อาหารมากิน 🍜 |

**กฎสำคัญ:** ฟังก์ชันที่ใช้ `await` ข้างใน ต้องมี `async` ข้างหน้า:

```js
// ❌ ผิด — ใช้ await ใน function ปกติไม่ได้
methods: {
  submitForm() {
    const response = await fetch(...)   // Error!
  }
}

// ✅ ถูก — ต้องใส่ async ข้างหน้า
methods: {
  async submitForm() {
    const response = await fetch(...)   // OK!
  }
}
```

---

## 📝 ขั้นตอน

---

## ส่วนที่ 1: ส่ง request สร้าง Note

### ขั้นตอนที่ 1: แก้ไข NoteCreate.vue — เชื่อมต่อ API จริง

เปิดไฟล์ `src/views/NoteCreate.vue` แล้ว**แก้ไขเป็นโค้ดนี้ทั้งหมด:**

```vue
<script>
export default {
  data() {
    return {
      title: '',
      body: ''
    }
  },

  methods: {
    async submitForm() {
      const response = await fetch('http://localhost:8000/api/notes/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: this.title,
          body: this.body
        })
      })

      if (response.ok) {
        alert('สร้าง Note สำเร็จ!')
        this.$router.push('/notes')
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>➕ สร้าง Note ใหม่</h1>

    <form @submit.prevent="submitForm">
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
      <button type="submit">💾 บันทึก</button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

> 💡 **สิ่งที่เปลี่ยนจากบทที่ 4:**
>
> | ก่อน (บทที่ 4) | หลัง (บทที่ 6) |
> |----------------|----------------|
> | `submitForm()` — function ธรรมดา | `async submitForm()` — ใส่ `async` |
> | `console.log(...)` + `alert(...)` | ใช้ `fetch()` ส่ง request จริง |
> | ไม่ได้คุยกับ Backend | ส่งข้อมูลไป Backend จริง! |
>
> **อธิบายโค้ดทีละบรรทัด:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `async submitForm()` | ใส่ `async` เพราะข้างในใช้ `await` |
> | `fetch('...url...', { ... })` | ส่ง HTTP request ไป Backend |
> | `method: 'POST'` | กำหนดวิธี = สร้างข้อมูลใหม่ |
> | `headers: { 'Content-Type': 'application/json' }` | บอก Backend ว่าส่ง JSON มา |
> | `body: JSON.stringify({ ... })` | แปลงข้อมูลเป็น JSON string แล้วส่งไป |
> | `this.title`, `this.body` | ค่าจาก input ที่ผู้ใช้กรอก (ผ่าน v-model) |
> | `response.ok` | ตรวจว่า Backend ตอบ status 200-299 (สำเร็จ) |
> | `this.$router.push('/notes')` | redirect ไปหน้ารายการ |

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteCreate.vue` ตามโค้ดด้านบน
- [ ] เข้าใจว่า `async` + `await` ทำหน้าที่อะไร
- [ ] เข้าใจว่า `fetch()` เหมือน Postman แต่เขียนเป็นโค้ด

---

### ขั้นตอนที่ 2: ทดสอบสร้าง Note ผ่านหน้าเว็บ

**ก่อนทดสอบ ตรวจสอบว่า:**
- Terminal 1: Vue.js ทำงานอยู่ (`npm run dev`)
- Terminal 2: Django ทำงานอยู่ (`uv run python manage.py runserver`)

**ทดสอบ:**
1. เปิด `http://localhost:5173/notes/create`
2. กรอก:
   - หัวข้อ: `ซื้อของ`
   - เนื้อหา: `ไข่ นม ขนมปัง`
3. กดปุ่ม **💾 บันทึก**
4. ควรเห็น `alert('สร้าง Note สำเร็จ!')` แล้ว redirect ไปหน้า `/notes`

**ตรวจสอบว่าสร้างจริง:**

เปิด Postman แล้ว **GET** `http://localhost:8000/api/notes/` — ควรเห็นโน้ตที่เพิ่งสร้าง!

> 💡 เรากำลังใช้ **2 เครื่องมือ** ไปในทิศทางเดียวกัน:
> - **หน้าเว็บ** = ส่ง request สร้าง Note
> - **Postman** = ตรวจสอบว่าข้อมูลถูกสร้างจริง

#### ✅ ตรวจสอบ
- [ ] กรอกฟอร์มแล้วกด บันทึก → เห็น alert "สร้างสำเร็จ"
- [ ] redirect ไปหน้า `/notes`
- [ ] เปิด Postman GET `/api/notes/` → เห็นโน้ตที่เพิ่งสร้าง

---

## ส่วนที่ 2: จัดการ Error

### ขั้นตอนที่ 3: ลองส่งข้อมูลผิด — ดูว่าเกิดอะไร

ลองกลับไปหน้าสร้าง Note แล้ว**กดบันทึกโดยไม่กรอกหัวข้อ:**

1. เปิด `http://localhost:5173/notes/create`
2. ปล่อยช่อง "หัวข้อ" ว่าง
3. พิมพ์เนื้อหาอะไรก็ได้
4. กด **💾 บันทึก**

**ผลลัพธ์:** ไม่เกิดอะไรเลย! 😱 ไม่มี alert ไม่มี redirect ไม่มี error

> 🤔 **ทำไม?**
>
> เพราะ Backend ตอบ Status `400 Bad Request` (ข้อมูลไม่ถูกต้อง)
> แต่โค้ดเราตรวจแค่ `if (response.ok)` — ถ้าไม่ ok ก็**ไม่ทำอะไรเลย**
>
> จำได้ไหม? ตอนทดสอบใน Postman บทที่ 5 เราเห็น error:
> ```json
> { "title": ["This field is required."] }
> ```
> แต่ตอนนี้ Vue.js ยังไม่ได้อ่าน error นี้ออกมาแสดง!

#### ✅ ตรวจสอบ
- [ ] ลองส่งฟอร์มว่าง → ไม่เกิดอะไร (ยังไม่มี error handling)
- [ ] เข้าใจว่าทำไมต้องเพิ่ม error handling

---

### ขั้นตอนที่ 4: เพิ่ม Error Handling

แก้ไข `src/views/NoteCreate.vue` — เพิ่มการจัดการ error:

```vue
<script>
export default {
  data() {
    return {
      title: '',
      body: '',
      errors: {}
    }
  },

  methods: {
    async submitForm() {
      // เคลียร์ error เก่าก่อน
      this.errors = {}

      const response = await fetch('http://localhost:8000/api/notes/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: this.title,
          body: this.body
        })
      })

      if (response.ok) {
        alert('สร้าง Note สำเร็จ!')
        this.$router.push('/notes')
      } else {
        // อ่าน error จาก Backend
        const data = await response.json()
        this.errors = data
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>➕ สร้าง Note ใหม่</h1>

    <form @submit.prevent="submitForm">
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
      <button type="submit">💾 บันทึก</button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

> 💡 **สิ่งที่เพิ่ม:**
>
> | โค้ดที่เพิ่ม | ทำอะไร |
> |-------------|--------|
> | `errors: {}` | ตัวแปรเก็บ error จาก Backend |
> | `this.errors = {}` | เคลียร์ error เก่าทุกครั้งที่กด submit |
> | `await response.json()` | อ่านข้อมูล JSON จาก response (error message) |
> | `this.errors = data` | เก็บ error ไว้แสดง |
> | `v-if="errors.title"` | แสดง error เฉพาะเมื่อมี |
> | `errors.title[0]` | แสดง error message แรกของ field `title` |
>
> 🤔 **ทำไมเป็น `errors.title[0]`?**
>
> เพราะ Backend ส่ง error มาในรูปแบบ **array** (อาจมีหลาย error ต่อ 1 field):
> ```json
> {
>   "title": ["This field is required."],
>   "body": ["This field may not be blank."]
> }
> ```
> เราเอาแค่ `[0]` (ตัวแรก) มาแสดง

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteCreate.vue` เพิ่ม error handling
- [ ] ลองกด บันทึก โดยไม่กรอกหัวข้อ → เห็นข้อความ error สีแดง
- [ ] กรอกหัวข้อแล้วกด บันทึก อีกครั้ง → error หาย + สร้างสำเร็จ

---

### ขั้นตอนที่ 5: ทดสอบ Error ต่างๆ

ลองทดสอบ error หลายแบบเพื่อดูว่าระบบจัดการได้ถูกต้อง:

**ทดสอบที่ 1 — ส่งหัวข้อว่าง:**
1. ปล่อยช่อง "หัวข้อ" ว่าง
2. กด บันทึก
3. ควรเห็น: `This field is required.` (หรือ `This field may not be blank.`) ใต้ช่องหัวข้อ

**ทดสอบที่ 2 — กรอกข้อมูลถูกต้อง:**
1. กรอกหัวข้อ: `ทดสอบ Error`
2. กรอกเนื้อหา: `ข้อมูลทดสอบ`
3. กด บันทึก
4. ควร: alert สำเร็จ → redirect ไป `/notes`

**ทดสอบที่ 3 — กรอกแค่หัวข้อ (ไม่ใส่เนื้อหา):**
1. กรอกหัวข้อ: `ทดสอบไม่ใส่เนื้อหา`
2. ปล่อยเนื้อหาว่าง
3. กด บันทึก
4. ควร: สร้างสำเร็จ! (เพราะ `body` ไม่บังคับ — default เป็น `""`)

#### ✅ ตรวจสอบ
- [ ] ส่งหัวข้อว่าง → เห็น error สีแดง
- [ ] กรอกครบแล้วส่ง → สำเร็จ
- [ ] ส่งแค่หัวข้อ (ไม่ใส่เนื้อหา) → สำเร็จ (เพราะ body ไม่บังคับ)

---

## ส่วนที่ 3: เพิ่ม Loading State

### ขั้นตอนที่ 6: ปัญหา — กดปุ่มซ้ำ

ลองจินตนาการ: ถ้า Backend ตอบช้า (เช่น internet ช้า) แล้วผู้ใช้**กดปุ่ม บันทึก หลายครั้ง** จะเกิดอะไร?

```
กดครั้งที่ 1 → POST /api/notes/create/ → สร้างโน้ตที่ 1
กดครั้งที่ 2 → POST /api/notes/create/ → สร้างโน้ตที่ 2 (ซ้ำ!)
กดครั้งที่ 3 → POST /api/notes/create/ → สร้างโน้ตที่ 3 (ซ้ำ!!)
```

วิธีแก้: เพิ่ม **loading state** — เมื่อกำลังส่ง request อยู่ ให้:
1. **ปิดปุ่ม** ไม่ให้กดซ้ำ
2. **แสดงสถานะ** ให้ผู้ใช้รู้ว่ากำลังทำงาน

---

### ขั้นตอนที่ 7: เพิ่ม Loading State + ปรับปรุงโค้ดทั้งหมด

แก้ไข `src/views/NoteCreate.vue` เป็น**เวอร์ชันสมบูรณ์:**

```vue
<script>
export default {
  data() {
    return {
      title: '',
      body: '',
      errors: {},
      loading: false
    }
  },

  methods: {
    async submitForm() {
      this.errors = {}
      this.loading = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/create/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.title,
            body: this.body
          })
        })

        if (response.ok) {
          this.$router.push('/notes')
        } else {
          const data = await response.json()
          this.errors = data
        }
      } catch (error) {
        alert('ไม่สามารถเชื่อมต่อ Backend ได้ — ตรวจสอบว่า Django server ทำงานอยู่')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>➕ สร้าง Note ใหม่</h1>

    <form @submit.prevent="submitForm">
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
      <button type="submit" :disabled="loading">
        {{ loading ? '⏳ กำลังบันทึก...' : '💾 บันทึก' }}
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
> | `loading: false` | ตัวแปรบอกว่ากำลังส่ง request อยู่หรือไม่ |
> | `this.loading = true` | เริ่มส่ง → เปลี่ยนสถานะเป็น loading |
> | `try { ... }` | ครอบโค้ดที่อาจเกิด error |
> | `catch (error) { ... }` | จับ error เมื่อ**เชื่อมต่อไม่ได้** (เช่น Backend ปิดอยู่) |
> | `finally { ... }` | ทำเสมอไม่ว่าสำเร็จหรือ error — ปิด loading |
> | `:disabled="loading"` | ปิดปุ่มเมื่อ `loading = true` |
> | `{{ loading ? '⏳...' : '💾...' }}` | เปลี่ยนข้อความปุ่มตาม loading |
>
> 🤔 **try / catch / finally คืออะไร?**
>
> ```
> try {
>   // ลองทำตรงนี้
>   // ถ้าสำเร็จ → ทำต่อปกติ
> } catch (error) {
>   // ถ้าเกิด error → ทำตรงนี้แทน
> } finally {
>   // ทำเสมอ ไม่ว่าสำเร็จหรือ error
> }
> ```
>
> | ส่วน | ทำเมื่อไหร่ | ตัวอย่าง |
> |------|------------|---------|
> | `try` | ลองทำ | ส่ง fetch request |
> | `catch` | เฉพาะเมื่อ error | Backend ปิด → แจ้งผู้ใช้ |
> | `finally` | ทุกครั้ง | ปิด loading ไม่ว่าจะยังไง |
>
> เปรียบเทียบ:
> - `try` = ลองยกของหนัก
> - `catch` = ถ้ายกไม่ไหว → วางลงแล้วบอกคนช่วย
> - `finally` = ไม่ว่ายกได้หรือไม่ → ล้างมือ

#### ✅ ตรวจสอบ
- [ ] แก้ไข `NoteCreate.vue` เป็นเวอร์ชันสมบูรณ์
- [ ] กดบันทึก → เห็นปุ่มเปลี่ยนเป็น "⏳ กำลังบันทึก..." แล้วกลับเป็น "💾 บันทึก"
- [ ] ลองปิด Django server แล้วกดบันทึก → เห็น alert บอกว่าเชื่อมต่อไม่ได้

---

### ขั้นตอนที่ 8: ทดสอบ Loading State

**ทดสอบที่ 1 — กดบันทึกปกติ:**
1. กรอกข้อมูลครบ
2. กดบันทึก
3. สังเกตว่าปุ่มเปลี่ยนเป็น "⏳ กำลังบันทึก..." สักครู่ แล้ว redirect

**ทดสอบที่ 2 — จำลอง Backend ปิด:**
1. ปิด Django server (กด `Ctrl+C` ใน Terminal 2)
2. ลองกดบันทึก
3. ควรเห็น alert: "ไม่สามารถเชื่อมต่อ Backend ได้..."
4. ปุ่มกลับเป็น "💾 บันทึก" (พร้อมให้กดอีกครั้ง)
5. **อย่าลืมเปิด Django server กลับ!** `uv run python manage.py runserver`

**ทดสอบที่ 3 — เปิด DevTools ดู Network:**
1. เปิด DevTools (กด `F12`) → แท็บ **Network**
2. กรอกข้อมูลแล้วกดบันทึก
3. จะเห็น request `create/` ในรายการ:
   - Method: `POST`
   - Status: `201` (Created)
   - Response: JSON ของโน้ตที่สร้าง

> 💡 **DevTools Network** คือ "Postman ที่อยู่ในเบราว์เซอร์" — เห็น request/response ที่ Vue.js ส่งจริง!

#### ✅ ตรวจสอบ
- [ ] กดบันทึก → ปุ่มเปลี่ยนเป็น loading แล้วกลับมา
- [ ] ปิด Backend → กดบันทึก → เห็น alert error + ปุ่มกลับเป็นปกติ
- [ ] เปิด DevTools Network → เห็น POST request + response

---

## ส่วนที่ 4: ทำความเข้าใจ CORS

### ขั้นตอนที่ 9: CORS คืออะไร? (ทำไมถึงเรียก API ได้)

คุณอาจสงสัยว่า ทำไม Vue.js (port 5173) ถึงส่ง request ไป Django (port 8000) ได้โดยไม่มีปัญหา?

คำตอบคือ Backend เราตั้งค่า **CORS** ไว้แล้ว!

> 💡 **CORS (Cross-Origin Resource Sharing) คืออะไร?**
>
> ปกติเบราว์เซอร์จะ **บล็อก** ไม่ให้หน้าเว็บส่ง request ไป domain/port อื่น เพื่อความปลอดภัย:
>
> ```
> ❌ http://localhost:5173  →  http://localhost:8000    (ต่าง port = ต่าง origin)
> ✅ http://localhost:5173  →  http://localhost:5173    (port เดียวกัน = OK)
> ```
>
> **CORS** คือกลไกที่ให้ Backend **อนุญาต** Frontend จาก origin อื่นเรียก API ได้
>
> เปรียบเทียบ:
> - เบราว์เซอร์ = ยาม (security guard) 🛡️
> - CORS = ใบอนุญาต — Backend ออกให้ว่า "ปล่อยคนจาก port 5173 เข้ามาได้"
>
> ใน Django เราตั้งค่าไว้ใน `settings.py`:
> ```python
> CORS_ALLOW_ALL_ORIGINS = True   # อนุญาตทุก origin (สำหรับพัฒนา)
> ```

#### ✅ ตรวจสอบ
- [ ] เข้าใจว่า CORS คือการอนุญาตให้ Frontend เรียก API จากต่าง origin
- [ ] เข้าใจว่า Backend ตั้งค่า `CORS_ALLOW_ALL_ORIGINS = True` ไว้แล้ว

---

## สรุปโค้ดทั้งหมดในบทนี้

ไฟล์เดียวที่แก้ไขในบทนี้:

**`src/views/NoteCreate.vue`** (เวอร์ชันสมบูรณ์):

```vue
<script>
export default {
  data() {
    return {
      title: '',
      body: '',
      errors: {},
      loading: false
    }
  },

  methods: {
    async submitForm() {
      this.errors = {}
      this.loading = true

      try {
        const response = await fetch('http://localhost:8000/api/notes/create/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.title,
            body: this.body
          })
        })

        if (response.ok) {
          this.$router.push('/notes')
        } else {
          const data = await response.json()
          this.errors = data
        }
      } catch (error) {
        alert('ไม่สามารถเชื่อมต่อ Backend ได้ — ตรวจสอบว่า Django server ทำงานอยู่')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<template>
  <div>
    <h1>➕ สร้าง Note ใหม่</h1>

    <form @submit.prevent="submitForm">
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
      <button type="submit" :disabled="loading">
        {{ loading ? '⏳ กำลังบันทึก...' : '💾 บันทึก' }}
      </button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

---

## ❌ ปัญหาที่พบบ่อย

### ปัญหา: กดบันทึกแล้วเห็น `CORS error` ใน Console

**สาเหตุ:** Django Backend ไม่ได้ติดตั้ง `django-cors-headers` หรือยังไม่ได้ตั้งค่า

**วิธีแก้:**
1. ตรวจว่า Django Backend มี `corsheaders` ใน `INSTALLED_APPS`
2. ตรวจว่า `CORS_ALLOW_ALL_ORIGINS = True` อยู่ใน `settings.py`
3. ตรวจว่า `corsheaders.middleware.CorsMiddleware` อยู่ใน `MIDDLEWARE`

> ⚠️ Backend ที่ให้มากับ tutorial ตั้งค่า CORS ไว้แล้ว — ถ้าไม่ได้แก้ไข settings.py ไม่ควรมีปัญหานี้

---

### ปัญหา: กดบันทึกแล้วได้ alert "ไม่สามารถเชื่อมต่อ Backend ได้"

**สาเหตุ:** Django server ไม่ได้ทำงานอยู่

**วิธีแก้:**
```bash
cd backend
uv run python manage.py runserver
```

ตรวจว่า Terminal แสดง `Starting development server at http://127.0.0.1:8000/`

---

### ปัญหา: กดบันทึกแล้วไม่เกิดอะไรเลย (ไม่มี alert ไม่มี error)

**สาเหตุ:** อาจลืมใส่ `async` หน้า function หรือ `await` หน้า `fetch()`

**วิธีแก้:** ตรวจสอบว่า:
```js
// ❌ ผิด
submitForm() {
  const response = fetch(...)
}

// ✅ ถูก
async submitForm() {
  const response = await fetch(...)
}
```

---

### ปัญหา: ได้ error `SyntaxError: Unexpected token` ใน Console

**สาเหตุ:** JSON format ใน `JSON.stringify()` ผิด หรือลืม `headers: { 'Content-Type': 'application/json' }`

**วิธีแก้:** ตรวจ 2 จุด:
1. มี `headers: { 'Content-Type': 'application/json' }` ใน fetch options
2. ข้อมูลใน `JSON.stringify()` ถูกต้อง:
```js
// ❌ ผิด — ลืม this.
body: JSON.stringify({ title: title, body: body })

// ✅ ถูก
body: JSON.stringify({ title: this.title, body: this.body })
```

---

### ปัญหา: ได้ `405 Method Not Allowed`

**สาเหตุ:** URL ผิด — ส่ง POST ไปที่ `/api/notes/` แทน `/api/notes/create/`

**วิธีแก้:**
```js
// ❌ ผิด — URL สำหรับ GET (list) ไม่ใช่ POST (create)
fetch('http://localhost:8000/api/notes/', { method: 'POST', ... })

// ✅ ถูก
fetch('http://localhost:8000/api/notes/create/', { method: 'POST', ... })
```

---

## 🏋️ ลองทำเอง (Challenge)

### ⭐ ระดับง่าย
เพิ่มช่อง **is_done** (checkbox) ในฟอร์มสร้าง Note:
- เพิ่ม `is_done: false` ใน `data()`
- เพิ่ม `<input type="checkbox" v-model="is_done">` ใน template
- ส่ง `is_done: this.is_done` ใน `JSON.stringify()`

### ⭐⭐ ระดับปานกลาง
เพิ่ม **success message** แทน `alert()`:
- เพิ่มตัวแปร `successMessage: ''` ใน data
- เมื่อสร้างสำเร็จ ตั้ง `this.successMessage = 'สร้าง Note สำเร็จ!'` แทน alert
- แสดงข้อความสีเขียวใน template: `<p v-if="successMessage" style="color: green;">{{ successMessage }}</p>`
- ใช้ `setTimeout(() => this.$router.push('/notes'), 1500)` เพื่อรอ 1.5 วินาทีก่อน redirect

### ⭐⭐⭐ ระดับยาก
สร้าง **API base URL** เป็นตัวแปรกลาง ไม่ต้องพิมพ์ `http://localhost:8000` ซ้ำทุกที่:
- สร้างไฟล์ `src/config.js`:
  ```js
  export const API_BASE_URL = 'http://localhost:8000'
  ```
- import มาใช้ใน NoteCreate.vue:
  ```js
  import { API_BASE_URL } from '../config.js'
  // ...
  fetch(API_BASE_URL + '/api/notes/create/', { ... })
  ```
- คิดว่าทำไมถึงควรทำแบบนี้? (คำตอบ: เมื่อ deploy จะเปลี่ยน URL แค่ที่เดียว)

<details>
<summary>💡 คำใบ้ระดับง่าย</summary>

เพิ่มใน `data()`:
```js
is_done: false
```

เพิ่มใน template ก่อน `<br />` สุดท้าย:
```html
<div>
  <label>
    <input type="checkbox" v-model="is_done" />
    เสร็จแล้ว
  </label>
</div>
```

แก้ `JSON.stringify`:
```js
body: JSON.stringify({
  title: this.title,
  body: this.body,
  is_done: this.is_done
})
```

</details>

<details>
<summary>💡 คำใบ้ระดับปานกลาง</summary>

เพิ่มใน `data()`:
```js
successMessage: ''
```

แก้ `if (response.ok)`:
```js
if (response.ok) {
  this.successMessage = 'สร้าง Note สำเร็จ!'
  setTimeout(() => {
    this.$router.push('/notes')
  }, 1500)
}
```

เพิ่มใน template (ก่อน `<form>`):
```html
<p v-if="successMessage" style="color: green; font-weight: bold;">
  ✅ {{ successMessage }}
</p>
```

</details>

<details>
<summary>💡 คำใบ้ระดับยาก</summary>

สร้างไฟล์ `src/config.js`:
```js
export const API_BASE_URL = 'http://localhost:8000'
```

ใน `NoteCreate.vue` เพิ่ม import (ใน `<script>` ก่อน `export default`):
```js
import { API_BASE_URL } from '../config.js'
```

แก้ fetch URL:
```js
const response = await fetch(API_BASE_URL + '/api/notes/create/', { ... })
```

**ข้อดี:**
- เปลี่ยน URL แค่ที่เดียว ไม่ต้องไล่แก้ทุก component
- ตอน deploy เป็น production เปลี่ยนจาก `localhost:8000` เป็น URL จริง ง่ายมาก
- ใช้ environment variable ร่วมด้วยได้ (บทขั้นสูง)

</details>

---

## 📖 คำศัพท์ที่เรียนรู้ในบทนี้

| คำศัพท์ | ความหมาย | เปรียบเทียบ |
|---------|----------|-------------|
| fetch() | ฟังก์ชัน JavaScript สำหรับส่ง HTTP request | เหมือน Postman แต่เขียนเป็นโค้ด |
| async | คำนำหน้า function ที่บอกว่า "ข้างในมีงานต้องรอ" | เหมือนป้ายบอก "ร้านนี้ต้องรอคิว" |
| await | คำสั่งบอกว่า "รอตรงนี้ก่อน แล้วค่อยทำต่อ" | เหมือนยืนรอรับอาหาร ก่อนเดินกลับโต๊ะ |
| response.ok | ตรวจว่า status code เป็น 200-299 (สำเร็จ) | เหมือนดูว่าได้อาหารหรือได้ข้อความ "หมดแล้ว" |
| response.json() | อ่านข้อมูล JSON จาก response | เหมือนเปิดกล่องอาหาร ดูว่าข้างในมีอะไร |
| JSON.stringify() | แปลง JavaScript object เป็น JSON string | เหมือนเขียนใบสั่งอาหารเป็นตัวอักษร |
| try/catch/finally | จัดการ error — try=ลอง, catch=ถ้าพลาด, finally=ทำเสมอ | เหมือน ลองยกของ / ถ้ายกไม่ไหวก็วาง / ล้างมือ |
| Loading State | สถานะบอกว่ากำลังทำงานอยู่ | เหมือนไฟ "กำลังดำเนินการ" ที่ธนาคาร |
| CORS | กลไกอนุญาตให้ Frontend เรียก API จากต่าง origin | เหมือนใบอนุญาตเข้าอาคาร — ต้องมีถึงจะเข้าได้ |

---

## สรุปสิ่งที่ได้เรียนรู้ ✅

| หัวข้อ | สิ่งที่เรียนรู้ |
|--------|----------------|
| fetch() | ส่ง HTTP request จาก JavaScript — เหมือน Postman เป็นโค้ด |
| async/await | จัดการงานที่ต้องรอ — ใส่ `async` หน้า function, `await` หน้า fetch |
| Error Handling | อ่าน error จาก Backend (`response.json()`) แล้วแสดงในฟอร์ม |
| try/catch/finally | จัดการกรณี Backend ปิด หรือ network error |
| Loading State | ป้องกันกดปุ่มซ้ำ + แสดงสถานะให้ผู้ใช้ |
| CORS | Backend ต้องอนุญาตให้ Frontend จากต่าง origin เรียก API ได้ |
| DevTools Network | ดู request/response ที่ Vue.js ส่งจริงในเบราว์เซอร์ |

---

> ➡️ **บทถัดไป:** [บทที่ 7: แสดงรายการ Note (Read)](./lesson-7-list-note.md)
