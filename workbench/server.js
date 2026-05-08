// 工作台本地保存服务
// 启动: node 工作台服务.js
// 工作台HTML会自动把数据POST到这里，保存成本地JSON文件
// 墨可以直接 Read 工作台数据.json

const http = require('http');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '工作台数据.json');
const IMG_DIR = path.join(__dirname, '工作台图片');
const PORT = 9876;

// ensure image dir exists
if (!fs.existsSync(IMG_DIR)) fs.mkdirSync(IMG_DIR);

const server = http.createServer((req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // 保存数据
  if (req.method === 'POST' && req.url === '/save') {
    let body = '';
    req.on('data', d => body += d);
    req.on('end', () => {
      try {
        // 验证是合法JSON
        JSON.parse(body);
        fs.writeFileSync(DATA_FILE, body, 'utf-8');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end('{"ok":true}');
      } catch(e) {
        res.writeHead(400);
        res.end('{"error":"invalid json"}');
      }
    });
    return;
  }

  // 读取数据
  // /data — 全部页面（目录概览）
  // /data?page=0 — 只看某一页的详细内容
  if (req.method === 'GET' && req.url.startsWith('/data')) {
    if (!fs.existsSync(DATA_FILE)) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end('{"error":"no data yet"}');
      return;
    }
    const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
    const urlObj = new URL(req.url, 'http://localhost');
    const pageParam = urlObj.searchParams.get('page');

    if (pageParam !== null) {
      const pageIdx = parseInt(pageParam);
      if (data.pages && data.pages[pageIdx]) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(data.pages[pageIdx], null, 2));
      } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end('{"error":"page not found"}');
      }
    } else {
      // 只返回页面目录，不返回详细内容
      const summary = {
        totalPages: data.pages.length,
        pages: data.pages.map((p, i) => ({
          index: i,
          name: p.name,
          texts: p.texts ? p.texts.length : 0,
          images: p.images || 0,
          drawings: p.drawings || 0
        }))
      };
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(summary, null, 2));
    }
    return;
  }

  // 保存图片
  if (req.method === 'POST' && req.url === '/save-image') {
    let chunks = [];
    req.on('data', d => chunks.push(d));
    req.on('end', () => {
      try {
        const body = JSON.parse(Buffer.concat(chunks).toString());
        const filename = body.filename;
        const base64 = body.data.replace(/^data:image\/\w+;base64,/, '');
        fs.writeFileSync(path.join(IMG_DIR, filename), Buffer.from(base64, 'base64'));
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end('{"ok":true}');
      } catch(e) {
        res.writeHead(400);
        res.end('{"error":"' + e.message + '"}');
      }
    });
    return;
  }

  // 列出图片
  if (req.method === 'GET' && req.url === '/images') {
    const files = fs.existsSync(IMG_DIR) ? fs.readdirSync(IMG_DIR).filter(f => /\.(png|jpg|jpeg|gif|webp)$/i.test(f)) : [];
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ images: files }));
    return;
  }

  // 琴房曲目
  if (req.method === 'GET' && req.url === '/pieces') {
    const piecesFile = path.join(__dirname, '琴房曲目.json');
    if (fs.existsSync(piecesFile)) {
      const data = fs.readFileSync(piecesFile, 'utf-8');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(data);
    } else {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('[]');
    }
    return;
  }

  res.writeHead(404);
  res.end('not found');
});

server.listen(PORT, () => {
  console.log(`工作台服务已启动 → http://localhost:${PORT}`);
  console.log(`数据文件: ${DATA_FILE}`);
  console.log(`墨可以直接 Read ${DATA_FILE}`);
});
