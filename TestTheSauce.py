import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

class TestTheSauce(unittest.TestCase):

	#runs before each test
	def setUp(self):
		#ensure the testing driver is available
		self.website_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

		self.website_driver.get('https://www.saucedemo.com')

		self.data = {
		'key':'secret_sauce',
		'standard':'standard_user',
		'locked':'locked_out_user',
		'invalid':'ONESaucyBOI'
		}


	def login(self, user):
		#enter username and password, then submit.
		username_field = self.website_driver.find_element(By.ID, 'user-name')
		username_field.send_keys(self.data[user])

		# WebDriverWait(self.website_driver, 2).until(EC.text_to_be_present_in_element((By.ID, 'user-name'), self.data[user][0])) <- Trying to fix the single character problem

		key_field = self.website_driver.find_element(By.ID, 'password')
		key_field.send_keys(self.data['key'])

		login_btn = self.website_driver.find_element(By.ID, 'login-button')
		login_btn.click()


	#login test cases
	def test_standard_login(self):	
		self.login('standard')
		w = WebDriverWait(self.website_driver, 5).until(EC.url_contains('saucedemo.com/inventory.html'))
		
	def test_locked_login(self):
		self.login('locked')
		w = WebDriverWait(self.website_driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='error-message-container error']")))

	def test_invalid_login(self):
		self.login('invalid')
		w = WebDriverWait(self.website_driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='error-message-container error']")))
		

	#runs after each test
	def tearDown(self):
		self.website_driver.close()


if __name__ == '__main__':
	unittest.main()
