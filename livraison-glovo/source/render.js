// usage: node render.js preview t1,t2,...   |   node render.js video out.mp4 [fps]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [mode, arg, fpsArg] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'video.html'));
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  // preload css background images
  await page.evaluate(async () => { for (const u of ['P01_Casablanca_LeDesk.jpg','P04_cuisine_Marrakech_2011.jpg','Glovo_Rider_-_Gran_Via_-_Madrid_03.jpg']) { const i = new Image(); i.src = 'img/' + u; await i.decode(); } });
  if (mode === 'preview') {
    for (const t of arg.split(',').map(Number)) {
      await page.evaluate(t => render(t), t);
      await page.screenshot({ path: `prev_${String(t).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 80 });
    }
  } else {
    const fps = Number(fpsArg || 30), dur = 59, n = Math.round(dur * fps);
    const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', arg], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let f = 0; f < n; f++) {
      await page.evaluate(t => render(t), f / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 150 === 0) console.error('frame', f, '/', n);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
