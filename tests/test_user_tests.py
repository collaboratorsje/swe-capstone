#from playwright.async_api import Page, expect
#import asyncio
#import pytest
from playwright.sync_api import Page, expect
import re

def test_unlogged_access_applications(page: Page):
    page.goto('http://localhost:5000/applications')
    expect(page).to_have_url(re.compile("login"))

def test_unlogged_access_admin(page: Page):
    page.goto('http://localhost:5000/admin')
    expect(page).to_have_url(re.compile("login"))

def test_unlogged_access_profile(page: Page):
    page.goto('http://localhost:5000/profile')
    expect(page).to_have_url(re.compile("login"))

def test_unlogged_access_register(page: Page):
    page.goto('http://localhost:5000/register')
    expect(page).to_have_url(re.compile("register"))

def test_unlogged_access_apply(page: Page):
    page.goto('http://localhost:5000/apply/1')
    expect(page).to_have_url(re.compile("login"))

def test_unlogged_access_login(page: Page):
    page.goto('http://localhost:5000/login')
    expect(page).to_have_url(re.compile("login"))

def test_login(page: Page):
    page.goto('http://localhost:5000/login')
    page.locator('input[name="user_email"]').fill("test@test.com")
    page.locator('input[name="user_pass"]').fill("test")
    page.get_by_role('button', name='Submit').click()
    expect(page)#.to_have_title("http://localhost:5000")
"""
def test_user_access_applications(page: Page):
    page.goto('http://localhost:5000/applications')
    expect(page).to_have_url(re.compile("login"))

def test_user_access_admin(page: Page):
    page.goto('http://localhost:5000/admin')
    expect(page).to_have_url(re.compile("login"))

def test_user_access_profile(page: Page):
    page.goto('http://localhost:5000/profile')
    expect(page).to_have_url(re.compile("login"))

def test_user_access_register(page: Page):
    page.goto('http://localhost:5000/register')
    expect(page).to_have_url(re.compile("register"))

def test_user_access_apply(page: Page):
    page.goto('http://localhost:5000/apply/1')
    expect(page).to_have_url(re.compile("login"))

def test_user_access_login(page: Page):
    page.goto('http://localhost:5000/login')
    expect(page).to_have_url(re.compile("login"))
"""
#pytest_plugins = ('pytest_asyncio_cooperative')

#@pytest.mark.asyncio_cooperative
#async def test_unlogged_access(page: Page):
#    await page.goto('http://localhost:5000/applications')
    #await expect(page.goto("http://localhost:5000/applications")).to_have_title(re.compile("login"))
    #print(page)
    #print(page.title)
    #expect(page.title == "Login")