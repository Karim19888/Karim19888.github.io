// Usage: node render.mjs frames <outDir> [fps] [workers]   |  node render.mjs stills <outDir> t1 t2 ...
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { pathToFileURL } from 'url';
import path from 'path';
const [mode, out, ...rest] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const url = pathToFileURL(path.resolve('composition.html')).href;
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
async function page() {
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto(url); await p.evaluate(() => window.ready); return p;
}
if (mode === 'stills') {
  const p = await page();
  for (const t of rest) { await p.evaluate(t => renderAt(t), parseFloat(t)); await p.screenshot({ path: `${out}/t${t}.jpg`, quality: 85, type: 'jpeg' }); }
} else {
  const fps = parseInt(rest[0] || '30'), W = parseInt(rest[1] || '4');
  const p0 = await page(); const dur = await p0.evaluate(() => window.DURATION); await p0.close();
  const N = Math.round(dur * fps); let next = 0; const t0 = Date.now();
  await Promise.all([...Array(W)].map(async () => {
    const p = await page();
    while (next < N) { const i = next++;
      await p.evaluate(t => renderAt(t), i / fps);
      await p.screenshot({ path: `${out}/f${String(i).padStart(5, '0')}.jpg`, quality: 92, type: 'jpeg' });
      if (i % 300 === 0) console.log(i, '/', N, ((Date.now() - t0) / 1000).toFixed(0) + 's');
    }
  }));
}
await browser.close();
