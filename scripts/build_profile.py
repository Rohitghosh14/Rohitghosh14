import json, os, urllib.request
from html import escape

USER = "Rohitghosh14"
NAME = "Rohit Ghosh"
TAGLINE = "AI/ML Engineering Student · Kolkata, India"
SUB = "Building ML systems end-to-end, not just notebooks"
STACK = ["Python", "PyTorch", "TensorFlow", "scikit-learn", "FastAPI",
         "Flask", "Streamlit", "NLP", "Computer Vision", "Git", "Kaggle"]

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


def fetch():
    user = api(f"/users/{USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&type=owner")
    repos = [r for r in repos if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in repos)
    prs = api(f"/search/issues?q=author:{USER}+is:pr+is:merged+-user:{USER}")["total_count"]
    top = sorted(repos, key=lambda r: (r["stargazers_count"], r["pushed_at"]), reverse=True)[:5]
    stats = [("Public repos", user["public_repos"]), ("Stars earned", stars),
             ("Followers", user["followers"]), ("Merged PRs (external)", prs)]
    return stats, top


def txt(x, y, s, size, color, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}" font-family="{FONT}">{escape(str(s))}</text>')


def clip(s, n):
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"


def render(theme, mobile, stats, top):
    t = THEMES[theme]
    W = 480 if mobile else 900
    pad = 28
    o = []
    y = 58
    o.append(txt(pad, y, NAME, 24 if mobile else 32, t["fg"], 700))
    y += 28
    o.append(txt(pad, y, TAGLINE, 14 if mobile else 16, t["accent"], 600))
    y += 22
    o.append(txt(pad, y, clip(SUB, 52 if mobile else 100), 12 if mobile else 13, t["muted"]))
    y += 30

    # stat boxes
    cols = 2 if mobile else 4
    gap = 12
    bw = (W - 2 * pad - (cols - 1) * gap) / cols
    bh = 64
    for i, (label, val) in enumerate(stats):
        r, c = divmod(i, cols)
        x = pad + c * (bw + gap)
        yy = y + r * (bh + gap)
        o.append(f'<rect x="{x}" y="{yy}" width="{bw}" height="{bh}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>')
        o.append(txt(x + 14, yy + 30, val, 22, t["fg"], 700))
        o.append(txt(x + 14, yy + 50, label, 12, t["muted"]))
    y += ((len(stats) + cols - 1) // cols) * (bh + gap) + 14

    # tech stack chips
    o.append(txt(pad, y + 12, "Tech stack", 14, t["fg"], 700))
    y += 26
    x = pad
    for s in STACK:
        w = len(s) * 7.6 + 24
        if x + w > W - pad:
            x = pad
            y += 34
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{t["card"]}" stroke="{t["border"]}"/>')
        o.append(txt(x + w / 2, y + 17, s, 12, t["accent"], 600, "middle"))
        x += w + 8
    y += 48

    # top repositories
    o.append(txt(pad, y, "Top repositories", 14, t["fg"], 700))
    y += 14
    for r in top:
        o.append(f'<rect x="{pad}" y="{y}" width="{W - 2 * pad}" height="54" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>')
        o.append(txt(pad + 14, y + 22, clip(r["name"], 22 if mobile else 40), 14, t["accent"], 700))
        meta = f'★ {r["stargazers_count"]}' + (f' · {r["language"]}' if r["language"] else "")
        o.append(txt(W - pad - 14, y + 22, meta, 12, t["muted"], 400, "end"))
        o.append(txt(pad + 14, y + 42, clip(r["description"] or "No description", 44 if mobile else 95), 12, t["muted"]))
        y += 62
    H = y + 14

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>' + "".join(o) + "</svg>")
    return svg


def main():
    stats, top = fetch()
    os.makedirs("assets", exist_ok=True)
    files = {
        "assets/public-builder-profile.svg": ("light", False),
        "assets/public-builder-profile-dark.svg": ("dark", False),
        "assets/public-builder-profile-mobile.svg": ("light", True),
        "assets/public-builder-profile-mobile-dark.svg": ("dark", True),
    }
    for path, (theme, mobile) in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(theme, mobile, stats, top))
        print("wrote", path)


if __name__ == "__main__":
    main()
