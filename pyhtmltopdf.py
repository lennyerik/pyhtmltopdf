import tempfile
from os.path import realpath
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import playwright

DEFAULT_LAUNCH_OPTIONS = {
    "headless": True,
    "handle_sigint": False,
    "handle_sigterm": False,
    "handle_sighup": False,
    "args": ["--no-sandbox"],
}


class AHTMLToPDFConverter:
    def __init__(self, launch_options={}):
        self._launch_options = launch_options
        self._browser = None
        self._playwright = None

    async def init(self):
        self._playwright = await async_playwright().start()

        try:
            self._browser = await self._playwright.chromium.launch(
                **(DEFAULT_LAUNCH_OPTIONS | self._launch_options)
            )
        except playwright._impl._api_types.Error as exc:
            await self._playwright.stop()
            raise RuntimeError(
                "An exception occurred while trying to launch browser"
            ) from exc

    async def finish(self):
        await self._browser.close()
        await self._playwright.stop()

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, *args):
        await self.finish()

    async def _pdf_from_page(
        self, page, output_path=None, header_html="", footer_html="", render_options={}
    ):
        render_options = {
            "display_header_footer": header_html != "" or footer_html != "",
            "header_template": header_html,
            "footer_template": footer_html,
            "format": "A4",
        } | render_options
        if output_path:
            render_options["path"] = output_path
        return await page.pdf(**render_options)

    async def from_file(self, file_path, *args, **kwargs):
        page = await self._browser.new_page()
        await page.goto("file://" + realpath(file_path), wait_until="load")
        pdf = await self._pdf_from_page(page, *args, **kwargs)
        await page.close()
        return pdf

    async def from_url(self, url, *args, **kwargs):
        page = await self._browser.new_page()
        await page.goto(url, wait_until="load")
        pdf = await self._pdf_from_page(page, *args, **kwargs)
        await page.close()
        return pdf

    async def from_string(self, string, *args, **kwargs):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=True) as f:
            f.write(string.encode())
            f.flush()
            return await self.from_file(f.name, *args, **kwargs)


class HTMLToPDFConverter:
    _browser = None

    def __init__(self, launch_options={}):
        self._launch_options = launch_options
        self._browser = None
        self._playwright = None

    def init(self):
        self._playwright = sync_playwright().start()
        try:
            self._browser = self._playwright.chromium.launch(
                **(DEFAULT_LAUNCH_OPTIONS) | self._launch_options
            )
        except playwright._impl._api_types.Error as exc:
            self._playwright.stop()
            raise RuntimeError(
                "An exception occurred while trying to launch browser"
            ) from exc

    def finish(self):
        self._browser.close()
        self._playwright.stop()

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, *args):
        self.finish()

    def _pdf_from_page(
        self, page, output_path=None, header_html="", footer_html="", render_options={}
    ):
        render_options = {
            "display_header_footer": header_html != "" or footer_html != "",
            "header_template": header_html,
            "footer_template": footer_html,
            "format": "A4",
        } | render_options
        if output_path:
            render_options["path"] = output_path
        return page.pdf(**render_options)

    def from_file(self, file_path, *args, **kwargs):
        page = self._browser.new_page()
        page.goto("file://" + realpath(file_path), wait_until="load")
        pdf = self._pdf_from_page(page, *args, **kwargs)
        page.close()
        return pdf

    def from_url(self, url, *args, **kwargs):
        page = self._browser.new_page()
        page.goto(url, wait_until="load")
        pdf = self._pdf_from_page(page, *args, **kwargs)
        page.close()
        return pdf

    def from_string(self, string, *args, **kwargs):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=True) as f:
            f.write(string.encode())
            f.flush()
            return self.from_file(f.name, *args, **kwargs)


async def afrom_file(
    file_path,
    output_path=None,
    header_html="",
    footer_html="",
    launch_options={},
    render_options={},
):
    async with AHTMLToPDFConverter(launch_options) as converter:
        return await converter.from_file(
            file_path, output_path, header_html, footer_html, render_options
        )


def from_file(
    file_path,
    output_path=None,
    header_html="",
    footer_html="",
    launch_options={},
    render_options={},
):
    with HTMLToPDFConverter(launch_options) as converter:
        return converter.from_file(
            file_path, output_path, header_html, footer_html, render_options
        )


async def afrom_url(
    url,
    output_path=None,
    header_html="",
    footer_html="",
    launch_options={},
    render_options={},
):
    async with AHTMLToPDFConverter(launch_options) as converter:
        return await converter.from_url(
            url, output_path, header_html, footer_html, render_options
        )


def from_url(
    url,
    output_path=None,
    header_html="",
    footer_html="",
    launch_options={},
    render_options={},
):
    with HTMLToPDFConverter(launch_options) as converter:
        return converter.from_url(
            url, output_path, header_html, footer_html, render_options
        )


async def afrom_string(
    string,
    output_path=None,
    header_html="",
    footer_html="",
    launch_options={},
    render_options={},
):
    async with AHTMLToPDFConverter(launch_options) as converter:
        return await converter.from_string(
            string, output_path, header_html, footer_html, render_options
        )


def from_string(
    string,
    output_path=None,
    header_html="",
    footer_html="",
    launch_options={},
    render_options={},
):
    with HTMLToPDFConverter(launch_options) as converter:
        return converter.from_string(
            string, output_path, header_html, footer_html, render_options
        )
