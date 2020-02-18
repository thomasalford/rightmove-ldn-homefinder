import os, sys
import random
import time

from selenium import webdriver

USAGE = '''\
usage: "python rightmove.py <rightmove search url>"'''


def closest_is_higherprice(number, pricelist):
    pricelist = list(range(100, 3000, 200))
    if number <= pricelist[0]:
        return pricelist[0]:
    elif number > li[-1]:
        return None
    else:
        diffs = [number - price for price in pricelist]
        for difference in diffs:
            if difference <= 0:
                idx = diffs.index(difference)
                return pricelist[idx]

def formatted_link():

    template = 'https://www.rightmove.co.uk/property-to-rent/find.html?'+\
    'searchType=RENT'+\
    '&locationIdentifier=STATION%5E6953'+\
    '&radius=3.0'
    '&minPrice='
    '&maxPrice=2750'
    '&minBedrooms=2'
    '&maxBedrooms=3'
    print(template)



def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit()
    else:
        start_link = sys.argv[1]
    print(start_link)



if __name__ == '__main__':
    main()
