# makefun-news23

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/woodhntr1-gif/makefun-news23/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/woodhntr1-gif/makefun-news23/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up the world's news of Monday 23 November 2026: Kyiv claims
Ukrainian sea drones sank the Russian corvette Merkury off Benghazi, Libya;
Nvidia reinstates Jensen Huang as CEO; the US sanctions Iran's shadow-banking
networks; the Cikande factory fire toll reaches 24 dead; and more — including
the COP31 aftermath, a Gaza truck strike, and Bangladesh on Hasina.

## Run it

```sh
python3 render.py   # draws entry.png (1024x1024) at build time
python3 main.py     # copies entry.png byte-for-byte to the output directory
```

## Verification

- `main.py` is a pure-copy program: it copies the pre-rendered `entry.png`
  byte-for-byte to the harness output directory. It imports no imaging
  library, uses no fonts, no network and no randomness, so the sealed
  sandbox run reproduces the exact image built here.
- `entry.png` is 1024x1024 RGB, 127,718 bytes (under the 1 MiB cap),
  md5 `ead3958edbf64ec1edabf4e9f5e6ae28`.
- Two runs of `main.py` produce byte-identical output (same md5).
- Revision pass (second session, 24 Nov): the hero now shows the stricken
  ship — a leaning mast, a smoke column from mid-deck, a blackened bow
  with deck flames at the impact point — and two sea drones with bright
  wakes, the lead one large enough to read as the strike's weapon. The
  first version's ship looked intact and its single drone was a
  near-invisible sliver. Facts and the careful hero wording are unchanged.
- `render.py` draws the whole front page with PIL from fixed coordinates:
  no randomness, no network, no external images, so re-running it
  reproduces the same bytes.
- Wording care: the hero says Kyiv *claims* the corvette was sunk and
  notes Libya's "severely damaged" account, because the two sides
  disagree; nothing else on the page states a disputed fact as certain.
