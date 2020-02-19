import sys, json, time
import re
import requests

from property_class import Property
from selenium import webdriver

def in_budget(bed_count, max_per_person, total_rent):
    actual_maximum = bed_count * max_per_person
    minium = actual_maximum * 0.6
    ## Assuming users will not want a minimum price much lower than their max - use 70% of max
    if minium < total_rent <= actual_maximum:
        return True

def closest_is_higher(number, the_list='prices'):
    '''This function takes a number input and returns from a list of
    numbers the one which is closest yet still more positive.'''

    pricelist = [100,150,200,250,300,350,400,450,500,600,700,
                800,900,1000,1100,1200,1250,1300,1400,1500,
                1750,2000,2250,2500,2750,3000,3500,4000,4500,
                5000,5500,6000]
    miles = [0, 0.25,0.5, 1, 3, 5, 10, 15, 20 ,30, 40]
    my_list = pricelist if the_list == 'prices' else miles
    if number <= my_list[0]:
        return my_list[0]
    elif not 0 < number <= my_list[-1]:
        print(f'Number must be between 0 and {my_list[-1]}.')
        sys.exit()
    else:
        diffs = [number - price for price in my_list]
        for difference in diffs:
            if difference <= 0:
                idx = diffs.index(difference)
                return my_list[idx]

def get_search_url():
    ## Get some inputs
    min_beds = input('\nEnter the minimum beds to search for: ')
    max_beds = input('Enter the maximum beds to search for: ')
    max_price_pppcm = input('Enter the maximum price per person per month: ') # per person per calendar month
    radius = input('Enter the radius in miles from the centre of London: ')

    max_price = closest_is_higher(int(max_beds)*int(max_price_pppcm))
    miles = closest_is_higher(float(radius), 'miles')

    template = f'''\
https://www.rightmove.co.uk/property-to-rent/find.html\
?searchType=RENT&locationIdentifier=STATION%5E6953&\
insId=1&radius={miles}&maxPrice={max_price}&minBedrooms={min_beds}\
&maxBedrooms={max_beds}\
&maxDaysSinceAdded=7'''

    return template, float(max_price_pppcm), float(radius), min_beds, max_beds

def price_to_number(pricetext):
    return float(re.sub('[^\d.]', '', pricetext))

def floorplan_available(link):
    src = requests.get(link)
    if src.text.count('floorplan') > 4:
        return True

def address_parser(fulladdress):
    pattern = r'[A-Z]{1,2}\d{1,2}'
    match = re.search(pattern, fulladdress)
    if match:
        return (fulladdress.split(match[0])[0].strip(), match[0])
    else:
        return (fulladdress, None)

def main():
    ## Load the first page of results
    url, max_price, max_radius, minBeds, maxBeds = get_search_url()
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(4.5)
    driver.minimize_window()
    import pdb; pdb.set_trace()
    try:                ## Need this as rightmove website spends ages downloading/running
        driver.get(url) ## scripts on page load, long delays - this triggers
    except:             ## timeout exception and just continues.
        pass

    ## Extract max page number
    pagination = driver.find_element_by_class_name('pagination-pageSelect').text
    maxpage = int(pagination.split('of')[1])

    properties = []

    ## Loop through and get any properties fitting our requirements
    count = 0 ## Not used now but could be to set a maximum No. properties to scrape
    for i in range(maxpage - 1):
    # for i in range(5):
        print(f'\n\tPage {i+1}/{maxpage}\n')
        search_results = driver.find_element_by_class_name('l-searchResults')
        items = search_results.find_elements_by_class_name('propertyCard')
        for item in items:
            # x = item.location_once_scrolled_into_view
            price_text = item.find_element_by_class_name('propertyCard-priceValue').text
            monthly_rent = price_to_number(price_text)
            link = item.find_element_by_partial_link_text(price_text).get_attribute('href')
            distance = item.find_element_by_class_name('propertyCard-distance').text
            dist_string = re.search(r'[\d.]+\s(miles|km|kms)' , distance)[0]
            distance_num = float(re.sub('[^\d.]', '', distance))
            bed_count = int(item.find_element_by_class_name('propertyCard-link').text.split('bed')[0])

            ## Dont bother collecting data on properties out of budget
            if in_budget(bed_count, max_price, monthly_rent):
                if distance_num <= max_radius:
                    fulladdress = item.find_element_by_class_name('propertyCard-address').text
                    addr, postcode = address_parser(fulladdress)
                    floorplan = floorplan_available(link)

                    ## get agent details
                    agentname = item.find_element_by_class_name('propertyCard-branchLogo-link').get_attribute('title')
                    agentnumber = item.find_element_by_class_name('propertyCard-contactsPhoneNumber').text
                    agent = {'name':agentname, 'telephone':agentnumber}

                    prop = Property(bed_count, dist_string, monthly_rent, link, agent, addr, postcode, floorplan)
                    properties.append(prop.serialize())
                    print(json.dumps(prop.serialize(), indent=4))
                else:
                    print(f'\tProperty out of range at {dist_string}.')
            else:
                print(f'\tThis {bed_count} bed property is out of budget range at {price_text}.')

        ## go to next page
        driver.find_element_by_css_selector('button[data-test="pagination-next"]').click()
        time.sleep(2)

    ## Write our data to a json file.
    fname = f'properties{len(properties)}_minBed={minBeds}_maxBed={maxBeds}_radius={max_radius}pcm={int(max_price)}'.replace('.','pt') + '.json'
    with open(fname, 'w') as f:
        # data = {'ResultCount':len(properties)}
        # data['search_paramaters'] = {
        #                             'minimumBeds': minBeds,
        #                             'maximumBeds': maxBeds,
        #                             'maxRadius': max_radius,
        #                             'maxPricePPPCM' : max_price
        #                             }
        data = properties
        json.dump(data, f, sort_keys=True, indent=4)



if __name__ == '__main__':
    main()
