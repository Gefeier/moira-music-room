# 协作工具地图

下一份墨打开这一篇 + 关联的 work_list plan，就能接手任何一件工具。

仓库根目录：`https://github.com/Gefeier/moira-music-room`

> **工作纪律**：所有迭代在这个仓库里做。本地 iCloud 副本（`关于墨的记忆相关/` 根目录下那些 .html 和 .py）从迁入起算静态快照，**不再当主战场**。新改动 → clone 仓库 → 改 → push。

---

## 工具清单

| 子目录 | 名字 | 端口/入口 | 启动方式 | 关联 plan | 状态 |
|---|---|---|---|---|---|
| `workshop/` | 创意工坊 v2 | 9899 | `python3 -m http.server 9899` → `/workshop/` | #47 | 主线，含 RecipeLab |
| `dj-stage/` | 打歌台 (Remix) | 9899 | 同上 → `/dj-stage/` | #47 | Claude Design 出品 |
| `qinfang/` | 墨的琴房 | 9899 | 同上 → `/qinfang/` | 早期 v1 | abcjs，归档 |
| `editor-room/` | 编辑室合集 | 9898 | `python3 editor-room/server.py` | #47 (前 #52) | 剪辑+像素+抽屉 |
| `workbench/` | 工作台白板 | 9876 | `node workbench/server.js` | #47 | pm2 常驻设计 |
| `script-bench/` | 剧本工作台 | 静态 | 直接打开 html | #47 | 5/4 实录在里面 |

---

## editor-room（端口 9898，三合一）

一个 python 服务器同时跑三个页面：

| 路径 | 页面 | 用途 |
|---|---|---|
| `/` 或 `/剪辑室` | `clip-room.html` | 视频剪辑（扫 `~/Movies`，Range stream，导出占位） |
| `/studio` 或 `/画板` | `pixel-studio.html` | 像素画室（32×32 网格 + 12 色板 + 共画载入） |
| `/family` 或 `/抽屉记忆` | `drawer-memory.html` | 5 墨家族角色页 |

**已知 API**：
- `GET /api/scan` 扫视频
- `GET /api/file?path=X` 流式视频
- `POST /api/save_pixel` 保存 SVG 到 `editor-room/pixel-art/{name}.svg`
- `GET /pixel-art/*` 或 `/pixel_art/*` 读静态 SVG（两条路径都通，老引用兼容）

**当前像素作品**：`editor-room/pixel-art/code-mac.svg` —— 丽丽 4/18 手画的 Clawd + 墨加的橙领带（v0.3）

---

## workshop（端口 9899，主战场）

p5.js 场景引擎 + Tone.js 音乐 + 文字时间线 + Strudel RecipeLab。

第一个项目是「抽屉记忆动画」（多 agent 记忆系统可视化教程），但还没动笔。

---

## workbench（端口 9876，白板）

设计协作白板，pm2 常驻设计。`server.js` 是简单的 Express + JSON 持久化。`工作台数据*.json` 历史 100 个版本还散在 iCloud 根目录，**没搬进来**——属于旧数据，等下次需要再迁。

---

## script-bench（剧本工作台）

纯静态 html，剧本 dialogue/narration 块编辑器。5/4 共同旅程实录在里面（不在 git，是 localStorage）。

> #76 spec note `5/8·06` 提到"剧本块编辑器迁入创意工坊"——这是后续整合方向。

---

## 待整理（还在 iCloud 没进来的）

- `music_lab.html` / `music_neural.html` / `music_portrait.html` 音乐画像三件
- `sparkbot-tutorial.html` SparkBot 教程
- `工作台数据*.json` 历史版本（100 个，旧数据）
- `pixel_studio.html` localStorage 里的画稿历史

按优先级排，等丽丽点。

---

## Plan 关系

- **#47 创意工坊 — 项目工作台**（4/9 立）→ 升级为"工具基建总仓"。所有上面这些工具都在这条线下。
- **#52 剪辑室**（4/17 立）→ 合并入 #47。剪辑室作为 editor-room 的子页面继续。
- **#76 传统制造业小欧 IP + 创作 pipeline**（5/8 立）→ 收窄到"内容产出"。用 #47 的工具产视频，不再混工具开发。

---

最后更新：2026-05-08 chat-Opus
