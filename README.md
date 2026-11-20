# The World in One Day — 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Notodirdjo/news-image-19-nov/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Notodirdjo/news-image-19-nov/reward.svg)](https://make.fun/bounty/news-image-20261119)

A single image that sums up Thursday 19 November 2026's world news,
drawn as a newspaper front page. Entry for the make.fun competition
[news-image-20261119](https://make.fun/bounty/news-image-20261119).

## The day in the image

- **Shenzhen** — Trump, Xi and Putin hold their first three-way summit
  and agree to talk on reducing nuclear risks.
- **The Hague** — the UN court rules Myanmar committed genocide of the
  Rohingya in the 2017 crackdown.
- **Gaming** — GTA VI launches worldwide after a 13-year wait.
- **Markets** — Anthropic's IPO raises about $81 billion, a record.
- **Kerch Bridge** — Ukraine hits the bridge a third time this week.

Plus an "ALSO TODAY" strip: unrest in Bangladesh, Israeli tanks in
central Gaza, Cyclone Akvan near India's east coast, and a record
$190.4 million Van Gogh sale.

## How it is built

`draw.py` renders `entry.png` (1024x1024) with Pillow from the verified
facts in the brief — real text, no AI-generated imagery. `main.py`
(Python 3.13, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`. It runs with no network and writes
identical bytes on every run.

```sh
python3 draw.py        # render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
