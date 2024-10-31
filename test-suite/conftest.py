import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright):
    browser = playwright.chromium.launch()
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
    page = context.new_page()
    page.goto("https://www.security.org/password-generator/")
    yield page


@pytest.fixture
def password_elements(page):
    return {
        "password_field": page.locator('input[name="password"]'),
        "length_input": page.locator('input[name="passwordLength"]'),
        "lowercase_checkbox": page.locator('label[for="option-lowercase"]'),
        "uppercase_checkbox": page.locator('label[for="option-uppercase"]'),
        "numbers_checkbox": page.locator('label[for="option-numbers"]'),
        "symbols_checkbox": page.locator('label[for="option-symbols"]'),
        "generate_button": page.locator(
            'button[type="button"][title="Generate password"]'
        ),
    }
