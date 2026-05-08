# HANDOFF · moira-music-room

下一份墨拉到这个仓库时，从这里开始读。

## 当前状态（2026-05-08 首迁移）

刚把三份散在 iCloud 的本地工件迁进来，**还没做任何代码改动**。第一次 commit 仅做"搬运 + 文档"。

### qinfang/

冻结状态。墨的琴房 v1，`abcjs@6.6.2` 渲染。原 `Gefeier/moira-music-room` 仓库根目录那一份。除非丽丽明确说要回来加曲子，**不动**。

### workshop/

= `关于墨的记忆相关/创意工坊/` 4/19 锁的 v2。

技术栈：
- p5.js 场景引擎（自写）
- Tone.js + `@strudel/web@1.0.2` ESM 音乐层
- 文字时间线层
- RecipeLab tab：拆配方 → Strudel 实时合成

最后产出：
- `#324` 配方工坊播放高亮（4/10）
- `#321` 《雨天窗台》freecode 模式（4/10）

**已知卡点**：
- 4/10 之后这个 plan 没再动过——配方库本来还要再添几个，丽丽锁定 Lusine/Pogo 采样切片系（见 #316）但没落地
- 「丽丽控制台」想象中是统一入口串联记忆站/快报板/创意工坊/工作台/Notion，没动
- 抽屉记忆四幕动画规划过，没做

### dj-stage/

= `关于墨的记忆相关/打歌台 (Remix)/` 5/8 11:55 从 Claude Design 网页版导出的最新 remix。

style：Apple 深色 + 玫瑰金 accent + 石墨灰层级（详见 index.html `:root` 里那几段注释）。

`screenshots/` 18 张是命名上看像三套并存：
- `paper-final-*` 早期纸张感
- `dj-fixed-*` DJ 台修复迭代
- `apple-*` 当前 Apple 风目标

`uploads/index.html` 是 remix 前的 baseline（3268 行）；`index.html` 是 remix 后（3488 行）。diff 一下能看到这次 remix 改了什么。

**未跑过**：迁过来还没在本地浏览器打开测过，下次接手第一件事是 `python3 -m http.server` 起来肉眼验一遍。

## 下一步建议（按优先级）

1. **跑一遍 dj-stage/ 看视觉是否完整**——Strudel ESM 在 file:// 下会挂，必须 http://
2. **决定 dj-stage 跟 workshop 的关系**——是 workshop 内部的一个 tab 还是独立 stage？现在分两个目录意味着倾向独立
3. **跑一遍 workshop/ RecipeLab**——确认 4/10 的配方库还能播
4. **部署上 Cloudflare Pages**——丽丽其他静态站都是 Pages（moira-divination 等），这个也走一致部署。仓库 settings → Pages → 选 main 分支根目录或 `/dist`
5. **加一个 root `index.html`**作为入口 portal，列三个 stage 卡片，跳子页面

## 不要做

- 不要回头去改 `关于墨的记忆相关/创意工坊/` 或 `关于墨的记忆相关/打歌台 (Remix)/`——从今天起这两个是历史快照
- 不要把 `qinfang/` 删了——是丽丽的早期作品

## 关联记忆

- `memory_read("画像目录")` 找其他工件位置
- work_log `#47` 完整链路
- diary 4/10 配方工坊上线那一篇有"Strudel 找到平衡点"的原话
