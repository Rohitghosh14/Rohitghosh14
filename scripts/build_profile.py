import datetime, json, math, os, urllib.request
from html import escape

USER = "Rohitghosh14"
NAME = "ROHIT GHOSH"
HANDLE = "@Rohitghosh14"
HEADLINE = "Building ML systems end-to-end, not just notebooks."
BADGES = ["AI/ML ENGINEERING STUDENT", "KOLKATA, INDIA", "BUILDING AOD-NET & RIO"]
STACK = ["Python", "PyTorch", "TensorFlow", "scikit-learn", "FastAPI", "Flask",
         "Streamlit", "NLP", "Computer Vision", "Git", "Kaggle"]
ROLES = [("BUILDING", "AOD-Net, from-scratch image dehazing rebuild"),
         ("BUILDING", "Rio, desktop AI companion"),
         ("LEARNING", "Deep learning, NLP and MLOps through projects"),
         ("TRAINING", "On Kaggle / Colab (no local GPU)")]
FEATURED = ["exoplanet-habitability-predictor", "fifa-worldcup-2026-predictor",
            "movie-recommender-model", "GUI_PASSWORD_MANAGER", "rio-ai-companion"]

THEMES = {
    "dark": dict(bg="#0b0e17", fg="#e8eaf4", muted="#9aa1b8", accent="#8b93ff", rule="#363b50", dot="#1b2033"),
    "light": dict(bg="#f6f7fc", fg="#14172a", muted="#5a6078", accent="#4a53e0", rule="#c8cce0", dot="#e1e4f2"),
}
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Courier New',monospace"
SERIF = "Georgia,'Times New Roman',serif"

_G = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#", "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".####|#....|#....|#....|#....|#....|.####", "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####", "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".####|#....|#....|#.###|#...#|#...#|.###.", "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": "#####|..#..|..#..|..#..|..#..|..#..|#####", "J": "..###|...#.|...#.|...#.|...#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#", "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#", "N": "#...#|##..#|#.#.#|#..##|#...#|#...#|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.", "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#", "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.", "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.", "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#", "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..", "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.", "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    "2": ".###.|#...#|....#|...#.|..#..|.#...|#####", "3": "####.|....#|....#|.###.|....#|....#|####.",
    "4": "#...#|#...#|#...#|#####|....#|....#|....#", "5": "#####|#....|####.|....#|....#|#...#|.###.",
    "6": ".###.|#....|#....|####.|#...#|#...#|.###.", "7": "#####|....#|...#.|..#..|.#...|.#...|.#...",
    "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.", "9": ".###.|#...#|#...#|.####|....#|....#|.###.",
    "#": ".#.#.|.#.#.|#####|.#.#.|#####|.#.#.|.#.#.", "/": "....#|....#|...#.|..#..|.#...|#....|#....",
    ".": ".....|.....|.....|.....|.....|.##..|.##..", "-": ".....|.....|.....|#####|.....|.....|.....",
    "%": "##..#|##..#|...#.|..#..|.#...|#..##|#..##", " ": ".....|.....|.....|.....|.....|.....|.....",
}
FONT = {k: v.split("|") for k, v in _G.items()}


def api(path):
    req = urllib.request.Request("https://api.github.com" + path)
    req.add_header("Accept", "application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def contributions():
    q = ("query($login:String!){user(login:$login){contributionsCollection{totalCommitContributions "
         "totalPullRequestContributions totalIssueContributions totalPullRequestReviewContributions}}}")
    try:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": q, "variables": {"login": USER}}).encode(),
            headers={"Authorization": "Bearer " + os.environ.get("GITHUB_TOKEN", ""),
                     "Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            c = json.load(r)["data"]["user"]["contributionsCollection"]
        return (c["totalCommitContributions"], c["totalPullRequestContributions"],
                c["totalIssueContributions"], c["totalPullRequestReviewContributions"])
    except Exception as e:
        print("graphql failed:", e)
        return 0, 0, 0, 0


def fmt(n):
    n = int(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def clamp(v):
    return max(0.0, min(100.0, v))


def fetch():
    user = api(f"/users/{USER}")
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in repos)
    followers = user["followers"]
    commits, prs, issues, reviews = contributions()
    now = datetime.datetime.now(datetime.timezone.utc)
    recent = 0
    for r in repos:
        p = datetime.datetime.strptime(r["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        if (now - p).days <= 90:
            recent += 1
    axes = [("CREATION", clamp(len(repos) / 40 * 100)),
            ("SHIPPING", clamp(commits / 1000 * 100)),
            ("COLLABORATION", clamp((prs + reviews) / 100 * 100)),
            ("MAINTENANCE", clamp(recent / 10 * 100)),
            ("COMMUNITY", clamp((followers + stars) / 200 * 100))]
    by = {r["name"].lower(): r for r in repos}
    return dict(
        followers=followers, repos=user["public_repos"], axes=axes,
        score=sum(a[1] for a in axes) / 5,
        activity=[("Owned stars", stars), ("Commits", commits), ("PRs", prs),
                  ("Issues", issues), ("Reviews", reviews), ("Public repos", user["public_repos"])],
        top=[by[n.lower()] for n in FEATURED if n.lower() in by])


def pxw(s, sc, gap=1):
    return len(str(s)) * (5 + gap) * sc - gap * sc


def px(x, y, s, sc, color, gap=1):
    out, cx = [], x
    for ch in str(s).upper():
        g = FONT.get(ch, FONT[" "])
        for r, row in enumerate(g):
            c = 0
            while c < 5:
                if row[c] == "#":
                    e = c
                    while e < 5 and row[e] == "#":
                        e += 1
                    out.append(f'<rect x="{cx + c * sc}" y="{y + r * sc}" width="{(e - c) * sc}" height="{sc}"/>')
                    c = e
                else:
                    c += 1
        cx += (5 + gap) * sc
    return f'<g fill="{color}">' + "".join(out) + "</g>"


def tx(x, y, s, size, color, family=MONO, weight=400, anchor="start", ls=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-family="{family}" '
            f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}">{escape(str(s))}</text>')


def rule(x1, x2, y, t):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t["rule"]}" stroke-width="1"/>'


def clip(s, n):
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"


def waves(x0, x1, y, t):
    out = []
    for k in range(5):
        pts = []
        for i in range(61):
            x = x0 + (x1 - x0) * i / 60
            yy = y + k * 7 + 14 * math.sin(i / 60 * 2 * math.pi * 1.3 + k * 0.35)
            pts.append(f"{x:.1f},{yy:.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{t["accent"]}" '
                   f'stroke-width="1" stroke-dasharray="8 5" opacity="{0.3 + 0.1 * k:.2f}"/>')
    return "".join(out)


def radar(cx, cy, R, axes, t, fs):
    def pt(i, r):
        a = math.radians(-90 + i * 72)
        return cx + r * math.cos(a), cy + r * math.sin(a)

    def poly(points, extra):
        return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in points)}" {extra}/>'

    o = []
    for k in (0.33, 0.66, 1.0):
        o.append(poly([pt(i, R * k) for i in range(5)], f'fill="none" stroke="{t["rule"]}"'))
    for i in range(5):
        x, y = pt(i, R)
        o.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["rule"]}"/>')
    data = [pt(i, max(R * 0.05, R * axes[i][1] / 100)) for i in range(5)]
    o.append(poly(data, f'fill="{t["accent"]}" fill-opacity="0.25" stroke="{t["accent"]}" stroke-width="2"'))
    for x, y in data:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{t["accent"]}"/>')
    for i, (name, _) in enumerate(axes):
        x, y = pt(i, R + 18)
        anchor = "middle" if abs(x - cx) < 5 else ("start" if x > cx else "end")
        o.append(tx(f"{x:.1f}", f"{y + 4:.1f}", name, fs, t["fg"], anchor=anchor))
    return "".join(o)


def render(theme, mobile, d):
    t = THEMES[theme]
    W = 480 if mobile else 1200
    P = 20 if mobile else 40
    o = []

    def section(y, label):
        o.append(rule(P, W - P, y, t))
        o.append(tx(P, y + 26, label, 11 if mobile else 12, t["fg"], weight=700, ls=1))
        return y + 46

    def stats(items, cols, y, nsc):
        cw = (W - 2 * P) / cols
        rh = 7 * nsc + 52
        for i, (lab, val) in enumerate(items):
            r, c = divmod(i, cols)
            x, yy = P + c * cw, y + r * rh
            o.append(px(x, yy, val, nsc, t["accent"]))
            o.append(tx(x, yy + 7 * nsc + 20, lab.upper(), 10, t["muted"], ls=1))
        return y + ((len(items) + cols - 1) // cols) * rh

    def score_block(x, y, sc, right):
        s = f'{d["score"]:.1f}'
        o.append(px(x, y, s, sc, t["accent"]))
        o.append(tx(x + pxw(s, sc) + 10, y + 7 * sc, "/100", 20 if sc >= 7 else 16, t["muted"]))
        o.append(tx(right, y + 8, "BUILDER INDEX", 10, t["muted"], anchor="end"))
        o.append(tx(right, y + 24, "CUSTOM SCORE", 10, t["muted"], anchor="end"))

    fs = 11 if mobile else 12
    o.append(tx(P, 34, "FIG_000 / PUBLIC BUILDER PROFILE", fs, t["accent"], weight=700, ls=1))
    o.append(tx(W - P, 34, HANDLE, fs, t["fg"], weight=700, anchor="end"))
    o.append(rule(P, W - P, 46, t))
    sc = 5 if mobile else 9
    o.append(px(P, 66, NAME, sc, t["accent"]))
    y = 66 + 7 * sc + (30 if mobile else 40)
    o.append(tx(P, y, HEADLINE, 15 if mobile else 26, t["fg"], SERIF))
    y += 26
    o.append(tx(P, y, " · ".join(BADGES), 9 if mobile else 12, t["muted"], ls=0 if mobile else 1))
    top = y + 34
    hero = f'{d["repos"]} REPOS'

    if not mobile:
        o.append(tx(P, top + 14, "FIG_001 / PUBLIC REPOSITORIES", 12, t["fg"], weight=700, ls=1))
        o.append(px(P, top + 36, hero, 14, t["accent"]))
        o.append(waves(P, 760, top + 200, t))
        o.append(tx(P, top + 330, f'{d["followers"]:,} PUBLIC FOLLOWERS', 26, t["fg"], SERIF))
        o.append(tx(P, top + 354, "Public data, refreshed daily", 12, t["accent"]))
        o.append(f'<line x1="800" y1="{top}" x2="800" y2="{top + 390}" stroke="{t["rule"]}" stroke-dasharray="2 5"/>')
        o.append(tx(840, top + 14, "FIG_002 / BUILDER PROFILE", 12, t["fg"], weight=700, ls=1))
        o.append(radar(985, top + 170, 95, d["axes"], t, 11))
        score_block(840, top + 320, 7, W - P)
        o.append(tx(W - P, top + 392, "PUBLIC DATA ONLY", 10, t["muted"], anchor="end"))
        y = top + 410
    else:
        o.append(tx(P, top + 14, "FIG_001 / PUBLIC REPOSITORIES", 11, t["fg"], weight=700, ls=1))
        o.append(px(P, top + 32, hero, 9, t["accent"]))
        o.append(tx(P, top + 128, f'{d["followers"]:,} PUBLIC FOLLOWERS', 18, t["fg"], SERIF))
        o.append(tx(P, top + 148, "Public data, refreshed daily", 10, t["accent"]))
        y = top + 180
        o.append(rule(P, W - P, y, t))
        o.append(tx(P, y + 26, "FIG_002 / BUILDER PROFILE", 11, t["fg"], weight=700, ls=1))
        cy = y + 170
        o.append(radar(W / 2, cy, 85, d["axes"], t, 10))
        score_block(P, cy + 130, 6, W - P)
        y = cy + 130 + 42 + 24

    y = section(y, "FIG_003 / PUBLIC ACTIVITY · 365 DAYS")
    y = stats([(a, fmt(b)) for a, b in d["activity"]], 2 if mobile else 6, y, 4 if mobile else 5)

    y = section(y, "FIG_004 / TOP REPOSITORIES")
    for r in d["top"]:
        meta = f'★ {r["stargazers_count"]}' + (f' · {r["language"]}' if r["language"] else "")
        desc = r["description"] or "No description yet"
        if mobile:
            o.append(tx(P, y + 14, clip(r["name"], 26), 13, t["accent"], weight=700))
            o.append(tx(W - P, y + 14, meta, 11, t["muted"], anchor="end"))
            o.append(tx(P, y + 34, clip(desc, 55), 13, t["muted"], SERIF))
            y += 52
        else:
            o.append(tx(P, y + 14, clip(r["name"], 34), 14, t["accent"], weight=700))
            o.append(tx(P + 330, y + 14, clip(desc, 80), 15, t["muted"], SERIF))
            o.append(tx(W - P, y + 14, meta, 12, t["muted"], anchor="end"))
            y += 36
    y += 8

    y = section(y, "FIG_005 / CURRENTLY")
    for lab, s in ROLES:
        o.append(tx(P, y + 14, lab, 11 if mobile else 12, t["accent"], weight=700, ls=1))
        o.append(tx(P + (90 if mobile else 130), y + 14, clip(s, 38 if mobile else 100),
                    14 if mobile else 18, t["fg"], SERIF))
        y += 28 if mobile else 32
    y += 8

    y = section(y, "FIG_006 / TECH STACK")
    x = P
    for s in STACK:
        w = len(s) * (6.8 if mobile else 7.4) + 22
        if x + w > W - P:
            x = P
            y += 36
        o.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="none" stroke="{t["rule"]}"/>')
        o.append(tx(f"{x + w / 2:.1f}", y + 17, s, 11 if mobile else 12, t["fg"], anchor="middle"))
        x += w + 8
    y += 56
    o.append(tx(P, y, "PUBLIC DATA ONLY · REFRESHED DAILY BY GITHUB ACTIONS", 10, t["muted"], ls=1))
    H = y + 24

    defs = (f'<defs><pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="0.9" fill="{t["dot"]}"/></pattern></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + defs + f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}"/>'
            + f'<rect width="{W}" height="{H}" rx="12" fill="url(#dots)"/>' + "".join(o) + "</svg>")


def main():
    d = fetch()
    os.makedirs("assets", exist_ok=True)
    files = {
        "assets/public-builder-profile.svg": ("light", False),
        "assets/public-builder-profile-dark.svg": ("dark", False),
        "assets/public-builder-profile-mobile.svg": ("light", True),
        "assets/public-builder-profile-mobile-dark.svg": ("dark", True),
    }
    for path, (theme, mobile) in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(theme, mobile, d))
        print("wrote", path)


if __name__ == "__main__":
    main()
