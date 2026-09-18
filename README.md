# 🎄 Christmas Magic — 手势交互圣诞树

> 用双手点亮一棵圣诞树。握拳成树、张手成银河、双手比心，注视礼盒就能打开藏着照片的礼物。

**🌐 在线体验**：https://你的用户名.github.io/christmas-magic/  
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
