# _3GPP_Spec_Downloader
#!/usr/bin/env python
# coding: utf-8

#################################################################################################
#
# Author: Yako K. Yako
#
#################################################################################################
#
# Script to automatically download, rename, and display the title of a given 
# 3GPP spec doc number (e.g 16.38.101) into the "path" provided in the script.
#
# Run command is as follow: python _3GPP_Spec_Downloader.py true true
#
# The 2 arguments (true true) are flags for download and rename respectively
# true  true   -> download and rename
# true  false  -> download and keep fine name ( default name is 3GPP spec number) 
# false false  -> no download or rename, just display the title of the spec doc number
# false true   -> no download or rename, just display the title of the spec doc number
#
# place the file "3GPP_Spec_Titles.xlsx" into the path you choose (optional) to
# quickly return the title of any spec doc# you enter 
# but you can add more series tables to the file as desired
#**note:if you don't provide doc# (e.g 16.38.) the script will download all docs in that series**
#
#################################################################################################
