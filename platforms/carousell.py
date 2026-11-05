
def inspect_carousell_form(page):
    print("\n=== MEMBUKA PEMILIHAN KATEGORI ===")

    try:
        # Cari elemen berdasarkan teks yang terlihat
        category = page.get_by_text(
            "Select a category",
            exact=True
        ).first

        print("Jumlah elemen:", category.count())

        if category.count() == 0:
            print("Select a category tidak ditemukan.")

            # Tampilkan tombol yang tersedia
            buttons = page.locator("button:visible")

            for i in range(buttons.count()):
                button = buttons.nth(i)

                print({
                    "text": button.inner_text().strip(),
                    "aria": button.get_attribute("aria-label")
                })

            return

        print("\nHTML kategori:")
        print(
            category.evaluate("(el) => el.parentElement.outerHTML")
        )

        category.click()
        page.wait_for_timeout(1000)

        print("\nDropdown berhasil dibuka.")

    except Exception as e:
        print("Gagal membuka kategori:", e)

def inspect_category_options(page):
    print("\n=== PEMERIKSAAN KATEGORI CAROUSELL ===")

    try:
        search = page.get_by_placeholder("Search categories...")

        # Periksa sebelum pencarian
        print("\n--- SEBELUM PENCARIAN ---")

        print(
            "Jumlah data-category-id:",
            page.locator("[data-category-id]").count()
        )

        # Ambil teks seluruh dialog
        print("\nTeks dialog:")

        dialog = page.locator('[role="dialog"]')

        if dialog.count() > 0:
            print(dialog.first.inner_text()[:5000])
        else:
            print("Dialog tidak ditemukan.")

        # Cari kategori Men's
        search.fill("Men")
        page.wait_for_timeout(2000)

        print("\n--- SETELAH PENCARIAN MEN ---")

        print(
            "Jumlah data-category-id:",
            page.locator("[data-category-id]").count()
        )

        # Periksa elemen yang memiliki teks Men
        elements = page.locator(
            'button, [role="option"], [role="button"], div'
        )

        for i in range(min(elements.count(), 150)):
            el = elements.nth(i)

            try:
                if not el.is_visible():
                    continue

                text = el.inner_text().strip()

                if text and "men" in text.lower():
                    print({
                        "index": i,
                        "tag": el.evaluate("(el) => el.tagName"),
                        "text": text[:300],
                        "html": el.evaluate(
                            "(el) => el.outerHTML"
                        )[:1000]
                    })

            except Exception:
                continue

    except Exception as e:
        print("Gagal memeriksa kategori:", e)
    print("\n=== PEMERIKSAAN STRUKTUR KATEGORI ===")

    try:
        search = page.get_by_placeholder("Search categories...")
        search.fill("Men")
        page.wait_for_timeout(2000)

        # Periksa seluruh elemen yang memiliki data-category-id
        categories = page.locator("[data-category-id]")

        print(f"\nJumlah kategori ditemukan: {categories.count()}")

        for i in range(categories.count()):
            category = categories.nth(i)

            try:
                print(f"\n--- KATEGORI {i} ---")

                # Ambil HTML induk tombol kategori
                parent_html = category.evaluate("""
                    el => el.parentElement?.outerHTML
                """)

                print(parent_html[:2500] if parent_html else "Parent tidak ditemukan")

            except Exception as e:
                print("Gagal membaca kategori:", e)

    except Exception as e:
        print("Gagal memeriksa kategori:", e)


def select_category(page):
    """Memilih Men's Fashion > Men's Clothes > Bottoms."""

    print("\n=== MEMILIH KATEGORI CAROUSELL ===")

    # Buka Select a category
    category_button = page.get_by_text(
        "Select a category",
        exact=True
    )

    category_button.click()
    page.wait_for_timeout(500)

    # Buka Men's Fashion melalui ikon panah
    mens_fashion = page.locator(
        "div.D_aTN.D_aTQ"
    ).filter(
        has=page.get_by_text("Men's Fashion", exact=True)
    )

    mens_fashion.locator("div.D_aTT").click()
    page.wait_for_timeout(500)

    print("Men's Fashion berhasil dibuka.")

    # Buka Men's Clothes melalui ikon panah
    mens_clothes = page.locator(
        "div.D_aTN.D_aTQ"
    ).filter(
        has=page.get_by_text("Men's Clothes", exact=True)
    )

    mens_clothes.locator("div.D_aTT").click()
    page.wait_for_timeout(500)

    print("Men's Clothes berhasil dibuka.")

    # Pilih Bottoms
    bottoms = page.locator(
        "div.D_aTN.D_aTU"
    ).filter(
        has=page.get_by_text("Bottoms", exact=True)
    )

    bottoms.click()
    page.wait_for_timeout(1000)

    print("Kategori Bottoms berhasil dipilih.")

    return True


def inspect_sell_form(page):
    print("\n=== PEMERIKSAAN FORM CAROUSELL ===")

    selectors = [
        "input",
        "textarea",
        "button",
        '[role="button"]',
        '[role="combobox"]',
        '[role="listbox"]',
        '[role="option"]',
    ]

    for selector in selectors:
        elements = page.locator(selector)

        print(f"\n--- {selector} ({elements.count()}) ---")

        for i in range(elements.count()):
            el = elements.nth(i)

            try:
                if not el.is_visible():
                    continue

                print({
                    "tag": el.evaluate("(e) => e.tagName"),
                    "text": el.inner_text().strip()[:150],
                    "placeholder": el.get_attribute("placeholder"),
                    "aria-label": el.get_attribute("aria-label"),
                    "role": el.get_attribute("role"),
                    "type": el.get_attribute("type"),
                    "name": el.get_attribute("name"),
                })

            except Exception:
                continue



def inspect_listing_fields(page):
    print("\n=== INSPEKSI FORM LISTING CAROUSELL ===")

    selectors = [
        "input:visible",
        "textarea:visible",
        '[contenteditable="true"]:visible',
        "button:visible",
        '[role="combobox"]:visible',
    ]

    for selector in selectors:
        elements = page.locator(selector)

        print(f"\n--- {selector} ({elements.count()}) ---")

        for i in range(elements.count()):
            el = elements.nth(i)

            try:
                info = el.evaluate("""
                    el => ({
                        tag: el.tagName,
                        type: el.getAttribute("type"),
                        name: el.getAttribute("name"),
                        placeholder: el.getAttribute("placeholder"),
                        ariaLabel: el.getAttribute("aria-label"),
                        value: el.value ?? null,
                        text: el.innerText?.trim().slice(0, 150),
                        html: el.outerHTML.slice(0, 500)
                    })
                """)

                print(f"Element {i}: {info}")

            except Exception:
                continue



def fill_listing_basic(page, listing):
    """Mengisi judul, harga, dan deskripsi Carousell."""

    print("\n=== MENGISI DATA LISTING CAROUSELL ===")

    results = []

    fields = {
        "title": (
            'input[name="field_title"]',
            listing.get("title")
        ),
        "price": (
            'input[name="field_price"]',
            listing.get("price")
        ),
        "description": (
            'textarea[name="field_description"]',
            listing.get("description")
        ),
    }

    for name, (selector, value) in fields.items():
        try:
            if value is None or str(value).strip() == "":
                print(f"{name}: data kosong, dilewati.")
                continue

            page.locator(selector).fill(str(value))
            print(f"{name}: berhasil diisi.")
            results.append(name)

        except Exception as e:
            print(f"{name}: gagal diisi - {e}")

    return results



def select_condition(page, condition):
    """Memetakan kondisi dari listing.json ke kondisi Carousell."""

    print("\n=== MEMILIH KONDISI CAROUSELL ===")

    condition_mapping = {
        "new": "Brand new",
        "used - like new": "Like new",
        "used - good": "Lightly used",
        "used - fair": "Well used",
    }

    normalized = str(condition or "").strip().casefold()
    selected_condition = condition_mapping.get(normalized)

    if not selected_condition:
        print(f"Kondisi tidak dikenali: {condition}")
        return False

    try:
        condition_button = page.get_by_role(
            "button",
            name=selected_condition,
            exact=True,
        )

        if condition_button.count() == 0:
            print(f"Pilihan '{selected_condition}' tidak ditemukan.")
            return False

        condition_button.first.click()

        print(f"Kondisi berhasil dipilih: {selected_condition}")
        return True

    except Exception as e:
        print(f"Gagal memilih kondisi: {e}")
        return False



def fill_brand(page, brand):
    """Mengisi Brand pada Optional Details Carousell."""

    if not brand:
        print("Brand kosong, dilewati.")
        return False

    print("\n=== MENGISI BRAND CAROUSELL ===")

    try:
        # Pastikan Optional Details terbuka.
        brand_input = page.locator(
            'input[name="field_brand"]'
        )

        if not brand_input.is_visible():
            optional_details = page.locator(
                "#FieldSetGroup-Container-group_optional_details_group"
            )

            optional_details.locator(
                'div[role="button"]'
            ).click()

            page.wait_for_timeout(500)

        # Isi Brand.
        brand_input.wait_for(state="visible", timeout=5000)
        brand_input.fill(str(brand))

        print(f"Brand berhasil diisi: {brand}")
        return True

    except Exception as e:
        print(f"Brand gagal diisi: {e}")
        return False


def select_deal_methods(page, methods):
    """Memilih metode transaksi Carousell."""

    print("\n=== MEMILIH DEAL METHODS CAROUSELL ===")

    if not isinstance(methods, list):
        print("deal_methods harus berupa list.")
        return False

    mapping = {
        "meetup": "field_meetup",
        "mailing": "field_mailing",
    }

    selected = [
        str(method).strip().casefold()
        for method in methods
    ]

    invalid = [
        method for method in selected
        if method not in mapping
    ]

    if invalid:
        print(f"Metode tidak dikenal: {invalid}")
        return False

    try:
        for method, field_name in mapping.items():

            checkbox = page.locator(
                f'input[name="{field_name}"]'
            )

            if checkbox.count() == 0:
                print(f"{method}: checkbox tidak ditemukan.")
                return False

            # Periksa kondisi checkbox saat ini.
            is_checked = checkbox.is_checked()
            should_check = method in selected

            if is_checked == should_check:
                print(f"{method}: sudah sesuai.")
                continue

            # Klik label, bukan input karena SVG menghalangi klik.
            checkbox.locator("xpath=..").click()

            page.wait_for_timeout(300)

            if checkbox.is_checked() != should_check:
                print(f"{method}: gagal mengubah checkbox.")
                return False

            status = "dipilih" if should_check else "tidak dipilih"
            print(f"{method}: {status}.")

        if "meetup" in selected:
            print(
                "Perhatian: pastikan lokasi Meet-up "
                "sudah dipilih."
            )

        return True

    except Exception as e:
        print(f"Gagal memilih deal methods: {e}")
        return False


def publish_carousell(page):
    """Klik tombol List now untuk menerbitkan listing Carousell."""

    print("\n=== MENERBITKAN LISTING CAROUSELL ===")

    try:
        list_button = page.get_by_role(
            "button",
            name="List now",
            exact=True
        )

        list_button.wait_for(
            state="visible",
            timeout=10000
        )

        if not list_button.is_enabled():
            print("Tombol List now belum aktif.")
            return False

        list_button.click()

        print("Tombol List now berhasil diklik.")
        print("Silakan periksa hasil listing di Chrome.")

        return True

    except Exception as e:
        print(f"Gagal menerbitkan listing: {e}")
        return False

def select_size(page, size):
    """Memilih ukuran pakaian pada listing Carousell."""

    print("\n=== MEMILIH SIZE CAROUSELL ===")

    size_mapping = {
        "Below Intl XS": "Below Intl XS / EU 38 / UK 28 / US 28",
        "XS": "Intl XS / EU 38 / UK 28 / US 28",
        "S": "Intl S / EU 40 / UK 30 / US 30",
        "M": "Intl M / EU 42 / UK 32 / US 32",
        "L": "Intl L / EU 44 / UK 34 / US 34",
        "XL": "Intl XL / EU 46 / UK 36 / US 36",
        "XXL": "Intl XXL / EU 48 / UK 38 / US 38",
        "Above XXL": "Above Intl XXL / EU 48 / UK 38 / US 38",
        "Others": "Others",
    }

    if not size:
        print("Size tidak tersedia di listing.json.")
        return False

    selected_size = size_mapping.get(size.strip())

    if not selected_size:
        print(f"Ukuran tidak valid: {size}")
        return False

    try:
        # Cari tombol Size berdasarkan ID field
        size_dropdown = page.locator(
            "#FieldSetField-Container-field_size_bottom button[role='listbox']"
        )

        size_dropdown.wait_for(
            state="visible",
            timeout=10000
        )

        size_dropdown.click()

        # Pilih ukuran dari dropdown
        option = page.get_by_role(
            "option",
            name=selected_size,
            exact=True
        )

        option.wait_for(
            state="visible",
            timeout=5000
        )

        option.click()

        # Verifikasi ukuran yang terpilih
        page.wait_for_timeout(300)

        print(f"Size berhasil dipilih: {selected_size}")
        return True

    except Exception as e:
        print(f"Gagal memilih size: {e}")
        return False
