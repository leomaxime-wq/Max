// Rendu image par image du film RESTO CONSEIL.
// node render.mjs --f 916|45|169 [--scale 2] [--fps 30] [--dur 55] [--stills 2,9,15] [--out out]
import { createRequire } from 'module';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require('/opt/node22/lib/node_modules/playwright'); }
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const f = arg('f', '169'), scale = +arg('scale', 1), fps = +arg('fps', 30), stills = arg('stills', null), out = arg('out', 'out');
const [W, H] = { 916: [1080, 1920], 45: [1080, 1350], 169: [1920, 1080] }[f];
fs.mkdirSync(out, { recursive: true });
const browser = await pw.chromium.launch({ args: ['--disable-gpu-vsync'] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exit(1); });
await page.goto('file://' + path.resolve('index.html') + `?render&f=${f}&s=${scale}`);
await page.evaluate(() => window.READY);
// read the canvas directly (works at any scale, faster than a screenshot)
const grab = t => page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', .95).split(',')[1]; }, t);
if (stills) {
  for (const s of stills.split(',')) fs.writeFileSync(`${out}/still_${f}_${s}.jpg`, Buffer.from(await grab(+s), 'base64'));
} else {
  const dst = `${out}/video_${f}${scale > 1 ? '_x' + scale : ''}.mp4`;
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', dst], { stdio: ['pipe', 'ignore', 'inherit'] });
  const N = Math.round(+arg('dur', 55) * fps);
  for (let i = 0; i < N; i++) {
    const buf = Buffer.from(await grab(i / fps), 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`${f} frame ${i}/${N}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
