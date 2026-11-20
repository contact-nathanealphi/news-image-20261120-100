#!/usr/bin/env python3
"""Draw the 20 November 2026 front page: 100 verified stories, one image.

Pillow + DejaVu only. No network, no randomness, no timestamps, so the
output bytes are identical on every run.

Layout: masthead with the date, five lead stories given larger space, then
the remaining 95 stories as numbered headlines in four dense columns,
grouped by section. The column font size adapts (11 down to 9 points) so
all 100 stories fit inside the page; nothing is ever dropped silently.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 26
CONTENT_W = W - 2 * MARGIN
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
PAPER = (253, 253, 247)
INK = (17, 17, 17)
MUTED = (90, 90, 86)
RULE = (40, 40, 40)
ACCENT = (139, 26, 26)

# n, section, headline, summary (summary only for the five leads).
STORIES = [
    (1, "World", "Trump puts Iran war decision off to 2027",
     "Trump says he is in no rush on Iran and will \u201csee what happens\u201d after "
     "1 January, pushing any decision on war into 2027."),
    (2, "World", "First Trump\u2013Xi\u2013Putin summit held in Shenzhen",
     "Trump, Xi and Putin hold the first three-way summit in Shenzhen (19 Nov); "
     "the declaration covers UN reform, nuclear arms and oil output."),
    (3, "World", "ICJ: Myanmar committed genocide against Rohingya",
     "The ICJ rules Myanmar\u2019s military intended to destroy much of the Rohingya "
     "minority in its 2017 crackdown \u2014 a historic genocide verdict."),
    (4, "World", "Houthi strike hits Riyadh; Saudi fund tower damaged", None),
    (5, "World", "Europe ready to talk to Russia to end Ukraine war", None),
    (6, "World", "Israel completes tank raid into Gaza", None),
    (7, "World", "Gaza peace plan scores 4 out of 26, aid groups say", None),
    (8, "World", "EU\u2013UK summit held in Brussels on 20 November", None),
    (9, "World", "Trump says he will meet Kim Jong-un", None),
    (10, "World", "E3 and Ukraine urge winter energy ceasefire", None),
    (11, "World", "Netherlands summons Russian envoy after Kyiv blast", None),
    (12, "World", "Macron: reopen question of Ukraine in NATO", None),
    (13, "World", "Trump phones European leaders at Berlin talks", None),
    (14, "World", "Zelensky thanks \u201ccoalition of the willing\u201d", None),
    (15, "World", "US and Venezuela restore military cooperation", None),
    (16, "World", "North Korea expands Yongbyon uranium site", None),
    (17, "World", "Ukraine hits Kerch Bridge; rail traffic disrupted", None),
    (18, "World", "South Korea court overturns ex-PM Han\u2019s verdict", None),
    (19, "World", "Fiji declares national disaster over drought", None),
    (20, "World", "Fire at ancestral home of Bangladesh\u2019s Yunus", None),
    (21, "World", "West presses Iran to restore nuclear inspections", None),
    (22, "World", "APEC leaders adopt Shenzhen declaration", None),
    (23, "World", "Board of Peace warns Gaza truce could collapse", None),
    (24, "World", "UK sanctions Israeli settlement builders", None),
    (25, "World", "Putin: Russia ready to work with China and US", None),
    (26, "World", "Modi meets Prince and Princess of Wales in Delhi", None),
    (27, "Indonesia", "Indonesia forest-fire emissions 3rd-highest ever", None),
    (28, "Indonesia", "Parliament passes Asset Forfeiture Law", None),
    (29, "Indonesia", "Cepu refinery blast kills one worker", None),
    (30, "Indonesia", "Trump unveils $17bn SE Asia deals; $2bn coal project", None),
    (31, "Indonesia", "EU approves signing Indonesia trade deal", None),
    (32, "Indonesia", "Giant sixgill shark caught by Indonesian fishers", None),
    (33, "Indonesia", "World\u2019s oldest cave art, 67,800 yrs, at climate risk", None),
    (34, "Indonesia", "Yogyakarta daycare chief jailed 5 years for abuse", None),
    (35, "Indonesia", "Citilink sees December travel improving", None),
    (36, "Indonesia", "Gibran resigns as VP; Prabowo to name successors", None),
    (37, "Indonesia", "Indonesia foreign debt hits $458.9bn", None),
    (38, "Indonesia", "Jakarta stocks fall 1.02% to 5,194, 4th day down", None),
    (39, "Indonesia", "Rupiah weakens to Rp18,254 per US dollar", None),
    (40, "Indonesia", "Indonesia eyes $86.8bn investment at APEC", None),
    (41, "Indonesia", "Indonesia halal market passes Rp5,974 trillion", None),
    (42, "Indonesia", "Titiek Soeharto rejects Javan rhino relocation", None),
    (43, "Indonesia", "ICW reports Puan, Habiburokhman to ethics council", None),
    (44, "Indonesia", "Defence minister pushes defence law revision", None),
    (45, "Indonesia", "Police to expose alleged treason case on Friday", None),
    (46, "Indonesia", "FLPP home loans pass 208,000 units, Rp25.99tn", None),

    (47, "Tech & AI", "Anthropic IPO: $83 a share, $81.3bn \u2014 largest ever",
     "Anthropic, maker of Claude, lists on Nasdaq at $83 a share and raises "
     "$81.3bn \u2014 the largest IPO in history. Shares close at $97.17, up 17%."),
    (48, "Tech & AI", "Jensen Huang steps down as Nvidia CEO", None),
    (49, "Tech & AI", "OpenAI launches GPT-6.2 Astra and Sol", None),
    (50, "Tech & AI", "Google launches Gemini 4 Neon; Gemini runs Macs", None),
    (51, "Tech & AI", "Microsoft unveils 7 MAI models; 60,000 AI buyouts", None),
    (52, "Tech & AI", "Meta\u2019s Muse AI mixed chats, leaked private data", None),
    (53, "Tech & AI", "Alibaba trains new AI on its own chips, not Nvidia", None),
    (54, "Tech & AI", "Anthropic releases Claude Fable 5.2, Mythos 5.2", None),
    (55, "Tech & AI", "Google opens Gemini 4 Carbon; replaces 3.8 Flash", None),
    (56, "Tech & AI", "Lenovo AI revenue tops $10bn for first time", None),
    (57, "Tech & AI", "DeepMind AI formally verifies Signal encryption", None),
    (58, "Tech & AI", "Nvidia SEED; AX100 chip taped out; Kling Image 4.0", None),
    (59, "Business", "Wall Street slides: S&P -2.02%, Dow -2.19%",
     "US stocks slide on Thursday (19 Nov) as investors sell tech after "
     "Anthropic\u2019s debut: the Dow falls 1,101 points to 49,097."),
    (60, "Business", "Gold below $3,700/oz, lowest since Sept 2025", None),
    (61, "Business", "\u201cSell Korea\u201d: $115.2bn outflow, KOSPI -44% off peak", None),
    (62, "Business", "Sensex and Nifty post strong gains", None),
    (63, "Business", "Mahanadi Coalfields IPO opens, ~\u20b98,981 crore", None),
    (64, "Business", "Walmart Q3 beats forecasts, lifts profit outlook", None),
    (65, "Business", "US jobless claims rise to 203,000", None),
    (66, "Business", "BoJ\u2019s Ueda: central bank will keep raising rates", None),
    (67, "Business", "US dollar near 19-month high; yen ~159.50", None),
    (68, "Business", "Brent $91.95 (-1.28%); WTI $83.26 (-3.2%)", None),
    (69, "Business", "Nvidia -3.3% (-40% from peak); Palo Alto +6%", None),
    (70, "Business", "India\u2013Israel defence deal worth \u20b91,976.40 crore", None),
    (71, "Sport", "India v NZ Test 1 \u2014 Nicholls 113* (NZ 243/5)", None),
    (72, "Sport", "Persib Bandung 6-0 Shan United (Shopee Cup)", None),
    (73, "Sport", "JDT 3-1 Hanoi; Svay Rieng 4-1 Port FC (Shopee Cup)", None),
    (74, "Sport", "NBA: Hawks stun OKC 117-112; Johnson triple-double", None),
    (75, "Sport", "76ers rally from 17 down to beat Magic 121-116", None),
    (76, "Sport", "Heat 137-130 Bucks (Giannis 27 vs ex-team)", None),
    (77, "Sport", "NFL Week 11: Vikings v 49ers in Mexico City", None),
    (78, "Sport", "Clemson at Duke Friday; ESPN picks Duke 29-17", None),
    (79, "Sport", "Packers 6-4 at bye; Parsons out 10 games", None),
    (80, "Sport", "AFF named AFC\u2019s best regional body, 2nd year on", None),
    (81, "Entertainment", "Taylor Swift returns to CMA Awards stage", None),
    (82, "Entertainment", "Bruno Mars\u2019s father Peter Hernandez dies, 74", None),
    (83, "Entertainment", "Ella Langley makes CMA history with 6 wins", None),
    (84, "Entertainment", "Robert Pattinson is the new James Bond", None),
    (85, "Entertainment", "Hunger Games: Sunrise on the Reaping out 20 Nov", None),
    (86, "Entertainment", "Netflix actor Alexander Haskin dies, 38", None),
    (87, "Entertainment", "Marvel actor, ex-Mets pitcher Lance Broadway, 43, dies", None),
    (88, "Entertainment", "GTA 6 sales pass The Odyssey\u2019s $1.80bn gross", None),
    (89, "Entertainment", "GTA VI tipped to sell 19.1m copies on day one", None),
    (90, "Science", "NASA: Voyager 1 reaches \u201clight-day\u201d distance", None),
    (91, "Science", "Hayabusa2 scraps asteroid landing over engine fault", None),
    (92, "Science", "Cyclone Akvan: 300,000 evacuated before Odisha hit", None),
    (93, "Science", "US Army to detonate 5 tons of explosive in Iowa", None),
    (94, "Science", "Parkinson\u2019s breakthrough study (Auckland, 20 Nov)", None),
    (95, "Science", "Blood test spots Alzheimer\u2019s before symptoms", None),
    (96, "Science", "COP31: fossil-fuel phase-out dropped; $120bn axed", None),
    (97, "Science", "COP31: 123 firms urge faster electrification", None),
    (98, "Science", "Venezuela uses AI for cleaner oil output (COP31)", None),
    (99, "Science", "ICMR reaches 100 health tech-transfer deals", None),
    (100, "Science", "India science festival in Pune, 19\u201322 December", None),
]

LEAD_NUMBERS = (1, 2, 3, 47, 59)
COL_LH = 1.12      # column line-height factor (roomier than 1.08)
COL_GAP = 4        # pixels after each column item
SUB_H = 22         # pixels per section subhead block (rule + label + gap)
SECTION_LABELS = {
    "World": "WORLD",
    "Indonesia": "INDONESIA",
    "Tech & AI": "TECHNOLOGY & AI",
    "Business": "BUSINESS & MARKETS",
    "Sport": "SPORT",
    "Entertainment": "ENTERTAINMENT",
    "Science": "SCIENCE & ENVIRONMENT",
}


def _font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def wrap_text(draw, text, font, max_w):
    """Greedy word wrap; returns the lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _lh(font):
    asc, desc = font.getmetrics()
    return asc + desc


def draw_masthead(draw):
    y = 14
    f_title = _font("DejaVuSerif-Bold.ttf", 44)
    draw.text((W // 2, y), "THE WORLD TODAY", font=f_title, fill=INK, anchor="ma")
    y += 52
    f_date = _font("DejaVuSans-Bold.ttf", 17)
    draw.text((MARGIN, y), "FRIDAY, 20 NOVEMBER 2026", font=f_date, fill=INK, anchor="la")
    f_tag = _font("DejaVuSans-Bold.ttf", 13)
    draw.text((W - MARGIN, y + 2), "100 STORIES \u00b7 ONE DAY", font=f_tag,
              fill=MUTED, anchor="ra")
    y += 26
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=3)
    y += 5
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    return y + 10


def draw_lead(draw, x, y, w, number, head, summary, head_size, sum_size):
    """One lead story; returns the y just below it."""
    f_num = _font("DejaVuSans-Bold.ttf", 11)
    f_head = _font("DejaVuSerif-Bold.ttf", head_size)
    f_sum = _font("DejaVuSans.ttf", sum_size)
    draw.text((x, y), f"{number} \u00b7 LEAD STORY", font=f_num, fill=ACCENT, anchor="la")
    y += 15
    for line in wrap_text(draw, head, f_head, w)[:2]:
        draw.text((x, y), line, font=f_head, fill=INK, anchor="la")
        y += int(_lh(f_head) * 1.05)
    for line in wrap_text(draw, summary, f_sum, w)[:2]:
        draw.text((x, y), line, font=f_sum, fill=INK, anchor="la")
        y += int(_lh(f_sum) * 1.08)
    return y


def plan_columns(draw, items, font, num_font, col_w, avail_h):
    """Split items into 4 even columns. Returns the plan, or None if any
    column would be taller than avail_h. A plan is a list of columns; each
    column is a list of ('sub', label) / ('item', story, lines) entries."""
    n = len(items)
    sizes = [n // 4 + (1 if i < n % 4 else 0) for i in range(4)]
    lh = int(_lh(font) * COL_LH)
    sub_h = SUB_H
    gap = COL_GAP
    columns = []
    idx = 0
    for size in sizes:
        entries = []
        h = 0
        cur_sec = None
        for item in items[idx:idx + size]:
            if item[1] != cur_sec:
                cur_sec = item[1]
                entries.append(("sub", SECTION_LABELS[cur_sec]))
                h += sub_h
            num_txt = f"{item[0]}. "
            num_w = draw.textlength(num_txt, font=num_font)
            lines = wrap_text(draw, item[2], font, col_w - num_w)
            entries.append(("item", item, lines, num_w))
            h += len(lines) * lh + gap
        if h > avail_h:
            return None
        columns.append(entries)
        idx += size
    return columns


def draw_columns(draw, columns, x0, y0, col_w, gutter, font, num_font):
    f_sub = _font("DejaVuSans-Bold.ttf", 12)
    lh = int(_lh(font) * COL_LH)
    gap = COL_GAP
    for ci, entries in enumerate(columns):
        x = x0 + ci * (col_w + gutter)
        y = y0
        for entry in entries:
            if entry[0] == "sub":
                draw.line([(x, y + 1), (x + col_w, y + 1)], fill=ACCENT, width=1)
                draw.text((x, y + 4), entry[1], font=f_sub, fill=ACCENT, anchor="la")
                y += SUB_H
            else:
                _, item, lines, num_w = entry
                draw.text((x, y), f"{item[0]}. ", font=num_font, fill=ACCENT, anchor="la")
                for line in lines:
                    draw.text((x + num_w, y), line, font=font, fill=INK, anchor="la")
                    y += lh
                y += gap


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)

    by_num = {n: (head, summ) for n, _sec, head, summ in STORIES}
    head, summ = by_num[1]
    y = draw_lead(draw, MARGIN, y, CONTENT_W, 1, head, summ, 21, 12)
    y += 10
    cell_w = (CONTENT_W - 12) // 2
    row1_y = y
    h = draw_lead(draw, MARGIN, row1_y, cell_w, 2, *by_num[2], 15, 11)
    h = max(h, draw_lead(draw, MARGIN + cell_w + 12, row1_y, cell_w, 3,
                         *by_num[3], 15, 11))
    row2_y = h + 10
    h = draw_lead(draw, MARGIN, row2_y, cell_w, 47, *by_num[47], 15, 11)
    h = max(h, draw_lead(draw, MARGIN + cell_w + 12, row2_y, cell_w, 59,
                         *by_num[59], 15, 11))
    y = h + 8

    f_sec = _font("DejaVuSans-Bold.ttf", 13)
    draw.text((MARGIN, y), "THE DAY IN 100 STORIES", font=f_sec, fill=INK, anchor="la")
    draw.text((W - MARGIN, y), "WORLD \u00b7 INDONESIA \u00b7 TECH \u00b7 MARKETS \u00b7 SPORT \u00b7 CULTURE \u00b7 SCIENCE",
              font=_font("DejaVuSans.ttf", 10), fill=MUTED, anchor="ra")
    y += 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 8
    col_top = y
    col_bottom = 1004
    avail_h = col_bottom - col_top
    col_w = (CONTENT_W - 3 * 12) // 4
    gutter = 12

    rest = [s for s in STORIES if s[0] not in LEAD_NUMBERS]
    chosen = None
    for size in (11, 10, 9):
        font = _font("DejaVuSans.ttf", size)
        num_font = _font("DejaVuSans-Bold.ttf", size)
        plan = plan_columns(draw, rest, font, num_font, col_w, avail_h)
        if plan is not None:
            chosen = (size, font, num_font, plan)
            break
    if chosen is None:
        raise SystemExit("ERROR: 100 stories do not fit even at 9pt; layout must change")
    size, font, num_font, plan = chosen
    draw_columns(draw, plan, MARGIN, col_top, col_w, gutter, font, num_font)

    draw.line([(MARGIN, 1010), (W - MARGIN, 1010)], fill=RULE, width=1)
    f_foot = _font("DejaVuSans.ttf", 10)
    draw.text((W // 2, 1014),
              "The World Today \u00b7 Friday 20 November 2026 \u00b7 All 100 stories verified from the day\u2019s reporting",
              font=f_foot, fill=MUTED, anchor="ma")

    out = Path(__file__).resolve().parent.parent / "assets" / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes), column font {size}pt, "
          f"stories {len(STORIES)}")


if __name__ == "__main__":
    main()
