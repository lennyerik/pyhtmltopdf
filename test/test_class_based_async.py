import unittest
import tempfile
from .common import *
from pyhtmltopdf import *


class TestClassBasedAsync(unittest.IsolatedAsyncioTestCase):
    async def test_from_file_init(self):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=True) as f:
            f.write(TEST_HTML.encode())
            f.flush()

            converter = AHTMLToPDFConverter(LAUNCH_OPTIONS)
            await converter.init()
            pdf = await converter.from_file(
                f.name,
                header_html=TEST_HEADER,
                footer_html=TEST_FOOTER,
                render_options={
                    "margin": {
                        "top": "2cm",
                        "bottom": "2cm",
                    },
                },
            )
            await converter.finish()
            check_test_pdf(self, pdf)

    async def test_from_file_with(self):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=True) as f:
            f.write(TEST_HTML.encode())
            f.flush()

            async with AHTMLToPDFConverter(LAUNCH_OPTIONS) as converter:
                pdf = await converter.from_file(
                    f.name,
                    header_html=TEST_HEADER,
                    footer_html=TEST_FOOTER,
                    render_options={
                        "margin": {
                            "top": "2cm",
                            "bottom": "2cm",
                        },
                    },
                )
                check_test_pdf(self, pdf)

    async def test_from_url_init(self):
        converter = AHTMLToPDFConverter(LAUNCH_OPTIONS)
        await converter.init()
        pdf = await converter.from_url(
            "https://example.com",
            header_html='<p style="font-size: 12pt;">Test Header</p>',
            footer_html='<p style="font-size: 12pt;">Test Footer</p>',
            render_options={
                "margin": {
                    "top": "2cm",
                    "bottom": "2cm",
                },
            },
        )
        await converter.finish()
        all_text = get_pdf_text(pdf)
        self.assertIn("Example", all_text)
        self.assertIn("Test Header", all_text)
        self.assertIn("Test Footer", all_text)

    async def test_from_url_with(self):
        async with AHTMLToPDFConverter(LAUNCH_OPTIONS) as converter:
            pdf = await converter.from_url(
                "https://example.com",
                header_html='<p style="font-size: 12pt;">Test Header</p>',
                footer_html='<p style="font-size: 12pt;">Test Footer</p>',
                render_options={
                    "margin": {
                        "top": "2cm",
                        "bottom": "2cm",
                    },
                },
            )
            all_text = get_pdf_text(pdf)
            self.assertIn("Example", all_text)
            self.assertIn("Test Header", all_text)
            self.assertIn("Test Footer", all_text)

    async def test_from_string_init(self):
        converter = AHTMLToPDFConverter(LAUNCH_OPTIONS)
        await converter.init()
        pdf = await converter.from_string(
            TEST_HTML,
            header_html=TEST_HEADER,
            footer_html=TEST_FOOTER,
            render_options={
                "margin": {
                    "top": "2cm",
                    "bottom": "2cm",
                },
            },
        )
        await converter.finish()
        check_test_pdf(self, pdf)

    async def test_from_string_with(self):
        async with AHTMLToPDFConverter(LAUNCH_OPTIONS) as converter:
            pdf = await converter.from_string(
                TEST_HTML,
                header_html=TEST_HEADER,
                footer_html=TEST_FOOTER,
                render_options={
                    "margin": {
                        "top": "2cm",
                        "bottom": "2cm",
                    },
                },
            )
            check_test_pdf(self, pdf)

    async def test_multiple(self):
        async with AHTMLToPDFConverter(LAUNCH_OPTIONS) as converter:
            first_pdf = await converter.from_string(
                "<!DOCTYPE html><html><body><h1>First PDF</h1></body></html>",
            )
            first_pdf_text = get_pdf_text(first_pdf)
            self.assertIn("First PDF", first_pdf_text)

            second_pdf = await converter.from_string(
                "<!DOCTYPE html><html><body><h1>Second PDF</h1></body></html>",
            )
            second_pdf_text = get_pdf_text(second_pdf)
            self.assertIn("Second PDF", second_pdf_text)
