#!/usr/bin/env python3
"""Generate the install-flow diagrams used by README.md / README.zh.md.

The diagrams are committed as static SVG (assets/install-flow.{en,zh}.svg)
instead of Mermaid: GitHub renders Mermaid inside an iframe served by
viewscreen.githubusercontent.com, and that host is routinely unreachable behind
proxies / on some networks, which surfaces as "Unable to render rich display".
Static SVG renders everywhere, looks the same in light and dark GitHub themes,
and keeps the repo self-contained.

The brand-fish watermark is read from the plugin source (src/client/critters.ts)
so the diagram follows the shipped logo.

Usage:
    python3 tools/make-install-flow-svg.py            # write assets/
    python3 tools/make-install-flow-svg.py --check    # fail if assets are stale
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

W, H = 960, 1180
CARD_X, CARD_W = 96, 768
CARD_CX = CARD_X + CARD_W // 2
STEP_H, STEP_PITCH, STEP_TOP = 64, 92, 204
N_STEPS = 7

FF = ("'Segoe UI', 'Inter', 'Helvetica Neue', Arial, "
      "'Microsoft YaHei', 'PingFang SC', 'Noto Sans SC', sans-serif")
MONO = "'JetBrains Mono', 'Cascadia Mono', Consolas, 'Courier New', monospace"

COPY = {
    "en": {
        "badge": "DSH DESKTOP  \u00b7  AQUA THEME",
        "title": "Install flow",
        "subtitle": "DeepSeek Harness desktop \u00b7 glassmorphism theme",
        "steps": [
            ("Open the DSH desktop app", None),
            ("Settings \u2192 Plugins \u2192 Plugin Manager", None),
            ("Click Add plugin", None),
            ("Paste the install string", "github:hkd-Duo/dsh-client-ui-aqua-desktop"),
            ("Wait for the install to finish", None),
            ("Fully quit the app", None),
            ("Reopen the app", None),
        ],
        "decision": "Glass effect visible after reopening?",
        "yes": "Installed",
        "yes_sub": "the glass UI is active",
        "no": "Check plugin version",
        "no_chip": "1.3.1-patch.9-dshfix",
        "loop": "fix \u2192 reopen",
        "tip": "Tip: quitting the app is the only mandatory step \u2014 the list is read at startup.",
        "version": "DSH 0.2.1-rc.5  \u00b7  v1.3.1-patch.9-dshfix",
        "yes_label": "YES",
        "no_label": "NO",
        "title_id": "Install flow",
    },
    "zh": {
        "badge": "DSH 桌面端  \u00b7  AQUA 玻璃主题",
        "title": "安装流程",
        "subtitle": "DeepSeek Harness 桌面端 \u00b7 玻璃拟态主题",
        "steps": [
            ("打开 DSH 桌面应用", None),
            ("设置 \u2192 插件 \u2192 插件管理器", None),
            ("点击「添加插件」", None),
            ("粘贴安装标识", "github:hkd-Duo/dsh-client-ui-aqua-desktop"),
            ("等待安装完成", None),
            ("完全退出应用", None),
            ("重新打开应用", None),
        ],
        "decision": "重新打开后，界面是否变成玻璃？",
        "yes": "安装完成",
        "yes_sub": "玻璃界面已生效",
        "no": "检查插件版本",
        "no_chip": "1.3.1-patch.9-dshfix",
        "loop": "修复后重开",
        "tip": "提示：唯一必须做的一步是「完全退出应用再重开」\u2014\u2014插件列表只在启动时读取。",
        "version": "DSH 0.2.1-rc.5  \u00b7  v1.3.1-patch.9-dshfix",
        "yes_label": "是",
        "no_label": "否",
        "title_id": "安装流程",
    },
}


def fish_path() -> str:
    """Read the brand-fish path from the plugin source (single source of truth)."""
    src = open(os.path.join(ROOT, "src", "client", "critters.ts"), encoding="utf-8").read()
    m = re.search(r"const FISH_PATH =([\s\S]*?)\n\n", src)
    if m is None:
        raise SystemExit("could not locate FISH_PATH in src/client/critters.ts")
    parts = re.findall(r"'([^']*)'", m.group(1))
    return "".join(parts)


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(lang: str, fish: str) -> str:
    c = COPY[lang]
    out = []
    a = out.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-labelledby="t d">')
    a(f'<title id="t">Aqua theme \u2014 {esc(c["title_id"])}</title>')
    a('<desc id="d">Install flow for the DSH desktop app: open the app, open the plugin manager, '
      'add the plugin, wait, fully quit, reopen, then verify the glass theme is active.</desc>')

    a('<defs>')
    a('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
      '<stop offset="0" stop-color="#060c13"/>'
      '<stop offset=".42" stop-color="#0a1622"/>'
      '<stop offset="1" stop-color="#07101a"/></linearGradient>')
    a('<radialGradient id="glowA" cx=".16" cy=".06" r=".62">'
      '<stop offset="0" stop-color="#2fd9c6" stop-opacity=".20"/>'
      '<stop offset="1" stop-color="#2fd9c6" stop-opacity="0"/></radialGradient>')
    a('<radialGradient id="glowB" cx=".92" cy=".82" r=".58">'
      '<stop offset="0" stop-color="#4c8dff" stop-opacity=".18"/>'
      '<stop offset="1" stop-color="#4c8dff" stop-opacity="0"/></radialGradient>')
    a('<radialGradient id="glowC" cx=".78" cy=".18" r=".34">'
      '<stop offset="0" stop-color="#39e0cf" stop-opacity=".10"/>'
      '<stop offset="1" stop-color="#39e0cf" stop-opacity="0"/></radialGradient>')
    a('<linearGradient id="title" x1="0" y1="0" x2="1" y2="0">'
      '<stop offset="0" stop-color="#f3fcff"/><stop offset="1" stop-color="#a9ece4"/></linearGradient>')
    a('<linearGradient id="hairline" x1="0" y1="0" x2="1" y2="0">'
      '<stop offset="0" stop-color="#39e0cf" stop-opacity="0"/>'
      '<stop offset=".5" stop-color="#39e0cf" stop-opacity=".45"/>'
      '<stop offset="1" stop-color="#39e0cf" stop-opacity="0"/></linearGradient>')
    a('<linearGradient id="cardFill" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#ffffff" stop-opacity=".055"/>'
      '<stop offset="1" stop-color="#ffffff" stop-opacity=".018"/></linearGradient>')
    a('<linearGradient id="cardStroke" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#9fd6ff" stop-opacity=".26"/>'
      '<stop offset="1" stop-color="#9fd6ff" stop-opacity=".09"/></linearGradient>')
    a('<linearGradient id="badgeFill" x1="0" y1="0" x2="1" y2="1">'
      '<stop offset="0" stop-color="#35e0cd"/><stop offset="1" stop-color="#4f9dff"/></linearGradient>')
    a('<linearGradient id="fishGrad" x1="0" y1="0" x2="1" y2="1">'
      '<stop offset="0" stop-color="#39e0cf" stop-opacity=".9"/>'
      '<stop offset="1" stop-color="#4f9dff" stop-opacity=".55"/></linearGradient>')
    a('<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">'
      '<circle cx="1.4" cy="1.4" r="1.1" fill="#a9dcff" fill-opacity=".065"/></pattern>')
    a('<filter id="shadow" x="-15%" y="-40%" width="130%" height="190%">'
      '<feDropShadow dx="0" dy="7" stdDeviation="12" flood-color="#000000" flood-opacity=".42"/></filter>')
    a('<marker id="arr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" '
      'orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 Z" fill="#3fd9cd"/></marker>')
    a('<marker id="arrAmber" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" '
      'orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 Z" fill="#e8b163"/></marker>')
    a('<marker id="arrGreen" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" '
      'orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 Z" fill="#4ade9e"/></marker>')
    a('</defs>')

    # background
    a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#glowA)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#glowB)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#glowC)"/>')
    a(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="26" fill="none" '
      f'stroke="#8fc8ff" stroke-opacity=".10"/>')

    # brand-fish watermark + bubbles
    a(f'<g transform="translate(786 30) scale(4.8)" opacity=".5" fill="none" stroke="url(#fishGrad)" '
      f'stroke-width=".32" stroke-linejoin="round"><path d="{fish}"/></g>')
    for cx, cy, r, o in ((894, 58, 4.6, .30), (916, 104, 3.2, .24), (884, 140, 2.2, .18)):
        a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#7fe6d8" stroke-opacity="{o}"/>')

    # header
    a(f'<rect x="{CARD_X}" y="46" width="252" height="28" rx="14" fill="#3fd9cd" fill-opacity=".07" '
      f'stroke="#3fd9cd" stroke-opacity=".28"/>')
    a(f'<text x="{CARD_X + 126}" y="64.5" text-anchor="middle" font-family="{FF}" font-size="10.5" '
      f'letter-spacing="1.5" fill="#7fe6d8">{esc(c["badge"])}</text>')
    a(f'<text x="{CARD_X}" y="126" font-family="{FF}" font-size="36" font-weight="600" '
      f'fill="url(#title)" letter-spacing=".2">{esc(c["title"])}</text>')
    a(f'<text x="{CARD_X}" y="153" font-family="{FF}" font-size="14.5" fill="#8aa4bd" '
      f'letter-spacing=".2">{esc(c["subtitle"])}</text>')
    a(f'<rect x="{CARD_X}" y="176" width="{CARD_W}" height="1" fill="url(#hairline)"/>')

    # steps
    for i, (label, chip) in enumerate(c["steps"]):
        y = STEP_TOP + i * STEP_PITCH
        cy = y + STEP_H / 2
        a(f'<g filter="url(#shadow)">'
          f'<rect x="{CARD_X}" y="{y}" width="{CARD_W}" height="{STEP_H}" rx="15" '
          f'fill="url(#cardFill)" stroke="url(#cardStroke)" stroke-width="1"/></g>')
        a(f'<rect x="{CARD_X + 18}" y="{y + 1.5}" width="{CARD_W - 36}" height="1" '
          f'fill="#ffffff" fill-opacity=".07"/>')
        a(f'<circle cx="{CARD_X + 42}" cy="{cy}" r="23" fill="#3fd9cd" fill-opacity=".08"/>')
        a(f'<circle cx="{CARD_X + 42}" cy="{cy}" r="17" fill="url(#badgeFill)"/>')
        a(f'<text x="{CARD_X + 42}" y="{cy + 4.6}" text-anchor="middle" font-family="{FF}" '
          f'font-size="13" font-weight="700" fill="#04141a">{i + 1}</text>')
        a(f'<text x="{CARD_X + 78}" y="{cy + 5.6}" font-family="{FF}" font-size="16.5" '
          f'fill="#e2eefb">{esc(label)}</text>')
        if chip is not None:
            chip_w = 84 + len(chip) * 7.35
            chip_x = CARD_X + CARD_W - 20 - chip_w
            a(f'<rect x="{chip_x:.1f}" y="{cy - 15}" width="{chip_w:.1f}" height="30" rx="8" '
              f'fill="#3fd9cd" fill-opacity=".08" stroke="#3fd9cd" stroke-opacity=".26"/>')
            a(f'<text x="{chip_x + chip_w / 2:.1f}" y="{cy + 4.4}" text-anchor="middle" '
              f'font-family="{MONO}" font-size="12.6" fill="#9ff0e2">{esc(chip)}</text>')
        if i < N_STEPS - 1:
            y2 = y + STEP_H
            a(f'<path d="M{CARD_CX} {y2 + 4} V{y2 + STEP_PITCH - 5}" stroke="#3fd9cd" '
              f'stroke-opacity=".55" stroke-width="2" fill="none" marker-end="url(#arr)"/>')

    # decision
    step7_bottom = STEP_TOP + (N_STEPS - 1) * STEP_PITCH + STEP_H
    dec_y, dec_h = step7_bottom + 28, 76
    dec_cy = dec_y + dec_h / 2
    a(f'<path d="M{CARD_CX} {step7_bottom + 4} V{dec_y - 5}" stroke="#3fd9cd" stroke-opacity=".55" '
      f'stroke-width="2" fill="none" marker-end="url(#arr)"/>')
    a(f'<g filter="url(#shadow)"><rect x="{CARD_X}" y="{dec_y}" width="{CARD_W}" height="{dec_h}" '
      f'rx="15" fill="#3fd9cd" fill-opacity=".055" stroke="#3fd9cd" stroke-opacity=".30"/></g>')
    a(f'<circle cx="{CARD_X + 42}" cy="{dec_cy}" r="23" fill="#3fd9cd" fill-opacity=".10"/>')
    a(f'<circle cx="{CARD_X + 42}" cy="{dec_cy}" r="17" fill="none" stroke="#3fd9cd" '
      f'stroke-opacity=".65" stroke-width="1.4"/>')
    a(f'<text x="{CARD_X + 42}" y="{dec_cy + 6.5}" text-anchor="middle" font-family="{FF}" '
      f'font-size="17" font-weight="600" fill="#8ff2e6">?</text>')
    a(f'<text x="{CARD_X + 78}" y="{dec_cy + 5.6}" font-family="{FF}" font-size="16.5" '
      f'fill="#e9f7ff">{esc(c["decision"])}</text>')

    # branches
    y_br_end = dec_y + dec_h + 3
    yes_cx, no_cx = 275, 688
    a(f'<path d="M{CARD_CX - 42} {y_br_end} C{CARD_CX - 90} {y_br_end + 32} {yes_cx + 60} {y_br_end + 34} '
      f'{yes_cx} {y_br_end + 40}" stroke="#4ade9e" stroke-opacity=".62" stroke-width="2" fill="none" '
      f'marker-end="url(#arrGreen)"/>')
    a(f'<path d="M{CARD_CX + 42} {y_br_end} C{CARD_CX + 90} {y_br_end + 32} {no_cx - 80} {y_br_end + 34} '
      f'{no_cx} {y_br_end + 40}" stroke="#e8b163" stroke-opacity=".62" stroke-width="2" fill="none" '
      f'marker-end="url(#arrAmber)"/>')
    a(f'<text x="{CARD_CX - 148}" y="{y_br_end + 34}" text-anchor="middle" font-family="{FF}" '
      f'font-size="11.5" letter-spacing="1.4" fill="#6ee7b7">{esc(c["yes_label"])}</text>')
    a(f'<text x="{CARD_CX + 148}" y="{y_br_end + 34}" text-anchor="middle" font-family="{FF}" '
      f'font-size="11.5" letter-spacing="1.4" fill="#e8b163">{esc(c["no_label"])}</text>')

    # outcomes
    out_y, out_h = dec_y + dec_h + 48, 76
    a(f'<g filter="url(#shadow)"><rect x="150" y="{out_y}" width="250" height="{out_h}" rx="15" '
      f'fill="#34d399" fill-opacity=".09" stroke="#4ade9e" stroke-opacity=".55"/></g>')
    a(f'<circle cx="188" cy="{out_y + 38}" r="16" fill="#4ade9e" fill-opacity=".16"/>')
    a(f'<path d="M181 {out_y + 38.5} l5 5.5 l9.5 -11" fill="none" stroke="#7ef0bd" stroke-width="2.2" '
      f'stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<text x="216" y="{out_y + 33}" font-family="{FF}" font-size="16.5" font-weight="600" '
      f'fill="#b9f7d6">{esc(c["yes"])}</text>')
    a(f'<text x="216" y="{out_y + 53}" font-family="{FF}" font-size="11.5" fill="#77b99c">'
      f'{esc(c["yes_sub"])}</text>')
    a(f'<g filter="url(#shadow)"><rect x="512" y="{out_y}" width="352" height="{out_h}" rx="15" '
      f'fill="#e8b163" fill-opacity=".075" stroke="#e8b163" stroke-opacity=".48"/></g>')
    a(f'<circle cx="550" cy="{out_y + 38}" r="16" fill="#e8b163" fill-opacity=".14"/>')
    a(f'<text x="550" y="{out_y + 44}" text-anchor="middle" font-family="{FF}" font-size="17" '
      f'font-weight="600" fill="#f3c983">!</text>')
    a(f'<text x="578" y="{out_y + 30}" font-family="{FF}" font-size="14.5" fill="#f3d6a4">'
      f'{esc(c["no"])}</text>')
    a(f'<rect x="578" y="{out_y + 40}" width="236" height="24" rx="7" fill="#e8b163" fill-opacity=".10" '
      f'stroke="#e8b163" stroke-opacity=".28"/>')
    a(f'<text x="590" y="{out_y + 56.5}" font-family="{MONO}" font-size="12.2" fill="#f7d9a3">'
      f'{esc(c["no_chip"])}</text>')

    # dashed loop-back to step 7
    step7_y = STEP_TOP + (N_STEPS - 1) * STEP_PITCH
    loop_mid = step7_y + STEP_H / 2
    no_right = 864
    no_mid = out_y + out_h / 2
    a(f'<path d="M{no_right} {no_mid} H906 V{loop_mid + 6} H{no_right + 6}" stroke="#e8b163" '
      f'stroke-opacity=".5" stroke-width="1.7" fill="none" stroke-dasharray="5 5" '
      f'marker-end="url(#arrAmber)"/>')
    a(f'<text transform="translate(927 {no_mid - 30}) rotate(-90)" font-family="{FF}" '
      f'font-size="11.2" letter-spacing=".6" fill="#d8b57a">{esc(c["loop"])}</text>')

    # footer
    a(f'<rect x="{CARD_X}" y="1100" width="{CARD_W}" height="1" fill="url(#hairline)"/>')
    a(f'<circle cx="{CARD_X + 7}" cy="1128" r="7" fill="none" stroke="#8aa4bd" stroke-opacity=".55"/>')
    a(f'<text x="{CARD_X + 7}" y="1132" text-anchor="middle" font-family="{FF}" font-size="9.5" '
      f'fill="#9db4c9">i</text>')
    a(f'<text x="{CARD_X + 24}" y="1132" font-family="{FF}" font-size="12.1" fill="#7b93ab">'
      f'{esc(c["tip"])}</text>')
    a(f'<text x="{CARD_X + CARD_W}" y="1132" text-anchor="end" font-family="{MONO}" font-size="10.7" '
      f'fill="#647c95">{esc(c["version"])}</text>')

    a('</svg>')
    return "\n".join(out) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    fish = fish_path()
    drift = False
    for lang in ("en", "zh"):
        target = os.path.join(ASSETS, f"install-flow.{lang}.svg")
        content = svg(lang, fish)
        if check:
            current = open(target, encoding="utf-8").read() if os.path.exists(target) else None
            if current != content:
                print(f"stale diagram: {target} (run python3 tools/make-install-flow-svg.py)")
                drift = True
            else:
                print(f"up to date: {target}")
        else:
            with open(target, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            print(f"wrote {target} ({len(content)} bytes)")
    if check and drift:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
