import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


browser = webdriver.Chrome()
browser.get("http://localhost:8000/")
print(browser.title)

try:
	wait = WebDriverWait(browser, 10)
	elem = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,"Tourn")))
	print(elem.text)
	elem.click()
	elem = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Oak")))
	print(elem.text)
	elem.click()
	elems = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h3")))
	print(elems.text)
	
except TimeoutException:
	print("locating links in wgt_website failed")

golf_soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
soup_elems = golf_soup.select('td a')

list_of_nums = []
for elem in soup_elems:
	elem_text = elem.getText()
	elem_text = elem_text.strip()
	elem_int = int(elem_text)	
	list_of_nums.append(elem_int)
sum_of_ints = sum(list_of_nums)
avg_of_ints = sum_of_ints/len(soup_elems)
print("Average tournament score: ", avg_of_ints)
browser.close()

