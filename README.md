<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=160&section=header&text=🔐%20密管&fontSize=55&fontColor=fff&animation=fadeIn&fontAlignY=38" width="100%"/>

<div align="center">

**纯本地 · 零服务器 · 开源免费的密码管理器**

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Web](https://img.shields.io/badge/网页版-开箱即用-blue?style=flat-square)](#-在线体验)
[![CLI](https://img.shields.io/badge/命令行版-Python-orange?style=flat-square)](#-命令行版)
[![Crypto](https://img.shields.io/badge/加密-AES--256--GCM-red?style=flat-square)](#-安全设计)

</div>

---

### ✨ 为什么用密管？

- 🔒 **数据永不离开你的设备**——没有服务器，没有账号体系，没有"顺便"上传云端
- 🛡️ **AES-256-GCM 加密**，主密码经 PBKDF2（12 万次迭代）派生密钥
- 🎲 内置密码生成器，一键生成高强度随机密码
- 🔍 秒搜：标题 / 用户名 / 网址模糊搜索
- 💾 加密备份导出 / 导入，换设备不丢数据
- ⏱️ 5 分钟无操作自动锁定
- 📋 一键复制，密码不落地剪贴板历史（网页版）

### 🚀 在线体验

👉 **https://0xtangmengyao.github.io/password/**

打开即用：设一个主密码 → 开始添加你的账号密码。刷新不丢失，全部存在浏览器本地。

### 💻 网页版（单文件）

`index.html` 零依赖、单文件，下载后双击就能在本地跑：

```bash
# 克隆后直接用浏览器打开 index.html
git clone https://github.com/0xtangmengyao/password.git
```

### ⌨️ 命令行版

```bash
pip install cryptography

python pwman.py init          # 初始化保险库
python pwman.py add           # 添加一条密码
python pwman.py list          # 列出所有标题
python pwman.py get github    # 查看某条（含密码）
python pwman.py search mail   # 搜索
python pwman.py gen 20        # 生成 20 位随机密码
python pwman.py del github    # 删除
```

保险库存放在 `~/.pwman/vault.dat`（权限 600），Fernet 加密。

### 🔐 安全设计

| 环节 | 方案 |
|---|---|
| 密钥派生 | PBKDF2-HMAC-SHA256，120k/200k 次迭代 |
| 对称加密 | AES-256-GCM（网页）/ Fernet（CLI） |
| 随机数 | `crypto.getRandomValues` / `secrets` |
| 存储 | 浏览器 localStorage / 本地文件，无网络请求 |

> ⚠️ 主密码丢了谁也找不回来——没有"找回密码"，这就是端到端加密的代价。请务必备份。

### 📁 文件结构

```
password/
├── index.html      # 网页版（单文件，零依赖）
├── pwman.py        # 命令行版（需 cryptography）
└── README.md
```

### 📄 开源协议

MIT — 随便用，欢迎 star ⭐ 和 PR。

---

<div align="center">

⭐ 如果觉得有用，点个 star 就是对我最大的鼓励 ⭐

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>
