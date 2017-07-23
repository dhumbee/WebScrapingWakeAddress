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
    browser, account, soup_detail = getResults(name_to_search)
    owner_table = getOwnerInfo(account, soup_detail)
    property_table = getPropertyData(account, soup_detail)

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
                return browser, account, soup_detail

# owner list
def getOwnerInfo(account, soup_detail):
    # owner data table information
    owner_info_list = []
        
    # owner_info contains each real estate id account
    owner_info = []
    
    # append real estate id as first item in each account record 
    owner_info.append(account)
   
    #loop thru 5th table tag to grab all td tags
    for el in soup_detail.findAll('table')[4].tbody.findAll('tr'):
        prop_el = el.findAll('td')
        # owner info
        account_num = prop_el[0].get_text().strip()
        owner1 = prop_el[3].get_text().strip()
        owner2 = prop_el[4].get_text().strip()
        mailing_address_name = prop_el[7].get_text().strip()
        mailing_address_1 = prop_el[8].get_text().strip()
        mailing_address_2 = prop_el[9].get_text().strip()
        # append owner info to owner_info list
        owner_info.append(account_num)
        owner_info.append(owner1)
        owner_info.append(owner2)
        owner_info.append(mailing_address_name)
        owner_info.append(mailing_address_1)
        owner_info.append(mailing_address_2)
        
    # append each record's information to data table list above
    owner_info_list.append(owner_info)
    return owner_info_list

# property list
def getPropertyData(account, soup_detail):    
    # property data table information
    property_info_list = []

    # property_info contains each real estate id account
    property_info = []

    # append real estate id as first item in each account record
    property_info.append(account)
    
    #loop thru 5th table tag to grab all td tags
    for el in soup_detail.findAll('table')[4].tbody.findAll('tr'):
        prop_el = el.findAll('td')
        # property info
        location_address_1 = prop_el[-3].get_text().strip()
        location_address_2 = prop_el[-2].get_text().strip()
        location_temp = prop_el[-1].get_text().strip()
        # append property info to property_info list
        property_info.append(location_address_1)
        property_info.append(location_address_2)
        property_info.append(location_temp)    
    
    #loop thru 10th table tag to grab all td tags
    for el in soup_detail.findAll('table')[9].tbody.findAll('tr'):
        # holds each pair of line items, field and value
        property_items = []
        prop_el = el.findAll('td')
        try:
            prop_text1 = prop_el[0].get_text().strip()
            prop_text2 = prop_el[1].get_text().strip()
            # skip Land Class and Acreage- they go in other groups
            if prop_text1 == 'Land Class' or prop_text1 == 'Acreage':
                continue
            property_items.append(prop_text1)
            property_items.append(prop_text2)
        except IndexError:
            prop_text1 = prop_el2[0].get_text().strip()
            # skip Land Class and Acreage- they go in other groups
            if prop_text1 == 'Land Class' or prop_text1 == 'Acreage':
                continue
            property_items.append(prop_text1)

        #append account record data/line items to property_info
        property_info.append(property_items)

    #loop thru 11th table tag to grab first 8 tr tags and all td tags inside
    for el in soup_detail.findAll('table')[10].tbody.findAll('tr')[0:8]:
        # holds each pair of line items, field and value
        property_items2 = []                    
        prop_el = el.findAll('td')
        try:                    
            prop_text1 = prop_el[0].get_text().strip()
            prop_text2 = prop_el[1].get_text().strip()
            property_items2.append(prop_text1)
            property_items2.append(prop_text2)
        except IndexError:
            prop_text1 = prop_el[0].get_text().strip()
            property_items2.append(prop_text1)

         #append account record data/line items to property_info
        property_info.append(property_items2)

    # append each record's information to data table list above
    property_info_list.append(property_info)
    
    return property_info_list   
                
# building list               
def getBuildingData(browser, account, soup_detail):

    # building data table information
    property_info_list = []

    # building_info contains each real estate id account
    building_info = []

    # append real estate id as first item in each account record
    building_info.append(account)

    #loop thru 11th table tag to grab last 4 tr tags and all td tags inside
    for el in soup_detail.findAll('table')[10].tbody.findAll('tr')[13:]:
        # holds each pair of line items, field and value
        building_items = []                    
        prop_el = el.findAll('td')
        try:                    
            build_text1 = prop_el[0].get_text().strip()
            build_text2 = prop_el[1].get_text().strip()
            building_items.append(prop_text1)
            building_items.append(prop_text2)
        except IndexError:
            build_text1 = prop_el[0].get_text().strip()
            building_items.append(build_text1)

        #append account record data/line items to property_info
        building_info.append(building_items)

    building_link = browser.find_element_by_link_text('Building.asp')
    building_link.click()
    



'''#append account record data/line items to inner list
    inner_trans_improv_data.append(trans_improv_items)  
#append individual account records to outer list
#to create lists of lists of lists
outer_trans_improv_data.append(inner_trans_improv_data)

#assessed value data table information
#inner list holds all data information per account record
inner_assessed_data = []
inner_assessed_data.append(account)
#loop thru 5th table tag to grab all td tags
for el in soup_detail.findAll('table')[11].tbody.findAll('tr'):
    # holds each pair of line items, field and value
    assessed_items = []                    
    prop_el4 = el.findAll('td')
    try:                    
        assessed_text1 = prop_el4[0].get_text().strip()
        assessed_text2 = prop_el4[1].get_text().strip()
        assessed_items.append(assessed_text1)
        assessed_items.append(assessed_text2)
    except IndexError:
        assessed_text1 = prop_el4[0].get_text().strip()
        assessed_items.append(assessed_text1)
    #append account record data/line items to inner list
    inner_assessed_data.append(assessed_items)
#append individual account records to outer list
#to create lists of lists of lists
outer_assessed_data.append(inner_assessed_data)
#go back to previous page
browser.execute_script("window.history.go(-1)")            
    print(outer_assessed_data)'''
               
        
               


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