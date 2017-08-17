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
    all_tables = getResults(name_to_search)
    

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
    count_pages = browser.find_element_by_name("spg")
    number_of_pages = []

    for option in count_pages.find_elements_by_tag_name("option"):
        number_of_pages.append(option.text)

    # owner data table information
    owner_info_list = []

    # property data table information
    property_info_list = []

    # tax info data table information
    tax_info_list =[]

    # building data table information
    building_info_list = []

    # land data table information
    land_info_list = []

    # sales data table information
    sales_info_list = []

    # taxbill data table information
    taxbill_info_list = []

    # loop thru pages to get each page of account results
    for page in number_of_pages:
        select = Select(browser.find_element_by_name("spg"))
        select.select_by_visible_text(page)
        go_button = browser.find_element_by_xpath("//input[@value='GO']")
        go_button.send_keys(Keys.RETURN)
        soup = bs4.BeautifulSoup (browser.page_source, "html.parser")    

        # loop through result set and locate account numbers for each property
        for row in soup.findAll('table')[4].tbody.findAll('tr'):            
            cols = row.findAll('td')
            if len(cols) > 9:
                account = cols[1].get_text()
            if account != "Account":
                account_link = browser.find_element_by_link_text(account) 
                account_link.click()
                soup_detail = bs4.BeautifulSoup(browser.page_source, "html.parser")
                
                owner_info = getOwnerInfo(account, soup_detail)
                # append each record's information to data table list above
                owner_info_list.append(owner_info)

                property_info = getPropertyData(account, soup_detail)
                # append each record's information to data table list above
                property_info_list.append(property_info)

                tax_info = getTaxData(account, soup_detail)
                # append each record's information to data table list above
                tax_info_list.append(tax_info)

                building_info = getBuildingData(browser, account, soup_detail)
                # append each record's information to data table list above
                building_info_list.append(building_info)

                land_info = getLandData(browser, account)
                # append each record's information to data table list above
                land_info_list.append(land_info)

                sales_info = getSales(browser, account)
                # append each record's information to data table list above
                sales_info_list.append(sales_info)

                taxbill_info = getTaxBillData(browser, account)
                # append each record's information to data table list above
                taxbill_info_list.append(taxbill_info)
                                
                print(sales_info)
    browser.close()  
          

# owner list
def getOwnerInfo(account, soup_detail):    
        
    # owner_info contains each real estate id account
    owner_info = []
    
    # append real estate id as first item in each account record 
    owner_info.append(account)
   
    #loop thru 5th table tag to grab all td tags
    for el in soup_detail.findAll('table')[4].tbody.findAll('tr'):
        prop_el = el.find('td')
        
        # owner info
        owner = prop_el.get_text().strip()
        owner_info.append(owner)
    del owner_info[1:3]
    del owner_info[3:5]
    del owner_info[-4: ]      
    
    return owner_info

# property list
def getPropertyData(account, soup_detail):    
    
    # property_info contains each real estate id account
    property_info = []

    # append real estate id as first item in each account record
    property_info.append(account)
    
    #loop thru 5th table tag to grab all td tags
    for el in soup_detail.findAll('table')[4].tbody.findAll('tr'):
        prop_el = el.find('td')
        
        # property info
        prop = prop_el.get_text().strip()
        property_info.append(prop)

    del property_info[1:11]   

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
    for el in soup_detail.findAll('table')[10].tbody.findAll('tr')[0:9]:                  
        prop_el = el.findAll('td')
        pair = pair_items(prop_el)
        #append account record data/line items to property_info
        property_info.append(pair)
    
    return property_info 
                
# tax info list
def getTaxData(account, soup_detail):

    # property_info contains each real estate id account
    tax_info = []

    # append real estate id as first item in each account record
    tax_info.append(account)

    for el in soup_detail.findAll('table')[11].tbody.findAll('tr'):                  
        prop_el = el.findAll('td')
        pair = pair_items(prop_el)
        #append account record data/line items to property_info
        tax_info.append(pair)

    return tax_info

# building list               
def getBuildingData(browser, account, soup_detail):

    # building_info contains each real estate id account
    building_info = []

    # append real estate id as first item in each account record
    building_info.append(account)

    
    try:
        #loop thru 11th table tag to grab last 4 tr tags and all td tags inside
        for el in soup_detail.findAll('table')[10].tbody.findAll('tr')[13:15]:            
            prop_el = el.findAll('td')
            pair = pair_items(prop_el)
            building_info.append(pair) 

        building_link = browser.find_element_by_link_text('Buildings')
        building_link.click()
        soup_detail = bs4.BeautifulSoup(browser.page_source, "html.parser")

        #loop thru 10th table tag to grab td tags
        for el in soup_detail.findAll('table')[9].tbody.findAll('tr'):
            prop_el = el.findAll('td')
            pair = pair_items(prop_el)
            building_info.append(pair)

        #loop thru 13th table tag to grab td tags
        for el in soup_detail.findAll('table')[12].tbody.findAll('tr')[0:9]:
            prop_el = el.findAll('td')
            pair = pair_items(prop_el)
            building_info.append(pair)

        #loop thru 11th table tag to grab td tags
        for el in soup_detail.findAll('table')[10].tbody.findAll('tr'):
            prop_el = el.findAll('td')
            pair = pair_items(prop_el)
            building_info.append(pair)

    except IndexError:
        pass

    # go back to account summary page
    browser.execute_script("window.history.go(-1)")
        
    
    return building_info

# land list
def getLandData(browser, account):
    # land_info contains each real estate id account
    land_info = []

    # append real estate id as first item in each account record
    land_info.append(account)

    try:
        land_link = browser.find_element_by_link_text('Land')
        land_link.click()
        soup_detail = bs4.BeautifulSoup(browser.page_source, "html.parser")

        #loop thru 5th table tag to grab td tags
        for el in soup_detail.findAll('table')[4].tbody.findAll('tr'):
            prop_el = el.findAll('td')
            pair = pair_items(prop_el)
            land_info.append(pair)

    except IndexError:
        pass

    # go back to account summary page
    browser.execute_script("window.history.go(-1)")

    return land_info

# sales list
def getSales(browser, account):

    # sales_info contains each real estate id account
    sales_info = []

    # append real estate id as first item in each account record
    sales_info.append(account)

    try:
        # go to sales link
        sales_link = browser.find_element_by_link_text('Sales')
        sales_link.click()
        soup_detail = bs4.BeautifulSoup(browser.page_source, "html.parser")

        # if multiple pages of sales results
        try:
            count_pages = browser.find_element_by_name("page")
            # stores number of page results (1,2,3,4....)
            number_of_pages = []

            for option in count_pages.find_elements_by_tag_name("option"):
                number_of_pages.append(option.text)

            for page in number_of_pages:
                select = Select(browser.find_element_by_name("page"))
                select.select_by_visible_text(page)
                go_button = browser.find_element_by_xpath("//input[@value='GO']")
                go_button.send_keys(Keys.RETURN)
                soup_detail = bs4.BeautifulSoup (browser.page_source, "html.parser")

                # grab 5th table tag 
                for el in soup_detail.findAll('table')[6].tbody.findAll('tr')[2:]:            
                    prop_els = el.findAll('td')
                    for prop_el in prop_els:
                        sales_item = prop_el.get_text().strip()
                        sales_info.append(sales_item)
                    

                browser.execute_script("window.history.go(-1)")


        # if only single page of results
        except NoSuchElementException:

            # grab 5th table tag 
                for el in soup_detail.findAll('table')[6].tbody.findAll('tr')[2:]:            
                    prop_els = el.findAll('td')
                    for prop_el in prop_els:
                        sales_item = prop_el.get_text().strip()
                        sales_info.append(sales_item)


    except IndexError:
        pass

    # go back to account summary page
    browser.execute_script("window.history.go(-1)")

    return sales_info

# tax bill list
def getTaxBillData(browser, account):

    # taxbill_info contains each real estate id account
    taxbill_info = []

    # append real estate id as first item in each account record
    taxbill_info.append(account)
    
    # go to tax bill link
    taxbill_link = browser.find_element_by_link_text('Tax Bill')
    taxbill_link.click()
    soup_detail = bs4.BeautifulSoup(browser.page_source, "html.parser")

    # if no tax bill information is available go back to account list page
    try:
        if browser.find_element_by_name('Form1'):
            browser.execute_script("window.history.go(-2)")

    # if tax bill information is available 'Form1' will not be found
    # then data collection for tax bill information
    except NoSuchElementException:
        # expand all tax bill results to one page if multiple pages
        try:
            full_page_link = browser.find_element_by_link_text('No Paging')
            full_page_link.click()
            for el in soup_detail.findAll('table')[6].tbody.findAll('tr')[2:]:
                prop_el = el.findAll('td')
                pair = pair_items(prop_el)
                taxbill_info.append(pair)

            #go back to previous page
            browser.execute_script("window.history.go(-3)")

        # if only one page of tax bill results
        except NoSuchElementException:
            for el in soup_detail.findAll('table')[6].tbody.findAll('tr')[2:]:
                prop_el = el.findAll('td')
                pair = pair_items(prop_el)
                taxbill_info.append(pair)

            #go back to previous page
            browser.execute_script("window.history.go(-2)")

        return taxbill_info


def pair_items(list_of_tags):
    items = []
    try:                    
        field = list_of_tags[0].get_text().strip()
        value = list_of_tags[1].get_text().strip()
        items.append(field)
        items.append(value)
    except IndexError:
        item = list_of_tags[0].get_text().strip()
        items.append(item)
    return items

main()

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
          
    print(outer_assessed_data)            
        
    if multiple pages not found-collect account number of each result
    run function call to getAccountDetails to pull information from detail page
    
    except NoSuchElementException:
        soup = bs4.BeautifulSoup (browser.page_source, "html.parser")
        for row in soup.findAll('table')[4].tbody.findAll('tr'):
            cols = row.findAll('td')
            if len(cols) > 9:
                account = cols[1].get_text()
                print(account)'''