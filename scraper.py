# -*- coding: utf-8 -*-

#### IMPORTS 1.0

import os
import re
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

#### FUNCTIONS 1.0

def validateFilename(filename):
    filenameregex = '^[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+_[0-9][0-9][0-9][0-9]_[0-9QY][0-9]$'
    dateregex = '[0-9][0-9][0-9][0-9]_[0-9QY][0-9]'
    validName = (re.search(filenameregex, filename) != None)
    found = re.search(dateregex, filename)
    if not found:
        return False
    date = found.group(0)
    now = datetime.now()
    year, month = date[:4], date[5:7]
    validYear = (2000 <= int(year) <= now.year)
    if 'Q' in date:
        validMonth = (month in ['Q0', 'Q1', 'Q2', 'Q3', 'Q4'])
    elif 'Y' in date:
        validMonth = (month in ['Y1'])
    else:
        try:
            validMonth = datetime.strptime(date, "%Y_%m") < now
        except:
            return False
    if all([validName, validYear, validMonth]):
        return True


def validateURL(url):
    try:
        r = urllib2.urlopen(url)
        count = 1
        while r.getcode() == 500 and count < 4:
            print ("Attempt {0} - Status code: {1}. Retrying.".format(count, r.status_code))
            count += 1
            r = urllib2.urlopen(url)
        sourceFilename = r.headers.get('Content-Disposition')
        if sourceFilename:
            ext = os.path.splitext(sourceFilename)[1].replace('"', '').replace(';', '').replace(' ', '')
        else:
            ext = os.path.splitext(url)[1].split('?')[0]
        validURL = r.getcode() == 200
        validFiletype = ext.lower() in ['.csv', '.xls', '.xlsx']
        return validURL, validFiletype
    except:
        print ("Error validating URL.")
        return False, False


def validate(filename, file_url):
    validFilename = validateFilename(filename)
    validURL, validFiletype = validateURL(file_url)
    if not validFilename:
        print filename, "*Error: Invalid filename*"
        print file_url
        return False
    if not validURL:
        print filename, "*Error: Invalid URL*"
        print file_url
        return False
    if not validFiletype:
        print filename, "*Error: Invalid filetype*"
        print file_url
        return False
    return True


def convert_mth_strings ( mth_string ):
    month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
    for k, v in month_numbers.items():
        mth_string = mth_string.replace(k, v)
    return mth_string

#### VARIABLES 1.0

entity_id = "E5020_THLBC_gov"
<<<<<<< HEAD
url = "http://www.towerhamlets.gov.uk/lgnl/council_and_democracy/Transparency/payments_to_suppliers.aspx"
=======
url = "http://www.towerhamlets.gov.uk/lgnl/council_and_democracy/council_budgets_and_spending/transparency/payments_to_suppliers.aspx"
>>>>>>> b8625ea82293042f2495ccbb57dd2d672ab87dd4
errors = 0
data = []

#### READ HTML 1.0

html = urllib2.urlopen(url)
soup = BeautifulSoup(html, 'lxml')


#### SCRAPE DATA
<<<<<<< HEAD

table_links = soup.find_all('a', 'sys_15')
for table_link in table_links:
    title =table_link.find_previous('th').text
    url = 'http://www.towerhamlets.gov.uk/' + table_link['href']
    csvYr = title[-4:]
    csvMth = title[:3]
    if 'AHW-Directorate' in url:
        break
    csvMth = convert_mth_strings(csvMth.upper())
    data.append([csvYr, csvMth, url])
table_links = soup.find_all('a', 'sys_18')
for table_link in table_links:
    title = table_link.text.replace(u'\xa0', ' ')
    if 'Payment' in title:

        csvYr = title.split('for ')[-1].strip()[-4:]
        csvMth = title.split('for ')[-1].strip()[:3]
        try:
            url = 'http://www.towerhamlets.gov.uk/' + table_link['href']
        except:
            pass
        csvMth = convert_mth_strings(csvMth.upper())
        data.append([csvYr, csvMth, url])
=======
import requests

html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')

links = soup.findAll('a', href=True)
for link in links:
    url = 'http://www.towerhamlets.gov.uk/' + link['href']
    title = link.text.strip()
    if title.startswith('Payment f') or title.startswith('Payments f') and 'card' not in title:
        title = title.upper().replace('\r',' ').replace('\n',' ')
        csvYr = title.replace(u'\xa0', ' ').strip().split(' ')[-1]
        csvMth = title.replace(u'\xa0', ' ').split(' ')[-2][:3]
        if 'APRIL' in title.replace(u'\xa0', ' ').split(' ')[-3]:
            csvMth = title.replace(u'\xa0', ' ').split(' ')[-3][:3]
        csvMth = convert_mth_strings(csvMth.upper())
        data.append([csvYr, csvMth, url])
table_links = soup.find('table').find('tbody').find_all('tr')
for table_link in table_links:
    title = table_link.find('th').text
    csvYr = title.strip().split('for ')[-1].split(' ')[-1]
    csvMth = title.strip().split('for ')[-1].split(' ')[0][:3]
    try:
        url = 'http://www.towerhamlets.gov.uk/' + table_link.find('td').find_next('td').find('a')['href']
    except:
        pass
    csvMth = convert_mth_strings(csvMth.upper())
    data.append([csvYr, csvMth, url])
>>>>>>> b8625ea82293042f2495ccbb57dd2d672ab87dd4



#### STORE DATA 1.0

for row in data:
    csvYr, csvMth, url = row
    filename = entity_id + "_" + csvYr + "_" + csvMth
    todays_date = str(datetime.now())
    file_url = url.strip()

    valid = validate(filename, file_url)

    if valid == True:
        scraperwiki.sqlite.save(unique_keys=['l'], data={"l": file_url, "f": filename, "d": todays_date })
        print filename
    else:
        errors += 1

if errors > 0:
    raise Exception("%d errors occurred during scrape." % errors)


#### EOF

