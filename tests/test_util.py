from playwright.sync_api import Page, expect
import sqlite3
import os

base = "http://localhost:5000"
lin = base+'/login'

def login(page: Page, user="testuc@test.com", pa="test"):
    page.goto(lin)
    page.locator('input[name="user_email"]').fill(user)
    page.locator('input[name="user_pass"]').fill(pa)
    page.get_by_role('button', name='Submit').click()

def click_register(page: Page, user="testtest@test.com", pa="test", id="000000001", fname="test", lname="test", gpa="4", hours="40", courses=None):
    page.goto(base)
    page.locator('li[name="nav-register"]').click()
    page.wait_for_load_state()
    if courses:
        page.locator('button[name="adducourse"]').click()
        page.select_option('select#course_id', "CS 101 - Problem Solving and Programming I")
        page.select_option('select#grade', "A")
        page.locator('input[id="courseSubmit"]').click()
        page.locator('button[class="btn-close"]').click()
    page.locator('input[name="user_id"]').fill(id)
    page.locator('input[name="user_fname"]').fill(fname)
    page.locator('input[name="user_lname"]').fill(lname)
    page.locator('input[name="user_email"]').fill(user)
    page.select_option('select#user_major', label="CS")
    page.select_option('select#user_degree', label="BS")
    page.locator('input[name="user_gpa"]').fill(gpa)
    page.locator('input[name="user_hours"]').fill(hours)
    page.locator('input[name="user_pass"]').fill(pa)
    page.locator('input[name="user_confirm_pass"]').fill(pa)
    page.get_by_role('button', name="submit").click()

def click_login(page: Page, user="testuc@test.com", pa="test"):
    page.goto(base)
    page.locator('li[name="nav-login"]').click()
    page.locator('input[name="user_email"]').fill(user)
    page.locator('input[name="user_pass"]').fill(pa)
    page.get_by_role('button', name='Submit').click()

def delete_test_user():
    cw = os.path.join(os.getcwd(), "instance")
    dbfile = os.path.join(cw, "database.db")
    with sqlite3.connect(dbfile) as db:
        db.cursor().execute("""DELETE FROM Users WHERE user_email='testtest@test.com'""")

def handle_dialog(d):
    d.accept()