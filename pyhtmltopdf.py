import asyncio
import tempfile
from os.path import realpath
from pyppeteer import launch


class AHTMLToPDFConverter:
    def __init__(self, launch_options={}):
        self.launch_options = launch_options

    async def init(self):
        self._browser = await launch(
            **(
                {
                    "headless": True,
                }
                | self.launch_options
            )
        )

    async def finish(self):
        await self._browser.close()

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, *args):
        await self.finish()

    async def _pdf_from_page(
        self, page, output_path=None, header_html="", footer_html="", render_options={}
    ):
        render_options = {
            "displayHeaderFooter": header_html != "" or footer_html != "",
            "headerTemplate": header_html,
            "footerTemplate": footer_html,
            "format": "A4",
        } | render_options
        if output_path:
            render_options["path"] = output_path
        return await page.pdf(**render_options)

    async def from_file(self, file_path, *args, **kwargs):
        page = await self._browser.newPage()
        await page.goto("file://" + realpath(file_path), waitUntil="load")
        pdf = await self._pdf_from_page(page, *args, **kwargs)
        await page.close()
        return pdf

    async def from_url(self, url, *args, **kwargs):
        page = await self._browser.newPage()
        await page.goto(url, waitUntil="load")
        pdf = await self._pdf_from_page(page, *args, **kwargs)
        await page.close()
        return pdf

    async def from_string(self, string, *args, **kwargs):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=True) as f:
            f.write(string.encode())
            f.flush()

            page = await self._browser.newPage()
            await page.goto("file://" + f.name, waitUntil="load")
            pdf = await self._pdf_from_page(page, *args, **kwargs)
            await page.close()
            return pdf


class HTMLToPDFConverter:
    def __init__(self, launch_options={}):
        self._converter = AHTMLToPDFConverter(launch_options)
        try:
            asyncio.get_event_loop().run_until_complete(self._converter.init())
        except RuntimeError:
            asyncio.set_event_loop((loop := asyncio.new_event_loop()))
            loop.run_until_complete(self._converter.init())

    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self._converter.finish())

    def from_file(self, *args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(
            self._converter.from_file(*args, **kwargs)
        )

    def from_url(self, *args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(
            self._converter.from_url(*args, **kwargs)
        )

    def from_string(self, *args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(
            self._converter.from_string(*args, **kwargs)
        )


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
    converter = HTMLToPDFConverter(launch_options)
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
    converter = HTMLToPDFConverter(launch_options)
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
    converter = HTMLToPDFConverter(launch_options)
    return converter.from_string(
        string, output_path, header_html, footer_html, render_options
    )
