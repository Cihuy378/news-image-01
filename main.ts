// news-image-01 entry (Node 22, standard library only): the image beside this file
// is copied to /output/entry.png. The image is a newspaper front page,
// "THE WORLD IN ONE DAY — Friday, 13 November 2026", summing up the day's
// world news: the Iran war escalation in the Strait of Hormuz (hero), Europe
// winning a seat at the Ukraine peace talks, the global Microsoft 365 outage,
// Nvidia chief Jensen Huang resigning and being summoned by Congress, plus
// Pope Leo XIV in Peru, the Brooklyn collapse toll and the $1.2B Binance-hack
// seizure. The gate takes a whole PNG or JPEG of at most 1 MiB and 1024 by
// 1024 pixels, and the judge sees exactly the bytes copied. The front page
// was composed by compose.py from AI-generated editorial illustrations in
// assets/ (see README.md for the stories and sources).
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
// Guard against a partial write: the judge must see exactly the bytes shipped.
if (statSync(src).size !== statSync(dest).size) throw new Error('entry.png copy size mismatch');
