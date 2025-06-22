import pytest
from src.patterns.mixins.mixin_static_examples import (
    DataConverterMixin,
    PDFDocument,
    WordDocument,
    DataConverterStaticClass,
)


# =============================
# Testing DataConverterMixin
# =============================
class TestDataConverterMixin:
    def test_static_methods(self):
        assert DataConverterMixin.bytes_to_mb(1048576) == 1.0
        assert DataConverterMixin.kb_to_bytes(10.0) == 10240

    def test_instance_methods_pdf(self):
        pdf = PDFDocument("file.pdf", 2097152, 10)
        assert abs(pdf.get_size_in_mb() - 2.0) < 0.01
        assert abs(pdf.get_size_in_kb() - 2048.0) < 0.01

    def test_instance_methods_word(self):
        word = WordDocument("file.docx", 10240, 1000)
        assert abs(word.get_size_in_mb() - 0.0098) < 0.001  # 10 KB to MB
        assert abs(word.get_size_in_kb() - 10.0) < 0.01

    def test_requires_attribute(self):
        class Incomplete(DataConverterMixin):
            pass
        incomplete = Incomplete()
        with pytest.raises(AttributeError):
            _ = incomplete.get_size_in_mb()


# =============================
# Testing DataConverterStaticClass
# =============================
class TestDataConverterStaticClass:
    def test_static_methods(self):
        assert DataConverterStaticClass.bytes_to_mb(1048576) == 1.0
        assert DataConverterStaticClass.kb_to_bytes(10.0) == 10240
        assert DataConverterStaticClass.format_size(500) == "500 bytes"

    def test_can_be_used_anywhere(self):
        # No need for inheritance or special attributes
        size_bytes = 2097152
        assert DataConverterStaticClass.bytes_to_mb(size_bytes) == 2.0

    def test_documents_get_size_in_mb(self):
        pdf = PDFDocument("file.pdf", 2097152, 10)
        word = WordDocument("file.docx", 10240, 1000)
        # Use the static class directly to get size in MB
        assert DataConverterStaticClass.bytes_to_mb(pdf.size_bytes) == 2.0
        assert abs(DataConverterStaticClass.bytes_to_mb(word.size_bytes) - 0.0098) < 0.001
