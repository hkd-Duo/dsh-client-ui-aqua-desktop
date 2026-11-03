# dsh-client-ui-aqua —— 桌面端（DSH 0.1.7-rc.2 / 0.2.0-rc.2 / macOS）修复

基线：`github:Aliww2468/dsh-client-ui-aqua-patched`（`1.3.1-patch.1`，为 DSH **0.1.2-rc.1** 修复）
本版：`1.3.1-patch.5`

安装目标：DSH 桌面应用 `desktop` profile（已验证 DSH **0.1.7-rc.2** 与 **0.2.0-rc.2**，macOS / darwin）

---

## 改动总览

| 版本 | 问题 | 改动 |
|---|---|---|
| `patch.2` | 外观行渲染即崩（React #130），设置里没有任何 Aqua 调节项 | `lib/client.js` 6 行：`IconCheckOutline16` → `IconCheckOutlineRegular` |
| `patch.2` | 宿主半调用已删除的 `settings.register`，每次启动报错 | `lib/index.js` 改为 no-op |
| `patch.3` | 桌面端主对话区被不透明容器盖住，只剩毛玻璃、没有流体和鲸鱼 | `lib/client.js` 1 行 CSS：补齐并提权"刷透明"规则 |
| **`patch.4`** | **开启主题后「插件」页点击无反应（页面永不挂载）** | seam 重盖 observer 改为默认关闭；节流 + 诊断开关 |
| **`patch.5`** | **DSH 升到 0.2.0-rc.2 后插件被判「不兼容」，无法安装/启用** | 只改 `package.json`：版本号 + 8 个 `@deepseek-ai/dsh*` peer 范围；**代码零改动** |

---

## patch.5 详细：为什么升级 DSH 后插件突然「不兼容」

### 症状

DSH 桌面应用升级到 **0.2.0-rc.2** 后，侧栏「插件」页把本插件标为「异常」：

```
dsh-client-ui-aqua@1.3.1-patch.4 与 DSH 0.2.0-rc.2 不兼容
（要求 @deepseek-ai/dsh-client-locale ^0.1.0-rc.5, @deepseek-ai/dsh-client-store ^0.1.2-rc.1,
  @deepseek-ai/dsh-client-ui-primitives ^0.1.0-rc.5, … @deepseek-ai/dsh-invariants ^0.1.0-rc.5）
运行它可能导致崩溃或数据丢失。请卸载后重新安装与当前 DSH 兼容的版本。
```

### 根因：宿主整包跨了小版本

0.2.0-rc.2 把**所有** `@deepseek-ai/dsh-client-*` 与 `dsh-invariants` 一并发布为 `0.2.0-rc.2`
（从 `app.asar` 内逐包解包核对，60+ 个包版本号一致）。插件声明的是 `^0.1.0-rc.5` / `^0.1.2-rc.1`，
按 semver `^0.1.x` 上界是 `<0.2.0`，于是 8 个 peer **全部**判不满足。

判定实现在 `@deepseek-ai/dsh-app-boot` 的 `evaluatePluginCompatibility()`：

```js
if (name !== "@deepseek-ai/dsh" && !name.startsWith("@deepseek-ai/dsh-")) continue;
if (!semver.satisfies(runtimeVersion, requirement, { includePrerelease: true })) peers[name] = range;
```

两点值得记住：

1. **只校验 `@deepseek-ai/dsh*` 前缀的 peer** —— 这正是报错里只有那 8 个、而没有
   `@deepseek-ai/cordis` 和 `react` 的原因（后两者虽然也不满足也从不参与判定）。
2. 这是**纯声明层**判定，不读插件代码、不探测 API。所以「代码还能不能跑」与「被判不兼容」是两件事。

### 「重装兼容版本」是死路

报错文案建议换一个兼容版本，但上游 `dsh-client-ui-aqua` 在 npm 上只有 `1.3.0` 和 `1.3.1`
（已查注册表），两者 peer 范围与本 fork 相同，**没有任何版本适配 0.2.0-rc.2**。
因此唯一出路是本地对齐声明。

### 改动（只有 `package.json`）

| 字段 | 旧 | 新 |
|---|---|---|
| `version` | `1.3.1-patch.4` | `1.3.1-patch.5` |
| 8 个 `@deepseek-ai/dsh-*` peer | `^0.1.0-rc.5` / `^0.1.2-rc.1` | `>=0.1.7-rc.2 <0.3.0` |

`lib/` 下的代码**一行未改**：patch.4 的行为已在 0.1.7-rc.2 实测通过，而 0.2.0-rc.2 的宿主 API
经逐项核对仍然齐备（见下）。范围取 `>=0.1.7-rc.2 <0.3.0` 是因为实测覆盖这两个运行时，
`^0.2.0-rc.2` 会把仍能工作的 0.1.7-rc.2 一并挡掉。

### 验证：离线复算宿主的判定函数

不重新实现判定逻辑，而是从 `app.asar` 里按 SHA256 校验解出 `@deepseek-ai/dsh-app-boot`，
按花括号配平**原样切出** `evaluatePluginCompatibility()` 及其 helpers，配上宿主同款 `semver@7.8.5`
复算。对照组（patch.4 的原范围）必须复现用户看到的报错，否则这套复算不可信：

| 用例 | 运行时 | 结果 |
|---|---|---|
| 对照：patch.4 原范围 | `0.2.0-rc.2` | **不兼容，8 个 peer** —— 与用户报错逐条一致 ✅ |
| patch.5 | `0.2.0-rc.2` | 兼容（无 issue）✅ |
| patch.5（回归） | `0.1.7-rc.2` | 兼容（无 issue）✅ |

复算脚本：`.inspect-020/verify-compat.mjs`（本机工作区内，非交付物）。

### 0.2.0-rc.2 宿主 API 逐项核对（代码为何仍可用）

| patch | 依赖点 | 0.2.0-rc.2 状态 |
|---|---|---|
| patch.2 | `IconCheckOutlineRegular`（primitives） | ✅ 仍导出 |
| patch.2 | 宿主半 `settings.register` | ✅ 已是 no-op，无影响 |
| patch.3 | `[data-platform=darwin] .centerCol{background:var(--dsw-alias-bg-base)}` | ✅ **不透明规则仍在，修复依然必要** |
| patch.3 | `centerCol` / `rightbarCol` / `frame` 类名子串 | ✅ 仍在 |
| patch.3 | `_pane_` / `_tabHost_` 类名子串 | ⚠️ 已归零 → 该两条选择器成死规则（无害） |
| patch.4 | `document.documentElement` MutationObserver | ✅ 与 DSH 版本无关 |
| — | `dsh-client-store` 的 `defineStore` | ✅ 仍在导出中 |
| — | `theme.getTheme` / `overrideTokens`、`slots.inject` / `register`、`locale.register` | ✅ 全部仍在 |
| — | `settings.general.item`（真正旋钮所在行） | ✅ 仍在 |
| — | `settings.plugin.item`（总开关卡片） | ❌ 仍不存在 → 注入静默失效（`slots.inject` 只在槽位被声明后触发），不影响加载 |

另注：`dsh-client-runtime` 在 0.2.0-rc.2 中**已被移除**，由 `dsh-client-store` 取代 ——
本 fork 自 patch.4 起注入的正是 `dsh-client-store`，而 npm 上的 `1.3.1` 仍要求
`dsh-client-runtime`，所以 web profile 里那份 `1.3.1` 在 0.2.0-rc.2 上同样不可用。

### 备选方案：官方精确版本豁免（本次未采用）

宿主提供 `compatibility.json` 豁免：`{"dsh-client-ui-aqua@1.3.1-patch.4": ["0.2.0-rc.2"]}`。
但 0.2.0-rc.2 的 `desktop` profile 只能由 Electron 应用管理，CLI 被
`rejectElectronProfile` 硬编码拒绝，而**所有 `dsh-client-*` 客户端包都没有调用豁免 API**
（已全量扫描确认），应用内也没有豁免入口 —— 只能手写该文件。既然声明本就可以对齐现实，
就没有必要引入一个「已知错误但被豁免」的状态。

---

## patch.4 详细：插件页被 seam observer 打死

### 症状

主题（玻璃 + 流体 + 鲸鱼）全部正常，但侧栏点「插件」**完全无反应**——页面不挂载，控制台只有一条与本插件无关的 `net::ERR_FAILED`（已确认插件不发起任何网络请求）。

### 定位过程

`off.stamper` 开关（只停 observer、保留首次盖属性）→ **插件页恢复正常**；`off.decor`（停全部装饰层）也正常。据此排除：

| 排除项 | 依据 |
|---|---|
| 点击被覆盖层吞掉 | ambient / mesh / whale / glow / fade **全部** `pointer-events:none` |
| 外部资源失败 | 插件 CSS 只有 base64 内嵌字体，**零外部 `url()`**；页面自身零 `fetch`/XHR |
| React 根被破坏 | aqua 注入的节点是 `#root` 的**兄弟**（body 下），不在 React 树内 |
| 扫描太慢 | 48k 节点下单次扫描仅 6.9ms；限到 4 次/秒**仍然坏** |
| 属性名与 DSH 冲突 | `data-dsh-surface` 等 8 个 seam 属性名 **DSH 0.1.7 全部未使用**（aqua 自造） |

### 根因

`startSeamStamper()` 挂了一个**监听整个文档**的 `MutationObserver`：

```js
observer.observe(document.documentElement, { childList: true, subtree: true });
```

它**在每次 React 提交后立即回写 14 组 seam 属性**。限流无效说明**机制是"回写"本身，不是频率**。

### 改动

- **observer 默认关闭**：`startSeamStamper()` 只在挂载时盖一次属性
  （`stampAll()` 保留——用户确认这个状态下主题外观正常）
- 需要旧行为时：`localStorage['dsh.ui-aqua.on.stamper'] = '1'`
- 诊断开关保留：`dsh.ui-aqua.off.stamper`（连首次盖章也停）、`dsh.ui-aqua.off.decor`（停全部装饰层）

```js
function startSeamStamper() {
  if (!shouldSkip("stamper")) stampAll();          // 首次盖章：保留
  if (!shouldEnable("stamper")) return () => {};   // observer：默认关闭
  ...
}
```

### 验证

用户实测：`off.stamper`（= 首次盖章 + 无 observer）→ **主题正常 + 插件页可打开**。
本版把这个配置固化为代码默认值，不再依赖 localStorage。

---

## patch.3 详细：为什么桌面端只有毛玻璃

### 症状

- 侧栏有青绿流体，**主对话区是一整块纯深色**，鲸鱼完全看不见
- 浏览器版宿主一切正常
- 所有客观指标正常：层已挂载、canvas 有尺寸、`opacity:1`、动画循环在跑、WebGL2 可用、`prefers-reduced-motion: false`、canvas 内容非空（PNG 130 万字符）

### 根因：一条只在桌面壳生效的 CSS 规则

DSH 布局包 `dsh-client-ui-layout` 的 `AppFrame.module.css` 里：

```css
.P9Gu9a_frame{background:var(--dsw-alias-bg-base)}         /* 不透明 */
[data-platform=darwin] .P9Gu9a_frame{background:0 0}        /* macOS 上被特意改透明 */
[data-platform=darwin] .P9Gu9a_centerCol{
  background:var(--dsw-alias-bg-base);                      /* ← 但中间列没有，保持不透明 */
  border-left:.5px solid var(--dsw-alias-border-l3)
}
```

`data-platform="darwin"` 这个属性 **只有 Electron 桌面壳会设置**（由 `dsh-web-frontend` 的引导流程写入 `<html>`）；浏览器版宿主不设。因此：

| | `<html data-platform>` | `.centerCol` 背景 |
|---|---|---|
| 浏览器版宿主 | 无此属性 | `rgba(0,0,0,0)` 透明 → 流体可见 ✅ |
| **桌面端 macOS** | `darwin` | `rgb(12,18,27)` 不透明 → **流体被盖住** ❌ |

Aqua 的背景层是负层级方案（`[data-dsh-aqua-ambient]{z-index:-1}`），必须靠"把上层容器刷透明"才能露出来。而插件原有的那条规则在 0.1.7 上**大部分是死规则**：

```css
[data-dsh-aqua] [data-dsh-frame],      /* 0.1.7 中该属性已不存在（0 处引用） */
[data-dsh-aqua] [data-phase],          /* 仍存在 */
[data-dsh-aqua] [data-dsh-details]     /* 0.1.7 中该属性已不存在 */
{background:0 0}
```

### 改动（1 行 CSS，在 `lib/client.js` 的 `css$1` 字符串内）

在原规则末尾补上 0.1.7 真正的不透明容器，并**重复属性选择器提权**：

```css
[data-dsh-aqua] [class*='centerCol'][class*='centerCol'],
[data-dsh-aqua] [class*='rightbarCol'][class*='rightbarCol'],
[data-dsh-aqua] [class*='_pane_'][class*='_pane_'],
[data-dsh-aqua] [class*='_tabHost_'][class*='_tabHost_']
{background:0 0}
```

**为什么必须提权**：DSH 的 `[data-platform="darwin"] .P9Gu9a_centerCol` 特异性是 `(0,2,0)`，与单写一份属性选择器的 `[data-dsh-aqua] [class*='centerCol']` **平手**；而 DSH 的样式表在文档中更靠后，平手时后者胜出——实测确认规则匹配上了却被打败。重复一次属性选择器把特异性提到 `(0,3,0)` 即可稳定胜出。

> 这不是自创新手法：插件自己就用同样的写法处理过 `composerSeat`：
> `[data-dsh-aqua] [data-phase] [class*=composerSeat][class*=composerSeat]{background:0 0}`

用 `class*=` 子串匹配而非硬编码类名，是因为这些是 CSS Module 的**哈希类名**（`P9Gu9a_`、`_1s7ij_`），每次构建都会变；子串部分（`centerCol`、`rightbarCol`、`_pane_`、`_tabHost_`）是稳定的。

### 验证

在临时 profile 上，**运行时把 `<html data-platform>` 设为 `darwin`** 即可复现桌面端条件（CSS 立即重算）：

| | 无属性（浏览器版宿主） | `darwin`（桌面端） |
|---|---|---|
| 修复前 `.centerCol` | `rgba(0,0,0,0)` | **`rgb(12,18,27)`** |
| 修复后 `.centerCol` | `rgba(0,0,0,0)` | **`rgba(0,0,0,0)`** ✅ |

截图证据见 `../evidence/`：

- `desktop-covered-BEFORE-fix.png` —— 主对话区纯深色，无流体无鲸鱼（== 用户看到的）
- `desktop-fixed-AFTER-fix.png` —— 青绿流体铺满全窗口 + 中央鲸鱼点阵 + 网状点阵

---

## patch.2 详细：设置面板缺失

### 图标被改名 → 外观行渲染即崩（致命）

DSH 0.1.7 把 UI primitives 的图标命名从 `Icon*16` 改为 `Icon*Outline{Artwork,Regular,Medium}`，
`IconCheckOutline16` 已不存在。外观行渲染到 `undefined` → React error #130 → 槽位宿主记录
`slot entry crashed in 'settings.general.item'` 并**丢弃整行**。

改为 `IconCheckOutlineRegular`（默认 16px / 1px 描边，与旧的 `...16` 等价），共 6 处：
第 69、683、701、719、747、764 行。

### 宿主半调用已删除的 API

`lib/index.js` 原调用 `scope.settings.register(...)`。0.1.7 的 `@deepseek-ai/dsh-settings`
已完全重写（不再有"设置命名空间注册表"，改由插件自己的 Loader Config 投影生成设置表单），
该 API 不存在，每次启动打印：

```
[ui-aqua] settings namespace skipped: TypeError: scope.settings.register is not a function
```

改为 no-op，失效原因写入注释。

### 已知限制（有意未做）

原版把「玻璃主题」总开关注册进 `settings.plugin.item`。该槽位在 0.1.7 已**整体移除**，
0.1.7 的对应机制是 `plugins.bundle.config`（以组合包包名为 key）。迁移需重写卡片组件
（0.1.7 里 `store` 选项语义已变为 scope 句柄，不再给组件 `useStore`），**本版未做**。

**关闭主题的办法**：侧栏「插件」→ 关闭 `dsh-client-ui-aqua` 的开关（或卸载）。

---

## 安装（桌面端）

桌面端 profile 被 Electron 壳独占，**CLI 无法管理**——`dsh plugin --profile desktop ...`
被硬编码拒绝：`profile "desktop" is managed exclusively by the Electron application`。
必须走应用内 UI：

1. 侧栏 **「插件」** → **「添加插件」**
2. 在「包名或地址」里填**绝对路径**，两种写法等价，宿主都归为 `kind: "path"`：
   - `/Users/avocado/dsh-plugin-work/dsh-client-ui-aqua-desktop`
   - `link:/Users/avocado/dsh-plugin-work/dsh-client-ui-aqua-desktop`
3. 安装源保持默认。此包**无构建脚本**，不会要求授权
4. 装完 **「立即启用」**（会写入 `dsh.profile.bundles`）
5. 重新加载客户端即可（已在运行时，HMR 会拉新模块；必要时重启应用）

> **别被「插件安装引导和示例」误导**：那一栏里的
> `https://github.com/author/dsh-plugin` 只是**示例模板**（对应的 hint 是
> `installGitTemplateHint`「请替换为实际的 Git 仓库地址」），点「填入示例」会把它填进输入框。
> 路径模板是第三条 `/Users/name/my-plugin`（`installPathTemplateHint`）。
> 判定在宿主 `plugin-manager/lib/index.js` 的 `parseInstallSpec()`：
> `if (path !== spec || isAbsolute(path))` → `kind: "path"`；
> **相对路径会被拒**（`a local path must be absolute`），因为安装面板里输入的 cwd 没有意义。
> 而且 `parseInstallSpec` 的注释说明了原因，`anchorPathSpec` 也只锚定 `.`/`..` 开头的相对路径。

> **安装即启用**：`installBundle(spec, options)` 的 `options.activate` **默认 true**，
> 装完会直接走 `selectBundle(name, true)` 追加进 `dsh.profile.bundles`，
> 所以「立即启用」通常只是确认动作，不是必要步骤。
>
> **path 是唯一会预检的类型**：`namedSpecManifest()` 里 `kind === "path"` 会直接读本地
> `package.json` 并跑 `evaluatePluginCompatibility()`；`registry` 走 `pnpm view`；
> 而 **git / tarball 直接 `return undefined`，不做兼容性预检**（启动时那次检查仍然会跑）。

#### 等价的手工安装（本次实际执行方式）

应用内 UI 与手工执行最终是同一件事 —— 用**应用自带**的 pnpm 在 profile 里跑 `pnpm add`。
注意必须用应用同款版本（`runtime/primary-runtime/runtime.json` 记录 node 24.21.0 / pnpm 11.7.0），
否则锁文件格式会和应用打架：

```sh
D=~/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies
"$D/node/bin/node" "$D/pnpm/bin/pnpm.mjs" add \
  "link:/Users/avocado/dsh-plugin-work/dsh-client-ui-aqua-desktop"
# cwd 必须是 ~/.dsh/profiles/desktop
```

然后手工往 `~/.dsh/profiles/desktop/package.json` 的 `dsh.profile.bundles` 追加
`"dsh-client-ui-aqua"`（等价于 `selectBundle`；它会追加到数组末尾）。**不需要改任何 YAML** ——
组合包 patch 是启动时由 `loadProfileDirectory()` 从 `dsh.profile.bundles` 在内存里合成的。

> **同名包重复安装会被拒绝**：`dsh-plugin-manager/lib/index.js:1586` 有
> `if (known.has(inspection.name)) return refused("already-installed", ...)`。
> 换版本前需先卸载。

### 升级到本版

本版是 `link:` 引用本地目录，**直接用新文件覆盖即生效**，不需要重新安装，只需重新加载客户端
（必要时重启桌面应用）。若从 github 版换过来，先卸载再按上面步骤安装。

> **patch.4 → patch.5 的当前情况**：patch.4 在升级到 DSH 0.2.0-rc.2 时已被判不兼容并**卸载**
> （desktop profile 的 `package.json` / `pnpm-lock.yaml` / `cordis.patch.yml` 均已不含它）。
> 因此本次需要**重新安装一次**，不能只靠覆盖文件。装完确认「插件」页出现
> `dsh-client-ui-aqua` 且**不再有「异常」标记**，再启用。

### 回滚

侧栏「插件」→ 卸载 `dsh-client-ui-aqua` → 重启。所有视觉效果都是可释放的 effect。

### 注意

- 安装以**本地路径**引用本目录，**不要移动或删除**
- 与 web profile 里的 `dsh-client-ui-aqua@1.3.1` 互不影响（profile 隔离）
- 本修复绑定 **0.1.7-rc.2 / 0.2.0-rc.2** 的 API 与 CSS 形状；其他版本需复验（判定依据见 patch.5 一节）
- 上游 AGPL-3.0-only，本修复沿袭

---

## 未验证 / 已知限制

- 未逐个点测全部旋钮；已验证：调节项渲染、模式切换写入 localStorage、装饰开关生效
- 视频壁纸、自定义图片壁纸（data URL 存 localStorage）的大文件配额行为未测
- 插件卡片（总开关）未迁移，见上文；0.2.0-rc.2 中 `settings.plugin.item` 仍不存在，
  注入静默失效，不影响加载
- **patch.5 的声明层修复已离线复算通过，但 0.2.0-rc.2 上的实际渲染尚未实测**：
  需重装后确认主题生效、主对话区不被不透明容器盖住
- `_pane_` / `_tabHost_` / `composerSeat` 三条选择器在 0.2.0-rc.2 已成死规则；
  0.2.0-rc.2 的 layout 类名只剩 `centerCol` / `frame` / `handle` / `leadingSeat` /
  `overlayLayer` / `rightbarCol` / `sidebarCol`，其中需要刷透明的两个（`centerCol`、
  `rightbarCol`）已被覆盖。若实测发现新容器盖住流体，再补选择器
- 仅在 DSH 0.1.7-rc.2 与 0.2.0-rc.2 验证；0.1.5-rc.3（CLI Web profile）未测
- 右侧栏（`rightbarCol`）已一并刷透明，但未实际打开右栏验证
