"""
reporter.py — JSON & HTML Report Generation
Saves structured scan results for documentation and portfolios.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class Reporter:
    """Collects scan findings and exports JSON + HTML reports."""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.findings: List[Dict[str, Any]] = []
        self.meta: Dict[str, Any] = {
            "tool": "Upload File Vulnerability Tester",
            "version": "2.0.0",
            "author": "HariCipher",
            "github": "https://github.com/HariCipher/Upload-file-vuln-tester",
            "scan_start": datetime.utcnow().isoformat() + "Z",
            "scan_end": None,
            "target": "",
            "waf": None,
            "total_attempts": 0,
            "successful": 0,
            "failed": 0,
        }

    # ------------------------------------------------------------------ #
    #  Data collection                                                     #
    # ------------------------------------------------------------------ #

    def set_target(self, url: str) -> None:
        self.meta["target"] = url

    def set_waf(self, waf_name: Optional[str], confidence: int = 0) -> None:
        self.meta["waf"] = {"name": waf_name, "confidence": confidence}

    def add_finding(
        self,
        technique: str,
        filename: str,
        status: str,           # "success" | "failure" | "error"
        http_code: Optional[int] = None,
        upload_url: Optional[str] = None,
        exec_result: Optional[str] = None,
        description: str = "",
        content_type: str = "",
    ) -> None:
        self.findings.append({
            "id": len(self.findings) + 1,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "technique": technique,
            "filename": filename,
            "content_type": content_type,
            "status": status,
            "http_code": http_code,
            "upload_url": upload_url,
            "exec_result": exec_result,
            "description": description,
        })
        self.meta["total_attempts"] += 1
        if status == "success":
            self.meta["successful"] += 1
        else:
            self.meta["failed"] += 1

    def finalize(self) -> None:
        self.meta["scan_end"] = datetime.utcnow().isoformat() + "Z"

    # ------------------------------------------------------------------ #
    #  Export                                                              #
    # ------------------------------------------------------------------ #

    def save_json(self, filename: Optional[str] = None) -> str:
        self.finalize()
        fname = filename or f"scan_{self._timestamp()}.json"
        path = os.path.join(self.output_dir, fname)
        report = {"meta": self.meta, "findings": self.findings}
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        return path

    def save_html(self, filename: Optional[str] = None) -> str:
        self.finalize()
        fname = filename or f"scan_{self._timestamp()}.html"
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f:
            f.write(self._render_html())
        return path

    def save_all(self) -> Dict[str, str]:
        ts = self._timestamp()
        return {
            "json": self.save_json(f"scan_{ts}.json"),
            "html": self.save_html(f"scan_{ts}.html"),
        }

    def print_summary(self) -> None:
        print("\n" + "=" * 60)
        print("  SCAN SUMMARY")
        print("=" * 60)
        print(f"  Target   : {self.meta['target']}")
        waf = self.meta.get("waf")
        print(f"  WAF      : {waf['name'] if waf else 'Not detected'}")
        print(f"  Total    : {self.meta['total_attempts']} attempts")
        print(f"  Success  : {self.meta['successful']}")
        print(f"  Failed   : {self.meta['failed']}")
        print("=" * 60)
        successes = [f for f in self.findings if f["status"] == "success"]
        if successes:
            print(f"\n  [+] {len(successes)} SUCCESSFUL UPLOAD(S):\n")
            for s in successes:
                print(f"      • [{s['technique']}] {s['filename']}")
                if s.get("upload_url"):
                    print(f"        URL : {s['upload_url']}")
                if s.get("exec_result"):
                    print(f"        RCE : {s['exec_result'][:80]}")
        else:
            print("\n  [-] No successful uploads found.")
        print()

    # ------------------------------------------------------------------ #
    #  HTML renderer                                                       #
    # ------------------------------------------------------------------ #

    def _render_html(self) -> str:
        meta = self.meta
        rows = ""
        for f in self.findings:
            status_color = "#27ae60" if f["status"] == "success" else "#e74c3c"
            exec_cell = f["exec_result"][:60] + "…" if f.get("exec_result") else "—"
            rows += f"""
            <tr>
                <td>{f['id']}</td>
                <td>{f['technique']}</td>
                <td><code>{f['filename']}</code></td>
                <td>{f['content_type']}</td>
                <td style="color:{status_color};font-weight:bold">
                    {f['status'].upper()}
                </td>
                <td>{f['http_code'] or '—'}</td>
                <td>{exec_cell}</td>
            </tr>"""

        waf = meta.get("waf") or {}
        waf_str = f"{waf.get('name','—')} ({waf.get('confidence',0)}%)" if waf.get("name") else "None detected"

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Upload Vuln Tester — Scan Report</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background:#0d1117; color:#c9d1d9; margin:0; padding:20px; }}
  h1 {{ color:#58a6ff; }}
  h2 {{ color:#8b949e; border-bottom:1px solid #30363d; padding-bottom:6px; }}
  .meta-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:24px; }}
  .card {{ background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; }}
  .card .label {{ font-size:12px; color:#8b949e; margin-bottom:4px; }}
  .card .value {{ font-size:20px; font-weight:bold; color:#58a6ff; }}
  table {{ width:100%; border-collapse:collapse; background:#161b22; border-radius:8px; overflow:hidden; }}
  th {{ background:#21262d; color:#8b949e; padding:10px 14px; text-align:left; font-size:13px; }}
  td {{ padding:10px 14px; border-top:1px solid #30363d; font-size:13px; }}
  code {{ background:#21262d; padding:2px 6px; border-radius:4px; font-size:12px; }}
  .badge {{ display:inline-block; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:bold; }}
  footer {{ margin-top:30px; text-align:center; color:#8b949e; font-size:12px; }}
</style>
</head>
<body>
<h1>🔍 Upload Vulnerability Scan Report</h1>
<p style="color:#8b949e">Generated: {meta['scan_end']} &nbsp;|&nbsp; Target: <code>{meta['target']}</code></p>

<div class="meta-grid">
  <div class="card"><div class="label">Total Attempts</div><div class="value">{meta['total_attempts']}</div></div>
  <div class="card"><div class="label">Successful</div><div class="value" style="color:#27ae60">{meta['successful']}</div></div>
  <div class="card"><div class="label">Failed</div><div class="value" style="color:#e74c3c">{meta['failed']}</div></div>
  <div class="card"><div class="label">WAF Detected</div><div class="value" style="font-size:14px">{waf_str}</div></div>
  <div class="card"><div class="label">Scan Duration</div>
    <div class="value" style="font-size:14px">{meta['scan_start']} → {meta['scan_end']}</div></div>
  <div class="card"><div class="label">Tool</div><div class="value" style="font-size:14px">{meta['tool']} v{meta['version']}</div></div>
</div>

<h2>Findings</h2>
<table>
  <thead>
    <tr>
      <th>#</th><th>Technique</th><th>Filename</th>
      <th>Content-Type</th><th>Status</th><th>HTTP</th><th>RCE Output</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>

<footer>
  {meta['tool']} {meta['version']} by <a href="{meta['github']}" style="color:#58a6ff">{meta['author']}</a>
  &nbsp;|&nbsp; For authorized testing only
</footer>
</body>
</html>"""

    @staticmethod
    def _timestamp() -> str:
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
