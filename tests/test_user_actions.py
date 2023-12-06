from playwright.sync_api import Page, expect
import re
from test_util import login, click_login, click_register, delete_test_user

base = "http://localhost:5000"
apps = base+'/applications'
admin = base+'/admin'
lin = base+'/login'
reg = base+'/register'
prof = base+'/profile'

# 2.2
def test_unlogged_click_login(page: Page):
    click_login(page)
    expect(page).to_have_url(base+'/')

# 2.1
def test_unlogged_click_register(page: Page):
    click_register(page)
    expect(page).to_have_url(lin)
    delete_test_user()

# 2.1
def test_unlogged_click_register_login(page: Page):
    click_register(page)
    click_login(page, user="testtest@test.com")
    expect(page).to_have_url(base+'/')
    delete_test_user()

# 2.3
def test_logged_click_logout(page:Page):
    login(page)
    page.locator('li[name="nav-logout"]').click()
    expect(page).to_have_url(base+'/')

# 2.1
#def test_logged_click_register_ucourses(page: Page):
# 6.1
def test_logged_click_apply_nocert(page: Page):
    login(page)
    page.goto(base)
    page.locator('a[class="btn apply-btn"]').all()[1].click()
    with page.expect_file_chooser() as fc:
        page.locator('input[name="transcript"]').click()
    transcript_choice = fc.value
    transcript_choice.set_files("testing-requirements.txt")
    page.get_by_role('button', name='submit').click()
    expect(page).to_have_url(base+'/')

"""
# 5.1
def test_filter_course(page: Page):

# 5.2 
def test_filter_position(page: Page):

# 5.3 
def test_filter_cert(page: Page):

# 5.4 
def test_filter_search(page: Page):

# 5.5 
def test_filter_combined(page: Page)
"""

# 6.2
def test_logged_click_apply_cert(page: Page):
    login(page)
    page.goto(base)
    page.locator('a[class="btn apply-btn"]').all()[0].click()
    with page.expect_file_chooser() as fc:
        page.locator('input[name="transcript"]').click()
    transcript_choice = fc.value
    transcript_choice.set_files("testing-requirements.txt")
    page.locator('input[name="toggleGtaCert"]').click()
    with page.expect_file_chooser() as fc:
        page.locator('input[name="gta_cert"]').click()
    gta_choice = fc.value
    gta_choice.set_files("testing-requirements.txt")
    page.get_by_role('button', name='submit').click()
    expect(page).to_have_url(base+'/')

# 6.3
#def test_logged_click_edit_app(page: Page):

# 6.4
# def test_logged_click_edit_profile(page: Page):

"""
# 7.1
def test_logged_click_edit_app(page: Page):

# 7.2
def test_admin_click_edit_job(page: Page):

# 7.3
def test_admin_click_remove_job(page: Page):

# 7.4
def test_admin_click_accept_app(page: Page):

# 7.5
def test_admin_click_reject_app(page: Page):

# 7.6
def test_admin_click_create_job(page: Page):
"""