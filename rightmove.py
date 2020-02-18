import os, sys
import random
import time

from selenium import webdriver

USAGE = '''\
usage: "python rightmove.py <rightmove search url>"'''


def closest_is_higherprice(number):
    '''This function takes a number input and returns from a list of
    numbers the one which is closest yet still more positive.'''
    pricelist = list(range(100, 3000, 200))
    if number <= pricelist[0]:
        return pricelist[0]
    elif number > pricelist[-1]:
        return None
    else:
        diffs = [number - price for price in pricelist]
        for difference in diffs:
            if difference <= 0:
                idx = diffs.index(difference)
                return pricelist[idx]

def formatted_link():
    ## Get some inputs
    min_beds = input('Enter the minimum beds to search for: ')
    max_beds = input('Enter the maximum beds to search for: ')
    max_price_pppcm = input('Enter the maximum price per person per month: ')
    radius = input('Enter the radius in miles from the centre of London: ')

    template = f'''\
https://www.rightmove.co.uk/property-to-rent/find.html\
?searchType=RENT&locationIdentifier=STATION%5E6953&\
insId=1&radius={radius}&minPrice=&maxPrice={closest_is_higherprice(int(max_beds)*int(max_price_pppcm))}&minBedrooms={min_beds}\
&maxBedrooms={max_beds}\
&maxDaysSinceAdded=7'''
    return template



def main():
    pass



if __name__ == '__main__':
    main()
