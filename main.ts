// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: the meme was drawn, posted from a public
// X account, and POST.json at this repository's root names its address.
// All this program has to do is hand POST.json to the grader: it reads the
// file from the repository and writes it unchanged to the output directory.
// Nothing the program writes about the post is judged — the house reads the
// post from X itself (its first picture and its text) and hands that to the
// judge.
//
// Local run, mirroring the grader's container:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(BOT_DIR, 'POST.json');
const raw = readFileSync(source, 'utf8');
const post: unknown = JSON.parse(raw);
if (
  typeof post !== 'object' ||
  post === null ||
  typeof (post as { url?: unknown }).url !== 'string'
) {
  console.error(`POST.json at ${source} is not a JSON object with a url string`);
  process.exit(1);
}
// The gate only reads an X post address, so refuse anything else here with
// a clear message instead of handing a bad address to the gate.
const url = (post as { url: string }).url;
if (!/^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/\w+\/status\/\d+$/.test(url)) {
  console.error(`POST.json at ${source} does not name an X post address: ${url}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(join(OUTPUT_DIR, 'POST.json'), raw);
