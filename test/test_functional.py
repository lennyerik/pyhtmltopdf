import unittest
import tempfile
from .common import *
from pyhtmltopdf import *


class TestFunctional(unittest.TestCase):
    def test_from_file(self):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=True) as f:
            f.write(TEST_HTML.encode())
            f.flush()

            pdf = from_file(
                f.name,
                header_html=TEST_HEADER,
                footer_html=TEST_FOOTER,
                render_options={
                    "margin": {
                        "top": "2cm",
                        "bottom": "2cm",
                    },
                },
                launch_options=LAUNCH_OPTIONS,
            )
            check_test_pdf(self, pdf)

    def test_from_url(self):
        pdf = from_url(
            "https://example.com",
            header_html='<p style="font-size: 12pt;">Test Header</p>',
            footer_html='<p style="font-size: 12pt;">Test Footer</p>',
            render_options={
                "margin": {
                    "top": "2cm",
                    "bottom": "2cm",
                },
            },
            launch_options=LAUNCH_OPTIONS,
        )
        all_text = get_pdf_text(pdf)
        self.assertIn("Example", all_text)
        self.assertIn("Test Header", all_text)
        self.assertIn("Test Footer", all_text)

    def test_from_string(self):
        pdf = from_string(
            TEST_HTML,
            header_html=TEST_HEADER,
            footer_html=TEST_FOOTER,
            render_options={
                "margin": {
                    "top": "2cm",
                    "bottom": "2cm",
                },
            },
            launch_options=LAUNCH_OPTIONS,
        )
        check_test_pdf(self, pdf)
