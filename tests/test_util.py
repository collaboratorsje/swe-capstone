from playwright.sync_api import Page, expect

base = "http://localhost:5000"
lin = base+'/login'

def login(page: Page, user="testuc@test.com", pa="test"):
    page.goto(lin)
    page.locator('input[name="user_email"]').fill(user)
    page.locator('input[name="user_pass"]').fill(pa)
    page.get_by_role('button', name='Submit').click()