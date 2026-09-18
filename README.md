# 🎄 Christmas Magic — 手势交互圣诞树

**中文** | [English](./README.en.md)

> 用双手点亮一棵圣诞树。握拳成树、张手成银河、双手比心，注视礼盒就能打开藏着照片的礼物。

**🌐 在线体验**：https://RayD-123.github.io/christmas-magic/  
（需要摄像头权限，建议使用 Chrome / Edge）

<!-- 动图占位：录好后替换成 ![Demo](assets/demo.gif) -->

---

## ✨ 玩法

| 手势 | 效果 |
|---|---|
| ✊ 握拳 | 圣诞树形态 |
| 🖐️ 张开五指 | 银河形态（粒子散开成星云） |
| ❤️ 双手比心 | 粉色爱心形态 |
| 👀 注视礼盒 2 秒 | 打开礼盒，展示照片 |
| 👌 OK 手势 | 关闭已打开的照片 |
| ✊ 握拳长按 5 秒 | 锁定视角，之后用食指控制 3D 旋转 |
| 📷 Add Photos | 上传照片，变成树上的礼物盒 |

**提示**：添加礼物需要在圣诞树形态下操作；银河形态用来寻找和打开礼物。

---

## 🚀 快速开始

### 在线体验
直接访问 GitHub Pages 链接（见顶部）。

### 本地运行
由于浏览器要求 HTTPS 或 localhost 才能调用摄像头，**直接双击打开 `index.html` 无法使用手势功能**。请用本地服务器：

```bash
# 方法一：Python（大多数系统自带）
python -m http.server 8000
# 然后访问 http://localhost:8000

# 方法二：VS Code 装 Live Server 插件，右键 index.html → Open with Live Server
```

---

## 🛠️ 技术栈

| 技术 | 用途 |
|---|---|
| **Three.js r160** | 3D 渲染引擎，负责场景、相机、光照、材质 |
| **MediaPipe Tasks Vision** | 手部关键点检测（21 个关键点，支持双手） |
| **GLSL Shader** | 自定义粒子系统 + 灯泡独立闪烁效果 |
| **InstancedMesh** | 单次 draw call 渲染上万个灯泡实例 |
| **Web Audio / Canvas** | 背景星空、极光效果 |
| **Pygame + OpenCV** | 最初的原型阶段（已归档到 legacy/） |

**核心技术点**：
- 通过手部关键点计算「手掌张开程度」识别握拳 / 张手 / 双手
- 屏幕中心射线检测（Raycaster）实现注视开盒
- 长按累积 + 优先级打断机制，避免手势冲突
- `onBeforeCompile` 注入 Shader 实现每个灯泡的独立闪烁

---

## 🧭 演进历程

这个项目经历了从 Python 桌面程序到网页 3D 交互的完整迁移，中间踩了不少坑。下面按时间顺序梳理。

| 阶段 | 技术方案 | 解决的问题 | 遗留问题 |
|---|---|---|---|
| 1. Pygame 鼠标原型 | Python + Pygame | 验证「粒子汇聚成树」的视觉可行性 | 没有交互性 |
| 2. 接入手势追踪 | MediaPipe Hands + Pygame | 用食指位置代替鼠标 | Python 帧率低，粒子被迫降到 1200 |
| 3. 迁移到网页 | Three.js + InstancedMesh | 上万粒子流畅渲染 | 只能用鼠标 |
| 4. 手势 + 3D 交互 | MediaPipe Tasks Vision | 握拳/张手/双手切换形态 | 开礼盒操作困难 |
| 5. 注视开盒 + 视角锁定 | Raycaster + 长按累积 | 眼睛看礼盒就能开 | 爱心是绿色的 |
| 6. 粒子系统重构尝试 | Points + 自定义 Shader | 想让叶子更细腻 | 密度不够，z-fighting，回退 |
| 7. 回到 InstancedMesh | onBeforeCompile 注入 | 灯泡独立闪烁 | — |
| 8. 独立爱心配色（最终版） | 粒子颜色随模式切换 | 视觉更贴合主题 | — |

### 阶段 1：Pygame 鼠标原型

最初只是想验证一个视觉想法：上千个粒子能不能从随机位置「流动」成一个圣诞树形状。

实现方式很朴素——用 Pygame 画圆点，鼠标位置作为引力中心，粒子被吸引 + 旋转，形成一个螺旋锥体。虽然简陋，但第一次看到粒子聚成树的瞬间还是挺震撼的。

📄 `legacy/v1_pygame_mouse.py`

### 阶段 2：接入手势

鼠标不够「魔法感」，想让手悬空控制。接入 MediaPipe Hands，取食指指尖坐标映射到屏幕，粒子受力方向由指尖位置决定。

**踩的坑**：Python + MediaPipe 帧率只有 15fps 左右，粒子数被迫从 1500 降到 1200，视觉上稀疏了不少。而且 MediaPipe 早期的 `mp.solutions.hands` API 和 Pygame 的事件循环不好协调，代码里能看到反复注释掉的迭代版本。

📄 `legacy/v2_pygame_handtrack.py`

### 阶段 3：迁移到网页

Python 性能是瓶颈，决定迁移到浏览器。用 Three.js 的 `InstancedMesh` 一次性渲染上万个球体，帧率从 15fps 提到 60fps。

这一版加了礼盒系统：用户可以上传照片，礼盒会挂在树上，鼠标点击打开。但此时还是鼠标操作。

📄 `legacy/v3_threejs_mouse_ai.html`

### 阶段 4：手势 + 3D 交互

把 MediaPipe 的 JS 版（Tasks Vision）接进来，通过计算手掌的「张开程度」（指尖到手腕的距离总和 / 手掌基准长度）来判断握拳、张手、双手：

- 张开程度 < 2.5 → 握拳 → 圣诞树
- 张开程度 > 5.5 → 张手 → 银河
- 检测到 2 只手 → 爱心

**坑**：手势抖动严重。加了 12 帧滑动窗口平均来平滑。

📄 `legacy/v4_gaze_lock.html`

### 阶段 5：注视开盒 + 视角锁定

鼠标点击开礼盒在纯手势场景里很违和。改成**注视检测**——屏幕中心发射射线，命中礼盒后累积 2 秒自动打开。

同时加入**视角锁定**：握拳保持 5 秒后进入锁定状态，之后食指位置映射为树体的 3D 旋转（X 轴俯仰、Y 轴偏航），可以自由查看树的另一面。

**坑**：注视读条和锁定读条会冲突。加了优先级判断——准星瞄准礼盒时强制打断锁定累积。

📄 `legacy/v5_stitched.html`

### 阶段 6：粒子系统重构（尝试）

想让叶子更细腻，把原本的 InstancedMesh 球体换成 `Points` 粒子系统，配合自定义 Shader 绘制圆形光点。

**结果**：视觉确实细腻了，但粒子数降低后整体密度不够，而且和灯泡的混合出现 z-fighting。这个方向最终回退了。

📄 `legacy/v6_particle_refactor.html`

### 阶段 7：回到 InstancedMesh

回退到球体方案，保留闪烁 Shader。通过 `onBeforeCompile` 给每个灯泡实例注入一个 `uTime` 相关的正弦波，实现「每个灯泡独立闪烁」的效果。

📄 `legacy/v7_interaction_ok.html`

### 阶段 8：最终版

在 v7 基础上：
- 添加粉色爱心模式（爱心形态下切换粒子颜色为 Hot Pink）
- 照片自适应宽高比（根据图片实际比例生成边框）
- 调整光球比例，减少视觉噪点

📄 `index.html`

---

## 🧩 关键技术点

### 1. InstancedMesh 渲染上万粒子

`MAX_PARTICLES = 15000` 个球体如果每个都是独立 `Mesh`，draw call 会爆炸。用 `InstancedMesh` 分成 5 类（红复古 / 红璀璨 / 金复古 / 金璀璨 / 银），每类一次 draw call。

```js
meshRedVintage = new THREE.InstancedMesh(sphereGeo, matRedVintage, MAX_PARTICLES);
// 每帧通过 setMatrixAt 更新每个实例的位置
```

### 2. 灯泡独立闪烁（Shader 注入）

用 `onBeforeCompile` 钩子往 MeshPhysicalMaterial 里注入 `gl_InstanceID` 和 `uTime`，让每个灯泡按不同相位闪烁：

```js
shader.fragmentShader = shader.fragmentShader.replace(
  '#include <emissivemap_fragment>',
  `#include <emissivemap_fragment>
   float flashSpeed = 2.0 + mod(vInstanceID, 4.0);
   float twinkle = 0.6 + 0.4 * sin(uTime * flashSpeed + flashOffset);
   totalEmissiveRadiance *= twinkle;`
);
```

### 3. 手势平滑（滑动窗口平均）

原始的手掌张开程度噪声很大，加 12 帧窗口平均：

```js
opennessHistory.push(currentOpenness);
if (opennessHistory.length > HISTORY_LENGTH) opennessHistory.shift();
const avgOpenness = opennessHistory.reduce((a, b) => a + b, 0) / opennessHistory.length;
```

### 4. 注视开盒（Raycaster + 时间累积）

屏幕中心 `(0, 0)` 发射射线，命中礼盒后累积时间，达到 2 秒触发打开：

```js
centerRaycaster.setFromCamera(centerVector, camera);
const intersects = centerRaycaster.intersectObjects(activeGiftMeshes, true);
// 命中后 giftGazeTimer += delta * 1000，达到 GIFT_OPEN_TIME 触发
```

### 5. 锁定读条 + 优先级打断

握拳保持 5 秒进入锁定。但如果准星瞄到了礼盒，就强制打断锁定累积——避免用户想开礼盒时不小心触发锁定：

```js
if (gazeTargetBox !== null) {
    triggerLock = false;
    lockAccumulator = 0;
}
```

### 6. 形态之间的平滑过渡

每种形态（树 / 银河 / 爱心）的目标位置预先算好存在 `shapes` 对象里，每帧用 lerp 让当前位置逼近目标位置，形成流动效果：

```js
currentPositions[ix] += (tPos[ix] * scaleMult - currentPositions[ix]) * speed;
```

---

## 📁 历史版本

所有历史版本保存在 `legacy/` 目录，文件名对应演进阶段：

- `v1_pygame_mouse.py` — Pygame 鼠标原型
- `v2_pygame_handtrack.py` — Pygame + MediaPipe 手势
- `v3_threejs_mouse_ai.html` — 迁移到 Three.js
- `v4_gaze_lock.html` — 手势 + 注视开盒
- `v5_stitched.html` — 外观 + 交互缝合版
- `v6_particle_refactor.html` — 粒子系统重构尝试（已废弃）
- `v7_interaction_ok.html` — InstancedMesh 回退版

---

## 📄 License

MIT License — 随意使用、修改、分发。
