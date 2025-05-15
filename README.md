# XES-3089
XKCD Encryption Standard, comprised of (currently) 3089 comics.

## Functionality
XES-3089 works by scraping every comic on the site xkcd.com for their alt-text, which it then stores to disk and reads into a dictionary. It then takes the inputted text, and provides comics IDs and word numbers in the format xxxx:yy-xxxx:yy, where xxxx is the comic ID and yy is the word number. Individual words are seperated by hyphens (-) and unknown words are marked as 0:0
