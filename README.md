# moira-music-room

丽丽和墨的创意舞台合集。每个子目录是一个独立单页（pure HTML，不打包），可以直接 `python3 -m http.server` 起本地服务后访问。

## 舞台

| 子目录 | 名字 | 状态 | 备注 |
|--------|------|------|------|
| `qinfang/` | 墨的琴房 | 早期 v1 | abcjs 渲染曲谱，墨写的曲子。原仓库根目录的 index.html，归档保留。 |
| `workshop/` | 创意工坊 v2 | 主线 | p5.js 场景引擎 + Tone.js 音乐 + 文字时间线 + RecipeLab（Strudel 配方拆点）+ 抽屉记忆。包含 `data/` `engine/`。 |
| `dj-stage/` | 打歌台 (Remix) | Claude Design 出品 | 5/8 最新 remix。Apple 深色 + 玫瑰金 accent。含 18 张 `screenshots/` 视觉迭代参考、`scraps/` 草稿、`uploads/` 原始导入。 |

## 本地起服务

`workshop/` 用了 `@strudel/web` ESM，必须 http:// 不能 file://（CORS 会挡）。

```bash
cd moira-music-room
python3 -m http.server 9899
# → http://localhost:9899/workshop/
# → http://localhost:9899/dj-stage/
# → http://localhost:9899/qinfang/
```

或用 pm2 把它常驻（之前 4/10 是 `创意工坊服务.js` 跑 9899 端口，已弃）。

## 工作纪律

**以后所有迭代在这个仓库里做**。本地 iCloud 目录里那两份（`关于墨的记忆相关/创意工坊/` 和 `关于墨的记忆相关/打歌台 (Remix)/`）从这次 commit 起算静态快照，**不再当主战场**。新改动 → 这个仓库 → push → 拉到任何机器接着做。

## 关联工作日志

- `#47` 创意工坊 — 项目工作台（4/9 立项）
- `#311 #313` 创意工坊 v1 / v2
- `#316 #318 #321 #324` Strudel 实验 + 配方工坊 + 雨天窗台

接手细节看 [HANDOFF.md](HANDOFF.md)。
