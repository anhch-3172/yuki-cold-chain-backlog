#!/usr/bin/env python3
"""Chấm SWP cho backlog theo rubric Scope × Complexity, xuất JSON + CSV + báo cáo HTML.

Cách dùng:
  python swp_score.py backlog.json --out out/ [--overrides overrides.json] [--meta meta.json]
"""
import argparse, csv, html, json, os, datetime

MATRIX = {1: {1: 1, 2: 2, 3: 3, 4: 5}, 2: {1: 2, 2: 3, 3: 5, 4: 8},
          3: {1: 3, 2: 5, 3: 8, 4: 13}, 4: {1: 5, 2: 8, 3: 13, 4: 21}}
HOURS = {1: 2, 2: 4, 3: 7, 5: 12, 8: 20, 13: 32, 21: 52}
SCOPE_EDGES = {2, 4, 7}          # đổi 1 đơn vị là đổi bậc
CPLX_EDGES = {1, 3}   # 1↔2 và 3↔4 là chỗ đổi bậc C


def scope_level(pts):
    return 1 if pts <= 2 else 2 if pts <= 4 else 3 if pts <= 7 else 4


def branch_pts(b):
    return 0 if b == 0 else 1 if b <= 2 else 2 if b <= 4 else 3


def cplx_level(pts):
    return 1 if pts <= 1 else 2 if pts == 2 else 3 if pts == 3 else 4


def score(item):
    f = item["f"]
    sp = f.get("screens", 0) + f.get("apis", 0) + f.get("tables", 0)
    cp = branch_pts(f.get("branches", 0)) + int(bool(f.get("special"))) \
        + int(bool(f.get("integrity"))) + int(bool(f.get("integration")))
    s, c = scope_level(sp), cplx_level(cp)
    swp = MATRIX[s][c]
    return dict(scope_pts=sp, cplx_pts=cp, S=s, C=c, swp_skill=swp)


def pick_samples(items):
    reasons = {}
    by_epic = {}
    for it in items:
        by_epic.setdefault(it["epic"], []).append(it)
    for epic, lst in by_epic.items():
        top = max(lst, key=lambda x: (x["swp_skill"], x["scope_pts"]))
        reasons.setdefault(top["id"], []).append(f"SWP cao nhất epic {epic}")
    for it in items:
        if it["f"].get("special") and it["swp_skill"] <= 3:
            reasons.setdefault(it["id"], []).append("Ràng buộc đặc thù nhưng SWP ≤ 3")
        if it["swp_skill"] >= 8 and (it["scope_pts"] in SCOPE_EDGES or it["cplx_pts"] in CPLX_EDGES):
            reasons.setdefault(it["id"], []).append(
                f"Sát ranh giới bậc (scope {it['scope_pts']}, complexity {it['cplx_pts']})")
        if it["swp_skill"] >= 13:
            reasons.setdefault(it["id"], []).append("SWP ≥ 13 – phải tách")
    return reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backlog")
    ap.add_argument("--out", default="out")
    ap.add_argument("--overrides")
    ap.add_argument("--meta")
    a = ap.parse_args()
    data = json.load(open(a.backlog, encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) else data
    epics = data.get("epics", {}) if isinstance(data, dict) else {}
    ov = json.load(open(a.overrides, encoding="utf-8")) if a.overrides and os.path.exists(a.overrides) else {}
    meta = json.load(open(a.meta, encoding="utf-8")) if a.meta and os.path.exists(a.meta) else {}
    for it in items:
        it.update(score(it))
    samples = pick_samples(items)
    for it in items:
        o = ov.get(it["id"])
        it["swp_final"] = o["swp"] if o else it["swp_skill"]
        it["override_reason"] = o.get("reason", "") if o else ""
        it["hours"] = HOURS[it["swp_final"]]
        it["sample"] = "; ".join(samples.get(it["id"], []))
        it["split_flag"] = it["swp_final"] >= 13
    os.makedirs(a.out, exist_ok=True)
    json.dump(items, open(os.path.join(a.out, "backlog_scored.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, "swp.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "epic", "parent", "title", "S", "C", "swp_skill", "swp_final", "hours"])
        for it in items:
            w.writerow([it["id"], it["epic"], it.get("parent", ""), it["title"], it["S"], it["C"],
                        it["swp_skill"], it["swp_final"], it["hours"]])
    with open(os.path.join(a.out, "swp.tsv"), "w", encoding="utf-8") as fh:
        fh.write("id\tswp_final\thours\n")
        for it in items:
            fh.write(f"{it['id']}\t{it['swp_final']}\t{it['hours']}\n")
    write_html(items, epics, samples, ov, meta, os.path.join(a.out, "swp-report.html"))
    print(f"{len(items)} issue · SWP skill {sum(i['swp_skill'] for i in items)} · "
          f"SWP chốt {sum(i['swp_final'] for i in items)} · giờ {sum(i['hours'] for i in items)} · "
          f"mẫu {len(samples)} · override {len(ov)}")


def write_html(items, epics, samples, ov, meta, path):
    e = html.escape
    tot_s = sum(i["swp_skill"] for i in items); tot_f = sum(i["swp_final"] for i in items)
    tot_h = sum(i["hours"] for i in items)
    rows_epic = ""
    for ep in sorted({i["epic"] for i in items}):
        lst = [i for i in items if i["epic"] == ep]
        rows_epic += (f"<tr><td>{e(ep)}</td><td>{e(epics.get(ep, ''))}</td><td class=n>{len(lst)}</td>"
                      f"<td class=n>{sum(i['swp_skill'] for i in lst)}</td><td class=n>{sum(i['swp_final'] for i in lst)}</td>"
                      f"<td class=n>{sum(i['hours'] for i in lst)}</td></tr>")
    def frow(i, extra=""):
        f = i["f"]; flags = " ".join(x for x, k in [("đặc thù", "special"), ("toàn vẹn", "integrity"), ("tích hợp", "integration")] if f.get(k))
        changed = i["swp_final"] != i["swp_skill"]
        return (f"<tr{' class=chg' if changed else ''}><td><b>{e(i['id'])}</b></td><td>{e(i['title'])}<div class=s>{e(i.get('spec',''))}</div></td>"
                f"<td class=n>{f.get('screens',0)}/{f.get('apis',0)}/{f.get('tables',0)} → S{i['S']}</td>"
                f"<td class=n>{f.get('branches',0)} nhánh {('· ' + flags) if flags else ''} → C{i['C']}</td>"
                f"<td class=n>{i['swp_skill']}</td><td class=n><b>{i['swp_final']}</b></td><td class=n>{i['hours']}</td>{extra}</tr>")
    sample_rows = "".join(frow(i, f"<td>{e(i['sample'])}</td><td>{e(i['override_reason']) or 'Giữ nguyên'}</td>")
                          for i in items if i["id"] in samples)
    all_rows = "".join(frow(i, f"<td class=s>{e(i.get('why',''))}</td>") for i in items)
    matrix = "".join(f"<tr><th>S{s}</th>" + "".join(f"<td class=n>{MATRIX[s][c]}</td>" for c in range(1, 5)) + "</tr>" for s in range(1, 5))
    gen = meta.get("generated", datetime.date.today().isoformat())
    doc = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SWP report — {e(meta.get('project','Backlog'))}</title><style>
:root{{--bg:#f6f8fa;--fg:#0e2a3b;--mut:#5b6b77;--line:#d8dee4;--hi:#fff4d6;--acc:#1f8a8a}}
@media (prefers-color-scheme: dark){{:root{{--bg:#0d1117;--fg:#e6edf3;--mut:#8b949e;--line:#30363d;--hi:#3a2f0b;--acc:#3fb9b9}}}}
body{{font-family:system-ui,"Segoe UI",sans-serif;background:var(--bg);color:var(--fg);margin:0;padding:24px;line-height:1.45}}
h1{{margin:0 0 4px}} h2{{margin-top:32px;border-bottom:2px solid var(--acc);padding-bottom:4px}}
.s{{color:var(--mut);font-size:12px}} .n{{text-align:center;white-space:nowrap}}
.wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid var(--line);padding:6px 8px;vertical-align:top}} th{{background:var(--line);text-align:left}}
tr.chg td{{background:var(--hi)}} .kpi{{display:flex;gap:16px;flex-wrap:wrap;margin:16px 0}}
.kpi div{{border:1px solid var(--line);padding:10px 16px;border-radius:8px}} .kpi b{{font-size:22px;display:block}}
</style></head><body>
<h1>Báo cáo chấm SWP</h1><div class=s>{e(meta.get('project',''))} · skill swp-estimator · chạy ngày {e(gen)}</div>
<div class=kpi><div><b>{len(items)}</b>issue lá</div><div><b>{tot_s}</b>SWP skill chấm</div><div><b>{tot_f}</b>SWP người chốt</div>
<div><b>{tot_h}</b>giờ ước lượng</div><div><b>{len(samples)}</b>issue mẫu đã kiểm</div><div><b>{len(ov)}</b>issue người sửa điểm</div></div>
<h2>1. Ma trận Scope × Complexity</h2><div class=wrap><table style="width:auto"><tr><th></th><th>C1</th><th>C2</th><th>C3</th><th>C4</th></tr>{matrix}</table></div>
<p class=s>Scope = màn hình + API + bảng (S1 ≤2 · S2 3–4 · S3 5–7 · S4 ≥8). Complexity = bậc nhánh nghiệp vụ (0/1–2/3–4/≥5 → 0/1/2/3) + đặc thù + toàn vẹn + tích hợp (C1 ≤1 · C2 2 · C3 3 · C4 ≥4). Giờ: 1→2 · 2→4 · 3→7 · 5→12 · 8→20 · 13→32.</p>
<h2>2. Issue mẫu cần người kiểm</h2><div class=wrap><table><tr><th>ID</th><th>Issue</th><th>Màn/API/bảng</th><th>Complexity</th><th>Skill</th><th>Chốt</th><th>Giờ</th><th>Vì sao chọn</th><th>Quyết định người review</th></tr>{sample_rows}</table></div>
<p class=s>Dòng nền vàng: người review đã sửa điểm của skill.</p>
<h2>3. Tổng theo epic</h2><div class=wrap><table><tr><th>Epic</th><th>Tên</th><th>Số issue</th><th>SWP skill</th><th>SWP chốt</th><th>Giờ</th></tr>{rows_epic}
<tr><th colspan=2>Tổng</th><th class=n>{len(items)}</th><th class=n>{tot_s}</th><th class=n>{tot_f}</th><th class=n>{tot_h}</th></tr></table></div>
<h2>4. Toàn bộ issue</h2><div class=wrap><table><tr><th>ID</th><th>Issue</th><th>Màn/API/bảng</th><th>Complexity</th><th>Skill</th><th>Chốt</th><th>Giờ</th><th>Căn cứ yếu tố</th></tr>{all_rows}</table></div>
</body></html>"""
    open(path, "w", encoding="utf-8").write(doc)


if __name__ == "__main__":
    main()
