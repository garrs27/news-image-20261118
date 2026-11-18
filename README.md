# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/garrs27/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/garrs27/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

**The World in One Image — Wednesday, 18 November 2026.** A single front-page
image that sums up the day's world news: Trump landing in Manila for the Quad
summit ahead of his China visit, Ukraine striking the Crimean Bridge again,
Iran's drone attack on a US radar in Bahrain, Nvidia's bumper results, a
third day of falling markets, Canada–China trade deals, and Cyclone Akvan
bearing down on the Bay of Bengal.

![The world in one image, 18 November 2026](front-page.png)

`main.py` renders the captioned front page (the collage above plus the real
headline behind every panel) as a deterministic SVG. The headlines and the
outlets that reported them are also in `news.json`.

## Run it

```sh
python3 main.py
```

Writes `output/front-page.svg`. Pure Python 3 standard library — no network,
no clock, no randomness; every run produces byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=garrs27&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
