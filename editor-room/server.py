#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪辑室后端 #52
- /api/scan         扫 ~/Movies 下的 mp4/mov 视频
- /api/file?path=X  流式返回视频文件（支持 Range，<video> 能 seek）
- /api/export       占位，下一步实现剪映草稿生成
端口 9898
"""
import os
import re
import json
import time
import mimetypes
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 9898
ROOTS = [
    os.path.expanduser('~/Movies'),
    os.path.expanduser('~/Desktop'),
    os.path.expanduser('~/Downloads'),
]
EXTS = {'.mp4', '.mov', '.m4v', '.MP4', '.MOV'}
EXCLUDE_DIRS = {'Final Cut Backups.localized', 'iMovie 剪辑资源库.imovielibrary',
                'JianyingPro', 'Motion Templates.localized', '.Trash', 'iMovie Theater.theater',
                'DaVinci Resolve Studio'}


def scan_videos(limit=200):
    items = []
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
            for fn in filenames:
                ext = os.path.splitext(fn)[1]
                if ext in EXTS:
                    full = os.path.join(dirpath, fn)
                    try:
                        st = os.stat(full)
                    except OSError:
                        continue
                    items.append({
                        'name': fn,
                        'path': full,
                        'size': st.st_size,
                        'mtime': time.strftime('%Y-%m-%d', time.localtime(st.st_mtime)),
                    })
            if len(items) >= limit * 3:
                break
    items.sort(key=lambda x: x['mtime'], reverse=True)
    return items[:limit]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # 静默
        pass

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Range,Content-Type')
        self.send_header('Access-Control-Expose-Headers', 'Content-Range,Content-Length,Accept-Ranges')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        path = u.path
        q = urllib.parse.parse_qs(u.query)

        if path == '/api/scan':
            items = scan_videos()
            body = json.dumps({'items': items, 'count': len(items)}, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == '/api/file':
            fp = q.get('path', [''])[0]
            return self._serve_file(fp)

        if path == '/api/ping':
            body = b'{"ok":true,"service":"editor_room","plan":52}'
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(body)
            return

        if path in ('/', '/index.html', '/剪辑室'):
            return self._serve_html('clip-room.html')
        if path in ('/studio', '/pixel', '/画板'):
            return self._serve_html('pixel-studio.html')
        if path in ('/family', '/drawer', '/抽屉记忆'):
            return self._serve_html('drawer-memory.html')
        if path.startswith('/pixel_art/') or path.startswith('/pixel-art/'):
            base = os.path.dirname(os.path.abspath(__file__))
            fp = os.path.join(base, path.lstrip('/'))
            if os.path.isfile(fp) and os.path.realpath(fp).startswith(os.path.realpath(base)):
                ctype = 'image/svg+xml' if fp.endswith('.svg') else 'application/json'
                with open(fp, 'rb') as f:
                    body = f.read()
                self.send_response(200)
                self._cors()
                self.send_header('Content-Type', ctype + '; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

        self.send_response(404)
        self._cors()
        self.end_headers()
        self.wfile.write(b'not found')

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == '/api/export':
            body = b'{"ok":false,"msg":"draft generator in development"}'
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(body)
            return
        if u.path == '/api/save_pixel':
            try:
                length = int(self.headers.get('Content-Length', 0))
                raw = self.rfile.read(length).decode('utf-8')
                data = json.loads(raw)
                name = data.get('name', 'unnamed').replace('/', '_').replace('\\', '_')
                svg = data.get('svg', '')
                if not svg or not name:
                    raise ValueError('missing name or svg')
                # 落盘到 editor-room/pixel-art/
                base = os.path.dirname(os.path.abspath(__file__))
                out_dir = os.path.join(base, 'pixel-art')
                os.makedirs(out_dir, exist_ok=True)
                svg_path = os.path.join(out_dir, name + '.svg')
                json_path = os.path.join(out_dir, name + '.json')
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg)
                # 保存像素数据供再次编辑
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump({'pixels': data.get('pixels', {}), 'size': data.get('size', 32)},
                              f, ensure_ascii=False, indent=2)
                body = json.dumps({'ok': True, 'path': 'pixel-art/' + name + '.svg'}).encode('utf-8')
                self.send_response(200)
                self._cors()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(body)
                return
            except Exception as e:
                body = json.dumps({'ok': False, 'msg': str(e)}).encode('utf-8')
                self.send_response(400)
                self._cors()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(body)
                return
        self.send_response(404)
        self._cors()
        self.end_headers()

    def _serve_html(self, filename):
        base = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(base, filename)
        if not os.path.isfile(fp):
            self.send_response(404); self._cors(); self.end_headers()
            self.wfile.write(b'html not found')
            return
        with open(fp, 'rb') as f:
            body = f.read()
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, fp):
        if not fp or not os.path.isfile(fp):
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(b'file not found')
            return
        # 安全：必须在ROOTS之下
        abs_fp = os.path.realpath(fp)
        if not any(abs_fp.startswith(os.path.realpath(r)) for r in ROOTS):
            self.send_response(403)
            self._cors()
            self.end_headers()
            self.wfile.write(b'path not allowed')
            return

        size = os.path.getsize(abs_fp)
        ctype = mimetypes.guess_type(abs_fp)[0] or 'video/mp4'
        rng = self.headers.get('Range')

        if rng:
            m = re.match(r'bytes=(\d+)-(\d*)', rng)
            if m:
                start = int(m.group(1))
                end = int(m.group(2)) if m.group(2) else size - 1
                end = min(end, size - 1)
                length = end - start + 1
                self.send_response(206)
                self._cors()
                self.send_header('Content-Type', ctype)
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
                self.send_header('Content-Length', str(length))
                self.end_headers()
                with open(abs_fp, 'rb') as f:
                    f.seek(start)
                    remaining = length
                    while remaining > 0:
                        chunk = f.read(min(65536, remaining))
                        if not chunk:
                            break
                        try:
                            self.wfile.write(chunk)
                        except (BrokenPipeError, ConnectionResetError):
                            return
                        remaining -= len(chunk)
                return

        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', ctype)
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Length', str(size))
        self.end_headers()
        with open(abs_fp, 'rb') as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return


def main():
    print(f'[剪辑室 #52] listening on http://localhost:{PORT}')
    print(f'[roots] {ROOTS}')
    HTTPServer(('127.0.0.1', PORT), Handler).serve_forever()


if __name__ == '__main__':
    main()
