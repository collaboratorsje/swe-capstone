from playwright.sync_api import Page, expect
import re
from test_util import login, click_login, click_register, delete_test_user, handle_dialog
import time

base = "http://localhost:5000"
apps = base+'/applications'
admin = base+'/admin'
lin = base+'/login'
reg = base+'/register'
prof = base+'/profile'

# 2.2
def test_unlogged_click_login(page: Page):
    click_login(page)
    page.wait_for_load_state()
    navs = page.locator('a[class="nav-item nav-link"]').all()[1]
    expect(page).to_have_url(base+'/')
    expect(navs).to_have_attribute('href', '/profile')

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
    navs = page.locator('a[class="nav-item nav-link"]').all()[1]
    expect(page).to_have_url(base+'/')
    expect(navs).to_have_attribute('href', '/profile')
    delete_test_user()

# 2.3
def test_logged_click_logout(page:Page):
    login(page)
    page.locator('li[name="nav-logout"]').click()
    page.wait_for_load_state()
    navs = page.locator('a[class="nav-item nav-link"]').all()[0]
    expect(page).to_have_url(base+'/')
    expect(navs).to_have_attribute('href', '/login')

# 2.1
def test_logged_click_register_ucourses(page: Page):
    click_register(page, courses=True)
    page.wait_for_load_state()
    click_login(page, user="testtest@test.com")
    page.wait_for_load_state()
    navs = page.locator('a[class="nav-item nav-link"]').all()[1]
    expect(page).to_have_url(base+'/')
    expect(navs).to_have_attribute('href', '/profile')
    delete_test_user()

# 5.1
def test_filter_course(page: Page):
    page.goto(base)
    page.select_option('select#course-filter', 'CS 201R - Problem Solving and Programming II')
    page.wait_for_load_state()
    time.sleep(0.5)
    listings = page.locator('li[class="list-group-item"]').all()
    for l in listings:
        i = l.locator('h5')
        print(i.text_content())
        if i.text_content().endswith("Grader"):
            expect(i).to_have_text("CS 201R - Problem Solving and Programming II Grader")
        elif i.text_content().endswith("Instructor"):
            expect(i).to_have_text("CS 201R - Problem Solving and Programming II Lab Instructor")

# 5.2 
def test_filter_position(page: Page):
    page.goto(base)
    page.select_option('select#role-filter', 'Grader')
    page.wait_for_load_state()
    time.sleep(0.5)
    listings = page.locator('li[class="list-group-item"]').all()
    for l in listings:
        i = l.locator('h5')
        expect(i).to_have_text(re.compile(r"Grader"))

# 5.3 
def test_filter_cert(page: Page):
    page.goto(base)
    page.selector('input[id="cert-filter"]').check()
    # check for non-cert jobs listed

# 5.4 
def test_filter_search(page: Page):
    page.goto(base)
    page.selector('input[id="query"]').fill('CS 201R')
    page.selector('button[id=""]').click()
    # check for non CS 201R jobs

# 5.5 
def test_filter_combined(page: Page):
    page.goto(base)
    page.select_option('select#course-filter', 'CS 201R - Problem Solving and Programming II')
    page.select_option('select#role-filter', 'Grader')
    page.selector('input[id="query"]').fill('CS 201R')
    page.selector('button[id=""]').click()
    # check for non CS 201R jobs

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
    # check for app in my applications

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
    # check for app in my applications

# 6.3
#def test_logged_click_edit_app(page: Page):

# 6.4
def test_logged_click_edit_profile(page: Page):
    login(page)
    page.goto(prof)
    page.locator('input[id="user_gpa"]').fill("3.75")
    page.get_by_role('button', name="submit").click()
    expect(page.locator('div[id="u-gpa"]')).to_have_text("3.75")
    page.locator('input[id="user_gpa"]').fill("3.87")
    page.get_by_role('button', name="submit").click()

# 7.1
def test_admin_click_edit_app(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('button[id="job-oc"]').click()
    # check if job is open

# 7.2
def test_admin_click_edit_job(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('button[id="job-edit"]').click()
    # Make some edit
    # Save edit
    # check job edited

# 7.3
def test_admin_click_remove_job(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('button[id="job-remove"]').click()
    page.on("dialog", handle_dialog)
    # check job is removed

# 7.4
def test_admin_click_accept_app(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('a[id="applicationsButton"]').click()
    page.locator('button[id="app-acc"]').click()
    # check if app is accepted

# 7.5
def test_admin_click_reject_app(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('a[id="applicationsButton"]').click()
    page.locator('button[id="app-rej"]').click()
    # check if app is rejected
# 7.6
def test_admin_click_create_job(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('a[id="create-job"]').click()
    page.select_option('select#role', 'Grader')
    page.select_option('select#course_required', 'CS 101 - Problem Solving and Programming I')
    page.get_by_role('button', 'submit').click()
    page.wait_for_load_state()
    #page.locator()
    # check if job present
