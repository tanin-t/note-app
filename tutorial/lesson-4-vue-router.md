# บทที่ 4: สร้าง Multi-page App ด้วย Vue Router

> 📍 **บทที่ 4 / 10** ━━━━━━━━━━ `[████████░░]`

| ⬅️ [บทที่ 3: ทำความเข้าใจ Error](./lesson-3-vuejs-error.md) | [สารบัญ](./tutorial.md) | [บทที่ 5: Postman ➡️](./lesson-5-postman.md) |
|:---|:---:|---:|

---

## 🎯 เป้าหมาย

ในบทนี้เราจะ:
- เข้าใจว่า **Vue Router** คืออะไร ทำไมต้องใช้
- ติดตั้งและตั้งค่า Vue Router ในโปรเจกต์
- **ลองสร้าง 2 หน้าง่ายๆ (PageA, PageB)** เพื่อทดสอบ Router
- นำความรู้มาสร้าง **4 หน้า** สำหรับ Note App: รายการ, สร้าง, แก้ไข, ลบ
- เข้าใจ **Route Parameters** (`:id`) สำหรับหน้าแก้ไข/ลบ

> 🎮 **Fun Fact:** ถ้าไม่ใช้ Router เว็บจะเป็น "Single Page" จริงๆ — คือมีแค่หน้าเดียว!
> Router ทำให้เราสร้าง "หลายหน้า" ภายใน Single Page Application ได้
> เหมือนห้องหลายห้องในบ้าน 1 หลัง — ไม่ต้องออกจากบ้านก็ไปห้องอื่นได้ 🏠

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

- ทำบทที่ 3 เสร็จแล้ว
- dev server ทำงานอยู่ (`npm run dev`)
- เข้าใจ Vue Component เบื้องต้น (`data()`, `methods`, `template`)

---

## 🧠 ทำไมต้องใช้ Vue Router?

ก่อนเริ่มลงมือ มาทำความเข้าใจปัญหาก่อน:

> 💡 **เปรียบเทียบ:**
>
> | ไม่มี Router | มี Router |
> |-------------|-----------|
> | เหมือนหนังสือมี 1 หน้า เขียนทุกอย่างรวมกัน | เหมือนหนังสือมีสารบัญ กดไปหน้าไหนก็ได้ |
> | URL เป็น `localhost:5173` ตลอด | URL เปลี่ยนตามหน้า เช่น `/page-a`, `/page-b` |
> | กด Back ในเบราว์เซอร์ไม่ได้ | กด Back ได้ กลับไปหน้าก่อนหน้า |
> | ส่ง URL ให้เพื่อน จะเห็นหน้าเดิมเสมอ | ส่ง URL ให้เพื่อน จะเห็นหน้าเดียวกัน |

---

## 📝 ขั้นตอน

---

## ส่วนที่ 1: ทดลอง Router กับ PageA / PageB

> เราจะเริ่มจากตัวอย่างง่ายๆ ก่อน เพื่อเข้าใจหลักการ Router แล้วค่อยนำไปใช้กับ Note App

### ขั้นตอนที่ 1: ติดตั้ง Vue Router

หยุด dev server ก่อน (กด `Ctrl+C` ใน Terminal) แล้วรัน:

```bash
npm install vue-router@4
```

> 💡 `vue-router@4` คือ Vue Router เวอร์ชัน 4 ที่ใช้กับ Vue 3

รอจนเสร็จแล้วรัน dev server อีกครั้ง:

```bash
npm run dev
```

#### ✅ ตรวจสอบ
- [ ] ติดตั้ง `vue-router` สำเร็จ ไม่มี error
- [ ] เปิด `package.json` แล้วเห็น `"vue-router"` ใน `dependencies`

---

### ขั้นตอนที่ 2: สร้าง PageA และ PageB

สร้างโฟลเดอร์ก่อน:

```bash
mkdir -p src/router src/views
```

สร้างไฟล์ `src/views/PageA.vue`:

```vue
<template>
  <div>
    <h1>🅰️ นี่คือ Page A</h1>
    <p>ยินดีต้อนรับสู่หน้า A</p>
  </div>
</template>
```

สร้างไฟล์ `src/views/PageB.vue`:

```vue
<template>
  <div>
    <h1>🅱️ นี่คือ Page B</h1>
    <p>ยินดีต้อนรับสู่หน้า B</p>
  </div>
</template>
```

> 💡 ทั้ง 2 ไฟล์เป็นแค่ component ธรรมดาที่มี `<template>` อย่างเดียว ง่ายที่สุด!

#### ✅ ตรวจสอบ
- [ ] มีไฟล์ `src/views/PageA.vue`
- [ ] มีไฟล์ `src/views/PageB.vue`

---

### ขั้นตอนที่ 3: ตั้งค่า Router

สร้างไฟล์ `src/router/index.js`:

```js
import { createRouter, createWebHistory } from 'vue-router'

import PageA from '../views/PageA.vue'
import PageB from '../views/PageB.vue'

const routes = [
  { path: '/page-a', component: PageA },
  { path: '/page-b', component: PageB },
  { path: '/', redirect: '/page-a' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

> 💡 **อธิบาย:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `path: '/page-a'` | เมื่อ URL เป็น `/page-a` → แสดง component `PageA` |
> | `path: '/'` + `redirect` | เมื่อเข้า `/` → redirect ไป `/page-a` อัตโนมัติ |
> | `createWebHistory()` | ใช้ URL สวยๆ เช่น `/page-a` (ไม่มี `#`) |

#### ✅ ตรวจสอบ
- [ ] สร้างไฟล์ `src/router/index.js` แล้ว
- [ ] มี 2 route: `/page-a` และ `/page-b`

---

### ขั้นตอนที่ 4: เชื่อม Router กับ App

แก้ไข `src/main.js`:

```js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'    // ← เพิ่ม

const app = createApp(App)
app.use(router)                  // ← เพิ่ม
app.mount('#app')
```

> 💡 `app.use(router)` คือการ "ติดตั้ง" Router เข้ากับ Vue app

#### ✅ ตรวจสอบ
- [ ] แก้ไข `src/main.js` เพิ่ม `import router` และ `app.use(router)`

---

### ขั้นตอนที่ 5: แก้ App.vue — ใส่ลิงก์ + router-view

แก้ `src/App.vue` ให้มี **ลิงก์สลับหน้า** และ **`<router-view>`**:

```vue
<template>
  <div>
    <nav>
      <router-link to="/page-a">ไป Page A</router-link>
      |
      <router-link to="/page-b">ไป Page B</router-link>
    </nav>

    <hr />

    <router-view />
  </div>
</template>
```

**บันทึกแล้วดูที่เบราว์เซอร์!** ลองกดลิงก์สลับไปมา

> 💡 **2 สิ่งสำคัญที่ต้องจำ:**
>
> | โค้ด | ทำอะไร | เปรียบเทียบ |
> |------|--------|------------|
> | `<router-link to="/page-b">` | สร้างลิงก์ไปหน้าอื่น **โดยไม่ reload** | เหมือนประตูระหว่างห้อง |
> | `<router-view />` | จุดที่ Vue จะ **สลับแสดง component** ตาม URL | เหมือนจอทีวี — เปลี่ยนช่องก็เปลี่ยนเนื้อหา |
>
> ```
> ┌──────────────────────────────┐
> │  ไป Page A | ไป Page B       │  ← ลิงก์ (อยู่ตลอด)
> │  ─────────────────────────── │
> │                              │
> │       <router-view />        │  ← ตรงนี้เปลี่ยนตาม URL
> │                              │
> │  URL = /page-a → PageA.vue   │
> │  URL = /page-b → PageB.vue   │
> └──────────────────────────────┘
> ```

> 🤔 **ทำไมใช้ `<router-link>` แทน `<a href>`?**
>
> | `<a href="/page-b">` | `<router-link to="/page-b">` |
> |----------------------|-------------------------------|
> | ❌ Reload ทั้งหน้า (ช้า!) | ✅ เปลี่ยนเฉพาะ content (เร็ว!) |
> | ❌ State หาย (ข้อมูลหาย) | ✅ State ยังอยู่ |
> | เหมือนปิดบ้านแล้วเปิดใหม่ | เหมือนเดินไปอีกห้อง |

#### ✅ ตรวจสอบ
- [ ] เห็นลิงก์ "ไป Page A" และ "ไป Page B"
- [ ] กดลิงก์แล้วเนื้อหาเปลี่ยน **โดยหน้าไม่ reload**
- [ ] URL ในเบราว์เซอร์เปลี่ยนตาม (`/page-a`, `/page-b`)
- [ ] กดปุ่ม **← Back** ของเบราว์เซอร์แล้วกลับหน้าก่อนหน้าได้

---

### ขั้นตอนที่ 6: เพิ่มปุ่มเปลี่ยนหน้าด้วย JavaScript

นอกจาก `<router-link>` เรายังเปลี่ยนหน้าด้วย **JavaScript** ได้!

แก้ `src/views/PageA.vue`:

```vue
<script>
export default {
  methods: {
    goToPageB() {
      this.$router.push('/page-b')
    }
  }
}
</script>

<template>
  <div>
    <h1>🅰️ นี่คือ Page A</h1>
    <p>ยินดีต้อนรับสู่หน้า A</p>
    <button @click="goToPageB">ไป Page B ด้วยปุ่ม →</button>
  </div>
</template>
```

> 💡 **`this.$router.push('/page-b')`** = เปลี่ยนหน้าด้วย JavaScript
>
> ใช้ตอนไหน? เช่น กดปุ่ม submit form แล้ว redirect ไปหน้าอื่น

#### ✅ ตรวจสอบ
- [ ] กดปุ่ม "ไป Page B ด้วยปุ่ม →" แล้วเปลี่ยนหน้าได้
- [ ] เข้าใจว่า `$router.push()` ใช้เปลี่ยนหน้าด้วย JavaScript

---

🎉 **เยี่ยม!** ตอนนี้เราเข้าใจหลักการ Router แล้ว:
- `<router-link>` = ลิงก์เปลี่ยนหน้า
- `<router-view>` = จุดแสดงเนื้อหา
- `$router.push()` = เปลี่ยนหน้าด้วย JS

ต่อไปเราจะนำมาใช้กับ **Note App จริง!**

---

## ส่วนที่ 2: สร้างหน้าสำหรับ Note App

### ขั้นตอนที่ 7: วางโครงสร้าง Note App

เราจะสร้าง **4 หน้า** ตามหลัก CRUD:

```
src/views/
├── NoteList.vue     ← 📋 หน้ารายการ Note ทั้งหมด
├── NoteCreate.vue   ← ➕ หน้าสร้าง Note ใหม่
├── NoteEdit.vue     ← ✏️ หน้าแก้ไข Note
└── NoteDelete.vue   ← 🗑️ หน้ายืนยันลบ Note
```

> 🤔 **ทำไมแยกโฟลเดอร์ `views/` กับ `components/`?**
>
> | โฟลเดอร์ | เก็บอะไร | ตัวอย่าง |
> |----------|---------|---------|
> | `views/` | **หน้า** — component ที่ผูกกับ URL | `NoteList.vue`, `NoteCreate.vue` |
> | `components/` | **ชิ้นส่วน** — component ย่อยที่ reuse ได้ | `Button.vue`, `Header.vue` |
>
> เปรียบเทียบ: `views/` คือ **ห้อง** (ห้องนอน, ห้องครัว) ส่วน `components/` คือ **เฟอร์นิเจอร์** (เตียง, โต๊ะ)

---

### ขั้นตอนที่ 8: สร้าง NoteList.vue

สร้างไฟล์ `src/views/NoteList.vue`:

```vue
<script>
export default {
  data() {
    return {
      notes: [
        { id: 1, title: 'ซื้อของ', body: 'ไข่ นม ขนมปัง' },
        { id: 2, title: 'การบ้าน', body: 'ทำแบบฝึกหัดบทที่ 4' },
        { id: 3, title: 'ประชุม', body: 'ประชุมทีมบ่าย 2 โมง' }
      ]
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

> 💡 **สิ่งใหม่ในโค้ดนี้:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `<router-link to="/notes/create">` | ลิงก์ไปหน้าสร้าง |
> | `:to="'/notes/' + note.id + '/edit'"` | ลิงก์แบบ dynamic เช่น `/notes/1/edit`, `/notes/2/edit` |

#### ✅ ตรวจสอบ
- [ ] สร้างไฟล์ `src/views/NoteList.vue` แล้ว
- [ ] เข้าใจ `<router-link>` แบบ dynamic ที่ใส่ตัวแปร `note.id` ลงใน URL

---

### ขั้นตอนที่ 9: สร้าง NoteCreate.vue

สร้างไฟล์ `src/views/NoteCreate.vue`:

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
    submitForm() {
      console.log('สร้าง Note:', { title: this.title, body: this.body })
      alert('สร้างสำเร็จ! (ยังไม่ได้เชื่อมต่อ API)')
      this.$router.push('/notes')
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
        <input v-model="title" type="text" placeholder="ใส่หัวข้อ" required />
      </div>
      <br />
      <div>
        <label>เนื้อหา:</label><br />
        <textarea v-model="body" placeholder="ใส่เนื้อหา" rows="5" required></textarea>
      </div>
      <br />
      <button type="submit">💾 บันทึก</button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

> 💡 **สิ่งใหม่ในโค้ดนี้:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `v-model="title"` | **Two-way binding** — เชื่อมค่า input กับตัวแปร `title` โดยอัตโนมัติ |
> | `@submit.prevent="submitForm"` | เรียก `submitForm` เมื่อ submit form + **ป้องกันหน้า reload** |
> | `this.$router.push('/notes')` | เปลี่ยนหน้าด้วย JavaScript (ที่เราเพิ่งเรียนในขั้นตอนที่ 6!) |
>
> 🤔 **v-model คืออะไร?**
>
> ```
> ✏️ ผู้ใช้พิมพ์ใน input  ──→  ค่าใน data() เปลี่ยน
>                              ↕  (Two-way)
> 📦 ค่าใน data() เปลี่ยน ──→  input แสดงค่าใหม่
> ```

#### ✅ ตรวจสอบ
- [ ] สร้างไฟล์ `src/views/NoteCreate.vue` แล้ว
- [ ] เข้าใจว่า `v-model` คือ two-way binding
- [ ] เข้าใจว่า `@submit.prevent` ป้องกัน form reload หน้า

---

### ขั้นตอนที่ 10: สร้าง NoteEdit.vue

สร้างไฟล์ `src/views/NoteEdit.vue`:

```vue
<script>
export default {
  data() {
    return {
      noteId: null,
      title: '',
      body: ''
    }
  },

  created() {
    this.noteId = this.$route.params.id

    // จำลองข้อมูล (ในบทหลังจะดึงจาก API จริง)
    this.title = 'ตัวอย่างหัวข้อ Note #' + this.noteId
    this.body = 'ตัวอย่างเนื้อหาของ Note #' + this.noteId
  },

  methods: {
    submitForm() {
      console.log('แก้ไข Note ID:', this.noteId, { title: this.title, body: this.body })
      alert('แก้ไขสำเร็จ! (ยังไม่ได้เชื่อมต่อ API)')
      this.$router.push('/notes')
    }
  }
}
</script>

<template>
  <div>
    <h1>✏️ แก้ไข Note #{{ noteId }}</h1>

    <form @submit.prevent="submitForm">
      <div>
        <label>หัวข้อ:</label><br />
        <input v-model="title" type="text" required />
      </div>
      <br />
      <div>
        <label>เนื้อหา:</label><br />
        <textarea v-model="body" rows="5" required></textarea>
      </div>
      <br />
      <button type="submit">💾 บันทึก</button>
      <router-link to="/notes">❌ ยกเลิก</router-link>
    </form>
  </div>
</template>
```

> 💡 **สิ่งใหม่ในโค้ดนี้:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `this.$route.params.id` | ดึงค่า **Route Parameter** จาก URL เช่น `/notes/5/edit` → `id = "5"` |
> | `created()` | **Lifecycle Hook** — ทำงานเมื่อ component ถูกสร้าง (ก่อน render) |
>
> 🤔 **`this.$route` vs `this.$router` ต่างกันยังไง?**
>
> | | `this.$route` | `this.$router` |
> |---|---------------|----------------|
> | คือ | ข้อมูลของหน้าปัจจุบัน | ตัวควบคุม Router |
> | ใช้ทำอะไร | **อ่าน** ข้อมูล URL, params | **สั่ง** เปลี่ยนหน้า |
> | ตัวอย่าง | `this.$route.params.id` | `this.$router.push('/notes')` |
> | เปรียบเทียบ | เหมือน GPS บอกว่า **อยู่ตรงไหน** | เหมือนพวงมาลัย บอกว่าจะ **ไปไหน** |

#### ✅ ตรวจสอบ
- [ ] สร้างไฟล์ `src/views/NoteEdit.vue` แล้ว
- [ ] เข้าใจว่า `this.$route.params.id` ดึงค่า id จาก URL
- [ ] เข้าใจความต่างระหว่าง `$route` (อ่าน) กับ `$router` (สั่ง)

---

### ขั้นตอนที่ 11: สร้าง NoteDelete.vue

สร้างไฟล์ `src/views/NoteDelete.vue`:

```vue
<script>
export default {
  data() {
    return {
      noteId: null
    }
  },

  created() {
    this.noteId = this.$route.params.id
  },

  methods: {
    confirmDelete() {
      console.log('ลบ Note ID:', this.noteId)
      alert('ลบสำเร็จ! (ยังไม่ได้เชื่อมต่อ API)')
      this.$router.push('/notes')
    }
  }
}
</script>

<template>
  <div>
    <h1>🗑️ ยืนยันการลบ</h1>
    <p>คุณต้องการลบ <strong>Note #{{ noteId }}</strong> ใช่หรือไม่?</p>
    <p style="color: red;">⚠️ การลบไม่สามารถกู้คืนได้!</p>
    <br />
    <button @click="confirmDelete">🗑️ ยืนยันลบ</button>
    <router-link to="/notes">❌ ยกเลิก</router-link>
  </div>
</template>
```

#### ✅ ตรวจสอบ
- [ ] สร้างไฟล์ `src/views/NoteDelete.vue` แล้ว
- [ ] มีปุ่ม "ยืนยันลบ" และ ลิงก์ "ยกเลิก"

---

### ขั้นตอนที่ 12: อัปเดต Router — เพิ่มเส้นทาง Note App

แก้ไข `src/router/index.js` — **ลบ PageA/PageB** แล้วเพิ่มเส้นทาง Note App:

```js
import { createRouter, createWebHistory } from 'vue-router'

import NoteList from '../views/NoteList.vue'
import NoteCreate from '../views/NoteCreate.vue'
import NoteEdit from '../views/NoteEdit.vue'
import NoteDelete from '../views/NoteDelete.vue'

const routes = [
  { path: '/notes', component: NoteList },
  { path: '/notes/create', component: NoteCreate },
  { path: '/notes/:id/edit', component: NoteEdit },
  { path: '/notes/:id/delete', component: NoteDelete },
  { path: '/', redirect: '/notes' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

> 💡 **`:id` คืออะไร?**
>
> `:id` คือ **ตัวแปร** ใน URL ที่รับค่าอะไรก็ได้:
>
> | URL ที่ผู้ใช้เข้า | `$route.params.id` |
> |------------------|--------------------|
> | `/notes/1/edit` | `"1"` |
> | `/notes/42/edit` | `"42"` |
> | `/notes/999/delete` | `"999"` |

#### ✅ ตรวจสอบ
- [ ] มี 4 route: `/notes`, `/notes/create`, `/notes/:id/edit`, `/notes/:id/delete`
- [ ] มี redirect จาก `/` ไป `/notes`
- [ ] เข้าใจว่า `:id` คือ Route Parameter

---

### ขั้นตอนที่ 13: อัปเดต App.vue — ใส่ Navigation ของ Note App

แก้ `src/App.vue`:

```vue
<template>
  <div>
    <nav>
      <strong>📝 Note App</strong>
      &nbsp;&nbsp;
      <router-link to="/notes">📋 รายการ</router-link>
      |
      <router-link to="/notes/create">➕ สร้าง Note</router-link>
    </nav>

    <hr />

    <router-view />
  </div>
</template>
```

**บันทึกแล้วดูที่เบราว์เซอร์!** 🎉

#### ✅ ตรวจสอบ
- [ ] เห็น Navbar มีลิงก์ "📋 รายการ" และ "➕ สร้าง Note"
- [ ] เห็นหน้ารายการ Note พร้อมตาราง
- [ ] กดลิงก์ "➕ สร้าง Note" → ไปหน้าสร้าง (URL เปลี่ยนเป็น `/notes/create`)
- [ ] กด "📋 รายการ" → กลับไปหน้ารายการ

---

### ขั้นตอนที่ 14: ทดสอบ Navigation ทั้งหมด

**ทดสอบที่ 1 — เปลี่ยนหน้า:**

1. เปิด `http://localhost:5173/` → redirect ไป `/notes` อัตโนมัติ
2. กด "➕ สร้าง Note" → ไปหน้า `/notes/create`
3. กด "❌ ยกเลิก" → กลับไป `/notes`
4. กด "✏️ แก้ไข" ของ Note → ไปหน้า `/notes/1/edit`
5. กด "🗑️ ลบ" → ไปหน้า `/notes/1/delete`

**ทดสอบที่ 2 — ปุ่ม Back/Forward:**

1. เปลี่ยนหน้าไปมาหลายครั้ง
2. กดปุ่ม **← Back** ของเบราว์เซอร์ → กลับหน้าก่อนหน้า
3. กดปุ่ม **→ Forward** → ไปหน้าถัดไป

**ทดสอบที่ 3 — พิมพ์ URL ตรง:**

ลองพิมพ์ URL ในเบราว์เซอร์:
- `http://localhost:5173/notes` → หน้ารายการ
- `http://localhost:5173/notes/create` → หน้าสร้าง
- `http://localhost:5173/notes/99/edit` → หน้าแก้ไข Note #99

**ทดสอบที่ 4 — ลองใช้ฟอร์ม:**

1. ไปหน้าสร้าง Note → กรอกข้อมูล → กด "💾 บันทึก"
2. เปิด Console (F12) → เห็น log ข้อมูลที่กรอก

#### ✅ ตรวจสอบ
- [ ] ทุกหน้าสลับกันได้ถูกต้อง
- [ ] ปุ่ม Back/Forward ทำงานได้
- [ ] ฟอร์มสร้าง/แก้ไข Note ทำงานได้ (log ข้อความ + redirect)
- [ ] หน้าแก้ไขแสดง Note ID ถูกต้อง

---

### ขั้นตอนที่ 15: ลบไฟล์ PageA, PageB

ตอนนี้เราไม่ต้องใช้ PageA, PageB แล้ว ลบได้เลย:

```bash
rm src/views/PageA.vue src/views/PageB.vue
```

#### ✅ ตรวจสอบ
- [ ] ลบ `PageA.vue` และ `PageB.vue` แล้ว
- [ ] แอปยังทำงานปกติ

---

## ❌ ปัญหาที่พบบ่อย

### ปัญหา: `[Vue Router warn]: No match found for location with path "/notes"`

**สาเหตุ:** ยังไม่ได้ติดตั้ง Router ใน `main.js` หรือ path สะกดผิด

**วิธีแก้:**
1. ตรวจสอบว่า `main.js` มี `app.use(router)` แล้ว
2. ตรวจสอบ path ใน `routes` ว่าตรงกับ URL ที่เข้า
3. ตรวจดูว่า import ถูกต้อง: `import router from './router'`

---

### ปัญหา: กดลิงก์แล้วหน้า reload ทั้งหมด

**สาเหตุ:** ใช้ `<a href="">` แทน `<router-link to="">`

**วิธีแก้:**

```html
<!-- ❌ ผิด — จะ reload ทั้งหน้า -->
<a href="/notes/create">สร้าง</a>

<!-- ✅ ถูก — เปลี่ยนเฉพาะ content -->
<router-link to="/notes/create">สร้าง</router-link>
```

---

### ปัญหา: `this.$route.params.id` ได้ค่า `undefined`

**สาเหตุ:** path ใน Router ไม่มี `:id` หรือ URL ไม่ตรงกับ pattern

**วิธีแก้:**
1. ตรวจว่า path เขียนถูก: `path: '/notes/:id/edit'`
2. ตรวจว่า URL มีตัวเลข: `/notes/5/edit` ไม่ใช่ `/notes/edit`
3. ใช้ `console.log(this.$route.params)` เพื่อดูค่าทั้งหมด

---

## 🏋️ ลองทำเอง (Challenge)

### ⭐ ระดับง่าย
เพิ่ม **หน้า About** ที่ URL `/about` แสดงข้อมูลเกี่ยวกับแอป:
- สร้างไฟล์ `src/views/About.vue`
- เพิ่ม route ใน `router/index.js`
- เพิ่มลิงก์ "ℹ️ เกี่ยวกับ" ใน Navbar

### ⭐⭐ ระดับปานกลาง
เพิ่ม **หน้า 404 Not Found** เมื่อผู้ใช้เข้า URL ที่ไม่มี:
- สร้าง `src/views/NotFound.vue` แสดงข้อความ "ไม่พบหน้าที่ค้นหา"
- เพิ่ม **catch-all route** ใน Router: `path: '/:pathMatch(.*)*'`
- มีปุ่มกลับไปหน้าหลัก

### ⭐⭐⭐ ระดับยาก
ทำให้ **ลิงก์ใน Navbar เปลี่ยนสี** ตามหน้าที่อยู่:
- ใช้ CSS class `router-link-exact-active`
- ลองหาความต่างระหว่าง `exact-active` กับ `active`

<details>
<summary>💡 คำใบ้ระดับง่าย</summary>

1. สร้าง `src/views/About.vue` เหมือน component ทั่วไป
2. ใน `router/index.js` เพิ่ม:
```js
{ path: '/about', component: About }
```
3. ใน `App.vue` เพิ่ม `<router-link to="/about">` ใน Navbar

</details>

<details>
<summary>💡 คำใบ้ระดับปานกลาง</summary>

1. Catch-all route ต้องอยู่ **ลำดับสุดท้าย** ใน routes array
2. ใช้ path:
```js
{ path: '/:pathMatch(.*)*', component: NotFound }
```
3. `/:pathMatch(.*)*` จับทุก URL ที่ไม่ตรงกับ route อื่น

</details>

<details>
<summary>💡 คำใบ้ระดับยาก</summary>

ความต่าง:
- `router-link-active` — ถูกเพิ่มเมื่อ URL **เริ่มด้วย** path ของลิงก์
  - URL `/notes/create` → ลิงก์ `/notes` จะ active ด้วย!
- `router-link-exact-active` — ถูกเพิ่มเมื่อ URL **ตรงกันพอดี**
  - URL `/notes/create` → ลิงก์ `/notes` จะ **ไม่** active

```css
a.router-link-exact-active {
  color: green;
  font-weight: bold;
}
```

</details>

<details>
<summary>✅ ดูเฉลยระดับง่าย</summary>

**`src/views/About.vue`**
```vue
<template>
  <div>
    <h1>ℹ️ เกี่ยวกับ Note App</h1>
    <p>สร้างด้วย Vue.js 3 + Vue Router 4 + Vite</p>
  </div>
</template>
```

**เพิ่มใน `router/index.js`:**
```js
import About from '../views/About.vue'
// เพิ่มใน routes:
{ path: '/about', component: About }
```

**เพิ่มใน `App.vue` Navbar:**
```html
<router-link to="/about">ℹ️ เกี่ยวกับ</router-link>
```

</details>

<details>
<summary>✅ ดูเฉลยระดับปานกลาง</summary>

**`src/views/NotFound.vue`**
```vue
<template>
  <div>
    <h1>😵 404 — ไม่พบหน้าที่ค้นหา</h1>
    <p>URL ที่คุณเข้าไม่มีในระบบ</p>
    <router-link to="/notes">🏠 กลับหน้าหลัก</router-link>
  </div>
</template>
```

**เพิ่มใน `router/index.js` (ลำดับสุดท้าย!):**
```js
import NotFound from '../views/NotFound.vue'
// เพิ่มเป็น route สุดท้าย:
{ path: '/:pathMatch(.*)*', component: NotFound }
```

ลองเข้า `http://localhost:5173/xyz` → จะเห็นหน้า 404!

</details>

<details>
<summary>✅ ดูเฉลยระดับยาก</summary>

เพิ่ม `<style>` ใน `App.vue`:

```vue
<style>
a.router-link-exact-active {
  color: green;
  font-weight: bold;
}
</style>
```

**ทดสอบ:**
- เข้า `/notes` → เฉพาะ "📋 รายการ" เป็นสีเขียว ✅
- เข้า `/notes/create` → เฉพาะ "➕ สร้าง Note" เป็นสีเขียว ✅

ถ้าใช้ `router-link-active` แทน → เข้า `/notes/create` จะทำให้ "📋 รายการ" ก็สีเขียวด้วย (เพราะ `/notes/create` เริ่มด้วย `/notes`)

</details>

---

## 📖 คำศัพท์ที่เรียนรู้ในบทนี้

| คำศัพท์ | ความหมาย | เปรียบเทียบ |
|---------|----------|-------------|
| Vue Router | Library สำหรับจัดการเส้นทาง URL ใน Vue.js | เหมือนป้ายบอกทางในอาคาร |
| Route | เส้นทาง 1 เส้น ที่ผูก URL กับ Component | เหมือนที่อยู่บ้าน |
| `<router-view>` | จุดที่ Vue จะแสดง Component ตาม URL | เหมือนจอทีวี — เปลี่ยนช่องก็เปลี่ยนเนื้อหา |
| `<router-link>` | ลิงก์สำหรับเปลี่ยนหน้าโดยไม่ reload | เหมือนประตูระหว่างห้อง |
| Route Parameter (`:id`) | ตัวแปรใน URL ที่รับค่าจากผู้ใช้ | เหมือนเลขห้อง — `/rooms/101` |
| `$route` | Object ข้อมูลของหน้าปัจจุบัน | เหมือน GPS — บอกว่าอยู่ตรงไหน |
| `$router` | Object สำหรับสั่งเปลี่ยนหน้า | เหมือนพวงมาลัย — ใช้เปลี่ยนทิศทาง |
| `v-model` | Two-way data binding สำหรับ input | เหมือนกระจก — เปลี่ยนด้านหนึ่งก็เห็นอีกด้าน |
| `created()` | Lifecycle hook ที่ทำงานเมื่อ component ถูกสร้าง | เหมือนเปิดไฟตอนเข้าห้อง |
| SPA | Single Page Application — แอปที่โหลด HTML ครั้งเดียว | เหมือนบ้าน 1 หลังที่มีหลายห้อง |

---

## สรุปสิ่งที่ได้เรียนรู้ ✅

| หัวข้อ | สิ่งที่เรียนรู้ |
|--------|----------------|
| Vue Router | Library สำหรับจัดการ navigation ในแอป |
| ติดตั้ง Router | `npm install vue-router@4` + `app.use(router)` ใน `main.js` |
| สร้าง Routes | กำหนด `path` + `component` ใน `router/index.js` |
| `<router-view>` | จุดแสดงเนื้อหาที่เปลี่ยนตาม URL |
| `<router-link>` | สร้างลิงก์ที่ไม่ reload หน้า |
| Route Parameter `:id` | รับค่าจาก URL เช่น `/notes/5/edit` → `id = "5"` |
| `$route` vs `$router` | `$route` = อ่านข้อมูล URL / `$router` = สั่งเปลี่ยนหน้า |
| `v-model` | Two-way binding สำหรับ form input |
| `@submit.prevent` | submit form โดยไม่ reload หน้า |

---

> ➡️ **บทถัดไป:** [บทที่ 5: ทดสอบ API ด้วย Postman](./lesson-5-postman.md)
