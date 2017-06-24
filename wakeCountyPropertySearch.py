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

    # loop thru pages to get each page of account results
    outer_owner_info = []
    outer_admin_data = []
    outer_trans_improv_data = []
    outer_assessed_data = []
    for page in number_of_pages:
        select = Select(browser.find_element_by_name("spg"))
        select.select_by_visible_text(page)
        go_button = browser.find_element_by_xpath("//input[@value='GO']")
        go_button.send_keys(Keys.RETURN)
        soup = bs4.BeautifulSoup (browser.page_source, "html.parser")
        
        # loop through result set and locate account numbers for each property record
    
        for row in soup.findAll('table')[4].tbody.findAll('tr'):            
            cols = row.findAll('td')
            if len(cols) > 9:
                account = cols[1].get_text()
            if account != "Account":
                account_link = browser.find_element_by_link_text(account) 
                account_link.click()
                soup_detail = bs4.BeautifulSoup(browser.page_source, "html.parser")

                # get text for database fields
                #owner data table information
                #inner list holds all data information per account record
                inner_owner_info = []
                inner_owner_info.append(account)
                #loop thru 5th table tag to grab all td tags
                for el in soup_detail.findAll('table')[4].tbody.findAll('tr'):
                    prop_el1 = el.find('td')
                    text = prop_el1.get_text().strip()
                    #append account record data to inner list
                    inner_owner_info.append(text)
                #append individual account records to outer list
                #to create lists of lists
                outer_owner_info.append(inner_owner_info)
                #go back to previous page
                #browser.execute_script("window.history.go(-1)")            
    
                #admin data table information
                #inner list holds all data information per account record
                inner_admin_data = []
                inner_admin_data.append(account)
                #loop thru 5th table tag to grab all td tags
                for el in soup_detail.findAll('table')[9].tbody.findAll('tr'):
                    # holds each pair of line items, field and value
                    admin_items = []
                    prop_el2 = el.findAll('td')
                    try:
                        admin_text1 = prop_el2[0].get_text().strip()
                        admin_text2 = prop_el2[1].get_text().strip()
                        admin_items.append(admin_text1)
                        admin_items.append(admin_text2)
                    except IndexError:
                        admin_text1 = prop_el2[0].get_text().strip()
                        admin_items.append(admin_text1)
                    #append account record data/line items to inner list
                    inner_admin_data.append(admin_items)
                #append individual account records to outer list
                #to create lists of lists of lists
                outer_admin_data.append(inner_admin_data)
                #go back to previous page
                #browser.execute_script("window.history.go(-1)")

                #transfer and improvement data table information
                #inner list holds all data information per account record
                inner_trans_improv_data = []
                inner_trans_improv_data.append(account)
                #loop thru 5th table tag to grab all td tags
                for el in soup_detail.findAll('table')[10].tbody.findAll('tr'):
                    # holds each pair of line items, field and value
                    trans_improv_items = []                    
                    prop_el3 = el.findAll('td')
                    try:                    
                        trans_improv_text1 = prop_el3[0].get_text().strip()
                        trans_improv_text2 = prop_el3[1].get_text().strip()
                        trans_improv_items.append(trans_improv_text1)
                        trans_improv_items.append(trans_improv_text2)
                    except IndexError:
                        trans_improv_text1 = prop_el3[0].get_text().strip()
                        trans_improv_items.append(trans_improv_text1)
                    #append account record data/line items to inner list
                    inner_trans_improv_data.append(trans_improv_items)
                #append individual account records to outer list
                #to create lists of lists of lists
                outer_trans_improv_data.append(inner_trans_improv_data)
                #go back to previous page
                browser.execute_script("window.history.go(-1)")            
    print(outer_owner_info, outer_admin_data, outer_trans_improv_data)
               
        
               


    # if multiple pages not found-collect account number of each result
    # run function call to getAccountDetails to pull information from detail page
    
    #except NoSuchElementException:
        #soup = bs4.BeautifulSoup (browser.page_source, "html.parser")
        #for row in soup.findAll('table')[4].tbody.findAll('tr'):
            #cols = row.findAll('td')
            #if len(cols) > 9:
                #account = cols[1].get_text()
                #print(account)
         
    browser.close()
main()