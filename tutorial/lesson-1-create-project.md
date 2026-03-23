# บทที่ 1: สร้างโปรเจกต์ Vue.js ด้วย Vite

> 📍 **บทที่ 1 / 10** ━━━━━━━━━━ `[██░░░░░░░░]`

| | [สารบัญ](./tutorial.md) | [บทที่ 2: Counter App ➡️](./lesson-2-counter-app.md) |
|:---|:---:|---:|

---

## 🎯 เป้าหมาย

ในบทนี้เราจะ:
- สร้างโปรเจกต์ Vue.js ด้วย Vite
- **รันโปรเจกต์แล้วเห็นผลลัพธ์บนเบราว์เซอร์ทันที**
- ลองแก้โค้ดแล้วเห็นหน้าเว็บอัปเดตอัตโนมัติ (มายากล!)
- ทำความเข้าใจโครงสร้างไฟล์ของโปรเจกต์

> 🎮 **Fun Fact:** Vue.js สร้างโดย Evan You ตอนทำงานที่ Google
> เขาชอบส่วนดีๆ ของ Angular แต่อยากให้มันเบาลง เลยสร้าง Vue ขึ้นมา
> ชื่อ "Vue" มาจากภาษาฝรั่งเศส แปลว่า "มุมมอง" (view) 🇫🇷

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

- ติดตั้ง [Node.js](https://nodejs.org/) เวอร์ชัน 18 ขึ้นไป
- ติดตั้ง Code Editor เช่น [VS Code](https://code.visualstudio.com/)
- เปิด Terminal ได้ (Command Prompt, PowerShell, หรือ Terminal บน Mac)

ตรวจสอบว่าติดตั้ง Node.js แล้ว:

```bash
node --version
```

ถ้าแสดงเลขเวอร์ชัน เช่น `v20.x.x` แสดงว่าพร้อมแล้ว ✅

---

## 📝 ขั้นตอน

### ขั้นตอนที่ 1: สร้างโปรเจกต์ + รัน (ดูผลทันที!)

เปิด Terminal แล้วรันคำสั่งนี้ทีละบรรทัด:

```bash
npm create vite@latest note-app -- --template vue
cd note-app
npm install
npm run dev
```

> 💡 **อธิบายคำสั่ง:**
> | คำสั่ง | ทำอะไร |
> |--------|--------|
> | `npm create vite@latest` | ใช้ Vite สร้างโปรเจกต์ใหม่ |
> | `note-app` | ชื่อโฟลเดอร์ของโปรเจกต์ |
> | `--template vue` | เลือกใช้ template ของ Vue.js |
> | `npm install` | ดาวน์โหลด library ที่โปรเจกต์ต้องใช้ |
> | `npm run dev` | เปิด dev server เพื่อดูเว็บบนเบราว์เซอร์ |

จะเห็นข้อความประมาณนี้ใน Terminal:

```
  VITE v6.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

เปิดเบราว์เซอร์แล้วไปที่ `http://localhost:5173/` 🎉

> 🤔 **ทำไมต้องใช้ Vite?**
>
> ก่อนมี Vite นักพัฒนาใช้ Webpack ซึ่งช้ามากเมื่อโปรเจกต์ใหญ่ขึ้น
> Vite ใช้เทคนิค ES Module ทำให้ dev server **เร็วขึ้น 10-100 เท่า**
>
> ตัวอย่าง: โปรเจกต์ที่ Webpack ใช้เวลา 30 วินาที → Vite ใช้แค่ ~300ms ⚡

#### ✅ ตรวจสอบ
- [ ] Terminal แสดง `VITE ready` ไม่มี error
- [ ] เปิด `http://localhost:5173/` แล้วเห็นหน้าเริ่มต้นของ Vue.js (มีโลโก้ Vue + Vite)
- [ ] เปิด DevTools (กด `F12`) → ไปแท็บ Console → ไม่มีข้อความ error สีแดง

---

### ขั้นตอนที่ 2: ลองแก้โค้ด — เห็นมายากล! ✨

ตอนนี้ dev server กำลังทำงานอยู่ เราจะลองแก้โค้ดแล้วดูว่าเกิดอะไรขึ้น

1. เปิดอีก Terminal tab ใหม่ (อย่าปิด Terminal เดิมที่รัน `npm run dev` อยู่)
2. เปิดโปรเจกต์ใน VS Code:

```bash
code note-app
```

3. เปิดไฟล์ `src/App.vue`
4. ลบโค้ดทั้งหมด แล้วพิมพ์โค้ดนี้แทน:

```vue
<script>
export default {
  data() {
    return {
      message: 'สวัสดี Vue.js! 🎉'
    }
  }
}
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
    <p>นี่คือโปรเจกต์แรกของฉัน</p>
  </div>
</template>

<style>
h1 {
  color: #42b883;
  font-family: Arial, sans-serif;
}
p {
  color: #666;
}
</style>
```

5. **กด `Ctrl+S` (หรือ `Cmd+S` บน Mac) เพื่อบันทึก**
6. **ดูที่เบราว์เซอร์ — หน้าเว็บอัปเดตทันทีโดยไม่ต้อง refresh!** 🤯

> 💡 **นี่คือ Hot Module Replacement (HMR)**
>
> Vite จะตรวจจับว่าไฟล์ถูกแก้ไข แล้วอัปเดตเฉพาะส่วนที่เปลี่ยน โดยไม่ต้อง reload ทั้งหน้า
> ลองแก้ข้อความใน `message` เป็นอย่างอื่นแล้วบันทึกดู จะเห็นว่าเปลี่ยนทันที!

#### ✅ ตรวจสอบ
- [ ] หน้าเว็บแสดง "สวัสดี Vue.js! 🎉" ด้วยสีเขียว
- [ ] แก้ข้อความใน `message` → บันทึก → หน้าเว็บเปลี่ยนทันทีโดยไม่ต้อง refresh
- [ ] เรียบร้อย! คุณเพิ่งเขียน Vue.js ได้สำเร็จ 🎊

---

### ขั้นตอนที่ 3: ทำความเข้าใจโครงสร้างโปรเจกต์

ตอนนี้เราเห็นผลลัพธ์แล้ว มาทำความเข้าใจว่า "สิ่งที่เราทำ" มันทำงานยังไง

```
note-app/
├── index.html          ← 🏠 หน้า HTML หลัก (จุดเริ่มต้นของเว็บ)
├── package.json        ← 📦 รายการ dependencies และ scripts
├── vite.config.js      ← ⚙️ การตั้งค่า Vite
├── src/
│   ├── main.js         ← 🚀 จุดเริ่มต้นของ JavaScript (สร้าง Vue app)
│   ├── App.vue         ← 🧩 Component หลัก (ไฟล์ที่เราเพิ่งแก้!)
│   ├── style.css       ← 🎨 CSS หลัก
│   ├── assets/         ← 🖼️ เก็บไฟล์ static เช่น รูปภาพ
│   └── components/     ← 📂 เก็บ Component ย่อยๆ
```

> 🤔 **ข้อมูลไหลยังไง?**
>
> ```
> เบราว์เซอร์เปิด index.html
>          ↓
> index.html โหลด src/main.js
>          ↓
> main.js สร้าง Vue App จาก App.vue
>          ↓
> App.vue ถูก render ในจอ 🎉
> ```

#### ✅ ตรวจสอบ
- [ ] เปิดโปรเจกต์ใน VS Code แล้วเห็นไฟล์ตามโครงสร้างด้านบน
- [ ] เข้าใจว่า `index.html` → `main.js` → `App.vue` เชื่อมกันยังไง

---

### ขั้นตอนที่ 4: ดูไฟล์หลักที่สำคัญ

#### 📄 `index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + Vue</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

> 💡 **สังเกต 2 จุดสำคัญ:**
> - `<div id="app"></div>` → Vue จะ render ทุกอย่างภายใน div นี้
> - `<script src="/src/main.js">` → โหลดไฟล์ JavaScript หลัก

#### 📄 `src/main.js`

```js
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

> 💡 **อธิบายทีละบรรทัด:**
> | บรรทัด | ทำอะไร |
> |--------|--------|
> | `import { createApp } from 'vue'` | นำเข้าฟังก์ชัน `createApp` จาก Vue |
> | `import App from './App.vue'` | นำเข้า Component หลักจากไฟล์ `App.vue` |
> | `createApp(App)` | สร้าง Vue application โดยใช้ `App` เป็น component หลัก |
> | `.mount('#app')` | เอา Vue app ไปแสดงผลใน `<div id="app">` |

#### 📄 `src/App.vue` — Vue Component

ทุกไฟล์ `.vue` จะมี **3 ส่วน** เสมอ:

```vue
<script>
// ส่วนที่ 1: JavaScript — ข้อมูลและลอจิก 🧠
</script>

<template>
  <!-- ส่วนที่ 2: HTML — โครงสร้างที่จะแสดงบนจอ 🖥️ -->
</template>

<style>
/* ส่วนที่ 3: CSS — ตกแต่งหน้าตา 🎨 */
</style>
```

> 🤔 **ทำไม Vue ถึงรวม 3 อย่างไว้ในไฟล์เดียว?**
>
> ปกติเราจะแยก HTML, CSS, JS เป็นคนละไฟล์ แต่ Vue ใช้แนวคิด **"แยกตาม Component ไม่ใช่ตามภาษา"**
>
> ลองคิดแบบนี้: ถ้าคุณสร้างปุ่ม Button → โค้ด HTML, CSS, JS **ของปุ่มนั้น** ควรอยู่ด้วยกัน เพราะมันเกี่ยวข้องกัน

มาดูโค้ดที่เราเขียนในขั้นตอนที่ 2 อีกครั้ง:

```vue
<script>
export default {
  // data() คืนค่า object ที่เก็บ "ข้อมูล" ของ component นี้
  data() {
    return {
      message: 'สวัสดี Vue.js! 🎉'
    }
  }
}
</script>

<template>
  <div>
    <!-- {{ message }} = แสดงค่าตัวแปร message (เรียกว่า "interpolation") -->
    <h1>{{ message }}</h1>
    <p>นี่คือโปรเจกต์แรกของฉัน</p>
  </div>
</template>

<style>
h1 {
  color: #42b883;
  font-family: Arial, sans-serif;
}
p {
  color: #666;
}
</style>
```

> 💡 **จำไว้ 3 อย่าง:**
> | ส่วน | หน้าที่ | จำง่ายๆ |
> |------|--------|---------|
> | `data()` | เก็บข้อมูล/ตัวแปรที่ใช้ใน component | **สมอง** — เก็บข้อมูล |
> | `{{ }}` | แสดงค่าตัวแปรใน HTML | **ปาก** — พูดข้อมูลออกมา |
> | `<style>` | ตกแต่งหน้าตา | **เสื้อผ้า** — แต่งตัวให้สวย |

#### ✅ ตรวจสอบ
- [ ] เข้าใจว่า `.vue` ไฟล์มี 3 ส่วน: `<script>`, `<template>`, `<style>`
- [ ] เข้าใจว่า `data()` คืนค่า object ที่เก็บข้อมูลของ component
- [ ] เข้าใจว่า `{{ }}` ใช้แสดงค่าตัวแปรจาก `data()` ใน HTML

---

### ขั้นตอนที่ 5: ลบไฟล์ที่ไม่ใช้

ลบไฟล์ที่ Vite สร้างมาแต่เราไม่ต้องการ เพื่อให้โปรเจกต์สะอาด:

```bash
rm src/components/HelloWorld.vue
rm src/assets/vue.svg
rm src/style.css
```

แล้วแก้ไข `src/main.js` — ลบบรรทัด `import './style.css'` ออก:

```js
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

> 💡 **ทำไมต้องลบ?**
> ไฟล์เหล่านี้เป็น template ตัวอย่างของ Vite เราจะสร้างโค้ดของตัวเองตั้งแต่ศูนย์
> การลบไฟล์ที่ไม่ใช้ทำให้โปรเจกต์เข้าใจง่าย ไม่สับสน

#### ✅ ตรวจสอบ
- [ ] ลบ 3 ไฟล์แล้ว ไม่มี `HelloWorld.vue`, `vue.svg`, `style.css`
- [ ] แก้ `main.js` แล้ว ไม่มี `import './style.css'`
- [ ] หน้าเว็บยังแสดง "สวัสดี Vue.js! 🎉" ปกติ

---

## ❌ ปัญหาที่พบบ่อย

### ปัญหา: `npm: command not found`

**สาเหตุ:** ยังไม่ได้ติดตั้ง Node.js

**วิธีแก้:**
1. ไปที่ [nodejs.org](https://nodejs.org/) แล้วดาวน์โหลด LTS version
2. ติดตั้งตามขั้นตอน
3. ปิด Terminal แล้วเปิดใหม่
4. ลองรัน `node --version` อีกครั้ง

---

### ปัญหา: `localhost:5173 refused to connect` หรือเปิดแล้วเห็นหน้าว่าง

**สาเหตุ:** dev server ไม่ได้ทำงาน หรือ port ถูกใช้งานอยู่

**วิธีแก้:**
1. ตรวจสอบว่ารัน `npm run dev` อยู่ใน Terminal
2. ดูว่า Terminal มี error อะไรหรือไม่
3. ลองปิด Terminal แล้วรัน `npm run dev` ใหม่
4. ถ้า port 5173 ถูกใช้อยู่ Vite จะเปลี่ยนเป็น 5174, 5175 — ดูเลข port ใน Terminal

---

### ปัญหา: แก้โค้ดแล้วหน้าเว็บไม่อัปเดต

**สาเหตุ:** ลืม save ไฟล์ หรือไฟล์ถูกแก้ผิดไฟล์

**วิธีแก้:**
1. กด `Ctrl+S` / `Cmd+S` ให้แน่ใจว่า save แล้ว (จุดบน tab ต้องหายไป)
2. ตรวจสอบว่าแก้ไฟล์ `src/App.vue` ไม่ใช่ไฟล์อื่น
3. ดู Terminal ว่ามี error สีแดงหรือไม่
4. ลองปิด dev server (`Ctrl+C`) แล้วรัน `npm run dev` ใหม่

---

### ปัญหา: `Error: Cannot find module...` หลังลบไฟล์

**สาเหตุ:** ลบไฟล์แล้วแต่ยังมี import ในไฟล์อื่น

**วิธีแก้:**
1. อ่าน error ว่าไฟล์ไหนยัง import ไฟล์ที่ลบไป
2. เปิดไฟล์นั้นแล้วลบบรรทัด `import ...` ที่เกี่ยวข้อง
3. บันทึกแล้วดูผลลัพธ์ใหม่

---

## 🏋️ ลองทำเอง (Challenge)

### ⭐ ระดับง่าย
เปลี่ยนสีข้อความ `h1` จากสีเขียว (`#42b883`) เป็นสีอื่นที่ชอบ

### ⭐⭐ ระดับปานกลาง
เพิ่มตัวแปรใหม่ชื่อ `author` ใน `data()` แล้วแสดงด้านล่างข้อความ เช่น "สร้างโดย: [ชื่อ]"

### ⭐⭐⭐ ระดับยาก
สร้าง Component ใหม่ชื่อ `Footer.vue` ในโฟลเดอร์ `src/components/` แล้ว import มาใช้ใน `App.vue`

- Footer ควรแสดงข้อความ "© 2026 Note App"
- ให้ `style` ของ Footer อยู่ด้านล่างของหน้า

<details>
<summary>💡 คำใบ้ระดับง่าย</summary>

แก้ค่า `color` ใน `<style>` — ลองใช้ชื่อสี เช่น `tomato`, `dodgerblue`, หรือรหัสสี เช่น `#ff6347`

</details>

<details>
<summary>💡 คำใบ้ระดับปานกลาง</summary>

ใน `data()` เพิ่ม property ใหม่ใน return object:
```js
data() {
  return {
    message: 'สวัสดี Vue.js! 🎉',
    author: 'ชื่อคุณ'  // ← เพิ่มตรงนี้
  }
}
```
แล้วใน `<template>` ใช้ `{{ author }}` เพื่อแสดงค่า

</details>

<details>
<summary>💡 คำใบ้ระดับยาก</summary>

1. สร้างไฟล์ `src/components/Footer.vue`
2. เขียน `<template>`, `<script>`, `<style>` ในไฟล์นั้น
3. ใน `App.vue` เพิ่ม:

```js
import Footer from './components/Footer.vue'

export default {
  components: { Footer },  // ← ลงทะเบียน component
  data() { ... }
}
```

4. ใน template ใช้ `<Footer />` เพื่อแสดง

</details>

<details>
<summary>✅ ดูเฉลยระดับปานกลาง</summary>

```vue
<script>
export default {
  data() {
    return {
      message: 'สวัสดี Vue.js! 🎉',
      author: 'Tanin'
    }
  }
}
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
    <p>นี่คือโปรเจกต์แรกของฉัน</p>
    <p>สร้างโดย: {{ author }}</p>
  </div>
</template>

<style>
h1 {
  color: #42b883;
  font-family: Arial, sans-serif;
}
p {
  color: #666;
}
</style>
```

</details>

<details>
<summary>✅ ดูเฉลยระดับยาก</summary>

**`src/components/Footer.vue`**
```vue
<template>
  <footer class="app-footer">
    <p>© 2026 Note App</p>
  </footer>
</template>

<style>
.app-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: 16px;
  background-color: #f5f5f5;
  color: #999;
  font-size: 14px;
}
</style>
```

**`src/App.vue`**
```vue
<script>
import Footer from './components/Footer.vue'

export default {
  components: {
    Footer
  },
  data() {
    return {
      message: 'สวัสดี Vue.js! 🎉'
    }
  }
}
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
    <p>นี่คือโปรเจกต์แรกของฉัน</p>
    <Footer />
  </div>
</template>

<style>
h1 {
  color: #42b883;
  font-family: Arial, sans-serif;
}
p {
  color: #666;
}
</style>
```

</details>

---

## 📖 คำศัพท์ที่เรียนรู้ในบทนี้

| คำศัพท์ | ความหมาย | เปรียบเทียบ |
|---------|----------|-------------|
| Vite | เครื่องมือสร้าง + จัดการโปรเจกต์ที่เร็วมาก | เหมือนเครื่องยนต์จรวด — เร็วกว่า Webpack มาก |
| Component | ชิ้นส่วน UI ที่ reuse ได้ (ไฟล์ `.vue`) | เหมือนชิ้น LEGO — ประกอบกันเป็นเว็บ |
| HMR | Hot Module Replacement — อัปเดตหน้าเว็บทันทีเมื่อแก้โค้ด | เหมือนเปลี่ยนยางรถขณะวิ่ง ไม่ต้องจอด |
| `data()` | ฟังก์ชันที่คืนค่า object เก็บข้อมูลของ component | เหมือนสมอง — เก็บข้อมูลที่ component ต้องใช้ |
| Interpolation `{{ }}` | ไวยากรณ์สำหรับแสดงค่าตัวแปรใน HTML | เหมือนช่องว่างในแบบฟอร์ม — เติมค่าตัวแปรลงไป |
| Dependencies | Library ภายนอกที่โปรเจกต์ต้องใช้ | เหมือนวัตถุดิบสำหรับทำอาหาร — ต้องมีก่อนทำ |

---

## สรุปสิ่งที่ได้เรียนรู้ ✅

| หัวข้อ | สิ่งที่เรียนรู้ |
|--------|----------------|
| Vite | เครื่องมือสร้างโปรเจกต์ที่เร็วและทันสมัย |
| โครงสร้างโปรเจกต์ | `index.html` → `main.js` → `App.vue` |
| Vue Component | ไฟล์ `.vue` มี 3 ส่วน: `<script>`, `<template>`, `<style>` |
| Data binding | ใช้ `{{ }}` แสดงข้อมูลจาก `data()` ใน template |
| Hot Reload | แก้โค้ดแล้วเห็นผลทันทีบนเบราว์เซอร์ |
| Clean project | ลบไฟล์ที่ไม่ใช้เพื่อให้โปรเจกต์เข้าใจง่าย |

---

> ➡️ **บทถัดไป:** [บทที่ 2: สร้าง Counter App ด้วย Options API](./lesson-2-counter-app.md)
