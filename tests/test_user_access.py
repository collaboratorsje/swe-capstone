#from playwright.async_api import Page, expect
#import asyncio
#import pytest
from playwright.sync_api import Page, expect
import re

base = "http://localhost:5000"
apps = base+'/applications'
admin = base+'/admin'
lin = base+'/login'
reg = base+'/register'
prof = base+'/profile'

def login(page: Page, user="testuc@test.com", pa="test"):
    page.goto(lin)
    page.locator('input[name="user_email"]').fill(user)
    page.locator('input[name="user_pass"]').fill(pa)
    page.get_by_role('button', name='Submit').click()

# 1.1
def test_unlogged_access_applications(page: Page):
    page.goto(apps)
    expect(page).to_have_url(re.compile("login"))
# 1.2
def test_unlogged_access_admin(page: Page):
    page.goto(base+'/admin')
    expect(page).to_have_url(re.compile("login"))
# 1.3
def test_unlogged_access_profile(page: Page):
    page.goto(prof)
    expect(page).to_have_url(re.compile("login"))
# 1.4
def test_unlogged_access_register(page: Page):
    page.goto(reg)
    expect(page).to_have_url(re.compile("register"))
# 1.5
def test_unlogged_access_apply(page: Page):
    page.goto('http://localhost:5000/apply/1')
    expect(page).to_have_url(re.compile("login"))
# 1.6
def test_unlogged_access_login(page: Page):
    page.goto(lin)
    expect(page).to_have_url(re.compile("login"))
# 2.2
def test_login(page: Page):
    login(page)
    expect(page).to_have_url(base+'/')
# 3.1
def test_user_access_applications(page: Page):
    login(page)
    page.goto(apps)
    expect(page).to_have_url(apps)
# 3.2
def test_user_access_admin(page: Page):
    login(page)
    page.goto(admin)
    expect(page).to_have_url(re.compile("login"))
# 3.3
def test_user_access_profile(page: Page):
    login(page)
    page.goto(prof)
    expect(page).to_have_url(prof)
# 3.4
def test_user_access_register(page: Page):
    login(page)
    page.goto(reg)
    expect(page).to_have_url(reg)
# 3.5
def test_user_access_apply(page: Page):
    login(page)
    page.goto('http://localhost:5000/apply/1')
    expect(page).to_have_url(re.compile("apply"))
# 3.6
def test_user_access_login(page: Page):
    login(page)    
    page.goto(lin)
    expect(page).to_have_url(re.compile("login"))
# 4.1
def test_admin_access_applications(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(apps)
    expect(page).to_have_url(apps)
# 4.2
def test_admin_access_admin(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    expect(page).to_have_url(admin)
# 4.3
def test_admin_access_profile(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(prof)
    expect(page).to_have_url(prof)
# 4.4
def test_admin_access_register(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(reg)
    expect(page).to_have_url(reg)
# 4.5
def test_admin_access_apply(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto('http://localhost:5000/apply/1')
    expect(page).to_have_url(re.compile("apply"))
# 4.6
def test_admin_access_login(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(lin)
    expect(page).to_have_url(re.compile("login"))
#pytest_plugins = ('pytest_asyncio_cooperative')

#@pytest.mark.asyncio_cooperative
#async def test_unlogged_access(page: Page):
#    await page.goto('http://localhost:5000/applications')
    #await expect(page.goto("http://localhost:5000/applications")).to_have_title(re.compile("login"))
    #print(page)
    #print(page.title)
    #expect(page.title == "Login")