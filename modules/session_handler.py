"""
session_handler.py — Authenticated Session Management
Handles login for DVWA, Juice Shop, and custom login forms.
"""

import requests
import re
from urllib.parse import urljoin
from typing import Optional, Dict


class SessionHandler:
    """Create and maintain an authenticated HTTP session."""

    KNOWN_APPS = {
        "dvwa": {
            "login_path": "/login.php",
            "username_field": "username",
            "password_field": "password",
            "submit_field": "Login",
            "csrf_field": "user_token",
            "csrf_regex": r'name=["\']user_token["\'] value=["\']([a-f0-9]+)["\']',
            "success_indicator": "logout.php",
            "default_creds": ("admin", "password"),
        },
        "juiceshop": {
            "login_path": "/rest/user/login",
            "json_body": True,
            "username_field": "email",
            "password_field": "password",
            "success_indicator": "token",
            "default_creds": ("admin@juice-sh.op", "admin123"),
        },
    }

    def __init__(
        self,
        target_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        app_type: str = "auto",
        custom_headers: Optional[Dict[str, str]] = None,
        verify_ssl: bool = False,
        timeout: int = 15,
        proxies: Optional[Dict[str, str]] = None
    ):
        self.target_url = target_url.rstrip("/")
        self.username = username
        self.password = password
        self.app_type = app_type.lower()
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.proxies = proxies or {}

        self.session = requests.Session()
        self.session.verify = verify_ssl
        if custom_headers:
            self.session.headers.update(custom_headers)

        self.authenticated = False
        self.auth_token: Optional[str] = None

    def get_session(self):
        return self.session

    def close(self):
        self.session.close()

    # ------------------------------------------------------------------ #
    #  Public API                                                        #
    # ------------------------------------------------------------------ #

    def login(self) -> bool:
        """Attempt login. Returns True on success."""
        if self.app_type == "auto":
            self.app_type = self._detect_app()

        if self.app_type == "dvwa":
            return self._login_dvwa()
        if self.app_type == "juiceshop":
            return self._login_juiceshop()
        return self._login_generic()

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, timeout=self.timeout,
                                proxies=self.proxies, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.session.post(url, timeout=self.timeout,
                                 proxies=self.proxies, **kwargs)

    def set_dvwa_security(self, level: str = "low") -> bool:
        """
        Set DVWA security level (low / medium / high / impossible).
        Must be authenticated first.
        """
        if not self.authenticated:
            return False
        url = urljoin(self.target_url, "/security.php")
        try:
            resp = self.session.get(url, timeout=self.timeout, proxies=self.proxies)
            token = self._extract_csrf(resp.text, r'user_token.*?value=["\']([a-f0-9]+)["\']')
            data = {
                "seclev_submit": "Submit",
                "security": level,
            }
            if token:
                data["user_token"] = token
            self.session.post(url, data=data, timeout=self.timeout, proxies=self.proxies)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  Login implementations                                             #
    # ------------------------------------------------------------------ #

    def _login_dvwa(self) -> bool:
        cfg = self.KNOWN_APPS["dvwa"]
        user = self.username or cfg["default_creds"][0]
        pwd  = self.password or cfg["default_creds"][1]
        login_url = urljoin(self.target_url, cfg["login_path"])

        try:
            # GET login page for CSRF token
            resp = self.session.get(login_url, timeout=self.timeout, proxies=self.proxies)
            token = self._extract_csrf(resp.text, cfg["csrf_regex"])

            data = {
                cfg["username_field"]: user,
                cfg["password_field"]: pwd,
                cfg["submit_field"]: "Login",
            }
            if token:
                data[cfg["csrf_field"]] = token

            resp = self.session.post(login_url, data=data,
                                     timeout=self.timeout, proxies=self.proxies)
            if cfg["success_indicator"] in resp.text:
                self.authenticated = True
                return True
        except requests.RequestException:
            pass
        return False

    def _login_juiceshop(self) -> bool:
        cfg = self.KNOWN_APPS["juiceshop"]
        user = self.username or cfg["default_creds"][0]
        pwd  = self.password or cfg["default_creds"][1]
        login_url = urljoin(self.target_url, cfg["login_path"])

        try:
            resp = self.session.post(
                login_url,
                json={cfg["username_field"]: user, cfg["password_field"]: pwd},
                timeout=self.timeout,
                proxies=self.proxies,
            )
            data = resp.json()
            # JuiceShop wraps token in data.authentication.token
            token = (data.get("authentication") or {}).get("token")
            if token:
                self.auth_token = token
                self.session.headers["Authorization"] = f"Bearer {token}"
                self.authenticated = True
                return True
        except Exception:
            pass
        return False

    def _login_generic(self) -> bool:
        """
        Attempt a generic form-based login by:
        1. GETting the page to find form fields + CSRF token
        2. POSTing credentials
        3. Checking for logout/dashboard indicators
        """
        if not self.username or not self.password:
            return False

        try:
            resp = self.session.get(self.target_url, timeout=self.timeout,
                                    proxies=self.proxies)
            form_data = self._parse_login_form(resp.text)
            form_data.update({
                self._guess_username_field(form_data): self.username,
                self._guess_password_field(form_data): self.password,
            })
            # Try to POST to same URL (most common pattern)
            action_url = self._extract_form_action(resp.text) or self.target_url
            action_url = urljoin(self.target_url, action_url)

            resp2 = self.session.post(action_url, data=form_data,
                                      timeout=self.timeout, proxies=self.proxies)
            # Heuristics for success
            for indicator in ["logout", "dashboard", "profile", "welcome", "sign out"]:
                if indicator in resp2.text.lower():
                    self.authenticated = True
                    return True
        except Exception:
            pass
        return False

    # ------------------------------------------------------------------ #
    #  Helpers                                                           #
    # ------------------------------------------------------------------ #

    def _detect_app(self) -> str:
        try:
            resp = self.session.get(self.target_url, timeout=self.timeout,
                                    proxies=self.proxies)
            text = resp.text.lower()
            if "dvwa" in text or "damn vulnerable" in text:
                return "dvwa"
            if "juice" in text or "owasp juice" in text:
                return "juiceshop"
        except Exception:
            pass
        return "generic"

    @staticmethod
    def _extract_csrf(html: str, pattern: str) -> Optional[str]:
        m = re.search(pattern, html, re.IGNORECASE)
        return m.group(1) if m else None

    @staticmethod
    def _parse_login_form(html: str) -> Dict[str, str]:
        """Extract all hidden/visible input fields from the first form."""
        fields: Dict[str, str] = {}
        for m in re.finditer(
            r'<input[^>]+name=["\']([^"\']+)["\'][^>]*(?:value=["\']([^"\']*)["\'])?',
            html, re.IGNORECASE
        ):
            fields[m.group(1)] = m.group(2) or ""
        return fields

    @staticmethod
    def _extract_form_action(html: str) -> Optional[str]:
        m = re.search(r'<form[^>]+action=["\']([^"\']+)["\']', html, re.IGNORECASE)
        return m.group(1) if m else None

    @staticmethod
    def _guess_username_field(fields: Dict[str, str]) -> str:
        for key in fields:
            if any(k in key.lower() for k in ["user", "email", "login", "name"]):
                return key
        return "username"

    @staticmethod
    def _guess_password_field(fields: Dict[str, str]) -> str:
        for key in fields:
            if "pass" in key.lower() or "pwd" in key.lower():
                return key
        return "password" 