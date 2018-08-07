#! python3

# SECTION: Dependencies

from zipfile import ZipFile as zf
from time import sleep
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

## SECTION: Variables

# Paths
downloadPath = 'path to where you want to save the zip files'
extractPath = 'path to where you want to extract the files'

# Lists
monthList = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
yearList = list(range(2010, 2019))
yearList = list(map(str, yearList))
attrList = ['QUARTER', 'FL_DATE', 'UNIQUE_CARRIER', 'FL_NUM', 'ORIGIN_AIRPORT_SEQ_ID', 'ORIGIN_CITY_MARKET_ID', 'DEST_AIRPORT_SEQ_ID', 'DEST_CITY_MARKET_ID', 'CRS_DEP_TIME',
            'DEP_TIME', 'DEP_DELAY_NEW', 'DEP_DEL15', 'CANCELLED', 'DISTANCE', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME']

# SECTION: Selenium actions
# Set download settings
chromeOptions = webdriver.ChromeOptions()
prefs = {'download.default_directory': downloadPath,
         "download.prompt_for_download": False}
chromeOptions.add_experimental_option('prefs', prefs)

# Start browser
browser = webdriver.Chrome(chrome_options=chromeOptions)
browser.get('https://transtats.bts.gov/DL_SelectFields.asp?Table_ID=236')

# Select attributes
for attr in attrList:
    attrSelect = browser.find_element_by_xpath(
        '//*[@value=\'' + attr + '\']')
    attrSelect.click()

# Find download button
downloadButton = browser.find_element_by_name('Download')

# SECTION: Functions

# clickDownload: Clicks download button


def clickDownload():
    downloadButton.click()

# extract: Extracts and renames CSV file from downloaded zip folder


def extract(yr, mo):
    for direc, ignore, files in os.walk(downloadPath):
        for file in files:
            filename = os.path.join(direc, file)
            if ('zip' in filename) and ('download' not in filename):
                z_file = zf(filename)
                for arch in z_file.namelist():
                    extracted = z_file.extract(arch, path=extractPath)
                    os.rename(extracted,
                              extractPath+'/'+yr+'_'+mo+'.csv')
                    yield z_file
                z_file.close()

# processDownloads: Calls extract(yr, mo) on downloaded zip, then deletes zip


def processDownloads(yr, mo, deleteFiles=True):
    waitDownload(sleeptime=1)
    for zf_obj in extract(yr, mo):
        if deleteFiles == True:
            zfp = zf_obj.fp.name
            zf_obj.close()
            os.remove(zfp)
        else:
            zf_obj.close()

# isDownloadFinished: Checks if download is finished


def isDownloadFinished():
    for file in os.listdir(downloadPath):
        if ('tmp' in file) or ('download' in file):
            return False
    return True

# waitDownload: Calls isDownloadFinished() and stops processes if download isn't finished


def waitDownload(sleeptime=1):
    while isDownloadFinished() is False:
        sleep(sleeptime)
        pass

# download: Downloads a file by calling clickDownload()


def download(yr, mo, Wait=True):
    if Wait == True:
        waitDownload()
    clickDownload()

# downloadAll: Begins process


def downloadAll(yrList, moList, Process=True, sleeptime=1):
    for yr in yrList:
        yearSelect = Select(browser.find_element_by_id('XYEAR'))
        yearSelect.select_by_visible_text(yr)
        for mo in moList:
            if yr == '2018' and moList.index(mo) > 4:
                break
            else:
                monthSelect = Select(
                    browser.find_element_by_id('FREQUENCY'))
                monthSelect.select_by_visible_text(mo)
                if yr == '2010' and mo == 'January':
                    download(yr, mo, Wait=False)
                else:
                    download(yr, mo, Wait=True)
                if Process == True:
                    processDownloads(yr, mo)
                    sleep(sleeptime)
                print("Data for " + mo + " " + yr + " downloaded!")
    print("Downloads finished!")
    return


downloadAll(yearList, monthList)

browser.quit()