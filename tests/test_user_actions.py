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
    
    expect(page).to_have_url(base+'/')
    expect(page.locator('a[class="nav-item nav-link"]').all()[1]).to_have_attribute('href', '/profile')

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
    expect(page.locator('a[class="nav-item nav-link"]').all()[1]).to_have_attribute('href', '/profile')
    delete_test_user()

# 2.3
def test_logged_click_logout(page:Page):
    login(page)
    page.locator('li[name="nav-logout"]').click()
    page.wait_for_load_state()
    expect(page).to_have_url(base+'/')
    expect(page.locator('a[class="nav-item nav-link"]').all()[0]).to_have_attribute('href', '/login')

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
def test_filter_position(page: Page, option = 'Grader'):
    page.goto(base)
    page.select_option('select#role-filter', option)
    page.wait_for_load_state()
    time.sleep(1)
    [expect(x).to_have_text(re.compile(option)) for x in page.locator('h5[id="job-name"]').all()]


# 5.3 
def test_filter_cert(page: Page):
    page.goto(base)
    page.locator('input[id="cert-filter"]').check()
    page.wait_for_load_state()
    time.sleep(1)
    [expect(x).to_have_text("Certification Required") for x in page.locator('p[id="cert-req"]').all()]

# 5.4 
def test_filter_search(page: Page, q = 'CS 201R'):
    page.goto(base)
    page.locator('input[id="query"]').fill(q)
    page.locator('button[id="search-submit"]').click()
    page.wait_for_load_state()
    time.sleep(1)
    [expect(x).to_have_text(re.compile(q)) for x in page.locator('h5[id="job-name"]').all()]

# 5.5 
def test_filter_combined(page: Page, option = 'Grader', q = 'CS 201R'):
    page.goto(base)
    page.select_option('select#course-filter', 'CS 201R - Problem Solving and Programming II')
    page.select_option('select#role-filter', option)
    page.locator('input[id="query"]').fill(q)
    page.locator('button[id="search-submit"]').click()
    [expect(x).to_have_text(re.compile(option)) for x in page.locator('h5[id="job-name"]').all()]
    [expect(x).to_have_text("Certification Required") for x in page.locator('p[id="cert-req"]').all()]
    [expect(x).to_have_text(re.compile(q)) for x in page.locator('h5[id="job-name"]').all()]

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
    page.goto(apps)
    expect(page.locator('li[class="list-group-item"]').all()[-1]).to_have_text(re.compile("CS 191 - Discrete Structures I"))

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
    page.goto(apps)
    expect(page.locator('li[class="list-group-item"]').all()[-1]).to_have_text(re.compile("CS 201R - Problem Solving and Programming II"))

# 6.3
def test_logged_click_edit_app(page: Page):
    login(page)
    page.goto(apps)
    page.wait_for_load_state()
    page.locator('a[id="app-edit"]').all()[0].click()
    page.wait_for_load_state()
    with page.expect_file_chooser() as fc:
        page.locator('input[id="transcript"]').click()
    t_choice = fc.value
    t_choice.set_files("testing-requirements.txt")
    with page.expect_file_chooser() as fc:
        page.locator('input[id="gta_cert"]').click()
    g_choice = fc.value
    g_choice.set_files("testing-requirements.txt")
    page.get_by_role('button', name='submit')
    page.wait_for_load_state()
    expect(page).to_have_url(base+'/')

# 6.4
def test_logged_click_edit_profile(page: Page):
    login(page)
    page.goto(prof)
    page.locator('input[id="user_gpa"]').fill("3.75")
    page.get_by_role('button', name="submit").click()
    page.wait_for_load_state()
    expect(page.locator('div[id="u-gpa"]')).to_have_text("3.75")
    page.locator('input[id="user_gpa"]').fill("3.87")
    page.get_by_role('button', name="submit").click()

# 7.1
# Dont remove commented print statements, test case fails without them, idk why
def test_admin_click_edit_app(page: Page):
    val = None
    vals = ["Closed", "Open"]
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('a[id="applicationsButton"]').click()
    page.wait_for_load_state()
    val = page.locator('span[id="app-status"]').all()[0].inner_text()
    #print(val)
    page.locator('button[id="app-oc"]').all()[0].click()
    page.on("dialog", handle_dialog)
    page.wait_for_load_state()
    page.locator('a[id="applicationsButton"]').click()
    page.wait_for_load_state()
    nv = [x for x in vals if x not in [page.locator('span[id="app-status"]').all()[0].inner_text()]]
    #print(nv)
    expect(page.locator('span[id="app-status"]').all()[0]).to_have_text(nv[0])

# 7.2
# Needs functionality
def test_admin_click_edit_job(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('a[id="job-edit"]').all()[0].click()
    page.select_option('select#role', 'Lab Instructor')
    page.locator('input[id="certification_required"]').uncheck()
    page.get_by_role('button', name="submit").click()
    page.wait_for_load_state()
    first = page.locator('li[class="list-group-item"]').all()[0]
    expect(first.locator('span[class="badge badge-primary"]')).to_have_text(re.compile("Lab Instructor"))
    expect(first.locator('p').all()[0]).to_be_empty()
    page.locator('a[id="job-edit"]').all()[0].click()
    page.select_option('select#role', 'Grader')
    page.locator('input[id="certification_required"]').check()
    page.get_by_role('button', name="submit").click()
    # Make some edit
    # Save edit
    # check job edited

# 7.3
def test_admin_click_remove_job(page: Page):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    last = page.locator('h5[id="course-name"]').all()[3].inner_text()
    page.locator('li[class="list-group-item"]').all()[3].locator('button[id="job-close"]').click(force=True)
    page.locator('li[class="list-group-item"]').all()[3].locator('button[id="job-close"]').dispatch_event('click')
    #page.locator('button[id="job-close"]').all()[-1].focus()
    #page.locator('button[id="job-close"]').all()[-1].dispatch_event('click')
    #page.locator('button[id="job-close"]').last()#.click()# .all()[-1].press("Enter")
    #page.on("dialog", handle_dialog)
    page.wait_for_load_state()
    expect(page.locator('h5[id="course-name"]').all()[3]).not_to_have_text(last)
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
    page.locator('button[id="app-rej"]').all()[0].click()
    # check if app is rejected
# 7.6
def test_admin_click_create_job(page: Page, course='CS 101 - Problem Solving and Programming I', position='Grader'):
    login(page, user="admin@admin.com", pa="admin")
    page.goto(admin)
    page.locator('button[id="create-job"]').click()
    page.select_option('select#role', position)
    page.select_option('select#course_required', course)
    page.get_by_role('button', name='submit').click()
    page.wait_for_load_state()
    expect(page.locator('li[class="list-group-item"]').all()[-1].locator("h5")).to_have_text(re.compile(course))