"""
Upload File Vulnerability Tester - Modules Package
Version: 2.0.0
"""

from .bypass_techniques import BypassTechniques
from .payload_generator import PayloadGenerator
from .session_handler import SessionHandler
from .waf_detector import WAFDetector
from .reporter import Reporter

__all__ = [
    "BypassTechniques",
    "PayloadGenerator",
    "SessionHandler",
    "WAFDetector",
    "Reporter",
]

__version__ = "2.0.0"
__author__ = "HariCipher"
