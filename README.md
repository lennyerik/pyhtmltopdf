# pyhtmltopdf
A tiny python PDF generation library which is intentionally **not** based on wkhtmltopdf.
Rather, it uses Chromium with the [pyppeteer library](https://github.com/pyppeteer/pyppeteer) (a python implementation of [Google's Puppeteer](https://github.com/puppeteer/puppeteer)).

## Installation

    pip install git+https://github.com/lennyerik/pyhtmltopdf.git

Or:

    git clone https://github.com/lennyerik/pyhtmltopdf.git
    cd pyhtmltopdf
    pip install -e ".[dev]"

## Usage
Simple use-cases can use the `from_file`, `from_url` and `from_string` (or their async-enabled variants `afrom_file`, `afrom_url`, `afrom_string`) functions:

```python
from pyhtmltopdf import from_file

# Convert input.html to output.pdf
from_file(
    "./input.html",
    "output.pdf",
    render_options={
        "margin": {
            "top": "3cm",
            "left": "2cm",
            "right": "2cm",
            "bottom": "3cm",
        },
    },
)


from pyhtmltopdf import from_url

# We can also write the file ourselves
out_file = open("output.pdf", "wb")
out_file.write(from_url(
    "https://example.com/",
    header_html="<p style=\"font-size: 12pt;\">This is a demo header</p>",
    footer_html="<p style=\"font-size: 12pt;\">Page No: <span class=\"pageNumber\"></span></p>",
    render_options={
        "margin": {
            "top": "2cm",
            "bottom": "2cm",
        }
    },
))
```

If you already have a chromium browser installed, you can add `executablePath` to the `launchOptions` like so:

```python
from_file(
    "./input.html",
    "output.pdf",
    launch_options={
        # This example uses Brave as the chromium-based browser
        "executablePath": "/usr/bin/brave",
    }
    render_options={
        "margin": {
            "top": "3cm",
            "left": "2cm",
            "right": "2cm",
            "bottom": "3cm",
        },
    },
)
```

In case you want to process multiple PDFs, the class based API is faster, since it only spins up one Chromium instance:
```python
from pyhtmltopdf import HTMLToPDFConverter

converter = HTMLToPDFConverter(launch_options={
    # Launch options are passed in here

    # In this example, we dump the stdout and stderr
    # of the browser to our stdout and stderr, enabling
    # us to see browser error messages
    "dumpio": True
})

converter.from_url(
    "https://example.com/",
    "output.pdf",
)
```

Or even asynchronously:

```python
from pyhtmltopdf import AHTMLToPDFConverter

# With AHTMLToPDFConverter , we have to either await init and finish before
# and after using the object or use an async with statement, like shown here
async with AHTMLToPDFConverter() as converter:
    await converter.from_url(
        "https://example.com/",
        "output.pdf",
    )
```

### API

All `from_x` functions have the following parameters:

* `file_path / url / string`: The input HTML / URL / string to process
* `output_path`: An optional output path to save the PDF to. Defaults to `None`
* `header_html`: An optional HTML string for the page header. Defaults to `""`
* `footer_html`: An optional HTML string for the page header. Defaults to `""`
* `render_options`: Can be any of [these](https://pyppeteer.github.io/pyppeteer/reference.html?highlight=pdf#pyppeteer.page.Page.pdf) PDF rendering options

Additionally, the top-level `from_x` functions as well as the constructors of the `HTMLToPDFConverter` and `AHTMLToPDFConverter` classes take the `launch_options` argument which can be any of [these chromium launch options](https://pyppeteer.github.io/pyppeteer/reference.html?highlight=launch#pyppeteer.launcher.launch).

## Development
To format the code, install with dev dependencies and run

    black .

To run the unit tests, install with dev dependencies and execute

    python -m unittest test

You can also set a specific browser:

    CHROMIUM=/usr/bin/brave python -m unittest test

## Why not wkhtmltopdf?
pyhtmltopdf uses an up-to-date version of Chromium, enabling use of features such as flexbox,
which are not supported by wkhtmltopdf's old version of WebKit.
Furthermore, the [current status of the wkhtmltopdf project](https://wkhtmltopdf.org/status.html) is questionable:

* the version of Qt it uses is unsupported since 2015
* it requires a patch to qt in order to enable full header and footer support
* the version of WebKit it uses is over 4 years old
