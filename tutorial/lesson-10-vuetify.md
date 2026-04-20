# บทที่ 10: ใช้ Vuetify ตกแต่ง UI — จาก HTML ธรรมดาสู่ Material Design

> 📍 **บทที่ 10 / 10** ━━━━━━━━━━ `[██████████]` 🎉

| ⬅️ [บทที่ 9: ลบ Note](./lesson-9-delete-note.md) | [สารบัญ](./tutorial.md) | 🏁 จบ Tutorial |
|:---|:---:|---:|

---

## 🎯 เป้าหมาย

ในบทนี้เราจะ:
- เข้าใจว่า **Vuetify** คืออะไร และ **Material Design** คืออะไร
- ติดตั้ง Vuetify ในโปรเจกต์ Vue.js
- เปลี่ยน **Navbar** ธรรมดาเป็น **App Bar** สวยๆ
- เปลี่ยน **ตาราง HTML** เป็น **Data Table** ของ Vuetify
- เปลี่ยน **ฟอร์ม** ธรรมดาเป็นฟอร์มที่สวยด้วย **Text Field**, **Textarea**, **Checkbox**
- เปลี่ยน **ปุ่ม** ธรรมดาเป็น **Button** ที่มี icon และสี
- ทำให้ทุกหน้า **สวยงาม** แบบ Material Design!

> 🎮 **Fun Fact:** ตลอด 9 บทที่ผ่านมา เราสร้าง CRUD App ที่ทำงานได้ครบสมบูรณ์
> แต่หน้าตายังเป็น HTML ธรรมดา — ในบทนี้เราจะแต่ง UI ให้สวยงามด้วย Vuetify!
>
> ```
> ก่อน: HTML ธรรมดา 😐 → หลัง: Material Design สวยๆ ✨
> ```

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

- ทำบทที่ 9 เสร็จแล้ว (CRUD ครบ 4 ปฏิบัติการ)
- มี **2 Terminal** ทำงาน:
  1. Terminal 1: `npm run dev` (Vue.js — port 5173)
  2. Terminal 2: `uv run python manage.py runserver` (Django — port 8000)
- มี Note อย่างน้อย 2-3 รายการในฐานข้อมูล

> 💡 **ถ้ายังไม่ได้ทำบทก่อนหน้า** สามารถเริ่มจาก branch สำเร็จได้:
> ```bash
> git checkout lesson-9-completed
> ```

---

## 🧠 ทำความเข้าใจก่อนเริ่ม

### Vuetify คืออะไร?

**Vuetify** คือ **UI Component Library** สำหรับ Vue.js — ให้ component สำเร็จรูปที่สวยงามพร้อมใช้

> 💡 **เปรียบเทียบ:**
>
> | เขียน HTML เอง | ใช้ Vuetify |
> |----------------|------------|
> | `<button>บันทึก</button>` | `<v-btn color="primary">บันทึก</v-btn>` |
> | ต้องเขียน CSS เอง | สวยพร้อมใช้ทันที |
> | ต้องทำ responsive เอง | responsive อัตโนมัติ |
> | เหมือนสร้างบ้านจากอิฐทีละก้อน 🧱 | เหมือนซื้อบ้านสำเร็จรูปที่ตกแต่งแล้ว 🏠 |

---

### Material Design คืออะไร?

**Material Design** คือ **ระบบออกแบบ** (Design System) ที่ Google สร้างขึ้น — ใช้ในแอป Google เช่น Gmail, YouTube, Google Maps

Vuetify นำ Material Design มาใช้กับ Vue.js ทำให้แอปของเราดูเหมือนแอป Google!

> 💡 **คุณใช้ Material Design ทุกวันโดยไม่รู้ตัว:**
>
> | แอป | ใช้ Material Design |
> |-----|-------------------|
> | Gmail | ✅ ปุ่ม Compose, Navigation Drawer |
> | YouTube | ✅ App Bar, Cards, ปุ่มแดง Subscribe |
> | Google Maps | ✅ Search Bar, Bottom Sheet |
> | แอปเราหลังบทนี้ | ✅ App Bar, Data Table, Forms! |

---

## 📝 ขั้นตอน

---

## ส่วนที่ 1: ติดตั้ง Vuetify

### ขั้นตอนที่ 1: ติดตั้ง Vuetify

หยุด dev server ก่อน (กด `Ctrl+C` ใน Terminal 1) แล้วรัน:

```bash
npm install vuetify @mdi/font
```

> 💡 **ติดตั้ง 2 อย่าง:**
>
> | Package | ทำอะไร |
> |---------|--------|
> | `vuetify` | UI Component Library |
> | `@mdi/font` | **Material Design Icons** — ไอคอนสวยๆ กว่า 7,000 ตัว เช่น 📝✏️🗑️ |

#### ✅ ตรวจสอบ
- [ ] ติดตั้งสำเร็จ ไม่มี error
- [ ] เปิด `package.json` → เห็น `"vuetify"` และ `"@mdi/font"` ใน `dependencies`

---

### ขั้นตอนที่ 2: ตั้งค่า Vuetify ใน main.js

แก้ไข `src/main.js`:

```js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives
})

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app')
```

> 💡 **อธิบาย:**
>
> | โค้ด | ทำอะไร |
> |------|--------|
> | `import 'vuetify/styles'` | โหลด CSS ของ Vuetify |
> | `import '@mdi/font/css/...'` | โหลด Material Design Icons |
> | `createVuetify({ components, directives })` | สร้าง Vuetify instance พร้อม components ทั้งหมด |
> | `app.use(vuetify)` | ติดตั้ง Vuetify เข้ากับ Vue app |

รัน dev server อีกครั้ง:

```bash
npm run dev
```

เปิดหน้าเว็บ — จะสังเกตว่า **font เปลี่ยน** (Vuetify ใช้ Roboto font) แต่ยังไม่มีอะไรเปลี่ยนมาก

#### ✅ ตรวจสอบ
- [ ] แก้ไข `main.js` ตามโค้ดด้านบน
- [ ] `npm run dev` ทำงานได้ ไม่มี error
- [ ] เปิดหน้าเว็บ → font เปลี่ยน (ตัวอักษรดูต่างจากเดิมเล็กน้อย)

---

## ส่วนที่ 2: ตกแต่ง App.vue — Layout + App Bar

### ขั้นตอนที่ 3: เปลี่ยน App.vue เป็น Vuetify Layout

แก้ไข `src/App.vue`:

```vue
<template>
  <v-app>
    <v-app-bar color="primary">
      <v-app-bar-title>📝 Note App</v-app-bar-title>

      <v-btn to="/notes" variant="text">
        <v-icon start>mdi-format-list-bulleted</v-icon>
        รายการ
      </v-btn>

      <v-btn to="/notes/create" variant="text">
        <v-icon start>mdi-plus</v-icon>
        สร้าง Note
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>
```

**บันทึกแล้วดูที่เบราว์เซอร์!** 🎉

> 💡 **อธิบาย Component ของ Vuetify:**
>
> | Component | ทำอะไร | แทนที่ |
> |-----------|--------|--------|
> | `<v-app>` | Container หลักของ Vuetify — **ต้องครอบทุกอย่าง** | `<div>` |
> | `<v-app-bar>` | แถบด้านบน (Navigation Bar) | `<nav>` |
> | `<v-app-bar-title>` | ชื่อแอปในแถบด้านบน | `<strong>` |
> | `<v-btn>` | ปุ่มที่สวยงามพร้อม ripple effect | `<router-link>` |
> | `<v-icon>` | ไอคอนจาก Material Design Icons | emoji 📋 ➕ |
> | `<v-main>` | พื้นที่เนื้อหาหลัก | `<div>` |
> | `<v-container>` | Container ที่จัดกลาง + กำหนดความกว้าง | ไม่มี |
>
> 🤔 **`mdi-format-list-bulleted` คืออะไร?**
>
> เป็นชื่อ **ไอคอน** จาก Material Design Icons — เขียนแบบ `mdi-ชื่อไอคอน`:
>
> | ชื่อไอคอน | แสดงเป็น | ใช้กับ |
> |-----------|---------|-------|
> | `mdi-format-list-bulleted` | ☰ (รายการ) | หน้ารายการ |
> | `mdi-plus` | ⊕ (บวก) | สร้าง Note |
> | `mdi-pencil` | ✏️ (ดินสอ) | แก้ไข |
> | `mdi-delete` | 🗑️ (ถังขยะ) | ลบ |
> | `mdi-magnify` | 🔍 (แว่นขยาย) | ค้นหา |
>
> ดูไอคอนทั้งหมด: https://pictogrammers.com/library/mdi/

#### ✅ ตรวจสอบ
- [ ] เห็น **แถบสีน้ำเงิน** (App Bar) ด้านบน
- [ ] มีปุ่ม "รายการ" และ "สร้าง Note" พร้อมไอคอน
- [ ] กดปุ่มแล้วเปลี่ยนหน้าได้
- [ ] เห็น **ripple effect** เมื่อกดปุ่ม (วงกลมกระเพื่อม)

---

## ส่วนที่ 3: ตกแต่ง NoteList.vue — Data Table + Search

### ขั้นตอนที่ 4: เปลี่ยน NoteList.vue เป็น Vuetify

แก้ไข `src/views/NoteList.vue` **ทั้งไฟล์:**

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
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <h1 class="text-h4">📋 รายการ Note ทั้งหมด</h1>

      <v-btn color="primary" to="/notes/create">
        <v-icon start>mdi-plus</v-icon>
        สร้าง Note ใหม่
      </v-btn>
    </div>

    <!-- ช่องค้นหา -->
    <v-text-field
      v-model="search"
      label="ค้นหาหัวข้อ..."
      prepend-inner-icon="mdi-magnify"
      variant="outlined"
      clearable
      @keyup.enter="fetchNotes()"
      @click:clear="search = ''; fetchNotes()"
      style="max-width: 400px;"
    />

    <!-- Loading -->
    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <!-- Error -->
    <v-alert v-else-if="error" type="error" variant="tonal">
      {{ error }}
    </v-alert>

    <!-- Empty state (ค้นหาแล้วไม่เจอ) -->
    <v-alert v-else-if="notes.length === 0 && search" type="info" variant="tonal">
      🔍 ไม่พบ Note ที่มีคำว่า "{{ search }}"
    </v-alert>

    <!-- Empty state (ไม่มี Note เลย) -->
    <v-alert v-else-if="notes.length === 0" type="info" variant="tonal">
      📭 ยังไม่มี Note — ลองสร้าง Note ใหม่!
    </v-alert>

    <!-- ตาราง Note -->
    <v-table v-else>
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
          <td>
            <v-chip :color="note.is_done ? 'success' : 'default'" size="small">
              {{ note.is_done ? '✅ เสร็จ' : '⬜ ยังไม่เสร็จ' }}
            </v-chip>
          </td>
          <td>{{ formatDate(note.updated_at) }}</td>
          <td>
            <v-btn size="small" variant="text" color="primary" :to="'/notes/' + note.id + '/edit'">
              <v-icon start>mdi-pencil</v-icon>
              แก้ไข
            </v-btn>
            <v-btn size="small" variant="text" color="error" :to="'/notes/' + note.id + '/delete'">
              <v-icon start>mdi-delete</v-icon>
              ลบ
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>

    <!-- จำนวนรายการ -->
    <p v-if="!loading && !error" class="text-grey mt-2">
      แสดง {{ notes.length }} รายการ
    </p>
  </div>
</template>
```

**บันทึกแล้วดูที่เบราว์เซอร์!**

> 💡 **Component ใหม่ที่ใช้:**
>
> | Component | ทำอะไร | แทนที่ |
> |-----------|--------|--------|
> | `<v-text-field>` | ช่อง input สวยๆ พร้อม label และ icon | `<input>` + `<button>` |
> | `<v-progress-linear>` | แถบ loading ที่วิ่งไปมา | `<p>⏳ กำลังโหลด...</p>` |
> | `<v-alert>` | กล่องข้อความแจ้งเตือนสีสวย | `<p style="color: red;">` |
> | `<v-table>` | ตารางที่สวย มีเส้นขอบและ hover effect | `<table border="1">` |
> | `<v-chip>` | ป้ายเล็กๆ แสดงสถานะ (เหมือน tag) | `✅` / `⬜` ธรรมดา |
> | `<v-btn>` | ปุ่มสวยพร้อม icon | `<router-link>` |
>
> 🤔 **`variant` คืออะไร?**
>
> เป็นรูปแบบการแสดงผลของ component:
>
> | variant | ลักษณะ | ใช้เมื่อ |
> |---------|--------|---------|
> | `"outlined"` | มีขอบ ไม่มีพื้นหลัง | ช่อง input, ปุ่มรอง |
> | `"tonal"` | มีพื้นหลังอ่อนๆ | alert, chip |
> | `"text"` | ไม่มีขอบ ไม่มีพื้นหลัง | ปุ่มใน toolbar |
>
> 🤔 **`clearable` คืออะไร?**
>
> เพิ่มปุ่ม ✕ ใน text field เพื่อล้างค่า — เราใช้ `@click:clear` เพื่อเรียก `fetchNotes()` เมื่อกดล้าง

#### ✅ ตรวจสอบ
- [ ] เห็นช่องค้นหาสวยๆ พร้อมไอคอน 🔍
- [ ] เห็น loading bar วิ่งขณะโหลด
- [ ] เห็นตารางสวย มี hover effect เมื่อชี้เมาส์
- [ ] สถานะแสดงเป็น chip สี (เขียว/เทา)
- [ ] ปุ่มแก้ไข/ลบ มีไอคอนและสี
- [ ] ค้นหา + กดล้าง ทำงานได้

---

## ส่วนที่ 4: ตกแต่ง NoteCreate.vue — Form สวยๆ

### ขั้นตอนที่ 5: เปลี่ยน NoteCreate.vue เป็น Vuetify

แก้ไข `src/views/NoteCreate.vue` **ทั้งไฟล์:**

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
    <h1 class="text-h4 mb-4">➕ สร้าง Note ใหม่</h1>

    <v-card max-width="600">
      <v-card-text>
        <v-text-field
          v-model="title"
          label="หัวข้อ"
          placeholder="ใส่หัวข้อ"
          variant="outlined"
          :error-messages="errors.title"
        />

        <v-textarea
          v-model="body"
          label="เนื้อหา"
          placeholder="ใส่เนื้อหา"
          variant="outlined"
          rows="5"
          :error-messages="errors.body"
        />
      </v-card-text>

      <v-card-actions>
        <v-btn color="primary" @click="submitForm" :loading="loading">
          <v-icon start>mdi-content-save</v-icon>
          บันทึก
        </v-btn>

        <v-btn variant="text" to="/notes">
          ยกเลิก
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
```

> 💡 **Component ใหม่ที่ใช้:**
>
> | Component | ทำอะไร | แทนที่ |
> |-----------|--------|--------|
> | `<v-card>` | กล่องสวยๆ มีเงา (shadow) | `<form>` + `<div>` |
> | `<v-card-text>` | พื้นที่เนื้อหาใน card | `<div>` |
> | `<v-card-actions>` | พื้นที่ปุ่มใน card | `<div>` |
> | `<v-text-field>` | ช่อง input สวยๆ | `<label>` + `<input>` |
> | `<v-textarea>` | ช่อง textarea สวยๆ | `<label>` + `<textarea>` |
>
> 🤔 **`:error-messages` คืออะไร?**
>
> เป็น prop ของ `v-text-field` ที่แสดง **validation error สีแดง** ใต้ช่อง input:
>
> | ก่อน (HTML ธรรมดา) | หลัง (Vuetify) |
> |-------------------|----------------|
> | `<p v-if="errors.title" style="color: red;">{{ errors.title[0] }}</p>` | `:error-messages="errors.title"` |
> | ต้องเขียน HTML + CSS เอง | Vuetify จัดการให้ทั้งหมด! |
>
> 🤔 **`:loading` ของ `v-btn` คืออะไร?**
>
> เมื่อ `loading = true` ปุ่มจะ:
> 1. แสดง **loading spinner** อัตโนมัติ
> 2. **ปิดปุ่ม** ไม่ให้กดซ้ำ
>
> ไม่ต้องเขียน `:disabled` และ ternary (`loading ? '⏳...' : '💾...'`) อีกแล้ว!

#### ✅ ตรวจสอบ
- [ ] เห็นฟอร์มอยู่ใน **card** สวยๆ มีเงา
- [ ] ช่อง input มี label ลอยขึ้นเมื่อ focus
- [ ] กดบันทึก → เห็น loading spinner ในปุ่ม
- [ ] ส่งหัวข้อว่าง → เห็น error สีแดงใต้ช่อง input
- [ ] กรอกครบ + กดบันทึก → redirect ไปหน้ารายการ

---

## ส่วนที่ 5: ตกแต่ง NoteEdit.vue

### ขั้นตอนที่ 6: เปลี่ยน NoteEdit.vue เป็น Vuetify

แก้ไข `src/views/NoteEdit.vue` **ทั้งไฟล์:**

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
    <h1 class="text-h4 mb-4">✏️ แก้ไข Note #{{ noteId }}</h1>

    <!-- Loading -->
    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <!-- Error -->
    <v-alert v-else-if="error" type="error" variant="tonal">
      {{ error }}
    </v-alert>

    <!-- ฟอร์มแก้ไข -->
    <v-card v-else max-width="600">
      <v-card-text>
        <v-text-field
          v-model="title"
          label="หัวข้อ"
          variant="outlined"
          :error-messages="errors.title"
        />

        <v-textarea
          v-model="body"
          label="เนื้อหา"
          variant="outlined"
          rows="5"
          :error-messages="errors.body"
        />

        <v-checkbox
          v-model="is_done"
          label="เสร็จแล้ว"
          color="success"
        />
      </v-card-text>

      <v-card-actions>
        <v-btn color="primary" @click="submitForm" :loading="saving">
          <v-icon start>mdi-content-save</v-icon>
          บันทึก
        </v-btn>

        <v-btn variant="text" to="/notes">
          ยกเลิก
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
```

> 💡 **Component ใหม่ที่ใช้:**
>
> | Component | ทำอะไร | แทนที่ |
> |-----------|--------|--------|
> | `<v-checkbox>` | checkbox สวยๆ พร้อม label | `<input type="checkbox">` + `<label>` |
>
> `<v-checkbox>` สวยกว่า HTML checkbox มาก — มี animation + สีสัน + ขนาดที่พอดี

#### ✅ ตรวจสอบ
- [ ] เปิดหน้าแก้ไข → เห็นข้อมูลเดิมในฟอร์ม Vuetify
- [ ] checkbox `เสร็จแล้ว` ทำงานได้
- [ ] กดบันทึก → เห็น loading spinner → redirect
- [ ] ลองส่งหัวข้อว่าง → เห็น error ใต้ช่อง

---

## ส่วนที่ 6: ตกแต่ง NoteDelete.vue

### ขั้นตอนที่ 7: เปลี่ยน NoteDelete.vue เป็น Vuetify

แก้ไข `src/views/NoteDelete.vue` **ทั้งไฟล์:**

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
    <h1 class="text-h4 mb-4">🗑️ ยืนยันการลบ</h1>

    <!-- Loading -->
    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <!-- Error -->
    <v-alert v-else-if="error" type="error" variant="tonal">
      {{ error }}
    </v-alert>

    <!-- ข้อมูล Note + ปุ่มยืนยัน -->
    <v-card v-else-if="note" max-width="600">
      <v-card-title>คุณต้องการลบ Note นี้ใช่หรือไม่?</v-card-title>

      <v-card-text>
        <v-table density="compact">
          <tbody>
            <tr>
              <th style="width: 100px;">หัวข้อ</th>
              <td>{{ note.title }}</td>
            </tr>
            <tr>
              <th>เนื้อหา</th>
              <td>{{ note.body || '(ไม่มีเนื้อหา)' }}</td>
            </tr>
            <tr>
              <th>สถานะ</th>
              <td>
                <v-chip :color="note.is_done ? 'success' : 'default'" size="small">
                  {{ note.is_done ? '✅ เสร็จแล้ว' : '⬜ ยังไม่เสร็จ' }}
                </v-chip>
              </td>
            </tr>
          </tbody>
        </v-table>

        <v-alert type="warning" variant="tonal" class="mt-4">
          ⚠️ การลบไม่สามารถกู้คืนได้!
        </v-alert>
      </v-card-text>

      <v-card-actions>
        <v-btn color="error" @click="confirmDelete" :loading="deleting">
          <v-icon start>mdi-delete</v-icon>
          ยืนยันลบ
        </v-btn>

        <v-btn variant="text" to="/notes">
          ยกเลิก
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
```

> 💡 **Component ใหม่ที่ใช้:**
>
> | Component | ทำอะไร |
> |-----------|--------|
> | `<v-card-title>` | หัวข้อของ card |
> | `<v-alert type="warning">` | กล่องเตือนสีส้ม |
> | `<v-btn color="error">` | ปุ่มสีแดง — บอกว่าเป็น destructive action |
> | `density="compact"` | ทำให้ตารางชิดกันมากขึ้น |

#### ✅ ตรวจสอบ
- [ ] เห็น card สวยๆ พร้อมข้อมูล Note
- [ ] เห็น warning alert สีส้ม
- [ ] ปุ่มลบเป็น**สีแดง**
- [ ] กดยืนยันลบ → เห็น loading spinner → redirect
- [ ] กดยกเลิก → กลับหน้ารายการ

---

## ส่วนที่ 7: ทดสอบทุกหน้า

### ขั้นตอนที่ 8: ทดสอบ CRUD ทั้งหมดกับ UI ใหม่

**ทดสอบ CRUD ครบวงจร:**

1. **หน้ารายการ** (`/notes`):
   - เห็น App Bar สีน้ำเงินด้านบน
   - เห็นตาราง + chip สถานะ + วันที่
   - ค้นหาใช้ได้ + ปุ่มล้าง (✕) ทำงาน

2. **สร้าง Note** (`/notes/create`):
   - กด **สร้าง Note** ใน App Bar
   - เห็นฟอร์มใน card สวยๆ
   - กรอกข้อมูล + กดบันทึก → redirect

3. **แก้ไข Note** (`/notes/:id/edit`):
   - กด **แก้ไข** ในตาราง
   - เห็นข้อมูลเดิมในฟอร์ม
   - ติ๊ก checkbox เสร็จแล้ว + กดบันทึก → สถานะเปลี่ยน

4. **ลบ Note** (`/notes/:id/delete`):
   - กด **ลบ** ในตาราง
   - เห็นข้อมูล Note ใน card
   - กดยืนยันลบ → Note หายจากรายการ

> 🎉 **ทุกอย่างทำงานเหมือนเดิม — แต่สวยขึ้นมาก!**

#### ✅ ตรวจสอบ
- [ ] Create → สร้าง Note ได้
- [ ] Read → ดูรายการ + ค้นหาได้
- [ ] Update → แก้ไข Note ได้
- [ ] Delete → ลบ Note ได้
- [ ] UI สวยงาม ✨

---

## สรุปโค้ดทั้งหมดในบทนี้

ไฟล์ที่แก้ไขในบทนี้:

| ไฟล์ | สิ่งที่เปลี่ยน |
|------|---------------|
| `src/main.js` | เพิ่ม Vuetify setup |
| `src/App.vue` | เปลี่ยน Navbar → App Bar |
| `src/views/NoteList.vue` | เปลี่ยนตาราง → v-table + v-text-field + v-chip |
| `src/views/NoteCreate.vue` | เปลี่ยนฟอร์ม → v-card + v-text-field + v-btn |
| `src/views/NoteEdit.vue` | เปลี่ยนฟอร์ม → v-card + v-checkbox + v-btn |
| `src/views/NoteDelete.vue` | เปลี่ยนข้อมูล → v-card + v-alert + v-btn |

---

## ❌ ปัญหาที่พบบ่อย

### ปัญหา: เปิดหน้าเว็บแล้วเห็น error `[Vuetify] Could not find defaults instance`

**สาเหตุ:** ไม่ได้ใส่ `<v-app>` ครอบทุก component

**วิธีแก้:** ตรวจว่า `App.vue` มี `<v-app>` ครอบทุกอย่าง:
```vue
<template>
  <v-app>    <!-- ← ต้องมี! -->
    ...
  </v-app>
</template>
```

---

### ปัญหา: ไอคอนไม่แสดง เห็นแค่ข้อความ `mdi-pencil`

**สาเหตุ:** ไม่ได้ import `@mdi/font`

**วิธีแก้:** ตรวจว่า `main.js` มี:
```js
import '@mdi/font/css/materialdesignicons.css'
```

และตรวจว่าติดตั้ง `@mdi/font` แล้ว:
```bash
npm install @mdi/font
```

---

### ปัญหา: แอปแสดงผลแบบเก่า ไม่มี Vuetify style

**สาเหตุ:** ไม่ได้ import Vuetify styles หรือไม่ได้ `app.use(vuetify)`

**วิธีแก้:** ตรวจ `main.js`:
```js
import 'vuetify/styles'                    // ← ต้องมี
import { createVuetify } from 'vuetify'    // ← ต้องมี
// ...
app.use(vuetify)                           // ← ต้องมี
```

---

### ปัญหา: `v-text-field` ไม่แสดง error message

**สาเหตุ:** ใช้ `errors.title[0]` แทน `errors.title`

**วิธีแก้:**
```vue
<!-- ❌ ผิด — ส่ง string ไม่ใช่ array -->
:error-messages="errors.title ? errors.title[0] : ''"

<!-- ✅ ถูก — Vuetify รับ array ได้โดยตรง! -->
:error-messages="errors.title"
```

Vuetify `v-text-field` รับ `error-messages` เป็น **array** ได้เลย — ไม่ต้อง `[0]`!

---

### ปัญหา: `npm run dev` ช้าลงหลังติดตั้ง Vuetify

**สาเหตุ:** ปกติ! Vuetify มี component เยอะ ตอน dev อาจใช้เวลาโหลดนานขึ้นเล็กน้อย

**วิธีแก้:** สามารถใช้ **tree-shaking** import เฉพาะ component ที่ใช้ แทน `import * as components`:

```js
// แบบ import ทั้งหมด (ง่าย แต่ bundle ใหญ่)
import * as components from 'vuetify/components'

// แบบ import เฉพาะที่ใช้ (เร็วกว่า — สำหรับ production)
import { VApp, VBtn, VCard, ... } from 'vuetify/components'
```

สำหรับ Tutorial นี้ใช้แบบ import ทั้งหมดก็ได้ — ไม่เป็นปัญหา!

---

## 🏋️ ลองทำเอง (Challenge)

### ⭐ ระดับง่าย
เปลี่ยน **ธีมสี** ของ App Bar:
- ลองเปลี่ยน `color="primary"` เป็น `color="teal"` หรือ `color="deep-purple"`
- ลองเพิ่ม `dark` attribute ใน `<v-app-bar>`
- ดูรายชื่อสีทั้งหมด: https://vuetifyjs.com/en/styles/colors/

### ⭐⭐ ระดับปานกลาง
เพิ่ม **Snackbar** แจ้งเตือนแทน `alert()`:
- ใช้ `<v-snackbar>` ของ Vuetify แสดงข้อความสำเร็จ/error
- เพิ่มตัวแปร `snackbar: false` และ `snackbarMessage: ''`
- แทนที่ `alert('...')` ด้วย `this.snackbarMessage = '...'; this.snackbar = true`

### ⭐⭐⭐ ระดับยาก
ทำ **Dark Mode Toggle** — ปุ่มสลับโหมดมืด/สว่าง:
- เพิ่มปุ่มใน App Bar: `<v-btn icon @click="toggleTheme"><v-icon>mdi-theme-light-dark</v-icon></v-btn>`
- ใช้ `useTheme()` composable ของ Vuetify
- เก็บ preference ไว้ใน `localStorage` เพื่อให้จำค่าเมื่อ refresh

<details>
<summary>💡 คำใบ้ระดับง่าย</summary>

Vuetify มีสีให้เลือกเยอะมาก:

```vue
<!-- ลองเปลี่ยน color -->
<v-app-bar color="teal">       <!-- สีเขียวอมฟ้า -->
<v-app-bar color="deep-purple"> <!-- สีม่วงเข้ม -->
<v-app-bar color="indigo">     <!-- สีคราม -->
<v-app-bar color="pink">       <!-- สีชมพู -->
```

ลองเปลี่ยนสีปุ่มด้วย:
```vue
<v-btn color="success">   <!-- สีเขียว -->
<v-btn color="warning">   <!-- สีส้ม -->
<v-btn color="info">      <!-- สีฟ้า -->
```

</details>

<details>
<summary>💡 คำใบ้ระดับปานกลาง</summary>

เพิ่มใน `data()`:
```js
snackbar: false,
snackbarMessage: '',
snackbarColor: 'success'
```

แทนที่ `alert('...')`:
```js
// แทนที่
alert('ไม่สามารถเชื่อมต่อ Backend ได้')

// ด้วย
this.snackbarMessage = 'ไม่สามารถเชื่อมต่อ Backend ได้'
this.snackbarColor = 'error'
this.snackbar = true
```

เพิ่มใน template:
```vue
<v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
  {{ snackbarMessage }}
  <template v-slot:actions>
    <v-btn variant="text" @click="snackbar = false">ปิด</v-btn>
  </template>
</v-snackbar>
```

`v-snackbar` จะแสดงข้อความแจ้งเตือนที่ด้านล่างของหน้าจอ แล้วหายไปอัตโนมัติหลัง 3 วินาที

</details>

<details>
<summary>💡 คำใบ้ระดับยาก</summary>

ใน `App.vue` เพิ่ม:

```vue
<script>
import { useTheme } from 'vuetify'

export default {
  setup() {
    const theme = useTheme()

    // โหลด preference จาก localStorage
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      theme.global.name.value = savedTheme
    }

    function toggleTheme() {
      const newTheme = theme.global.current.value.dark ? 'light' : 'dark'
      theme.global.name.value = newTheme
      localStorage.setItem('theme', newTheme)
    }

    return { toggleTheme }
  }
}
</script>
```

เพิ่มปุ่มใน `<v-app-bar>`:
```vue
<v-btn icon @click="toggleTheme">
  <v-icon>mdi-theme-light-dark</v-icon>
</v-btn>
```

**หมายเหตุ:** ใช้ `setup()` ซึ่งเป็น Composition API — แตกต่างจาก Options API ที่เราเรียนมาทั้ง Tutorial
นี่คือตัวอย่างว่า Vue.js มี 2 แบบ: Options API (ที่เราใช้) และ Composition API (แบบใหม่)
จะเรียนเพิ่มเติมได้ใน Vue.js documentation!

</details>

---

## 📖 คำศัพท์ที่เรียนรู้ในบทนี้

| คำศัพท์ | ความหมาย | เปรียบเทียบ |
|---------|----------|-------------|
| Vuetify | UI Component Library สำหรับ Vue.js | เหมือนชุดเฟอร์นิเจอร์สำเร็จรูป — สวยพร้อมใช้ |
| Material Design | ระบบออกแบบของ Google | เหมือนแบบพิมพ์เขียวของสถาปนิก — กำหนดกฎการออกแบบ |
| v-app | Container หลักที่ Vuetify ต้องการ | เหมือนกรอบรูป — ต้องมีก่อนใส่รูป |
| v-btn | ปุ่มพร้อม ripple effect, icon, loading | เหมือนปุ่มลิฟต์สวยๆ — กดแล้วมีไฟกระพริบ |
| v-card | กล่องเนื้อหาที่มีเงา | เหมือนกระดาษลอยอยู่บนโต๊ะ — มีเงาด้านล่าง |
| v-text-field | ช่อง input พร้อม label ลอย + validation | เหมือนช่องกรอกในแบบฟอร์มราชการ — สวย เป็นระเบียบ |
| v-chip | ป้ายเล็กๆ แสดงข้อมูลย่อ | เหมือน tag ราคาสินค้า — เล็ก กะทัดรัด มีสี |
| v-alert | กล่องข้อความแจ้งเตือน | เหมือนป้ายประกาศ — มีสีตามประเภท (error=แดง, warning=ส้ม) |
| variant | รูปแบบการแสดงผลของ component | เหมือนสีเสื้อ — เลือกได้ว่าจะเป็นแบบไหน |
| MDI | Material Design Icons — ชุดไอคอนของ Google | เหมือนสติ๊กเกอร์ emoji — เลือกแปะได้ตามใจ |

---

## สรุปสิ่งที่ได้เรียนรู้ ✅

| หัวข้อ | สิ่งที่เรียนรู้ |
|--------|----------------|
| Vuetify Setup | ติดตั้ง Vuetify + MDI Icons แล้วตั้งค่าใน main.js |
| v-app + v-app-bar | สร้าง layout หลักพร้อม Navigation Bar สวยๆ |
| v-text-field + v-textarea | ช่อง input ที่มี label ลอย + validation error อัตโนมัติ |
| v-btn + :loading | ปุ่มพร้อม loading spinner อัตโนมัติ — ไม่ต้องเขียน disabled/ternary |
| v-table + v-chip | ตารางสวย + ป้ายสถานะสี |
| v-card | จัดกลุ่มเนื้อหาในกล่องที่มีเงา |
| v-alert | แสดง error/warning/info สวยๆ แทน `<p style="color: red;">` |
| Material Design | ระบบออกแบบที่ทำให้แอปดูเป็นมืออาชีพ |

---

## 🎉 ยินดีด้วย!! คุณเรียนจบ Tutorial แล้ว!

คุณได้เรียนรู้ตั้งแต่ **สร้างโปรเจกต์เปล่า** จนถึง **CRUD App สมบูรณ์ที่สวยงาม** ด้วย Vuetify!

```
บทที่  1: สร้างโปรเจกต์ Vue.js           ✅
บทที่  2: Counter App                    ✅
บทที่  3: ทำความเข้าใจ Error              ✅
บทที่  4: Vue Router                     ✅
บทที่  5: ทดสอบ API ด้วย Postman          ✅
บทที่  6: สร้าง Note (Create)             ✅
บทที่  7: แสดงรายการ Note (Read)          ✅
บทที่  8: แก้ไข Note (Update)             ✅
บทที่  9: ลบ Note (Delete)               ✅
บทที่ 10: ตกแต่ง UI ด้วย Vuetify          ✅
```

### 🚀 สิ่งที่ควรเรียนต่อ

| หัวข้อ | ทำไม | แหล่งเรียน |
|--------|------|-----------|
| **Composition API** | วิธีเขียน Vue แบบใหม่ที่ยืดหยุ่นกว่า | [Vue.js Docs](https://vuejs.org/guide/extras/composition-api-faq.html) |
| **Pinia** | State Management สำหรับแอปที่ซับซ้อน | [Pinia Docs](https://pinia.vuejs.org/) |
| **Axios** | HTTP client ที่ใช้แทน fetch() | [Axios Docs](https://axios-http.com/) |
| **Authentication** | ระบบ login/logout สำหรับผู้ใช้ | JWT + Django REST Framework |
| **Deployment** | นำแอปขึ้น server จริง | Docker, Nginx, Gunicorn |

> 💪 **ขอให้สนุกกับการเขียนโปรแกรม — คุณทำได้!** 🎉
