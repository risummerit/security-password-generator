import allure
import pytest
from playwright.sync_api import expect


@allure.title("Password Generator")
@allure.description("Smoke Test")
@allure.testcase("TC001")
@pytest.mark.smoke
@pytest.mark.password_generator
@pytest.mark.regression
def test_password_generator_smoke_test(page, password_elements):
    expect(password_elements["password_field"]).to_be_visible(timeout=5000)
    assert "Random Password Generator" in page.title(), "Page failed to load."


@allure.title("Password Generator")
@allure.description("Password Length Input and Generated Password Length")
@allure.testcase("TC002")
@pytest.mark.parametrize("password_length", ["6", "12", "18", "24", "32"])
@pytest.mark.password_generator
@pytest.mark.password_length_input_field
@pytest.mark.regression
def test_password_length_input_and_generated_password_length(
    password_length, page, password_elements
):
    expect(password_elements["length_input"]).to_be_visible(timeout=5000)
    password_elements["length_input"].fill(password_length)

    password = password_elements["password_field"].input_value()
    assert password, "Password field should have a generated value"
    assert len(password) == int(
        password_length
    ), f"Expected password length {password_length}, but got {len(password)}"


@allure.title("Password Generator")
@allure.description("Default Checkbox Setup and Password Content")
@allure.testcase("TC004")
@pytest.mark.password_generator
@pytest.mark.password_options_combinations_with_checkboxes
@pytest.mark.regression
def test_checkboxes_password_options_default_setup(page, password_elements):
    # Verifying visibility of checkboxes
    expect(password_elements["lowercase_checkbox"]).to_be_visible(timeout=5000)
    expect(password_elements["uppercase_checkbox"]).to_be_visible(timeout=5000)
    expect(password_elements["numbers_checkbox"]).to_be_visible(timeout=5000)
    expect(password_elements["symbols_checkbox"]).to_be_visible(timeout=5000)

    # Verifying default state of checkboxes
    expect(password_elements["lowercase_checkbox"]).to_be_checked()
    expect(password_elements["uppercase_checkbox"]).to_be_checked()
    expect(password_elements["numbers_checkbox"]).not_to_be_checked()
    expect(password_elements["symbols_checkbox"]).not_to_be_checked()

    # Verifying default generated password content
    password = password_elements["password_field"].input_value()
    assert password, "Password field should have a generated value by default"
    assert any(
        char.islower() for char in password
    ), "Password should contain lowercase letters by default."
    assert any(
        char.isupper() for char in password
    ), "Password should contain uppercase letters by default."
    assert not any(
        char.isdigit() for char in password
    ), "Password should not contain numbers by default."
    assert not any(
        not char.isalnum() for char in password
    ), "Password should not contain symbols by default."
    assert len(password) == 6, "Default password length should be 6."


checkbox_combinations = [
    (True, False, False, False),  # Only Lowercase
    (False, True, False, False),  # Only Uppercase
    (False, False, True, False),  # Only Numbers
    (False, False, False, True),  # Only Symbols
    (True, True, False, False),  # Lowercase + Uppercase
    (True, False, True, False),  # Lowercase + Numbers
    (True, False, False, True),  # Lowercase + Symbols
    (False, True, True, False),  # Uppercase + Numbers
    (False, True, False, True),  # Uppercase + Symbols
    (False, False, True, True),  # Numbers + Symbols
    (True, True, True, False),  # Lowercase + Uppercase + Numbers
    (True, True, False, True),  # Lowercase + Uppercase + Symbols
    (True, False, True, True),  # Lowercase + Numbers + Symbols
    (False, True, True, True),  # Uppercase + Numbers + Symbols
    (True, True, True, True),  # All selected
]


@allure.title("Password Generator")
@allure.description("Checkbox Combinations for Password Content")
@allure.testcase("TC005")
@pytest.mark.parametrize(
    "lowercase, uppercase, numbers, symbols", checkbox_combinations
)
@pytest.mark.password_generator
@pytest.mark.password_options_combinations_with_checkboxes
@pytest.mark.regression
def test_checkboxes_generated_password_combinations(
    lowercase, uppercase, numbers, symbols, page, password_elements
):
    # Setting initial state: Lowercase checked, Uppercase unchecked, Numbers and Symbols unchecked
    if not page.locator("input#option-lowercase").is_checked():
        password_elements["lowercase_checkbox"].click()
    elif not page.locator("input#option-uppercase").is_checked():
        password_elements["uppercase_checkbox"].click()
    if not page.locator("input#option-numbers").is_checked():
        password_elements["numbers_checkbox"].click()
    if not page.locator("input#option-symbols").is_checked():
        password_elements["symbols_checkbox"].click()

    # Adjusting checkboxes based on the test parameters
    if lowercase:
        if not page.locator("input#option-lowercase").is_checked():
            password_elements["lowercase_checkbox"].click()
    else:
        if page.locator("input#option-lowercase").is_checked():
            password_elements["lowercase_checkbox"].click()

    if uppercase:
        if not page.locator("input#option-uppercase").is_checked():
            password_elements["uppercase_checkbox"].click()
    else:
        if page.locator("input#option-uppercase").is_checked():
            password_elements["uppercase_checkbox"].click()

    if numbers:
        if not page.locator("input#option-numbers").is_checked():
            password_elements["numbers_checkbox"].click()
    else:
        if page.locator("input#option-numbers").is_checked():
            password_elements["numbers_checkbox"].click()

    if symbols:
        if not page.locator("input#option-symbols").is_checked():
            password_elements["symbols_checkbox"].click()
    else:
        if page.locator("input#option-symbols").is_checked():
            password_elements["symbols_checkbox"].click()

    # Reading the updated password
    password = page.locator('input[name="password"]').input_value()

    # Assertions based on checkbox settings
    if lowercase:
        assert any(
            char.islower() for char in password
        ), "Password should contain lowercase letters."
    else:
        assert not any(
            char.islower() for char in password
        ), "Password should not contain lowercase letters."

    if uppercase:
        assert any(
            char.isupper() for char in password
        ), "Password should contain uppercase letters."
    else:
        assert not any(
            char.isupper() for char in password
        ), "Password should not contain uppercase letters."

    if numbers:
        assert any(
            char.isdigit() for char in password
        ), "Password should contain numbers."
    else:
        assert not any(
            char.isdigit() for char in password
        ), "Password should not contain numbers."

    if symbols:
        assert any(
            not char.isalnum() for char in password
        ), "Password should contain symbols."
    else:
        assert not any(
            not char.isalnum() for char in password
        ), "Password should not contain symbols."


@allure.title("Password Generator")
@allure.description("Slider Moving Right for Length")
@allure.testcase("TC007")
@pytest.mark.parametrize(
    "password_length, step", [(7, 1), (12, 6), (18, 12), (24, 18), (32, 26)]
)
@pytest.mark.password_generator
@pytest.mark.password_length_slider
@pytest.mark.regression
def test_password_length_slider_moving_right(
    password_length, step, page, password_elements
):
    slider = page.locator('input[type="range"]')
    for _ in range(step):
        slider.press("ArrowRight")
    password = password_elements["password_field"].input_value()
    assert password, "Password field should have a generated value"
    assert (
        len(password) == password_length
    ), f"Expected {password_length}, got {len(password)}"


@allure.title("Password Generator")
@allure.description("Generate Password Button Test")
@allure.testcase("TC011")
@pytest.mark.password_generator
@pytest.mark.generate_password_button
@pytest.mark.regression
def test_password_generator_generate_password_button(page, password_elements):
    old_password = password_elements["password_field"].input_value()
    password_elements["generate_button"].click()
    new_password = password_elements["password_field"].input_value()
    assert old_password != new_password, "New password not generated."


@allure.title("Password Generator")
@allure.description("Copy Password Button Test")
@allure.testcase("TC013")
@pytest.mark.password_generator
@pytest.mark.copy_password_button
@pytest.mark.regression
def test_copy_password_main_button_copies_password_to_clipboard(
    page, password_elements
):
    # Waiting until the password field is populated with a generated password
    page.wait_for_function("document.querySelector('input#password').value !== ''")
    # Retrieving the generated password
    password_field = page.locator('input[id="password"]')
    password = password_field.input_value()
    copy_password_button = page.locator('button[type="button"][title="Copy password"]')
    copy_password_button.click()
    page.wait_for_timeout(1000)  # 1 second wait to ensure clipboard is updated
    # Retrieving clipboard content and verify it matches the password
    clipboard_content = page.evaluate(
        "async () => await navigator.clipboard.readText()"
    )
    assert (
        clipboard_content == password
    ), f"Expected clipboard to contain '{password}', but got '{clipboard_content}'"
