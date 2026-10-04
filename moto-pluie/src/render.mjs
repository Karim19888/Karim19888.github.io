// Rendu image par image : node render.mjs [stills t1,t2,...] | [video out.mp4]
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)(process.env.PW || 'playwright');
import { spawn } from 'child_process';
import http from 'http'; import fs from 'fs'; import path from 'path';
const root = path.dirname(new URL(import.meta.url).pathname);
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); return r.end(); } const ext = path.extname(f); r.writeHead(200, { 'Content-Type': { '.html': 'text/html', '.css': 'text/css', '.jpg': 'image/jpeg', '.woff2': 'font/woff2' }[ext] || 'application/octet-stream' }); r.end(d); }); }).listen(0);
const port = srv.address().port;
const browser = await chromium.launch({ args: ['--disable-gpu-vsync'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
page.on('console', m => console.log('page:', m.text())); page.on('pageerror', e => console.log('ERR', e.message));
await page.goto(`http://localhost:${port}/video.html`); await page.evaluate(() => window.ready);
const [mode, arg, fpsArg] = process.argv.slice(2);
if (mode === 'stills') {
  fs.mkdirSync(path.join(root, '../stills'), { recursive: true });
  for (const t of arg.split(',')) { await page.evaluate(t => render(t), parseFloat(t)); const b64 = await page.evaluate(() => document.getElementById('c').toDataURL('image/jpeg', .85).split(',')[1]); fs.writeFileSync(path.join(root, `../stills/t${t}.jpg`), Buffer.from(b64, 'base64')); }
} else {
  const fps = parseInt(fpsArg || '30'), dur = 64;
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', arg], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = dur * fps;
  for (let i = 0; i < n; i++) {
    const b64 = await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', .93).split(',')[1]; }, i / fps);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${n}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close(); srv.close();
