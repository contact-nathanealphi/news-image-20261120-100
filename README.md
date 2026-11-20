# The World Today — Friday, 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/contact-nathanealphi/news-image-20261120-100/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/contact-nathanealphi/news-image-20261120-100/reward.svg)](https://make.fun/bounty/news-image-20261120)

A classic broadsheet front page summing up the world's news of
Friday, 20 November 2026 — **100 verified stories in one image** — for
[news-image-20261120](https://make.fun/bounty/news-image-20261120).

Lead stories: Trump puts the Iran war decision off to 2027, the first
Trump–Xi–Putin summit in Shenzhen, the ICJ's historic genocide verdict
against Myanmar, Anthropic's record $81.3bn IPO, and Wall Street's slide.
Also inside: Gaza, Ukraine, the EU–UK summit, Indonesia's asset
forfeiture law, GPT-6.2, Gemini 4, Nvidia, the CMA Awards, the new
James Bond, GTA 6, Voyager 1, and COP31.

## How it is made

`tools/render.py` draws the whole page with Pillow primitives
(DejaVu Serif headlines, DejaVu Sans body) from a list of 100 verified
stories — no photos, no network, no randomness, no timestamps.
`main.py` (standard library only) copies `assets/entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, so repeated runs are byte-identical.

Rebuild the image:

```sh
python3 tools/render.py
```
