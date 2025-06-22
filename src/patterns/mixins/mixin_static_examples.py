"""
DataConverter: Mixin vs Static Class Comparison

This example demonstrates two approaches for providing data conversion utilities:
1. Using a mixin class (composition via multiple inheritance)
2. Using a static utility class (composition via delegation)
"""

# =============================================================================
# APPROACH 1: USING MIXIN (Multiple Inheritance)
# =============================================================================

from typing import Any


class DataConverterMixin:
    """
    Mixin that provides data conversion utilities to any class that inherits from it.
    Best when: You want the conversion methods to feel like native methods of the document class.
    """

    @staticmethod
    def bytes_to_kb(size_bytes: int) -> float:
        """Convert bytes to kilobytes"""
        return size_bytes / 1024

    @staticmethod
    def bytes_to_mb(size_bytes: int) -> float:
        """Convert bytes to megabytes"""
        return size_bytes / (1024 * 1024)

    @staticmethod
    def kb_to_bytes(size_kb: float) -> int:
        """Convert kilobytes to bytes"""
        return int(size_kb * 1024)

    @staticmethod
    def mb_to_bytes(size_mb: float) -> int:
        """Convert megabytes to bytes"""
        return int(size_mb * 1024 * 1024)

    def get_size_in_mb(self) -> float:
        """Instance method that uses the static conversion method"""
        return self.bytes_to_mb(self.size_bytes)  # type: ignore[attr-defined]

    def get_size_in_kb(self) -> float:
        """Instance method that uses the static conversion method"""
        return self.bytes_to_kb(self.size_bytes)  # type: ignore[attr-defined]


class Document:
    """Base document class"""

    name: str
    size_bytes: int

    def __init__(self, name: str, size_bytes: int) -> None:
        self.name = name
        self.size_bytes = size_bytes

    def get_info(self) -> str:
        return f"Document: {self.name}, Size: {self.size_bytes} bytes"


class PDFDocument(DataConverterMixin, Document):
    """PDF document with conversion capabilities via mixin"""

    page_count: int

    def __init__(self, name: str, size_bytes: int, page_count: int) -> None:
        super().__init__(name, size_bytes)
        self.page_count = page_count

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info}, Pages: {self.page_count}, Size: {self.get_size_in_mb():.2f} MB"

    def compress(self, compression_ratio: float) -> None:
        """Compress PDF and update size using mixin methods"""
        pass


class WordDocument(DataConverterMixin, Document):
    """Word document with conversion capabilities via mixin"""

    word_count: int

    def __init__(self, name: str, size_bytes: int, word_count: int) -> None:
        super().__init__(name, size_bytes)
        self.word_count = word_count

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info}, Words: {self.word_count}, Size: {self.get_size_in_kb():.2f} KB"

    def add_content(self, additional_words: int) -> None:
        """Add content and estimate size increase using mixin methods"""
        pass


# =============================================================================
# APPROACH 2: USING STATIC UTILITY CLASS (Delegation)
# =============================================================================


class DataConverterStaticClass:
    """
    Static utility class for data conversion operations.
    Best when: You want explicit control over when conversions are used,
    or when you need the same utilities across unrelated class hierarchies.
    """

    @staticmethod
    def bytes_to_kb(size_bytes: int) -> float:
        """Convert bytes to kilobytes"""
        return size_bytes / 1024

    @staticmethod
    def bytes_to_mb(size_bytes: int) -> float:
        """Convert bytes to megabytes"""
        return size_bytes / (1024 * 1024)

    @staticmethod
    def kb_to_bytes(size_kb: float) -> int:
        """Convert kilobytes to bytes"""
        return int(size_kb * 1024)

    @staticmethod
    def mb_to_bytes(size_mb: float) -> int:
        """Convert megabytes to bytes"""
        return int(size_mb * 1024 * 1024)

    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Smart formatting that chooses appropriate unit"""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{DataConverterStaticClass.bytes_to_kb(size_bytes):.2f} KB"
        else:
            return f"{DataConverterStaticClass.bytes_to_mb(size_bytes):.2f} MB"


class DocumentV2:
    """Base document class without mixin"""

    name: str
    size_bytes: int

    def __init__(self, name: str, size_bytes: int) -> None:
        self.name = name
        self.size_bytes = size_bytes

    def get_info(self) -> str:
        return f"Document: {self.name}, Size: {self.size_bytes} bytes"

    def get_formatted_size(self) -> str:
        """Uses the static utility class explicitly"""
        return DataConverterStaticClass.format_size(self.size_bytes)


class PDFDocumentV2(DocumentV2):
    """PDF document using static utility class"""

    page_count: int

    def __init__(self, name: str, size_bytes: int, page_count: int) -> None:
        super().__init__(name, size_bytes)
        self.page_count = page_count

    def get_info(self) -> str:
        base_info = super().get_info()
        formatted_size = DataConverterStaticClass.format_size(self.size_bytes)
        return f"{base_info}, Pages: {self.page_count}, Size: {formatted_size}"

    def compress(self, compression_ratio: float) -> None:
        """Compress PDF using explicit DataConverter calls"""
        pass


class WordDocumentV2(DocumentV2):
    """Word document using static utility class"""

    word_count: int

    def __init__(self, name: str, size_bytes: int, word_count: int) -> None:
        super().__init__(name, size_bytes)
        self.word_count = word_count

    def get_info(self) -> str:
        base_info = super().get_info()
        formatted_size = DataConverterStaticClass.format_size(self.size_bytes)
        return f"{base_info}, Words: {self.word_count}, Size: {formatted_size}"

    def add_content(self, additional_words: int) -> None:
        """Add content using explicit DataConverter calls"""
        pass


# =============================================================================
# DEMONSTRATION AND COMPARISON
# =============================================================================


def demonstrate_mixin_approach() -> None:
    """Demonstrate the mixin approach"""
    print("=== MIXIN APPROACH ===")

    # Create documents with mixin capabilities
    pdf = PDFDocument("report.pdf", 2500000, 25)  # 2.5 MB
    word = WordDocument("letter.docx", 45000, 500)  # 45 KB

    print(f"PDF: {pdf.get_info()}")
    print(f"Word: {word.get_info()}")

    # Use mixin methods directly on the objects
    print(f"\nPDF size in KB: {pdf.get_size_in_kb():.2f}")
    print(f"Word size in MB: {word.get_size_in_mb():.4f}")


def demonstrate_static_class_approach() -> None:
    """Demonstrate the static utility class approach"""
    print("\n=== STATIC CLASS APPROACH ===")

    # Create documents without mixin
    pdf = PDFDocumentV2("report.pdf", 2500000, 25)  # 2.5 MB
    word = WordDocumentV2("letter.docx", 45000, 500)  # 45 KB

    print(f"PDF: {pdf.get_info()}")
    print(f"Word: {word.get_info()}")

    # Use static utility methods explicitly
    print(
        f"\nPDF size in KB: {DataConverterStaticClass.bytes_to_kb(pdf.size_bytes):.2f}"
    )
    print(
        f"Word size in MB: {DataConverterStaticClass.bytes_to_mb(word.size_bytes):.4f}"
    )

    # Use utility class for additional operations
    print(f"\nSmart formatting:")
    print(f"PDF: {DataConverterStaticClass.format_size(pdf.size_bytes)}")
    print(f"Word: {DataConverterStaticClass.format_size(word.size_bytes)}")


if __name__ == "__main__":
    demonstrate_mixin_approach()
    demonstrate_static_class_approach()
