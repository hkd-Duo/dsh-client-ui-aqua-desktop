# dsh-client-ui-aqua —— DSH 桌面端玻璃主题

![version](https://img.shields.io/badge/version-1.3.1--patch.9--dshfix-blue)
![DSH](https://img.shields.io/badge/DSH-0.2.1--rc.5-green)
![platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey)
![license](https://img.shields.io/badge/license-AGPL--3.0--only-orange)

装到 DSH 桌面应用上，界面立刻变成磨砂玻璃：顶栏、侧边栏、输入框、统计行、轨迹视图都变成悬浮玻璃片，背景可以是流动流体板，也可以是你自己的壁纸。关掉总开关就完全还原原生界面。

[English](README.md) | 中文

---

## ⚡ 一眼看懂

| 项目 | 值 |
|---|---|
| **适配桌面版本** | **DSH 0.2.1-rc.5**（已实测 ✅） |
| **插件版本** | `1.3.1-patch.9-dshfix` |
| **适用平台** | macOS ✅ ／ Windows ✅（安装方式相同） |
| **安装方式** | 插件管理器填入 `github:hkd-Duo/dsh-client-ui-aqua-desktop` |
| **必须做的一步** | 装完**完全退出应用**再重开（否则不加载） |
| **默认状态** | 装完主题**自动开启** |

### 安装流程图

```mermaid
flowchart TD
    A[打开 DSH 桌面应用] --> B[设置 - 插件 - 插件管理器]
    B --> C[点添加插件]
    C --> D[填入 GitHub 安装标识]
    D --> E[等待安装完成]
    E --> F[完全退出应用]
    F --> G[重新打开应用]
    G --> H{界面变成玻璃效果}
    H -- 是 --> I[安装成功]
    H -- 否 --> J[检查版本 1.3.1-patch.9-dshfix]
    J --> F
```

### 版本适配矩阵

| DSH 桌面版本 | 状态 | 说明 |
|---|---|---|
| **0.2.1-rc.5** | ✅ **已实测** | 本仓库当前适配基线 |
| 0.2.1-rc.3 | ⚠️ 未实测 | 上游修补分支的验证基线 |
| 0.2.0 / 0.1.7 系列 | ⚠️ 未实测 | peer 声明允许，但未跑过 |
| 0.1.2-rc.1 及更早 | ❌ 不适用 | 旧内核，API 已变 |

---

## 一、安装步骤

### 方式 A：插件管理器（推荐，macOS / Windows 通用）

1. 打开 **DSH 桌面应用**
2. 进入 **设置 → 插件 → 插件管理器（Plugin Manager）**
3. 点 **添加插件（Add plugin）**
4. 输入：`github:hkd-Duo/dsh-client-ui-aqua-desktop`
5. 等待安装完成
6. **完全退出应用**再重新打开（macOS `⌘Q`；Windows 托盘右键 → 退出）
7. 界面应立刻变成玻璃质感

> 第 6 步不能省：插件会把自己写进 profile 的 bundle 列表，宿主只在启动时读取。

### 方式 B：本地目录（开发/调试）

适合改源码或离线安装；改完只需刷新窗口（macOS `⌘R`），不用重装。

```sh
git clone https://github.com/hkd-Duo/dsh-client-ui-aqua-desktop.git
dsh plugin --profile desktop add link:/绝对路径/dsh-client-ui-aqua-desktop
```

- macOS 例：`link:/Users/你的用户名/dsh-client-ui-aqua-desktop`
- Windows 例：`link:C:\Users\你的用户名\dsh-client-ui-aqua-desktop`

路径必须是**绝对路径**，相对路径会被拒绝。Windows 上没有 `dsh` 命令也没关系，用方式 A 即可。

---

## 二、具体文件位置

### 目录结构图示

```mermaid
flowchart LR
    P[desktop profile 根目录] --> P1[package.json 里的 bundle 注册]
    P --> N[node_modules]
    N --> A[dsh-client-ui-aqua]
    A --> A1[lib/client.js 插件入口]
    A --> A2[package.json 版本 1.3.1-patch.9-dshfix]
    A1 --> D1[主题设置存于 localStorage]
```

### macOS

| 内容 | 路径 |
|---|---|
| 应用本体 | `/Applications/DeepSeek Harness.app` 或 `~/Applications/DeepSeek Harness.app` |
| desktop profile 根目录 | `~/.dsh/profiles/desktop/` |
| **插件本体** | `~/.dsh/profiles/desktop/node_modules/dsh-client-ui-aqua/` |
| 插件入口文件 | `~/.dsh/profiles/desktop/node_modules/dsh-client-ui-aqua/lib/client.js` |
| **bundle 注册位置** | `~/.dsh/profiles/desktop/package.json` → `dsh.profile.bundles` 应含 `dsh-client-ui-aqua` |
| 应用数据目录 | `~/Library/Application Support/@deepseek-ai/dsh-desktop/` |
| **主题设置存储** | 上述目录下 `Local Storage/leveldb/` 内的 `dsh.ui-aqua.*` 键 |
| 应用自带 CLI | `/Applications/DeepSeek Harness.app/Contents/Resources/runtime/cli/bin/dsh` |

### Windows

| 内容 | 路径 |
|---|---|
| 应用本体 | 由安装器决定（开始菜单快捷方式 → 右键 → **打开文件所在位置** 可确认） |
| desktop profile 根目录 | `%USERPROFILE%\.dsh\profiles\desktop\` |
| **插件本体** | `%USERPROFILE%\.dsh\profiles\desktop\node_modules\dsh-client-ui-aqua\` |
| 插件入口文件 | `%USERPROFILE%\.dsh\profiles\desktop\node_modules\dsh-client-ui-aqua\lib\client.js` |
| **bundle 注册位置** | `%USERPROFILE%\.dsh\profiles\desktop\package.json` → `dsh.profile.bundles` |
| 应用数据目录 | `%APPDATA%\@deepseek-ai\dsh-desktop\` |
| **主题设置存储** | 上述目录下 `Local Storage\leveldb\` 内的 `dsh.ui-aqua.*` 键 |

### 装好后的自检（两条都成立）

1. 插件页里 Aqua 的版本显示 **`1.3.1-patch.9-dshfix`**
2. `package.json` 的 `dsh.profile.bundles` 里有 **`dsh-client-ui-aqua`**

---

## 三、使用步骤

### 1. 总开关

**设置 → 插件 → Aqua 卡片**，里面是总开关。主题**装完默认开启**；关掉后所有效果移除，界面还原原生。

### 2. 调参数

**设置 → 通用设置 → 外观**（在「外观」区块正下方，没有独立标题）：

| 控件 | 作用 |
|---|---|
| 模式 | **云母（Mica）**= 悬浮玻璃卡片布局；**兼容模式**= 保留原版排版，只换材质 |
| 模糊度 / 磨砂度 | 云母模式下玻璃的模糊与磨砂强度 |
| 色调 / 颜色深浅 | 流体背景的色相与深浅 |
| 背景亮度 | 深色模式压暗（0–50）、浅色模式提亮（50–100），50 为原样 |
| 背景来源 | 流体板 / 自定义壁纸（壁纸另带模糊度、亮度、删除） |
| 粒子鲸鱼 | 聊天区中央的粒子鲸鱼开关 |

总开关关闭时，整块调节会自动隐藏。

### 3. 切换模式

| 模式 | 效果 | 适合 |
|---|---|---|
| **云母（Mica）** | 侧栏/顶栏/输入框变成悬浮玻璃卡片 | 想要最强观感 |
| **兼容模式** | 不改布局，只把材质换成玻璃 | 怕布局变化、或与其它插件共存 |

在「外观 → 模式」里切换，立即生效。

### 4. 更新

插件管理器里点更新 → **重启应用**。`link:` 安装的则 `git pull` 后刷新窗口（`⌘R`）。

### 5. 卸载

```sh
dsh plugin --profile desktop remove dsh-client-ui-aqua
```

或在插件管理器里卸载，然后**重启应用**。所有效果都是可释放的 effect，移除即回收。

---

## 四、Windows 支持

**可以，安装方式与 macOS 完全一致，不需要改任何东西。**

理由：

1. 插件是纯客户端产物（`dsh.client.platform = "web"`），桌面应用在各平台加载**同一份前端代码**
2. 本仓库的修复不含 macOS 专属逻辑 —— 透明规则用 `[class*='centerCol']`、`[class*='rightbarCol']` 这类**类名子串匹配**，Windows 上同样是这些类名
3. 桌面端专用的主栏背景修复本身就覆盖 Windows 自定义标题栏模式
4. 安装标识 `github:hkd-Duo/dsh-client-ui-aqua-desktop` 两端完全一样

平台差异只有路径（见上表）和 `link:` 安装要用 `C:\...` 绝对路径。

**Windows 自证三点：**

| 检查 | 期望 |
|---|---|
| 插件页版本 | `1.3.1-patch.9-dshfix` |
| 界面效果 | 明显磨砂玻璃（侧栏、输入框） |
| 调节项 | 设置 → 通用设置 → 外观 下方出现 Aqua 控件 |

三条都成立即正常工作。

> **⚠️ Windows 用户注意：鲸鱼/流体/点阵看起来是"静止的"？**
>
> 如果系统关闭了「动画效果」（设置 → 辅助功能 → 视觉效果 → 动画效果），Chromium/Electron 会向网页上报
> `prefers-reduced-motion: reduce`，本主题会按无障碍规范**只渲染静态帧**：粒子鲸鱼不游动、鼠标移上去不响应，
> 背景流体和网状点阵也不再流动（小鱼/气泡是 CSS 动画，不受影响）。
>
> **这不是插件故障。** 打开「动画效果」即可恢复（或 `SystemPropertiesPerformance.exe` → 视觉效果 → 自定义，
> 勾选"在窗口内动画控件和元素"等），然后重新加载客户端 / 重启应用（插件在挂载时读取该偏好）。
> 毛玻璃、配色、壁纸等其他功能不受影响。
>
> 快速自检：在客户端 DevTools 控制台执行 `matchMedia('(prefers-reduced-motion: reduce)').matches`，
> 返回 `true` 即说明系统"减少动态"生效中。

---

## 五、更新记录

| 版本 | 内容 |
|---|---|
| `patch.2` | 修复外观行渲染崩溃（React #130）；修复启动时报 `settings.register` 不存在 |
| `patch.3` | 修复主对话区被不透明容器盖住、只剩毛玻璃没有流体 |
| `patch.4` | 修复开启主题后「插件」页点击无反应 |
| `patch.5` | 放宽 peer 版本范围，适配新版 DSH |
| `patch.6` | 会话列表时间戳改用无衬线体 + 等宽数字 |
| `patch.7` | （已废弃）曾调整大表面透明度，非根因 |
| `patch.8` | 修复兼容模式右侧聊天区发糊：兼容模式模糊规则不再作用于布局面板 |
| `patch.9` | 适配 0.2 设置入口（`plugins.bundle.config`）、空页头排除、输入框悬停横向滚动条修复 |

---

## 六、两种不要装的形式

**1. npm 裸包名**

```sh
dsh plugin --profile desktop add dsh-client-ui-aqua   # ← 未经修补的旧版
```

该名称解析到旧发布版，在当前 DSH 线会报错。

**2. 没有 bundle patch 的包**

插件管理器只管理组合包，`package.json` 里缺少 `dsh.bundle.patch` 声明的包会在安装前直接被拒绝。本仓库已包含该声明，可正常安装。

---

## 七、运行行为

- 无网络请求、无文件/凭据访问、无 `eval`、无遥测
- 状态只存于 `localStorage` 的 `dsh.ui-aqua.*` 键
- 安装过程不执行任何构建脚本（`lib/` 随包提供预构建产物）

## 八、Release 产物与源码包

每个 Release 页面（[查看全部版本](https://github.com/hkd-Duo/dsh-client-ui-aqua-desktop/releases)）包含两类东西：

### 1. 工作流上传的产物

| 文件 | 用途 |
|---|---|
| `client.js` | 实际运行的前端 bundle，可用于审计或手动比对 |
| `install.ps1` | 上游辅助脚本，仅作出处保留 |

### 2. GitHub 自动生成的源码包

Release 页底部的 **`Source code (zip)`** 和 **`Source code (tar.gz)`** 是 **GitHub 自动生成**的，不是工作流上传的：

- 内容是**该 tag 对应的完整仓库快照**（含 `src/`、`lib/`、全部文档）
- 适合审计、归档，或完全离线安装
- 下载后**无需构建** —— `lib/` 已经是预构建产物

**从源码包离线安装：**

1. 下载 `Source code (tar.gz)` 并解压
2. 以本地目录方式安装（必须绝对路径）：

   ```sh
   dsh plugin --profile desktop add link:/解压后的绝对路径
   ```

3. 完全退出应用后重新打开

## 九、参与贡献

- 提交问题前先读 [贡献指南](CONTRIBUTING.md)
- 请使用 [Issue 模板](https://github.com/hkd-Duo/dsh-client-ui-aqua-desktop/issues/new/choose) —— 会自动要求填写 DSH 版本、插件版本、自检结果
- 本地开发方式、提交前自检命令、PR 流程、发布流程都写在 [CONTRIBUTING.md](CONTRIBUTING.md)

## 截图

![](assets/1.png)

![](assets/2.png)

![](assets/3.png)

![](assets/4.png)

## 许可证

本仓库沿用上游 `LICENSE`（**AGPL-3.0-only**）。若 AGPL 与你的使用场景不相容，请不要安装。
