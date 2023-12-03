from playwright.sync_api import Page, expect
import re
from test_util import login

base = "http://localhost:5000"
apps = base+'/applications'
admin = base+'/admin'
lin = base+'/login'
reg = base+'/register'
prof = base+'/profile'

#def test_