# pip install playwright
# playwright install

from playwright.sync_api import sync_playwright, Playwright
import time
import re

URL = "https://www.bettingpros.com/nba/props/deni-avdija/points/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)

    # make sure a table exists
    page.wait_for_selector("td[class*='table-cell--line']")

    # find specific table of historical odds, then find the odds column
    log_table = page.locator("section.player-game-log-card")
    prop_lines = log_table.locator("td[class*='table-cell--line']")

    # loop thru each line cell
    for i in range(prop_lines.count()):
        text = prop_lines.nth(i).inner_text().strip()
        print(text)

    # open dropdown menu and scrape last season
    page.click("#player-game-log-season-dropdown")
    page.locator("li#player-game-log-season-dropdown-opt-1").click()

    # Pause program to let page load, maybe find better way to wait?
    time.sleep(5)

    # find specific table of historical odds, then find the odds column in 2024 season
    log_table = page.locator("section.player-game-log-card")
    prop_lines = log_table.locator("td[class*='table-cell--line']")

    # loop thru each line cell
    for i in range(prop_lines.count()):
        text = prop_lines.nth(i).inner_text().strip()
        print(text)

    browser.close()
