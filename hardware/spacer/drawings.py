#!/usr/bin/env python3
"""Dimensioned 2D drawings (SVG) of the Mini Floppy spacer variants.

Parts are turned (rotationally symmetric), so each part is described by
its outer and inner radius profile over the height z. Values match
spacer.scad; change both together.
"""
import sys

S = 6.0          # drawing scale (6:1), SVG user unit = 1 mm on paper
STROKE = 0.35
FONT = 3.2

# Profiles: list of (r, z) points from bottom (z=0) to top.
SCREW_SPACER = {
    "name": "Variante A: Schraub-Abstandshalter",
    "outer": [(3.0, 0), (3.0, 11)],
    "inner": [(1.3, 0), (1.3, 11)],
    "dims_v": [(0, 11, "11")],
    "dims_d": [(3.0, "Ø6"), (1.3, "Ø2,6")],
    "notes": ["Kernloch Ø2,6: M3 schneidet Gewinde selbst",
              "Fase 0,4×45° an beiden Enden", "Druck stehend, 100 % Füllung"],
}
SNAP_SLEEVE = {
    "name": "Variante B: Hülse",
    "outer": [(3.0, 0), (3.0, 11)],
    "inner": [(1.45, 0), (1.45, 2), (1.8, 2), (1.8, 9), (1.45, 9), (1.45, 11)],
    "dims_v": [(0, 2, "2"), (2, 9, "7"), (9, 11, "2"), (0, 11, "11")],
    "dims_d": [(3.0, "Ø6"), (1.8, "Ø3,6"), (1.45, "Ø2,9")],
    "notes": ["Rastkante 2 mm je Ende",
              "Fase 0,3×45° an beiden Enden",
              "Druck stehend, 100 % Füllung"],
}
SNAP_PIN = {
    "name": "Variante B: Raststift (2×)",
    "outer": [(3.0, 0), (3.0, 1.2), (1.4, 1.2), (1.4, 4.9), (1.7, 4.9),
              (1.7, 6.1), (1.1, 6.7)],
    "inner": None,
    "slot": (0.8, 2.7, 6.7),
    "dims_v": [(0, 1.2, "1,2"), (1.2, 4.9, "3,7"), (4.9, 6.7, "1,8"),
               (0, 6.7, "6,7")],
    "dims_d": [(3.0, "Ø6"), (1.7, "Ø3,4"), (1.4, "Ø2,8")],
    "notes": ["Schlitz 0,8 breit, 4 lang ab Spitze",
              "Druck Kopf nach unten",
              "PETG empfohlen (federt)"],
}


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.items = w, h, []

    def line(self, x0, y0, x1, y1, dash=False, width=STROKE, cls=""):
        d = ' stroke-dasharray="1.5,1"' if dash else ""
        self.items.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" '
                          f'y2="{y1:.2f}" stroke="#000" stroke-width="{width}"{d}/>')

    def poly(self, pts, fill="none", hatch=False):
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        f = "url(#hatch)" if hatch else fill
        self.items.append(f'<polygon points="{p}" fill="{f}" stroke="#000" '
                          f'stroke-width="{STROKE}"/>')

    def circle(self, cx, cy, r, dash=False):
        d = ' stroke-dasharray="1.5,1"' if dash else ""
        self.items.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" '
                          f'fill="none" stroke="#000" stroke-width="{STROKE}"{d}/>')

    def text(self, x, y, s, size=FONT, anchor="middle", rot=0, bold=False):
        t = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
        b = ' font-weight="bold"' if bold else ""
        self.items.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" '
                          f'font-family="DejaVu Sans, Arial" text-anchor="{anchor}"{b}{t}>'
                          f'{s}</text>')

    def arrow_dim_v(self, x, y0, y1, label, ext_from=None):
        if ext_from is not None:
            for y in (y0, y1):
                self.line(ext_from, y, x + 1.5 * (1 if x > ext_from else -1), y, width=0.18)
        self.line(x, y0, x, y1, width=0.18)
        for y, s in ((y0, 1), (y1, -1)):
            self.poly([(x, y), (x - 0.8, y + 2.2 * s), (x + 0.8, y + 2.2 * s)], fill="#000")
        self.text(x - 1.2, (y0 + y1) / 2, label, rot=-90)

    def arrow_dim_h(self, y, x0, x1, label):
        self.line(x0, y, x1, y, width=0.18)
        for x, s in ((x0, 1), (x1, -1)):
            self.poly([(x, y), (x + 2.2 * s, y - 0.8), (x + 2.2 * s, y + 0.8)], fill="#000")
        self.text((x0 + x1) / 2, y - 1.2, label)

    def render(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" '
                f'height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">'
                '<defs><pattern id="hatch" width="1.6" height="1.6" '
                'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                '<line x1="0" y1="0" x2="0" y2="1.6" stroke="#000" stroke-width="0.25"/>'
                '</pattern></defs>'
                f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>')
        return head + "".join(self.items) + "</svg>"


def side(svg, part, cx, base, section):
    """Front view (hidden bore dashed) or full section A-A at axis cx."""
    outer = [(r * S, z * S) for r, z in part["outer"]]
    inner = [(r * S, z * S) for r, z in part["inner"]] if part["inner"] else None
    top = max(z for _, z in outer)

    def P(x, z):
        return (cx + x, base - z)

    if section:
        if inner:
            for sign in (1, -1):
                pts = [P(sign * x, z) for x, z in outer] + \
                      [P(sign * x, z) for x, z in reversed(inner)]
                svg.poly(pts, hatch=True)
        else:
            pts = [P(x, z) for x, z in outer] + [P(-x, z) for x, z in reversed(outer)]
            svg.poly(pts, hatch=True)
    else:
        pts = [P(0, 0)] + [P(x, z) for x, z in outer] + [P(0, top)]
        pts += [P(-x, z) for x, z in reversed(outer)]
        svg.poly(pts)
        for (x0, z0), (x1, z1) in zip(outer, outer[1:]):
            if z0 == z1:
                svg.line(*P(-max(x0, x1), z0), *P(max(x0, x1), z0))
        if inner:
            for sign in (1, -1):
                for (x0, z0), (x1, z1) in zip(inner, inner[1:]):
                    svg.line(*P(sign * x0, z0), *P(sign * x1, z1), dash=True)
            for (x0, z0), (x1, z1) in zip(inner, inner[1:]):
                if z0 == z1:
                    svg.line(*P(-max(x0, x1), z0), *P(max(x0, x1), z0), dash=True)
    if "slot" in part and not section:
        w, z0, z1 = part["slot"]
        for sign in (1, -1):
            svg.line(*P(sign * w / 2 * S, z0 * S), *P(sign * w / 2 * S, top), dash=False)
        svg.line(*P(-w / 2 * S, z0 * S), *P(w / 2 * S, z0 * S))
    svg.line(cx, base + 3, cx, base - top - 3, dash=True, width=0.18)


def top_view(svg, part, cx, cy):
    radii = sorted({r for r, _ in part["outer"]} |
                   ({r for r, _ in part["inner"]} if part["inner"] else set()),
                   reverse=True)
    inner_min = min(r for r, _ in part["inner"]) if part["inner"] else None
    outer_r = {r for r, _ in part["outer"]}
    for r in radii:
        # bore steps below the narrowest bore are hidden from above
        svg.circle(cx, cy, r * S, dash=(r not in outer_r and r != inner_min))
    if "slot" in part:
        w = part["slot"][0] * S / 2
        rmax = 1.7 * S
        svg.line(cx - w, cy - rmax, cx - w, cy + rmax)
        svg.line(cx + w, cy - rmax, cx + w, cy + rmax)
    svg.line(cx - 22, cy, cx + 22, cy, dash=True, width=0.18)
    svg.line(cx, cy - 22, cx, cy + 22, dash=True, width=0.18)


def part_sheet(svg, part, x0, y0):
    """One row: front view, section A-A, top view, with dimensions."""
    height = max(z for _, z in part["outer"]) * S
    base = y0 + height + 14
    svg.text(x0, y0 + 4, part["name"], size=4.2, anchor="start", bold=True)
    # front view
    cx = x0 + 40
    side(svg, part, cx, base, section=False)
    svg.text(cx, base + 9, "Vorderansicht")
    total = height / S
    for z0, z1, lab in part["dims_v"]:
        is_total = (z0, z1) == (0, total) and len(part["dims_v"]) > 1
        svg.arrow_dim_v(cx - 3.0 * S - (16 if is_total else 8),
                        base - z0 * S, base - z1 * S, lab, ext_from=cx - 3.0 * S)
    # section A-A
    cx2 = x0 + 110
    side(svg, part, cx2, base, section=True)
    svg.text(cx2, base + 9, "Schnitt A–A")
    for i, (r, lab) in enumerate(part["dims_d"]):
        y = base - height - 5 - 6 * i if i else base + 4
        svg.arrow_dim_h(y, cx2 - r * S, cx2 + r * S, lab)
    # top view
    cx3 = x0 + 175
    cy3 = base - height / 2
    top_view(svg, part, cx3, cy3)
    svg.text(cx3, base + 9, "Draufsicht")
    svg.text(cx3 - 22, cy3 - 1, "A", size=4, bold=True)
    svg.text(cx3 + 22, cy3 - 1, "A", size=4, bold=True)
    # notes
    for i, n in enumerate(part["notes"]):
        svg.text(x0 + 200, y0 + 14 + 6 * i, "• " + n, size=2.9, anchor="start")
    return base + 16


def assembly(svg, variant, x0, y0):
    """Mounted situation: two PCBs, spacer and fasteners, sectioned."""
    gap, pcb, hole = 11, 1.6, 3.0
    s = S
    cx = x0 + 60
    base = y0 + (gap + 2 * pcb + 6) * s
    svg.text(x0, y0 + 4, "Einbausituation (Schnitt), Platinen 1,6 mm angenommen",
             size=4.2, anchor="start", bold=True)

    def P(x, z):
        return (cx + x * s, base - z * s)

    for zb in (0, pcb + gap):
        for sign in (1, -1):
            pts = [P(sign * hole / 2, zb), P(sign * 9, zb), P(sign * 9, zb + pcb),
                   P(sign * hole / 2, zb + pcb)]
            svg.poly(pts, fill="#d8ead2")
    part = SCREW_SPACER if variant == "A" else SNAP_SLEEVE
    shifted = dict(part, outer=[(r, z + pcb) for r, z in part["outer"]],
                   inner=[(r, z + pcb) for r, z in part["inner"]])
    for sign in (1, -1):
        pts = [P(sign * r, z) for r, z in shifted["outer"]] + \
              [P(sign * r, z) for r, z in reversed(shifted["inner"])]
        svg.poly(pts, hatch=True)
    top = 2 * pcb + gap
    if variant == "A":
        # M3x8 countersunk (DIN 7991) from both sides; head sits proud on the
        # plain board hole: cone Ø6→Ø3 over 1.5 mm.
        for zsurf, d in ((top, 1), (0, -1)):
            pts = [P(-1.5, zsurf), P(-3, zsurf + 1.5 * d), P(3, zsurf + 1.5 * d), P(1.5, zsurf)]
            svg.poly(pts, fill="#bbb")
            tip = zsurf - d * (8 - 1.5)
            svg.poly([P(-1.5, zsurf), P(1.5, zsurf), P(1.5, tip), P(-1.5, tip)], fill="#bbb")
        svg.text(cx + 30, base - top * s - 2, "M3×8 Senkkopf (DIN 7991), steht ca. 1,5 mm über",
                 size=3.0, anchor="start")
        svg.text(cx + 30, base + 1.5 * s, "oder M3×6 Linsenkopf (ISO 7380), Kopf 1,65 mm",
                 size=3.0, anchor="start")
    else:
        for zsurf, d in ((top, 1), (0, -1)):
            prof = SNAP_PIN["outer"]
            pts = [P(r, zsurf - d * (z - 1.2)) for r, z in prof]
            pts += [P(-r, zsurf - d * (z - 1.2)) for r, z in reversed(prof)]
            svg.poly(pts, fill="#bbb")
        svg.text(cx + 30, base - top * s - 2, "Raststift von oben und unten, Kopf 1,2 mm",
                 size=3.0, anchor="start")
    svg.arrow_dim_v(cx - 9 * s - 8, base - pcb * s, base - (pcb + gap) * s, "11",
                    ext_from=cx - 9 * s)
    svg.arrow_dim_h(base + 1.5 * s + 6, cx - hole / 2 * s, cx + hole / 2 * s, "Ø3 (Loch)")
    for x in (-hole / 2, hole / 2):
        svg.line(cx + x * s, base, cx + x * s, base + 1.5 * s + 7, width=0.18)
    return base + 1.5 * s + 14


def sheet(parts, variant, title, path):
    svg = Svg(297, 10)
    y = 6
    svg.text(6, y + 6, title, size=5.5, anchor="start", bold=True)
    svg.text(291, y + 6, "Maßstab 6:1, Maße in mm", size=3.4, anchor="end")
    y += 14
    for p in parts:
        y = part_sheet(svg, p, 6, y) + 4
    y = assembly(svg, variant, 6, y) + 4
    svg.text(6, y + 2, "Annahmen: Platinenstärke 1,6 mm, Loch Ø3,0 (von Stefan gemessen), "
             "Abstand 11 mm (gemessen). Toleranzen für FDM 0,4 mm Düse.",
             size=3.0, anchor="start")
    svg.h = y + 8
    with open(path, "w") as f:
        f.write(svg.render())


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    sheet([SCREW_SPACER], "A", "Mini Floppy – Abstandshalter Variante A (Schraube)",
          f"{out}/spacer-a-screw.svg")
    sheet([SNAP_SLEEVE, SNAP_PIN], "B", "Mini Floppy – Abstandshalter Variante B (Raststift)",
          f"{out}/spacer-b-snap.svg")
