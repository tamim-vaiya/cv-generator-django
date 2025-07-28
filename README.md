# cv-generator-django

### 📄 How PDF Generation Works in This Project

To generate a PDF resume, this project uses **Playwright**, a browser automation tool that opens real web pages and prints them to PDF.

---

### ✅ Step-by-step Explanation

```python
import asyncio
from django.http import FileResponse, Http404
from django.conf import settings
from pathlib import Path
from playwright.async_api import async_playwright
```

These are the required imports:

* `asyncio` is used to run asynchronous code.
* `FileResponse` sends the generated PDF back to the browser as a file.
* `Http404` is raised if the user profile doesn't exist.
* `settings.BASE_DIR` is used to build file paths relative to the project root.
* `Path` helps manage filesystem paths.
* `async_playwright` is the asynchronous Playwright API.

---

### 🧠 The Function: `generate_pdf`

```python
async def generate_pdf(url: str, output_path: Path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.pdf(path=str(output_path), format='A4')
        await browser.close()
```

This function:

* Launches a Chromium browser using Playwright
* Opens a new page and navigates to the given URL (e.g., the resume page)
* Saves the loaded HTML page as a PDF (A4 format)
* Closes the browser

Note: This is an `async` function and must be run with `asyncio.run()` inside synchronous Django views.

---

### 📤 The View: `resume_pdf`

```python
def resume_pdf(request, id):
    try:
        profile = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        raise Http404("Profile not found")

    url = request.build_absolute_uri(f'/{id}/')

    output_dir = Path(settings.BASE_DIR) / "pdfs"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f'resume_{id}.pdf'

    asyncio.run(generate_pdf(url, output_file))

    return FileResponse(open(output_file, 'rb'), content_type='application/pdf')
```

What this view does:

1. Loads the user profile based on the provided `id`
2. Builds the full URL to the HTML resume page (e.g., `http://127.0.0.1:8000/2/`)
3. Creates a `pdfs/` directory if it doesn't exist
4. Generates the PDF file and saves it as `resume_<id>.pdf`
5. Returns the file as a downloadable PDF response
