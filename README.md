# rightmove-ldn-homefinder
## Python based tool to narrow down searches for rental properties on the [rightmove website](https://rightmove.co.uk)

Having recently undergone the process of finding a place to live in London, despite the fairly useful nature of rightmove's searching and filtering functions I thought that a tool could be developed to gather available options.

For example, it is not possible on the standalone website to search for properties with differing numbers of beds whilst only displaying those which the price per person per calendar month stays within a given budget. You may search for 2, 3, 4
bed properties and set your maximum budget to 4 * (e.g. £800 pcm) = £3,200 this number should be rounded up to £3,500 due to the non-continuous `"&maxPrice={x}"` aspect of the url query string. Similarly when entering how many miles to look for properties from the center of london.

Program takes some inputs from the user such as minimum and maximum number of beds to search for, also the maximum price per person per calendar month.

Outputs a .JSON file to this directory which can be used to write to a csv etc. When I was using an earlier version of this tool, and a relatively large number of appropriate links had been extracted, I used the random and webbrowser libraries to open up samples of ~15 webpages to view and ultimately discard.

External libraries:
Requires Selenium, and chromedriver.exe to be in sys.path as well as the requests library.
