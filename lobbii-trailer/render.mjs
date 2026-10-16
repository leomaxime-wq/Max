// Usage: node render.mjs [--scale 1|2] [--fps 30] [--stills 2,7,9.5,...]
import { createRequire } from 'module';
import { spawn } from 'child_process';
import path from 'path';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require('/opt/node22/lib/node_modules/playwright'); }
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const scale = +arg('scale', 1), fps = +arg('fps', 30), stills = arg('stills', null), out = arg('out', 'out');
const url = 'file://' + path.resolve('index.html') + '?render';
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
await page.goto(url); await page.evaluate(() => document.fonts.ready);
if (stills) {
  for (const s of stills.split(',')) { await page.evaluate(t => render(t), +s); await page.screenshot({ path: `${out}/still_${s}.png` }); }
} else {
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', `${out}/video_noaudio.mp4`], { stdio: ['pipe', 'ignore', 'inherit'] });
  const N = 30 * fps;
  for (let f = 0; f < N; f++) {
    await page.evaluate(t => render(t), f / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 96 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 90 === 0) console.log(`frame ${f}/${N}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
