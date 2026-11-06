#!/usr/bin/env python3
"""Dựng GitHub Project cho backlog LAB-5 bằng gh CLI.

Chạy từ gốc repo (đã push lên GitHub, public):
  python tools/setup_github_project.py --owner <user> --repo <repo> --student-id <mã> [--dry-run]

Chạy lại an toàn: trạng thái lưu ở tools/state.json (issue đã tạo thì bỏ qua).
Yêu cầu: gh auth login với scope repo, project (gh auth refresh -s project).
SWP / Giờ ước lượng / SWP reviewed KHÔNG ghi ở đây — Agent của skill ghi:
  bash skills/swp-estimator/scripts/push_to_project.sh swp-report/swp.tsv <owner> <project-number>
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "tools", "state.json")
DRY = False


def gh(*args, parse=False, check=True):
    if DRY:
        print("DRY gh", " ".join(a if len(a) < 80 else a[:77] + "..." for a in args))
        return {} if parse else ""
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        sys.exit(f"gh {' '.join(args[:3])} lỗi:\n{r.stderr}")
    return json.loads(r.stdout or "{}") if parse else r.stdout.strip()


def gql(query, **v):
    args = ["api", "graphql", "-f", f"query={query}"]
    for k, val in v.items():
        args += ["-f", f"{k}={val}"]
    return gh(*args, parse=True)


def load(p):
    return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))


def save(state):
    if not DRY:
        json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    global DRY
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True); ap.add_argument("--repo", required=True)
    ap.add_argument("--student-id", required=True); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(); DRY = a.dry_run
    full = f"{a.owner}/{a.repo}"
    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {"issues": {}}
    bl = load("backlog/backlog.json"); plan = load("backlog/plan.json")
    scored = {i["id"]: i for i in load("swp-report/backlog_scored.json")}
    P = {p["id"]: p for p in plan["plan"]}
    gh("auth", "status")

    # 1. Labels
    for name, color, desc in [("epic", "5319e7", "Epic"), ("rang-buoc-dac-thu", "d93f0b", "Ràng buộc nghiệp vụ đặc thù"),
                              ("gap-lab4", "fbca04", "Chỗ hở phát hiện từ LAB-4"), ("lam-ro", "0e8a16", "Issue làm rõ với khách")]:
        gh("label", "create", name, "--repo", full, "--color", color, "--description", desc, "--force")

    # 2. Issues
    def create(key, title, body, labels):
        if key in state["issues"]:
            return state["issues"][key]
        args = ["issue", "create", "--repo", full, "--title", title, "--body", body]
        if labels:
            args += ["--label", ",".join(labels)]
        url = gh(*args)
        if DRY:
            info = {"number": 0, "id": f"DRY-{key}", "url": f"https://github.com/{full}/issues/0"}
        else:
            info = gh("issue", "view", url, "--json", "number,id,url", parse=True)
        state["issues"][key] = info; save(state); print("issue", key, info["number"])
        return info

    for ep, name in bl["epics"].items():
        tot = [i for i in scored.values() if i["epic"] == ep]
        create(ep, f"[{ep}] {name}",
               f"Epic **{ep} — {name}**\n\n{len(tot)} issue lá · {sum(i['swp_final'] for i in tot)} SWP · "
               f"{sum(i['hours'] for i in tot)} giờ dev.\nXem `task-breakdown.md`.", ["epic"])
    for pid, pv in bl["parents"].items():
        ch = [i for i in scored.values() if i["parent"] == pid]
        create(pid, f"[{pid}] {pv['title']}",
               f"Issue cha thuộc epic {pv['epic']} — {len(ch)} sub-issue, {sum(i['swp_final'] for i in ch)} SWP.", [])
    for iid, it in scored.items():
        p = P[iid]; f = it["f"]
        flags = ", ".join(k for k, n in [("đặc thù", "special"), ("toàn vẹn", "integrity"), ("tích hợp", "integration")] if f.get(n)) or "—"
        ov = f" (skill {it['swp_skill']} → người chốt {it['swp_final']}: {it['override_reason']})" if it["override_reason"] else ""
        body = (f"**Spec LAB-4**: {it['spec']}\n**Epic**: {it['epic']} · **Iteration**: {p['iteration']} · **Phụ trách (giả định)**: {p['owner']}\n"
                f"**SWP (đã review)**: {it['swp_final']} · **Giờ ước lượng**: {it['hours']}{ov}\n"
                f"**Yếu tố chấm**: màn/API/bảng {f['screens']}/{f['apis']}/{f['tables']} → S{it['S']} · {f['branches']} nhánh · cờ: {flags} → C{it['C']}\n\n"
                "**DoD**: code + unit test (case R-06 liên quan) · requireRole + zod + writeAudit cho API ghi · PR được người review, CI xanh · cập nhật spec nếu lệch.")
        labels = (["rang-buoc-dac-thu"] if f.get("special") else []) + (["gap-lab4"] if it["title"].startswith("Gap LAB-4") else []) \
            + (["lam-ro"] if it["title"].startswith("Làm rõ") else [])
        create(iid, f"[{iid}] {it['title']}", body, labels)

    # 3. Sub-issues (epic → issue cha / issue lá, issue cha → sub-issue)
    links = [(pv["epic"], pid) for pid, pv in bl["parents"].items()] + [(it["parent"], iid) for iid, it in scored.items()]
    state.setdefault("links", [])
    for parent, child in links:
        k = f"{parent}>{child}"
        if k in state["links"]:
            continue
        gql("mutation($p:ID!,$c:ID!){addSubIssue(input:{issueId:$p,subIssueId:$c}){issue{number}}}",
            p=state["issues"][parent]["id"], c=state["issues"][child]["id"])
        state["links"].append(k); save(state)
    print("sub-issue links:", len(state["links"]))

    # 4. Project
    if "project" not in state:
        pj = gh("project", "create", "--owner", a.owner, "--title", "Yuki Cold Chain — LAB-5 backlog (Product B)", "--format", "json", parse=True)
        state["project"] = {"number": pj.get("number", 0), "url": pj.get("url", ""), "id": pj.get("id", "DRY")}; save(state)
    num = str(state["project"]["number"]); pid = state["project"]["id"]
    gh("project", "edit", num, "--owner", a.owner, "--visibility", "PUBLIC")
    gh("project", "link", num, "--owner", a.owner, "--repo", full, check=False)

    # 5. Fields
    existing = gh("project", "field-list", num, "--owner", a.owner, "--format", "json", parse=True).get("fields", [])
    names = {f["name"] for f in existing}
    for name, typ, opts in [("SWP", "NUMBER", None), ("Giờ ước lượng", "NUMBER", None), ("SWP reviewed", "SINGLE_SELECT", "Yes,No"),
                            ("Phụ trách (giả định)", "SINGLE_SELECT", "BE-1,BE-2,FE-1,QA-1,BrSE-1"),
                            ("Trạng thái", "SINGLE_SELECT", "Todo,In Progress,In Review,Blocked,Done")]:
        if name not in names:
            args = ["project", "field-create", num, "--owner", a.owner, "--name", name, "--data-type", typ]
            if opts:
                args += ["--single-select-options", opts]
            gh(*args)
    if "Iteration" not in names:
        its = ",".join(f'{{title:"{t}",startDate:"{d[0]}",duration:14}}' for t, d in plan["dates"].items())
        r = subprocess.run(["gh", "api", "graphql", "-f", "query=mutation{createProjectV2Field(input:{projectId:\"%s\",dataType:ITERATION,name:\"Iteration\","
                            "iterationConfiguration:{startDate:\"2026-11-09\",duration:14,iterations:[%s]}}){projectV2Field{... on ProjectV2IterationField{id}}}}" % (pid, its)],
                           capture_output=True, text=True) if not DRY else None
        if r is not None and r.returncode != 0:
            sys.exit("Không tạo được field Iteration bằng API. Tạo tay trên Project: + New field → Iteration, tên 'Iteration', "
                     "bắt đầu 09/11/2026, 2 tuần, 6 iteration (Sprint 1…Sprint 6), rồi chạy lại script.\n" + r.stderr)

    # 6. Field ids / options
    q = gql("query($id:ID!){node(id:$id){... on ProjectV2{fields(first:50){nodes{"
            "... on ProjectV2Field{id name} ... on ProjectV2SingleSelectField{id name options{id name}}"
            "... on ProjectV2IterationField{id name configuration{iterations{id title}}}}}}}}", id=pid)
    F = {n["name"]: n for n in (q.get("data", {}).get("node", {}) or {}).get("fields", {}).get("nodes", []) if n}
    opt = lambda f, v: next((o["id"] for o in F.get(f, {}).get("options", []) if o["name"] == v), None)
    iters = {i["title"]: i["id"] for i in F.get("Iteration", {}).get("configuration", {}).get("iterations", [])}
    STATUS = {"Todo": "Todo", "In Progress": "In Progress", "In Review": "In Progress", "Blocked": "In Progress", "Done": "Done"}

    # 7. Items + giá trị field (trừ SWP / giờ — Agent của skill ghi)
    state.setdefault("items", {})
    for key, info in state["issues"].items():
        if key not in state["items"]:
            it = gh("project", "item-add", num, "--owner", a.owner, "--url", info["url"], "--format", "json", parse=True)
            state["items"][key] = it.get("id", f"DRY-{key}"); save(state)
        if key not in P:
            continue
        p = P[key]; item = state["items"][key]
        def edit(field, **kw):
            fid = F.get(field, {}).get("id")
            if not fid:
                return
            args = ["project", "item-edit", "--project-id", pid, "--id", item, "--field-id", fid]
            for k, v in kw.items():
                if v:
                    args += [f"--{k.replace('_', '-')}", str(v)]
            gh(*args)
        edit("Phụ trách (giả định)", single_select_option_id=opt("Phụ trách (giả định)", p["owner"]))
        edit("Trạng thái", single_select_option_id=opt("Trạng thái", p["status"]))
        edit("Status", single_select_option_id=opt("Status", STATUS[p["status"]]))
        edit("Iteration", iteration_id=iters.get(p["iteration"]))
        if p["status"] == "Done":
            gh("issue", "close", info["url"], check=False)
    print("items:", len(state["items"]))

    # 8. Thay token trong markdown + bật GitHub Pages
    repo_url = f"https://github.com/{full}"; pages = f"https://{a.owner.lower()}.github.io/{a.repo}"
    gh("api", "-X", "POST", f"repos/{full}/pages", "-f", "source[branch]=main", "-f", "source[path]=/", check=False)
    for md in ["README.md", "PREMISE.md", "task-breakdown.md", "estimate.md", "progress-report.md", "AI-report.md"]:
        p = os.path.join(ROOT, md); s = open(p, encoding="utf-8").read()
        s = re.sub(r"\{\{#([A-Z0-9-]+[a-z]?)\}\}", lambda m: f"#{state['issues'][m.group(1)]['number']}" if m.group(1) in state["issues"] else m.group(0), s)
        s = s.replace("{{REPO_URL}}", repo_url).replace("{{PROJECT_URL}}", state["project"]["url"]) \
             .replace("{{PAGES_URL}}", pages).replace("{{MA_HOC_VIEN}}", a.student_id)
        if not DRY:
            open(p, "w", encoding="utf-8").write(s)
    left = sorted({t for md in ["README.md", "PREMISE.md", "task-breakdown.md", "estimate.md", "progress-report.md"]
                   for t in re.findall(r"\{\{[^}]+\}\}", open(os.path.join(ROOT, md), encoding="utf-8").read())})
    print("Token còn lại (chỉ nên còn {{INCOGNITO_CHECK}}):", left)
    print(f"Xong. Project: {state['project']['url']} — tiếp theo chạy Agent ghi SWP:\n"
          f"  bash skills/swp-estimator/scripts/push_to_project.sh swp-report/swp.tsv {a.owner} {num}")


if __name__ == "__main__":
    main()
