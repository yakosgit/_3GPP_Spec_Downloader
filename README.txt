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
