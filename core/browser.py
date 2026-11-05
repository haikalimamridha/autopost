
def go(page, url):
    try:
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=120000,
        )
    except Exception as e:
        print(
            f"Peringatan: halaman belum selesai dimuat "
            f"({type(e).__name__})."
        )


def inspect_form(page):
    print("\n=== PEMERIKSAAN ELEMEN FORM ===")

    elements = page.locator(
        'input, textarea, '
        '[contenteditable="true"], '
        '[role="textbox"], '
        '[role="combobox"]'
    )

    for i in range(elements.count()):
        el = elements.nth(i)

        try:
            info = el.evaluate("""
                el => ({
                    tag: el.tagName,
                    type: el.getAttribute('type'),
                    role: el.getAttribute('role'),
                    placeholder: el.getAttribute('placeholder'),
                    ariaLabel: el.getAttribute('aria-label'),
                    contenteditable: el.getAttribute('contenteditable'),
                    text: el.innerText,
                    outerHTML: el.outerHTML.substring(0, 400)
                })
            """)

            print(f"\nElement {i}:")
            print(info)

        except Exception:
            continue
