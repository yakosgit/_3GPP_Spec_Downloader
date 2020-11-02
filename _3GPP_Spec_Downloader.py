#################################################################################################
#
# Author: Yako K. Yako
#
#################################################################################################
# Script to automatically download, rename, and display the title the URL of a requested 
# 3GPP spec doc number (e.g 16.38.101)
#
# HOW TO USE:
# 1- change the "path" variable in the script to a proper path (e.g. path=r"C:\Users\YOURPC\Desktop\3GPP/")
# 2- place the file "3GPP_Spec_Titles.xlsx" into the path you choose (optional) 
#    - needed in order to return the title of any spec doc# you enter and rename the downloaded files
# 3- Run command: python _3GPP_Spec_Downloader.py arg1 arg2 (e.g. python _3GPP_Spec_Downloader.py true true)
#    The 2 arguments (arg1 arg2) are flags for download and rename options respectively
#    true  true   -> download and rename (e.g 16.38.201 will be saved as "38201-g00-NR; Physical layer; General description-Rel-16")
#    true  false  -> download and keep original file name ( default name is 3GPP spec number, e.g 38201-g00-NR) 
#    false false  -> no download or rename, just display the title of the spec doc number
#    false true   -> no download or rename, just display the title of the spec doc number
# 4- when prompeted "Enter desired 3GPP release.series.doc# (e.g 16.38.101): ", enter the info of the doc you need
#**note:if you don't provide doc# (e.g 16.38.) the script will download all docs in that series**
# 5- ENJOY :)
#
#################################################################################################

import os
from ftplib import FTP 
import pandas as pd
import zipfile
import numpy as np
from urllib.request import urlopen, Request
import sys
import re
import requests
from bs4 import BeautifulSoup as bs

#################################################################################################

# path where spec files will be downloaded and where "3GPP_Spec_Titles.xlsx" file is located
path=r"C:\Users\YOURPC\Desktop\3GPP/"
# path where you want to save 3gpp spec files
where_to_save = path+r'\3gpp_spec_files'
# read sys argv for download and rename options
download = sys.argv[1].lower() == 'true'
rename = sys.argv[2].lower() == 'true'
# reading user input of desired 3gpp doc to download 
_3GPP_Release, _3GPP_Series, _3GPP_Doc_Num = input("Enter desired 3GPP release.series.doc# (e.g 16.38.101): ").split('.') 

# func to retrieve full spec title from a spec number
def get_3gpp_spec_titles(_3GPP_Series, _3GPP_Doc_Num):
    _3GPP_Spec_Num = str(_3GPP_Series) + '.' + str(_3GPP_Doc_Num)
    temp1=_3GPP_Spec_Titles[_3GPP_Spec_Titles['spec_number'].str.contains(_3GPP_Spec_Num)]
    if temp1.shape[0]==0:
        print("Doc Not Found in Spec Titles Table")
    for index, row in temp1.iterrows():
        print(row["spec_number"], row["title"], '\n') 

# read "3GPP_Spec_Titles.xlsx" into a data frame (only 28,32,36,37,38 series)
spec_titles=True
try:
    _3GPP_Spec_Titles=pd.read_excel(path+'3GPP_Spec_Titles.xlsx')
    _3GPP_Spec_Titles['spec_number_cln']=_3GPP_Spec_Titles.spec_number.str.replace('.', '')
    print('\n')
    print('3gpp_spec_title(s):', '\n')
    print(get_3gpp_spec_titles(_3GPP_Series, _3GPP_Doc_Num ))
except:
    print('3GPP_Spec_Titles.xlsx file NOT found')
    spec_titles=False

# create spec doc download URL and print a list of matching doc links
_3gpp_spec_ftp_url = "http://www.3gpp.org/ftp/Specs/latest/Rel-"+str(_3GPP_Release)+'/'+str(_3GPP_Series)+"_series/"
_3gpp_url_reqest = Request(_3gpp_spec_ftp_url, headers={'User-Agent': 'Chrome'})
match_link_list=[]
try:
    html_obj = urlopen(_3gpp_url_reqest)
    html_obj_read = html_obj.read()
    soup = bs(html_obj_read, 'html.parser')
    a_link_list = [link for link in soup.find_all("a")]
    match_link_list=[k for k in a_link_list if (str(_3GPP_Series) + str(_3GPP_Doc_Num)) in k.get('href')]
    print('Matching Link(s) Found on (www.3gpp.org)', '\n')
    print(*match_link_list, sep='\n') 
    if not match_link_list:
        print('No Matching Link(s) Found on (www.3gpp.org)')
except:
    print('No Matching Link(s) Found on (www.3gpp.org)')

# download the desired 3gpp spec zip files
if download and match_link_list: 
    print('downloading and unzipping')
    # create dir for dowloading spec files
    if not os.path.exists(where_to_save):
        os.makedirs(where_to_save)
    os.chdir(where_to_save)
    for item in match_link_list:
        item_url_link= item.get('href')
        request = requests.get(item_url_link)
        zip_file_name = re.match(r'(.*)/(.*)', item_url_link)
        os.chdir(where_to_save)
        with open(zip_file_name.group(2), 'wb') as outputfile:
            outputfile.write(request.content)
        print(zip_file_name.group(2))
    # extract doc files from zip files
    for item in os.listdir(where_to_save):
        if item.endswith(".zip"):
            file_name = where_to_save+"\\"+item
            zip_obj = zipfile.ZipFile(file_name)
            zip_obj.extractall(where_to_save)
            zip_obj.close()
            os.remove(file_name)
    print('downloading and unzipping complete')

# rename 3gpp spec file to include title 
if download and rename and match_link_list and spec_titles:
    print('renaming')
    for filename in os.listdir('.'):
        _3GPP_Spec_Num = re.match(r'(.*)-(g.*).(doc.*)', filename)
        try:
            if _3GPP_Spec_Titles['spec_number_cln'].str.contains(_3GPP_Spec_Num.group(1)).any():
                title = _3GPP_Spec_Titles[_3GPP_Spec_Titles['spec_number_cln'].str.contains(_3GPP_Spec_Num.group(1))].title.values[0]
                title = re.sub(r'.doc.*','',filename)+'-' + title
                title = re.sub(r'[<>:"/\|?*]','', title)
                os.rename(filename, title+ '-Rel-' +str(_3GPP_Release)+'.'+_3GPP_Spec_Num.group(3))
                print(filename, 'renamed')
        except:
            print('cannot rename', filename )
    print('renaming complete')
