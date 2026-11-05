import re

def select_category(page, category):
    if not category:
        print("Kategori tidak tersedia di listing.json.")
        return False

    print(f"\nMemilih kategori: {category}")

    try:
        dropdowns = page.locator('label[role="combobox"]')
        dropdown = None

        for i in range(dropdowns.count()):
            item = dropdowns.nth(i)

            try:
                if item.inner_text().strip().casefold() == "category":
                    dropdown = item
                    break
            except Exception:
                continue

        if dropdown is None:
            print("Dropdown Category tidak ditemukan.")
            return False

        dropdown.click(timeout=5000)
        page.wait_for_timeout(800)

        for selector in ['[role="option"]', '[role="menuitem"]']:
            options = page.locator(selector)

            for i in range(options.count()):
                option = options.nth(i)

                try:
                    if (
                        option.is_visible()
                        and option.inner_text().strip().casefold()
                        == category.strip().casefold()
                    ):
                        option.click(timeout=5000)
                        print("Kategori berhasil dipilih.")
                        return True
                except Exception:
                    continue

        options = page.get_by_text(category, exact=True)

        for i in range(options.count()):
            option = options.nth(i)

            try:
                if option.is_visible():
                    option.click(timeout=5000)
                    print("Kategori berhasil dipilih.")
                    return True
            except Exception:
                continue

        print(f"Pilihan kategori '{category}' tidak ditemukan.")
        return False

    except Exception as e:
        print("Kategori gagal dipilih:", e)
        return False


def select_condition(page, condition):
    if not condition:
        print("Condition tidak tersedia di listing.json.")
        return False

    valid_conditions = [
        "New",
        "Used - Like New",
        "Used - Good",
        "Used - Fair",
    ]

    matched_condition = next(
        (
            item for item in valid_conditions
            if item.casefold() == condition.strip().casefold()
        ),
        None
    )

    if not matched_condition:
        print(f"Condition tidak valid: {condition}")
        print("Pilihan:", ", ".join(valid_conditions))
        return False

    print(f"\nMemilih kondisi: {matched_condition}")

    try:
        dropdowns = page.locator('label[role="combobox"]')
        dropdown = None

        for i in range(dropdowns.count()):
            item = dropdowns.nth(i)

            try:
                if item.inner_text().strip().casefold() == "condition":
                    dropdown = item
                    break
            except Exception:
                continue

        if dropdown is None:
            print("Dropdown Condition tidak ditemukan.")
            return False

        dropdown.click(timeout=5000)
        page.wait_for_timeout(800)

        for selector in ['[role="option"]', '[role="menuitem"]']:
            options = page.locator(selector)

            for i in range(options.count()):
                option = options.nth(i)

                try:
                    if (
                        option.is_visible()
                        and option.inner_text().strip().casefold()
                        == matched_condition.casefold()
                    ):
                        option.click(timeout=5000)
                        print("Condition berhasil dipilih.")
                        return True
                except Exception:
                    continue

        options = page.get_by_text(matched_condition, exact=True)

        for i in range(options.count()):
            option = options.nth(i)

            try:
                if option.is_visible():
                    option.click(timeout=5000)
                    print("Condition berhasil dipilih.")
                    return True
            except Exception:
                continue

        print(f"Pilihan condition '{matched_condition}' tidak ditemukan.")
        return False

    except Exception as e:
        print("Condition gagal dipilih:", e)
        return False


def fill_description(page, description):
    if not description:
        print("Description kosong, dilewati.")
        return False

    print("\nMengisi Description...")

    try:
        label = page.get_by_text("Description", exact=True).first
        container = label.locator("xpath=..")
        textarea = container.locator("textarea")

        textarea.wait_for(state="visible", timeout=10000)
        textarea.fill(str(description))

        print("Description berhasil diisi.")
        return True

    except Exception as e:
        print("Description gagal diisi:", e)
        return False


def open_more_details(page):
    try:
        more_details = page.locator(
            '[role="button"]'
        ).filter(
            has_text="More details"
        ).first

        more_details.wait_for(state="visible", timeout=10000)

        expanded = more_details.get_attribute("aria-expanded")

        if expanded == "false":
            more_details.click()
            page.wait_for_timeout(1000)

        print("More details terbuka.")
        return True

    except Exception as e:
        print("Gagal membuka More details:", e)
        return False


def fill_brand(page, brand):
    if not brand:
        print("Brand kosong, dilewati.")
        return False

    print("\nMengisi Brand...")

    try:
        if not open_more_details(page):
            return False

        label = page.locator("label").filter(
            has=page.get_by_text("Brand", exact=True)
        ).first

        brand_input = label.locator('input[type="text"]')

        brand_input.wait_for(state="visible", timeout=5000)
        brand_input.fill(str(brand))

        page.wait_for_timeout(1000)

        print(f"Brand berhasil diisi: {brand}")
        return True

    except Exception as e:
        print("Brand gagal diisi:", e)
        return False


def fill_location(page, city):
    if not city:
        print("Location kosong, dilewati.")
        return False

    print(f"\nMengisi Location: {city}")

    try:
        location = page.locator(
            'input[aria-label="Location"]'
        ).first

        location.wait_for(state="visible", timeout=10000)
        location.fill(str(city))

        page.wait_for_timeout(1500)

        options = page.locator('[role="option"]')

        for i in range(options.count()):
            option = options.nth(i)

            try:
                if not option.is_visible():
                    continue

                option_text = option.inner_text().strip()
                print("Pilihan lokasi:", option_text)

                if city.casefold() in option_text.casefold():
                    option.click(timeout=5000)
                    print("Location berhasil dipilih.")
                    return True

            except Exception:
                continue

        print("Pilihan lokasi belum ditemukan.")
        print("Nilai input:", location.input_value())
        return False

    except Exception as e:
        print("Location gagal dipilih:", e)
        return False


def select_availability(page, availability):
    if not availability:
        print("Availability kosong, dilewati.")
        return False

    print(f"\nMemilih Availability: {availability}")

    try:
        if not open_more_details(page):
            return False

        dropdown = page.locator(
            'label[role="combobox"]'
        ).filter(
            has=page.get_by_text("Availability", exact=True)
        ).first

        dropdown.wait_for(state="visible", timeout=5000)
        dropdown.click()

        page.wait_for_timeout(500)

        option = page.get_by_text(
            availability,
            exact=True
        ).last

        option.wait_for(state="visible", timeout=5000)
        option.click()

        page.wait_for_timeout(500)

        selected = dropdown.inner_text()

        if availability.casefold() in selected.casefold():
            print(f"Availability berhasil dipilih: {availability}")
            return True

        print("Availability belum sesuai:", selected)
        return False

    except Exception as e:
        print("Availability gagal dipilih:", e)
        return False


def click_marketplace_button(page, button_names, step_name):
    print(f"\nMencari tombol {step_name}...")

    for name in button_names:
        try:
            button = page.get_by_role(
                "button",
                name=re.compile(rf"^{re.escape(name)}$", re.I)
            ).last

            button.wait_for(state="visible", timeout=5000)

            if not button.is_enabled():
                continue

            button.click(timeout=10000)

            print(f"Tombol {name} berhasil diklik.")
            return True

        except Exception:
            continue

    print(f"Tombol {step_name} tidak ditemukan.")
    return False


def publish_facebook(page):
    print("\n=== PROSES PUBLISH FACEBOOK ===")

    next_clicked = click_marketplace_button(
        page,
        ["Next", "Berikutnya"],
        "Next"
    )

    if not next_clicked:
        print("Tidak bisa melanjutkan ke tahap Publish.")
        return False

    page.wait_for_timeout(2000)

    publish_clicked = click_marketplace_button(
        page,
        ["Publish", "Terbitkan"],
        "Publish"
    )

    if not publish_clicked:
        print("Tombol Publish belum ditemukan.")
        print("Silakan periksa halaman Chrome secara manual.")
        return False

    page.wait_for_timeout(3000)

    print("\nPerintah Publish berhasil dikirim.")
    return True
