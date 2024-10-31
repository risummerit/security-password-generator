import allure
import pytest
from playwright.sync_api import expect


@allure.title("Password Generator")
@allure.description("Invalid input tests for the length field")
@allure.testcase("TC003")
@pytest.mark.password_generator
@pytest.mark.regression
@pytest.mark.parametrize("invalid_length, expected_length", [
    ("5", "6"),   # Below minimum length
    ("33", "32"), # Above maximum length
    ("abc", "6"), # Non-numeric input defaults to minimum length
])
def test_negative_invalid_length_input(invalid_length, expected_length, page, password_elements):
    # Setting invalid password length
    expect(password_elements["length_input"]).to_be_visible(timeout=5000)
    try:
        password_elements["length_input"].fill(invalid_length)
    except:
        # Handling if non-numeric input raises an error by setting a valid default
        password_elements["length_input"].fill("6")
    # Generating a new password and validate length
    old_password = password_elements["password_field"].input_value()
    password_elements["generate_button"].click()
    page.wait_for_function("document.querySelector('input[name=\"password\"]').value !== ''", timeout=5000)
    new_password = password_elements["password_field"].input_value()
    assert old_password != new_password, "New password wasn't generated."
    assert str(len(new_password)) == expected_length, f"Expected length {expected_length}, but got {len(new_password)}."


@allure.title("Password Generator")
@allure.description("Ensure at least one checkbox remains selected")
@allure.testcase("TC006")
@pytest.mark.password_generator
@pytest.mark.regression
@pytest.mark.password_options_combinations_with_checkboxes
def test_last_checkbox_remains_checked(page, password_elements):
    # Locating all character checkboxes
    checkboxes = {
        "lowercase": page.locator('input#option-lowercase'),
        "uppercase": page.locator('input#option-uppercase'),
        "numbers": page.locator('input#option-numbers'),
        "symbols": page.locator('input#option-symbols')
    }

    # Uncheck all but one checkbox and verify each time
    selected_checkboxes = [name for name, checkbox in checkboxes.items() if checkbox.is_checked()]

    # Attempt to uncheck all but the last remaining checkbox
    for checkbox_name in selected_checkboxes[:-1]:  # Leave the last one checked
        password_elements[f"{checkbox_name}_checkbox"].click()
        assert not checkboxes[checkbox_name].is_checked(), f"{checkbox_name.capitalize()} checkbox should be unchecked."

    # Try to uncheck the last remaining checkbox and confirm it stays checked
    last_checkbox_name = selected_checkboxes[-1]
    password_elements[f"{last_checkbox_name}_checkbox"].click()
    assert checkboxes[last_checkbox_name].is_checked(), f"{last_checkbox_name.capitalize()} checkbox should remain checked as the only selected option."
