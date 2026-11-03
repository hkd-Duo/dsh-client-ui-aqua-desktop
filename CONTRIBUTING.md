# 贡献指南

感谢你愿意改进这个桌面端主题。这是一个**个人维护**的项目，重点是"能在当前 DSH 桌面版上正常跑"，所以范围有意收窄。

## 项目范围

**欢迎**

- 修复与新版本 DSH 桌面端的兼容问题
- 修复主题本身的视觉/布局 bug
- 改善文档（安装步骤、Windows 说明、排错）
- 补充可复现的验证证据

**不在范围内**

- 新增大型功能（这是主题，不是 IDE）
- 改主题的整体设计语言
- 任何绕过授权、破解、去水印类的需求

## 报告问题

请用 issue 模板：

- **Bug** → `.github/ISSUE_TEMPLATE/bug_report.yml`
- **功能建议** → `.github/ISSUE_TEMPLATE/feature_request.yml`

提 issue 前请先完成 README 里的「装好后的自检」，并在 issue 里贴出自检结果。**没有版本号的 issue 很难处理**，因为不同 DSH 版本行为差异很大。

最少要提供：

| 信息 | 从哪看 |
|---|---|
| DSH 桌面版本 | 应用「关于」或安装包版本 |
| 插件版本 | 插件页 Aqua 卡片，应为 `1.3.1-patch.9-dshfix` |
| 操作系统 | macOS / Windows（附版本） |
| 安装方式 | 插件管理器 `github:` / 本地 `link:` |
| 现象截图 | 界面问题的关键 |

## 本地开发

### 1. 克隆并以本地目录方式安装

```sh
git clone https://github.com/hkd-Duo/dsh-client-ui-aqua-desktop.git
dsh plugin --profile desktop add link:/绝对路径/dsh-client-ui-aqua-desktop
```

`link:` 是软链安装 —— 改文件不用重装。

### 2. 看到改动

| 改了什么 | 怎么生效 |
|---|---|
| `lib/client.js` 里的 CSS/JS | 刷新窗口（macOS `⌘R`） |
| `package.json`（版本、bundle、peer） | 需要**重启应用** |
| `cordis.patch.yml` | 需要**重启应用** |

### 3. 改代码的注意点

- **`lib/` 才是真正运行的产物**，`src/` 只是源码镜像。改完 `lib/` 请同步 `src/`，保持一致。
- 本仓库**没有可用的构建环境**（上游的 monorepo 依赖是 `workspace:^`，无法独立构建），所以是直接改预构建产物。
- 涉及宿主 API 的改动要**兼容降级**，不要直接调用可能不存在的接口：

  ```js
  // 好：能力探测后再用
  if (typeof scope.settings.register === 'function') { ... }

  // 不好：宿主删掉这个 API 就整页崩
  scope.settings.register(...)
  ```

- 改 CSS 选择器时优先用**类名子串匹配**（`[class*='centerCol']`），因为宿主类是 CSS Module 哈希名，每次构建都会变，但语义片段稳定。
- 版本号改动请遵循 `1.3.1-patch.N-dshfix` 的形式，并同步更新两个 README 里的版本号（CI 会检查）。

### 4. 提交前自检

CI 跑的就是这些，本地先跑一遍能省一轮：

```sh
node -e "JSON.parse(require('fs').readFileSync('package.json','utf8'))"   # package.json 合法
node --check lib/client.js && node --check lib/index.js                    # 语法
node -e "const p=require('./package.json'); if(!p.dsh?.bundle?.patch) process.exit(1)"  # bundle patch
node .github/scripts/check-mermaid.mjs                                     # 图表可渲染
grep -nE "dsh plugin --profile web|--profile web " README.md README.zh.md   # 不应有输出
for f in README.md README.zh.md; do grep -q "0.2.1-rc.5" "$f" || echo "缺版本声明: $f"; done
```

### 5. 图表（Mermaid）注意事项

GitHub 是在浏览器端渲染 Mermaid 的，解析失败会显示 **"Unable to render rich display"**。节点标签里**不要**用：

- 双引号 `"`、中文引号 `“”`
- HTML，例如 `<br/>`
- Unicode 箭头 `→` `←`
- emoji `✅` `⚠️`

CI 里的 `check-mermaid.mjs` 会拦住这类写法。

## 提交 PR

1. 从 `main` 拉分支：`git checkout -b fix/短描述`
2. 只改和标题相关的东西，别顺手重构
3. 跑完上面「提交前自检」
4. PR 描述里写清：**改了什么 / 为什么 / 怎么验证的**，附 DSH 版本
5. 如果改了 `lib/`，说明对应的 `src/` 也同步了

## 发布流程（维护者）

```sh
# 1. 改 package.json 版本 + 两个 README 的版本号
# 2. 本地自检通过后提交
git add -A && git commit -m "release: v1.3.1-patch.N"
git push origin main

# 3. 打 tag 并推送 —— Release 由 workflow 自动创建
git tag -a v1.3.1-patch.N -m "dsh-client-ui-aqua v1.3.1-patch.N-dshfix"
git push origin v1.3.1-patch.N
```

推送 tag 后 `.github/workflows/release.yml` 会自动：

- 创建 GitHub Release
- 附上 `lib/client.js` 和 `install.ps1`
- 写入适配版本、安装方式、**自动生成的源码包说明**

## 许可

提交即表示同意你的贡献按本仓库的 **AGPL-3.0-only** 许可发布。
