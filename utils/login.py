import time

from playwright.sync_api import sync_playwright
from Shinomiya.Src.logger import *

def get_cloud_session(token, passwd):
    _playwright = sync_playwright().start()
    with _playwright.chromium.launch(headless=True) as browser:
        with browser.new_context() as context:
            page = context.new_page()
            url = f"https://cloud.tsinghua.edu.cn/u/d/{token}/"
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.locator("[id='password']").type(passwd)
            page.keyboard.press('Enter')
            time.sleep(3)
            page.goto(url)
            page.wait_for_load_state("networkidle")
            cookies = []
            csrf_token = None
            for cookie in context.cookies(url):
                if cookie['name'] == 'sfcsrftoken':
                    csrf_token = cookie['value']
                cookies.append(f"{cookie['name']}={cookie['value']}")
            cookies = '; '.join(cookies)
            return cookies, csrf_token
