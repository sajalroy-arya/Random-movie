from __future__ import annotations

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def _build_driver(user_data_dir: str, profile_dir: str) -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_argument("--start-maximized")

    service = webdriver.ChromeService(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def post_to_linkedin(
    post_text: str,
    user_data_dir: str,
    profile_dir: str,
    dry_run: bool = False,
) -> None:
    driver = _build_driver(user_data_dir=user_data_dir, profile_dir=profile_dir)
    wait = WebDriverWait(driver, 25)

    try:
        driver.get("https://www.linkedin.com/feed/")

        start_post = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@aria-label,'Start a post') or contains(.,'Start a post')]",
                )
            )
        )
        start_post.click()

        editor = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor"))
        )
        editor.click()
        editor.send_keys(post_text)

        if dry_run:
            return

        post_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@aria-label,'Post') or .//span[text()='Post'] or text()='Post']",
                )
            )
        )
        post_button.click()

        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Post successful')]")),
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Post']")),
            )
        )
    except TimeoutException as exc:
        raise RuntimeError(
            "LinkedIn elements were not found in time. The page layout may have changed or login is required."
        ) from exc
    finally:
        driver.quit()
