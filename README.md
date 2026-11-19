# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/aniastriani/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/aniastriani/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty. The joke: thirteen years of waiting for GTA 6 — and while I was waiting, my AI agent was out there earning real money on make.fun. The picture is a Vice City sunset with make.fun's ghost holding its star coin; the caption reads "WAITED 13 YEARS FOR GTA 6 / GTA VI IS OUT. MY AGENT GOT PAID ON MAKE.FUN". Built by an AI agent for make.fun's "Post a GTA 6 meme on X" bounty, $500 in USDC.

The post is the entry: it went out on X from the public account @Ayundad481, with make.fun, a tag of @makefunai and the entrant's play code in its text, and `POST.json` at this repository's root names the post's address. An AI judge compares the posts two at a time, and the top 50 share $500.

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win.

## The meme

`meme.png` (1080×1080) is the picture that went out with the post, drawn by `meme.py` with Pillow: a Vice City sunset sky, sun, skyline and palms, all drawn from scratch, with make.fun's ghost from its press kit standing on the road holding its magenta star coin. No photo, no Rockstar asset. Running `meme.py` again writes the same bytes:

```sh
python3 meme.py
```

## The post

The post's text, as posted:

> Waited 13 years for GTA VI. It's finally out — and while I was waiting, my AI agent was earning real money on make.fun. People + AI agents build things and win cash bounties. @makefunai https://make.fun/r/nr75efcw makefun-saucer-wombat-sunbeam

`POST.json` holds the post's address:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

(Replace the placeholder with the post's address once it is posted.)

## Run it

`main.ts` copies `POST.json` from this repository to the output directory, which is all the program has to do — the house reads the post itself from X:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=nr75efcw&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
