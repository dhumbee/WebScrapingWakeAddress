'''
1.launch chrome and open to wake gov page: http://services.wakegov.com/realestate/
2. obtain street name to search for from user
3. enter street name in "street name" box under "search by location address"
4. hit "Go!" button to perform search
5. check checkboxes
6. hit "Go!"
7. obtain all results from all pages
8. get individual acct details from all results
9. put details in file
'''

import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# main func to call and get user input street name
def main():

    name_to_search = input("Enter a street name to search for: ")
    #name_to_search = 'Fire'
    getResults(name_to_search)

# get search results
def getResults(name_to_search):
    browser = webdriver.Chrome()
    browser.get("http://services.wakegov.com/realestate/")
    print(browser.title)

    street_name_box = browser.find_element_by_name("stname")
    #name_to_search = input("Enter a street name to search for: ")
    street_name_box.send_keys(name_to_search)
    go_button = browser.find_element_by_name("Search by Address")
    go_button.send_keys(Keys.RETURN)
    

    # if multiple pfxs will try to check all instances    
    try:
        checkboxes = browser.find_elements_by_xpath("//input[@name='c1']")

        for box in checkboxes:
            box.click()

        go_button = browser.find_element_by_name("Search Selected Streets")
        go_button.send_keys(Keys.RETURN)

    # if not multiple, will pass over
    except NoSuchElementException:
        pass

    # if multiple pages of results try to loop through all pages
    # and collect account number of each result
    # run function call to getAccountDetails to pull information from detail page
    #try:
    count_pages = browser.find_element_by_name("spg")
    number_of_pages = []
    for option in count_pages.find_elements_by_tag_name("option"):
        number_of_pages.append(option.text)

    for page in number_of_pages:
        select = Select(browser.find_element_by_name("spg"))
        select.select_by_visible_text(page)
        go_button = browser.find_element_by_xpath("//input[@value='GO']")
        go_button.send_keys(Keys.RETURN)
        soup = bs4.BeautifulSoup (browser.page_source, "html.parser")
        for row in soup.findAll('table')[4].tbody.findAll('tr'):
            cols = row.findAll('td')
            if len(cols) > 9:
                account = cols[1].get_text()
                if account != "Account":
                    account_link = browser.find_element_by_link_text(account)
                    account_link.click()

                



    # if multiple pages not found-collect account number of each result
    # run function call to getAccountDetails to pull information from detail page
    
    #except NoSuchElementException:
        #soup = bs4.BeautifulSoup (browser.page_source, "html.parser")
        #for row in soup.findAll('table')[4].tbody.findAll('tr'):
            #cols = row.findAll('td')
            #if len(cols) > 9:
                #account = cols[1].get_text()
                #print(account)
         
    #browser.close()
main()