// 逐帧渲染 index.html 并用 ffmpeg 编码为 MP4。
// 用法：node render.mjs [输出文件=junzheng-h1-2026.mp4] [fps=30]
//       node render.mjs --preview 2,6,12,18,23,28   # 只导出若干时间点的 PNG
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

const dir = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(pathToFileURL(path.join(dir, 'index.html')).href + '?capture');
await page.evaluate(() => document.fonts.ready);
const canvas = await page.$('#c');

if (args[0] === '--preview') {
  for (const s of args[1].split(',')) {
    await page.evaluate(t => window.renderFrame(t), Number(s));
    await canvas.screenshot({ path: path.join(dir, `preview-${s}s.png`) });
  }
} else {
  const out = path.resolve(args[0] || path.join(dir, 'junzheng-h1-2026.mp4'));
  const fps = Number(args[1] || 30);
  const total = Math.round((await page.evaluate(() => window.DURATION)) * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => window.renderFrame(t), i / fps);
    const buf = await canvas.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 90 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg exit ' + c))));
  console.log('wrote', out);
}
await browser.close();
