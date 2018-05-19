import re
import sys
import json
import requests
import io
import random
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup  
requests.packages.urllib3.disable_warnings()

PttName=""
load={
'from':'/bbs/'+PttName+'/index.html',
'yes':'yes' 
}

rs=requests.session()
res=rs.post('https://www.ptt.cc/ask/over18',verify=False,data=load)
FILENAME=""
