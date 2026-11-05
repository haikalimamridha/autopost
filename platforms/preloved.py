
def inspect_preloved_form(page):
    """Memeriksa seluruh elemen form Preloved."""

    print("\n" + "=" * 45)
    print("PEMERIKSAAN FORM PRELOVED")
    print("=" * 45)

    print("\n=== INPUT ===")

    inputs = page.locator("input")

    for i in range(inputs.count()):
        element = inputs.nth(i)

        print(f"\nInput {i}:")
        print("Type:", element.get_attribute("type"))
        print("Name:", element.get_attribute("name"))
        print("Placeholder:", element.get_attribute("placeholder"))
        print("Aria-label:", element.get_attribute("aria-label"))
        print("HTML:", element.evaluate("(el) => el.outerHTML")[:500])

    print("\n=== TEXTAREA ===")

    textareas = page.locator("textarea")

    for i in range(textareas.count()):
        element = textareas.nth(i)

        print(f"\nTextarea {i}:")
        print("Placeholder:", element.get_attribute("placeholder"))
        print("HTML:", element.evaluate("(el) => el.outerHTML")[:500])

    print("\n=== SELECT ===")

    selects = page.locator("select")

    for i in range(selects.count()):
        element = selects.nth(i)

        print(f"\nSelect {i}:")
        print("HTML:", element.evaluate("(el) => el.outerHTML")[:1000])

    print("\n=== BUTTON ===")

    buttons = page.locator("button")

    for i in range(buttons.count()):
        element = buttons.nth(i)

        if element.is_visible():
            print(
                f"Button {i}:",
                element.inner_text().strip(),
                "| Aria:",
                element.get_attribute("aria-label")
            )

    print("\n=== LABEL ===")

    labels = page.locator("label")

    for i in range(labels.count()):
        element = labels.nth(i)

        if element.is_visible():
            print("Label:", element.inner_text().strip())

    print("\n" + "=" * 45)



def fill_preloved_basic(page, data):
    """Mengisi field dasar listing Preloved."""

    result = {}

    # Judul
    title = str(data.get("title", "")).strip()

    if 10 <= len(title) <= 60:
        page.locator('input[placeholder^="cth."]').fill(title)
        result["title"] = True
    else:
        print("Judul harus terdiri dari 10-60 karakter.")
        result["title"] = False

    # Harga
    price = str(data.get("price", ""))
    price = "".join(char for char in price if char.isdigit())

    if price and int(price) >= 30000:
        page.locator('input[name="price"]').fill(price)
        result["price"] = True
    else:
        print("Harga minimal Rp30.000.")
        result["price"] = False

    # Deskripsi
    description = str(data.get("description", "")).strip()

    if description:
        page.locator("textarea#description").fill(description)
        result["description"] = True
    else:
        result["description"] = False

    return result


def inspect_preloved_controls(page):
    """Memeriksa elemen custom seperti kategori dan kondisi."""

    print("\n=== PEMERIKSAAN KATEGORI DAN DETAIL ===")

    forms = page.locator("form")

    print("Jumlah form:", forms.count())

    if forms.count() == 0:
        print("Form tidak ditemukan.")
        return

    form = forms.last

    # Tombol dalam form
    buttons = form.locator("button")

    print("\n=== BUTTON ===")

    for i in range(buttons.count()):
        element = buttons.nth(i)

        if element.is_visible():
            print(
                f"\nButton {i}:",
                element.inner_text().strip(),
                "| Aria:",
                element.get_attribute("aria-label"),
                "| HTML:",
                element.evaluate("(el) => el.outerHTML")[:1000]
            )

    # Elemen custom yang dapat diklik
    elements = form.locator(
        '[role="combobox"], '
        '[role="listbox"], '
        '[role="option"], '
        '[role="button"]'
    )

    print("\n=== ROLE ELEMENTS ===")

    for i in range(elements.count()):
        element = elements.nth(i)

        if element.is_visible():
            print(
                f"\nElement {i}:",
                element.inner_text().strip()[:200],
                "| HTML:",
                element.evaluate("(el) => el.outerHTML")[:1000]
            )

    # Semua label dan elemen induknya
    labels = form.locator("label")

    print("\n=== LABEL ===")

    for i in range(labels.count()):
        element = labels.nth(i)

        print(
            element.inner_text().strip(),
            "| HTML:",
            element.evaluate(
                "(el) => el.parentElement.outerHTML"
            )[:1500]
        )
def select_preloved_category(page, categories):
    print("\n=== PEMILIHAN KATEGORI PRELOVED ===")

    category_button = page.locator("#categories")

    for category_name in categories:

        # Buka dropdown jika tertutup
        if category_button.get_attribute("aria-expanded") != "true":
            category_button.click()
            page.wait_for_timeout(1000)

        # Tunggu sampai opsi kategori muncul
        options = page.locator(
            '#category-picker-list [role="option"]'
        )

        try:
            options.first.wait_for(
                state="visible",
                timeout=5000
            )
        except:
            print("Dropdown kategori tidak terbuka.")
            return False

        # Cari opsi berdasarkan teks
        option = options.filter(
            has_text=category_name
        )

        # Periksa kecocokan teks secara fleksibel
        target = None

        for i in range(options.count()):
            item = options.nth(i)

            if not item.is_visible():
                continue

            text = item.inner_text().strip()

            if text.casefold() == category_name.casefold():
                target = item
                break

        if target is None:
            print(f"Kategori '{category_name}' tidak ditemukan.")

            print("\nPilihan yang tersedia:")
            for i in range(options.count()):
                item = options.nth(i)

                if item.is_visible():
                    print("-", item.inner_text().strip())

            return False

        target.click()
        page.wait_for_timeout(1200)

        print(f"Berhasil memilih: {category_name}")

    print("\nKategori berhasil dipilih.")
    return True
def publish_preloved(page):
    button = page.get_by_role(
        "button",
        name="Terbitkan produk",
        exact=True
    )

    if button.count() == 0:
        print("Tombol Terbitkan produk tidak ditemukan.")
        return False

    if not button.is_enabled():
        print("Tombol Terbitkan produk belum aktif.")
        return False

    button.click()
    page.wait_for_timeout(2000)

    print("Tombol Terbitkan produk berhasil diklik.")
    return True


def detect_preloved_category(data):
    # Gabungkan informasi produk
    text = " ".join([
        str(data.get("title", "")),
        str(data.get("description", "")),
        str(data.get("brand", ""))
    ]).casefold()

    # Tentukan kategori gender
    gender_hint = str(data.get("category", "")).casefold()

    if any(word in gender_hint for word in ["men", "pria", "male"]):
        gender = "Pria"

    elif any(word in gender_hint for word in ["women", "wanita", "female"]):
        gender = "Wanita"

    else:
        print("Gender produk tidak dapat ditentukan.")
        return None

    # Tentukan subkategori berdasarkan kata kunci
    category_rules = [
        {
            "keywords": ["jeans", "denim"],
            "path": ["Bottoms", "Jeans"]
        },
        {
            "keywords": ["shorts", "celana pendek"],
            "path": ["Bottoms", "Shorts"]
        },
        {
            "keywords": ["jogger", "sweatpants"],
            "path": ["Bottoms", "Sweatpants & Joggers"]
        },
        {
            "keywords": ["formal pants", "celana formal"],
            "path": ["Bottoms", "Formal pants"]
        },
        {
            "keywords": ["jacket", "jaket"],
            "path": ["Outerwear"]
        },
        {
            "keywords": ["t-shirt", "kaos", "shirt", "kemeja"],
            "path": ["Tops"]
        }
    ]

    for rule in category_rules:
        if any(keyword in text for keyword in rule["keywords"]):
            return [gender] + rule["path"]

    print("Jenis produk tidak dikenali.")
    return None


def select_preloved_size(page, size):
    print("\n=== PEMILIHAN SIZE PRELOVED ===")

    size = str(size).strip().upper()

    dropdown = page.locator("#sizes")

    if dropdown.count() == 0:
        print("Dropdown Size tidak ditemukan.")
        return False

    # Buka dropdown
    if dropdown.get_attribute("aria-expanded") != "true":
        dropdown.click()
        page.wait_for_timeout(500)

    # Cari opsi berdasarkan ukuran
    options = page.locator(
        '#select-field-6 [role="option"]'
    )

    try:
        options.first.wait_for(
            state="visible",
            timeout=5000
        )
    except:
        print("Pilihan Size tidak muncul.")
        return False

    selected_option = None

    for i in range(options.count()):
        option = options.nth(i)

        if not option.is_visible():
            continue

        # Ambil ukuran pertama, misalnya M
        size_label = option.locator("span.w-16").first

        if size_label.count() == 0:
            continue

        available_size = size_label.inner_text().strip().upper()

        if available_size == size:
            selected_option = option
            break

    if selected_option is None:
        print(f"Size '{size}' tidak tersedia.")

        print("Pilihan yang tersedia:")
        for i in range(options.count()):
            print("-", options.nth(i).inner_text().strip())

        return False

    selected_option.click()
    page.wait_for_timeout(700)

    print(f"Berhasil memilih size: {size}")

    return True

def select_preloved_brand(page, brand):
    print("\n=== PEMILIHAN BRAND PRELOVED ===")

    brand = str(brand or "").strip()

    if not brand:
        print("Brand tidak tersedia di listing.json.")
        return False

    dropdown = page.locator("#brands")

    if dropdown.count() == 0:
        print("Dropdown Brand tidak ditemukan.")
        return False

    # Buka dropdown
    if dropdown.get_attribute("aria-expanded") != "true":
        dropdown.click()
        page.wait_for_timeout(700)

    # Ambil ID listbox secara dinamis
    list_id = dropdown.get_attribute("aria-controls")

    if not list_id:
        print("ID pilihan Brand tidak ditemukan.")
        return False

    # Cari input pencarian di dalam dropdown
    search_input = page.locator(
        f'#{list_id} input[role="combobox"]'
    )

    if search_input.count() == 0:
        search_input = page.locator(
            'input[role="combobox"][aria-controls="' + list_id + '"]'
        )

    if search_input.count() == 0:
        print("Kolom pencarian Brand tidak ditemukan.")
        return False

    # Ketik nama brand
    search_input.fill(brand)
    page.wait_for_timeout(1000)

    # Ambil opsi hasil pencarian
    options = page.locator(
        f'#{list_id} [role="option"]'
    )

    try:
        options.first.wait_for(
            state="visible",
            timeout=5000
        )
    except:
        print(f"Hasil pencarian brand '{brand}' tidak ditemukan.")
        return False

    selected_option = None

    for i in range(options.count()):
        option = options.nth(i)

        if not option.is_visible():
            continue

        option_text = option.inner_text().strip()

        if option_text.casefold() == brand.casefold():
            selected_option = option
            break

    if selected_option is None:
        print(f"Brand '{brand}' tidak ditemukan dalam hasil pencarian.")
        print("Hasil pencarian:")

        for i in range(options.count()):
            option = options.nth(i)

            if option.is_visible():
                print("-", option.inner_text().strip())

        return False

    selected_option.click()
    page.wait_for_timeout(700)

    print(f"Berhasil memilih brand: {brand}")

    return True

def select_preloved_condition(page, condition):
    print("\n=== PEMILIHAN CONDITION PRELOVED ===")

    condition = str(condition or "").strip()

    condition_mapping = {
        "new with tags": "Baru dengan tag",
        "new without tags": "Baru tanpa tag",
        "used - like new": "Sangat baik",
        "used - good": "Baik",
        "used - fair": "Memuaskan",
    }

    target = condition_mapping.get(condition.casefold())

    if not target:
        print(f"Condition '{condition}' belum memiliki pemetaan.")
        return False

    dropdown = page.locator("#condition")

    if dropdown.count() == 0:
        print("Dropdown Condition tidak ditemukan.")
        return False

    # Buka dropdown
    if dropdown.get_attribute("aria-expanded") != "true":
        dropdown.click()
        page.wait_for_timeout(700)

    # Ambil ID listbox secara dinamis
    list_id = dropdown.get_attribute("aria-controls")

    if not list_id:
        print("ID pilihan Condition tidak ditemukan.")
        return False

    options = page.locator(
        f'#{list_id} [role="option"]'
    )

    try:
        options.first.wait_for(
            state="visible",
            timeout=5000
        )
    except:
        print("Pilihan Condition tidak muncul.")
        return False

    selected_option = None

    for i in range(options.count()):
        option = options.nth(i)

        if not option.is_visible():
            continue

        option_text = option.inner_text().strip()

        # Cocokkan nama kondisi di awal teks,
        # bukan seluruh deskripsi kondisinya.
        if option_text.casefold().startswith(target.casefold()):
            selected_option = option
            break

    if selected_option is None:
        print(f"Condition '{target}' tidak ditemukan.")

        print("\nPilihan yang tersedia:")
        for i in range(options.count()):
            option = options.nth(i)

            if option.is_visible():
                print("-", option.inner_text().strip())

        return False

    selected_option.click()
    page.wait_for_timeout(700)

    print(f"Berhasil memilih condition: {target}")

    return True

def select_preloved_colors(page, colors):
    print("\n=== PEMILIHAN COLOR PRELOVED ===")

    if not colors:
        print("Warna tidak tersedia di listing.json.")
        return False

    if isinstance(colors, str):
        colors = [colors]

    dropdown = page.locator("#colors")

    if dropdown.count() == 0:
        print("Dropdown Color tidak ditemukan.")
        return False

    list_id = dropdown.get_attribute("aria-controls")

    if not list_id:
        print("ID pilihan Color tidak ditemukan.")
        return False

    selected_count = 0

    for color in colors:
        color = str(color).strip()

        if not color:
            continue

        # Buka dropdown jika belum terbuka
        if dropdown.get_attribute("aria-expanded") != "true":
            dropdown.click()
            page.wait_for_timeout(700)

        options = page.locator(
            f'#{list_id} [role="option"]'
        )

        try:
            options.first.wait_for(
                state="visible",
                timeout=5000
            )
        except:
            print("Pilihan Color tidak muncul.")
            return False

        selected_option = None

        for i in range(options.count()):
            option = options.nth(i)

            if not option.is_visible():
                continue

            option_text = option.inner_text().strip()

            if option_text.casefold() == color.casefold():
                selected_option = option
                break

        if selected_option is None:
            print(f"Warna '{color}' tidak ditemukan.")

            print("Pilihan yang tersedia:")
            for i in range(options.count()):
                option = options.nth(i)

                if option.is_visible():
                    print("-", option.inner_text().strip())

            return False

        selected_option.click()
        page.wait_for_timeout(500)

        selected_count += 1
        print(f"Berhasil memilih warna: {color}")

    # Tutup dropdown setelah semua warna dipilih
    if dropdown.get_attribute("aria-expanded") == "true":
        dropdown.click()
        page.wait_for_timeout(700)

    print("Dropdown Color berhasil ditutup.")

    return selected_count > 0