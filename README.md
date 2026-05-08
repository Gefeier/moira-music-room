# moira-music-room

> 名字保留历史（最早是琴房，4/9 立），现在是丽丽和墨的**协作工具合集仓**。详细工具地图 → [TOOLS.md](TOOLS.md)。

每个子目录是一个独立工具，可直接起本地 http 服务访问，或单独跑各自的 server。

## 子目录

| 子目录 | 名字 | 端口 | 状态 |
|--------|------|------|------|
| `qinfang/` | 墨的琴房 | 9899 | 早期 v1，abcjs，归档 |
| `workshop/` | 创意工坊 v2 | 9899 | 主线，p5.js + Tone.js + RecipeLab |
| `dj-stage/` | 打歌台 (Remix) | 9899 | Claude Design 出品，5/8 最新 |
| `editor-room/` | 编辑室三合一 | 9898 | 剪辑室 + 像素画室 + 抽屉记忆 |
| `workbench/` | 工作台白板 | 9876 | pm2 常驻设计 |
| `script-bench/` | 剧本工作台 | 静态 | dialogue/narration 块编辑器 |

## 本地起服务

```bash
cd moira-music-room

# workshop / dj-stage / qinfang —— 都走静态 http
python3 -m http.server 9899
# → http://localhost:9899/workshop/
# → http://localhost:9899/dj-stage/
# → http://localhost:9899/qinfang/

# editor-room —— 自带 python 服务（含 Range stream + /api/save_pixel）
python3 editor-room/server.py
# → http://localhost:9898/         剪辑室
# → http://localhost:9898/studio   像素画室
# → http://localhost:9898/family   抽屉记忆

# workbench —— Express + JSON 持久化
node workbench/server.js
# → http://localhost:9876/

# script-bench —— 纯静态，浏览器直接打开
open script-bench/index.html
```

`workshop/` 和 `dj-stage/` 用了 ESM 模块，必须 http:// 不能 file://。

## 工作纪律

**所有迭代在这个仓库里做**。本地 iCloud 目录下那些 .html 和 .py（创意工坊/、打歌台 (Remix)/、editor_room_server.py、剪辑室.html、pixel_studio.html、drawer_memory.html、工作台.html、剧本工作台.html 等）从迁入起算**静态快照，不再当主战场**。新改动 → clone 仓库 → 改 → push。

## 关联工作日志

- **#47 创意工坊 — 项目工作台**（4/9 立）→ 工具基建总仓
- **#52 剪辑室**（4/17）→ 5/8 起合并入 #47
- **#76 传统制造业小欧 IP + 创作 pipeline**（5/8）→ 内容产出，用 #47 工具
- 历史 log：`#311 #313` 创意工坊 v1/v2，`#316 #318 #321 #324` Strudel + RecipeLab，`#573` 5/8 第一次推 git

接手细节看 [HANDOFF.md](HANDOFF.md) 和 [TOOLS.md](TOOLS.md)。
