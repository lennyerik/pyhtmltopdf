from os import environ
from io import BytesIO
from PyPDF2 import PdfReader

TEST_HTML = """<!DOCTYPE html>
<html>
    <body>
        <h1>Test HTML</h1>
        <p>Some example text</p>
    </body>
</html>"""

TEST_HEADER = '<p style="font-size: 12pt;">Test Header</p>'
TEST_FOOTER = '<p style="font-size: 12pt;">Test Footer</p>'

LAUNCH_OPTIONS = {
    "executable_path": environ.get("CHROMIUM"),
}


def get_pdf_text(pdf_bytes):
    io = BytesIO(pdf_bytes)
    reader = PdfReader(io)
    return "".join([page.extract_text() for page in reader.pages])


def check_test_pdf(testcls, pdf):
    all_text = get_pdf_text(pdf)
    testcls.assertIn("Test HTML", all_text)
    testcls.assertIn("Some example text", all_text)
    testcls.assertIn("Test Header", all_text)
    testcls.assertIn("Test Footer", all_text)
