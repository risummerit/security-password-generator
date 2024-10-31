import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.testcase_id("TC001")
@pytest.mark.smoke
@pytest.mark.password_generator
@pytest.mark.regression
def test_password_generator_smoke_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")

        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."
        
        # Check that the password field is visible
        password_field = page.locator('input[name="password"]')
        assert password_field.is_visible(), "Password field not visible."

        # Check that the password length input field is visible
        length_input = page.locator('input[name="passwordLength"]')
        assert length_input.is_visible(), "Password length input not visible."

        browser.close()


@pytest.mark.testcase_id("TC002")
@pytest.mark.password_generator
@pytest.mark.password_length_input_field
@pytest.mark.regression
@pytest.mark.parametrize("password_length", ["6", "12", "18", "24", "32"])
def test_password_length_input_and_generated_password_length(password_length):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")
        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        # Set password length
        length_input = page.locator('input[name="passwordLength"]')
        length_input.fill(password_length)

        # Retrieve the generated password
        password = page.locator('input[name="password"]').input_value()

        # Check if the length of the password is as expected
        assert len(password) == int(password_length), f"Expected password length {password_length}, but got {len(password)}"
        
        browser.close()


@pytest.mark.testcase_id("TC004")
@pytest.mark.password_generator
@pytest.mark.password_options_combinations_with_checkboxes
@pytest.mark.regression
def test_checkboxes_password_options_default_setup():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")
        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        length_input = page.locator('input[name="passwordLength"]')

        # All boxes data
        lowercase_label = page.locator('label[for="option-lowercase"]')
        lowercase_checkbox = page.locator('input#option-lowercase')

        uppercase_label = page.locator('label[for="option-uppercase"]')
        uppercase_checkbox = page.locator('input#option-uppercase')

        numbers_label = page.locator('label[for="option-numbers"]')
        numbers_checkbox = page.locator('input#option-numbers')

        symbols_label = page.locator('label[for="option-symbols"]')
        symbols_checkbox = page.locator('input#option-symbols')

        # Check initial setup - All checkboxes are visible; Lowercase checked, Uppercase checked, Numbers unchecked, Symbols unchecked. 
        # Default password length should be 6
        assert lowercase_label.is_visible(), "Lowercase checkbox not visible."
        assert uppercase_label.is_visible(), "Uppercase checkbox not visible."
        assert numbers_label.is_visible(), "Numbers checkbox not visible."
        assert symbols_label.is_visible(), "Symbols checkbox not visible."
        assert length_input.is_visible(), "Password input filed should be visible"

        assert lowercase_checkbox.is_checked(), "Lowercase checkbox should be checked by default."
        assert uppercase_checkbox.is_checked(), "Uppercase checkbox should be checked by default."
        assert not numbers_checkbox.is_checked(), "Numbers checkbox should not be checked by default."
        assert not symbols_checkbox.is_checked(), "Symbols checkbox should not be checked by default."

        # Check default generated password
        password = page.locator('input[name="password"]').input_value()
        assert any(char.islower() for char in password), "Password should contain lowercase letters by default."
        assert any(char.isupper() for char in password), "Password should contain uppercase letters by default."
        assert not any(char.isdigit() for char in password), "Password should not contain numbers by default."
        assert not any(not char.isalnum() for char in password), "Password should not contain symbols by default."
        assert len(password) == 6, "Default password length should be 6."

        browser.close()



checkbox_combinations = [
    (True, False, False, False),  # Only Lowercase
    (False, True, False, False),  # Only Uppercase
    (False, False, True, False),  # Only Numbers
    (False, False, False, True),  # Only Symbols
    (True, True, False, False),   # Lowercase + Uppercase
    (True, False, True, False),   # Lowercase + Numbers
    (True, False, False, True),   # Lowercase + Symbols
    (False, True, True, False),   # Uppercase + Numbers
    (False, True, False, True),   # Uppercase + Symbols
    (False, False, True, True),   # Numbers + Symbols
    (True, True, True, False),    # Lowercase + Uppercase + Numbers
    (True, True, False, True),    # Lowercase + Uppercase + Symbols
    (True, False, True, True),    # Lowercase + Numbers + Symbols
    (False, True, True, True),    # Uppercase + Numbers + Symbols
    (True, True, True, True)      # All selected
]
@pytest.mark.testcase_id("TC005")
@pytest.mark.parametrize("lowercase, uppercase, numbers, symbols", checkbox_combinations)
@pytest.mark.password_generator
@pytest.mark.password_options_combinations_with_checkboxes
@pytest.mark.regression
def test_checkboxes_generated_password_combinations(lowercase, uppercase, numbers, symbols):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")
        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        # Locate checkbox labels and inputs
        lowercase_label = page.locator('label[for="option-lowercase"]')
        uppercase_label = page.locator('label[for="option-uppercase"]')
        numbers_label = page.locator('label[for="option-numbers"]')
        symbols_label = page.locator('label[for="option-symbols"]')

        # Set initial state: Lowercase checked, Uppercase unchecked, Numbers and Symbols unchecked
        if not page.locator('input#option-lowercase').is_checked():
            lowercase_label.click()
        elif not page.locator('input#option-uppercase').is_checked():
            uppercase_label.click()
        if not page.locator('input#option-numbers').is_checked():
            numbers_label.click()
        if not page.locator('input#option-symbols').is_checked():
            symbols_label.click()


        # Adjust checkboxes based on the test parameters
        if lowercase:
            if not page.locator('input#option-lowercase').is_checked():
                lowercase_label.click()
        else:
            if page.locator('input#option-lowercase').is_checked():
                lowercase_label.click()

        if uppercase:
            if not page.locator('input#option-uppercase').is_checked():
                uppercase_label.click()
        else:
            if page.locator('input#option-uppercase').is_checked():
                uppercase_label.click()

        if numbers:
            if not page.locator('input#option-numbers').is_checked():
                numbers_label.click()
        else:
            if page.locator('input#option-numbers').is_checked():
                numbers_label.click()

        if symbols:
            if not page.locator('input#option-symbols').is_checked():
                symbols_label.click()
        else:
            if page.locator('input#option-symbols').is_checked():
                symbols_label.click()

        # Read the updated password
        password = page.locator('input[name="password"]').input_value()

        # Assertions based on checkbox settings
        if lowercase:
            assert any(char.islower() for char in password), "Password should contain lowercase letters."
        else:
            assert not any(char.islower() for char in password), "Password should not contain lowercase letters."

        if uppercase:
            assert any(char.isupper() for char in password), "Password should contain uppercase letters."
        else:
            assert not any(char.isupper() for char in password), "Password should not contain uppercase letters."

        if numbers:
            assert any(char.isdigit() for char in password), "Password should contain numbers."
        else:
            assert not any(char.isdigit() for char in password), "Password should not contain numbers."

        if symbols:
            assert any(not char.isalnum() for char in password), "Password should contain symbols."
        else:
            assert not any(not char.isalnum() for char in password), "Password should not contain symbols."

        browser.close()


# Tests for checking slider. Parametrizing the test to cover edge cases and middle points
@pytest.mark.testcase_id("TC007")
@pytest.mark.password_generator
@pytest.mark.password_length_slider
@pytest.mark.regression
@pytest.mark.parametrize("password_length, step", [
    (7, 1), (12, 6), (18, 12), (24, 18), (32, 26)
])

def test_password_length_slider_moving_right(password_length, step):

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")
        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        # Locate the password length slider and the password field
        slider = page.locator('input[type="range"]')

        current_slider_value = page.locator('input#passwordLengthRange').input_value()

        for i in range (step):
            slider.press("ArrowRight")

        new_slider_value = page.locator('input#passwordLengthRange').input_value()

        # Verify that the displayed password length matches the expected value
        assert int(new_slider_value) == password_length, f"Expected slider length to be {password_length}, but got {new_slider_value}"

        # Read the generated password and verify its length
        password_field = page.locator('input[name="password"]')
        password = password_field.input_value()

        assert len(password) == password_length, f"Expected password length to be {password_length}, but got {len(password)}"

        browser.close()


# Tests for checking slider. Parametrizing the test to cover edge cases and middle points
@pytest.mark.testcase_id("TC008")
@pytest.mark.parametrize("password_length, step", [
    (31, 1), (23, 9), (18, 14), (10, 22), (6, 26)
])
@pytest.mark.password_generator
@pytest.mark.password_length_slider
@pytest.mark.regression
def test_password_length_slider_moving_left(password_length, step):

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")
        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        # Setting start point to maximum length - 32 as by default page is opened with length 6
        length_input = page.locator('input[name="passwordLength"]')
        length_input.fill("32")

        # Locate the password length slider and the password field
        slider = page.locator('input[type="range"]')

        current_slider_value = page.locator('input#passwordLengthRange').input_value()

        for i in range (step):
            slider.press("ArrowLeft")

        new_slider_value = page.locator('input#passwordLengthRange').input_value()

        # Verify that the displayed password length matches the expected value
        assert int(new_slider_value) == password_length, f"Expected password length to be {password_length}, but got {new_slider_value}"

        # Read the generated password and verify its length
        password_field = page.locator('input[name="password"]')
        password = password_field.input_value()

        assert len(password) == password_length, f"Expected password length to be {password_length}, but got {len(password)}"

        browser.close()


# Tests for arrows for setting up password length. Parametrizing the test to cover edge cases and middle points
@pytest.mark.testcase_id("TC009")
@pytest.mark.parametrize("password_length, step", [
    (7, 1), (12, 6), (18, 12), (24, 18), (32, 26)
])
@pytest.mark.password_generator
@pytest.mark.password_length_arrows
@pytest.mark.regression
def test_password_length_arrow_up(password_length, step):

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")
        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        # Locate the password length slider and the password field
        slider = page.locator('input[type="range"]')

        current_slider_value = page.locator('input#passwordLengthRange').input_value()

        for i in range (step):
            slider.press("ArrowUp")

        new_slider_value = page.locator('input#passwordLengthRange').input_value()

        # Verify that the displayed password length matches the expected value
        assert int(new_slider_value) == password_length, f"Expected slider length to be {password_length}, but got {new_slider_value}"

        # Read the generated password and verify its length
        password_field = page.locator('input[name="password"]')
        password = password_field.input_value()

        assert len(password) == password_length, f"Expected password length to be {password_length}, but got {len(password)}"

        browser.close()


# Tests for arrows for setting up password length. Parametrizing the test to cover edge cases and middle points
@pytest.mark.testcase_id("TC010")
@pytest.mark.parametrize("password_length, step", [
    (31, 1), (23, 9), (18, 14), (10, 22), (6, 26)
])
@pytest.mark.password_generator
@pytest.mark.password_length_slider
@pytest.mark.regression
def test_password_length_arrow_down(password_length, step):

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")
        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        # Setting start point to maximum length - 32 as by default page is opened with length 6
        length_input = page.locator('input[name="passwordLength"]')
        length_input.fill("32")

        # Locate the password length slider and the password field
        slider = page.locator('input[type="range"]')

        current_slider_value = page.locator('input#passwordLengthRange').input_value()

        for i in range (step):
            slider.press("ArrowDown")

        new_slider_value = page.locator('input#passwordLengthRange').input_value()

        # Verify that the displayed password length matches the expected value
        assert int(new_slider_value) == password_length, f"Expected password length to be {password_length}, but got {new_slider_value}"

        # Read the generated password and verify its length
        password_field = page.locator('input[name="password"]')
        password = password_field.input_value()

        assert len(password) == password_length, f"Expected password length to be {password_length}, but got {len(password)}"

        browser.close()


# This button is used for regenerating password
@pytest.mark.testcase_id("TC011")
@pytest.mark.password_generator
@pytest.mark.generate_password_button
@pytest.mark.regression
def test_password_generator_generate_password_button():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")

        # Basic smoke check
        assert "Random Password Generator" in page.title(), "Page failed to load."

        old_password = page.locator('input[name="password"]').input_value()

        # Check that Generate password is visible
        generate_button = page.locator('button[type="button"][title="Generate password"]')
        assert generate_button.is_visible(), "Generate password not visible."

        # Regenerate password
        generate_button.click()

        new_password = page.locator('input[name="password"]').input_value()

        # Check that the password is changed
        assert not new_password == old_password, "New password wasn't generated."

        browser.close()


@pytest.mark.testcase_id("TC012")
@pytest.mark.password_generator
@pytest.mark.copy_button_password
@pytest.mark.regression
def test_copy_small_icon_button_copies_password_to_clipboard():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")

        # Wait until the password field is populated with a generated password
        page.wait_for_function("document.querySelector('input#password').value !== ''")

        # Retrieve the generated password
        password_field = page.locator('input[id="password"]')
        password = password_field.input_value()

        # Click the copy button next to the password field
        copy_button = page.locator('button:has-text("Copy")')
        copy_button.click()

        # Wait a moment to ensure the password is copied to the clipboard
        page.wait_for_timeout(500)  # 500 milliseconds

        # Retrieve clipboard content and verify it matches the password
        clipboard_content = page.evaluate("navigator.clipboard.readText()")
        assert clipboard_content == password, f"Expected clipboard to contain '{password}', but got '{clipboard_content}'"

        browser.close()


@pytest.mark.testcase_id("TC013")
@pytest.mark.password_generator
@pytest.mark.copy_password_button
@pytest.mark.regression
def test_copy_password_main_button_copies_password_to_clipboard():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Navigate to the password generator page
        page.goto("https://www.security.org/password-generator/")

        # Wait until the password field is populated with a generated password
        page.wait_for_function("document.querySelector('input#password').value !== ''")

        # Retrieve the generated password
        password_field = page.locator('input[id="password"]')
        password = password_field.input_value()

        # Click the "Copy Password" button
        copy_password_button = page.locator('button[type="button"][title="Copy password"]')
        copy_password_button.click()

        # Wait for clipboard to update
        page.wait_for_timeout(1000)  # 1 second wait to ensure clipboard is updated

        # Retrieve clipboard content and verify it matches the password
        clipboard_content = page.evaluate("async () => await navigator.clipboard.readText()")
        assert clipboard_content == password, f"Expected clipboard to contain '{password}', but got '{clipboard_content}'"

        # Close the browser
        browser.close()
