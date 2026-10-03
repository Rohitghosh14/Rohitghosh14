import json, os, urllib.parse, urllib.request
from html import escape

USER = "Rohitghosh14"
NAME = "Rohit Ghosh"
TAGLINE = "AI/ML Engineering Student · Kolkata, India"
SUB = "Building ML systems end-to-end, not just notebooks"
STACK = ["Python", "PyTorch", "TensorFlow", "scikit-learn", "FastAPI", "Flask",
         "Streamlit", "NLP", "Computer Vision", "Git", "Kaggle"]
ROLES = [("Building", "AOD-Net, from-scratch image dehazing rebuild"),
         ("Building", "Rio, desktop AI companion"),
         ("Learning", "Deep learning, NLP and MLOps through projects"),
         ("Training", "On Kaggle / Colab (no local GPU)")]
FEATURED = ["exoplanet-habitability-predictor", "fifa-worldcup-2026-predictor",
            "movie-recommender-model", "GUI_PASSWORD_MANAGER", "rio-ai-companion"]
REGIONS = [("World", ""), ("India", "location:India"), ("USA", 'location:"United States"'),
           ("UK", 'location:"United Kingdom"'), ("China", "location:China")]

THEMES = {
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#656d76",
                  accent="#0969da", card="#f6f8fa", border="#d0d7de"),
    "dark": dict(bg="#0d1117", fg="#e6edf3", muted="#8b949e",
                 accent="#58a6ff", card="#161b22", border="#30363d"),
}
FONT = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"


def api(path):
    req = urllib.request.Request("https://api.github.com" + path)
    req.add_header("Accept", "application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def rank(followers, extra):
    q = f"followers:>{followers} {extra}".strip()
    try:
        return api("/search/users?q=" + urllib.parse.quote(q))["total_count"] + 1
    except Exception:
        return None


def fmt(n):
    if n is None:
        return "-"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def fetch():
    user = api(f"/users/{USER}")
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in repos)
    prs = api(f"/search/issues?q=author:{USER}+is:pr+is:merged+-user:{USER}")["total_count"]
    by = {r["name"].lower(): r for r in repos}
    top = [by[n.lower()] for n in FEATURED if n.lower() in by]
    langs = {}
    for r in repos:
        if r["language"]:
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    langs = sorted(langs.items(), key=lambda x: -x[1])[:5]
    f = user["followers"]
    return dict(
        stats=[("Public repos", user["public_repos"]), ("Stars earned", stars),
               ("Followers", f), ("Merged PRs (external)", prs)],
        ranks=[(name, rank(f, extra)) for name, extra in REGIONS],
        langs=langs, top=top)


def txt(x, y, s, size, color, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" '
            f'text-anchor="{anchor}" font-family="{FONT}">{escape(str(s))}</text>')


def rect(x, y, w, h, fill, stroke=None, rx=10):
    s = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}/>'


def clip(s, n):
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"


def title(o, t, pad, y, s):
    o.append(txt(pad, y + 12, s, 14, t["fg"], 700))
    return y + 26


def grid(o, t, items, cols, y, pad, W, bh=64):
    gap = 12
    bw = (W - 2 * pad - (cols - 1) * gap) / cols
    for i, (label, val) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (bw + gap)
        yy = y + r * (bh + gap)
        o.append(rect(x, yy, bw, bh, t["card"], t["border"]))
        o.append(txt(x + 14, yy + bh / 2 + 2, val, 22, t["fg"], 700))
        o.append(txt(x + 14, yy + bh - 12, label, 12, t["muted"]))
    return y + ((len(items) + cols - 1) // cols) * (bh + gap)


def render(theme, mobile, d):
    t = THEMES[theme]
    W = 480 if mobile else 900
    pad = 28
    o = []
    y = 58
    o.append(txt(pad, y, NAME, 24 if mobile else 32, t["fg"], 700)); y += 28
    o.append(txt(pad, y, TAGLINE, 14 if mobile else 16, t["accent"], 600)); y += 22
    o.append(txt(pad, y, clip(SUB, 52 if mobile else 100), 12 if mobile else 13, t["muted"])); y += 30

    y = grid(o, t, d["stats"], 2 if mobile else 4, y, pad, W) + 8

    y = title(o, t, pad, y, "Follower rank (GitHub, by followers)")
    ranks = [(n, "#" + fmt(v) if v else "-") for n, v in d["ranks"]]
    y = grid(o, t, ranks, 3 if mobile else 5, y, pad, W, 56) + 8

    y = title(o, t, pad, y, "Currently")
    for lab, s in ROLES:
        o.append(rect(pad, y, W - 2 * pad, 34, t["card"], t["border"]))
        o.append(txt(pad + 14, y + 22, lab, 12, t["accent"], 700))
        o.append(txt(pad + 92, y + 22, clip(s, 38 if mobile else 90), 13, t["fg"]))
        y += 42
    y += 8

    y = title(o, t, pad, y, "Languages (public repos)")
    mx = max([c for _, c in d["langs"]] or [1])
    bmax = W - 2 * pad - 110 - 40
    for name, c in d["langs"]:
        o.append(txt(pad, y + 10, name, 12, t["fg"]))
        o.append(rect(pad + 110, y, bmax, 10, t["card"], None, 5))
        o.append(rect(pad + 110, y, max(8, bmax * c / mx), 10, t["accent"], None, 5))
        o.append(txt(pad + 110 + bmax + 10, y + 10, c, 12, t["muted"]))
        y += 24
    y += 10

    y = title(o, t, pad, y, "Tech stack")
    x = pad
    for s in STACK:
        w = len(s) * 7.6 + 24
        if x + w > W - pad:
            x = pad
            y += 34
        o.append(rect(x, y, w, 26, t["card"], t["border"], 13))
        o.append(txt(x + w / 2, y + 17, s, 12, t["accent"], 600, "middle"))
        x += w + 8
    y += 48

    y = title(o, t, pad, y, "Top repositories")
    for r in d["top"]:
        o.append(rect(pad, y, W - 2 * pad, 54, t["card"], t["border"]))
        o.append(txt(pad + 14, y + 22, clip(r["name"], 22 if mobile else 40), 14, t["accent"], 700))
        meta = f'★ {r["stargazers_count"]}' + (f' · {r["language"]}' if r["language"] else "")
        o.append(txt(W - pad - 14, y + 22, meta, 12, t["muted"], 400, "end"))
        o.append(txt(pad + 14, y + 42, clip(r["description"] or "No description", 44 if mobile else 95), 12, t["muted"]))
        y += 62
    H = y + 14

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            + "".join(o) + "</svg>")


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
