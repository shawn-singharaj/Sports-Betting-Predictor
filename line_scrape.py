from playwright.sync_api import sync_playwright, Playwright
import re

URL = "https://www.bettingpros.com/nba/props/deni-avdija/points/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)

    page.wait_for_selector("td[class*='table-cell--line']")

    log_table = page.locator("section.player-game-log-card")
    prop_lines = log_table.locator("td[class*='table-cell--line']")

    # loop thru each line cell
    for i in range(prop_lines.count()):
        text = prop_lines.nth(i).inner_text().strip()
        print(text)

    browser.close()
