import os
import urllib.parse
import requests
import json
import re

requestkey = "Place your API key here"

def getShare():
  global link
  link = input("Please provide the share link to the level you want to generate a new link\n")
  check_link = re.search("https://exoracer.page.link/", link)
  if check_link == None:
    check_link = re.search("https://preview.page.link/", link)
    if check_link == None:
      link = "https://exoracer.page.link/" + link
    else:
      getShare()

def parseData():
  global default_ver
  global default_level_id
  global default_title 
  global default_desc
  req = requests.get(link)
  web_code = req.text
  check_link = re.search("<title>Dynamic Link Not Found</title>", web_code)
  if check_link == None:
    full_id = re.search("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}-[0-9]{1,}", web_code)
    print(full_id)
    default_ver = full_id.group()[37:]
    default_level_id = full_id.group()[:36]
    default_title = re.search('<meta name="twitter:title" content="(.){0,}?"/>', web_code).group()[36:]
    default_title = default_title[:len(default_title) - 3]
    default_desc = re.search('<meta name="description" content="(.){0,}?"/>', web_code).group()[34:]
    default_desc = default_desc[:len(default_desc) - 3]
  else:
    print("This is an invalid link. Please try again.")
    getShare()




  
getShare()
parseData()

("Your level ID:")
print(default_level_id)
# print("Your level version:")
# print(default_ver)
# print("Your share link title:")
# print(default_title)
# print("Your share link description:")
# print(default_desc)

### getting all of the information from the user
level_id = input("Type your level id (provided above) (Leave blank for default)\n") or default_level_id
ver = input("Type your level version (provided above) (Leave blank for default)\n") or default_ver
title = urllib.parse.quote(input("Type your title: (Leave blank for default)\n") or default_title)
desc = urllib.parse.quote(input("Type your description: (Leave blank for default)\n") or default_desc)
urlrequest = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=" + requestkey
thumb = input("Custom thumbnail? (Leave blank for default)")
if thumb == "":
  thumb = "https://storage.googleapis.com/exoracer-bd008.appspot.com/levels/" + level_id + "-" + ver

### putting the info into a var

longLink = "https://exoracer.page.link/?link=https://exoracer.io/?link%3DLEVEL%26levelId%3D" + level_id + "%26levelVersion%3D" + ver + "&apn=com.nyanstudio.exoracer&ofl=https://exoracer.io/deeplinkfallback.php?title%3D" + title + "%26description%3D" + desc + "%26imageUrl%3D" + urllib.parse.quote(thumb) + "&ibi=com.nyanstudio.exoracer&st=" + title + "&sd=" + desc + "&si=" + thumb

ask = input("\n\n\nShow long link? (y/n): ")
if ask == "y":
  print("\n" + longLink + "\n\n")
else:
  print("\n\n\n")

### puts the long link into the data for a request

  

### gets short url
type = input("Short or long?\n1 = SHORT\n2 = UNGUESSABLE\n\n")
if type == "1":
  data = '{\n  "longDynamicLink": "' + longLink + '",\n  "suffix": {\n    "option": "SHORT"\n  }\n}'
  print("\n Generating link...")
  link = requests.post(urlrequest, data=data)
  info = link.text
  data = json.loads(info)
  shortLink = data['shortLink']
  print("\n" + shortLink)
else:
  data = '{\n  "longDynamicLink": "' + longLink + '",\n  "suffix": {\n    "option": "UNGUESSABLE"\n  }\n}'
  print("\n Generating link...")
  link = requests.post(urlrequest, data=data)
  info = link.text
  info_table = json.loads(info)
  shortLink = info_table["shortLink"]
  print("\n" + shortLink)

save = input("Save data to external file? (data.json) (y/n)")
if save == "y":
  data = open('data.json')
  data = data.read()
  data = json.loads(data)
  data["input"]["levelID"] = level_id
  data["input"]["name"] = title
  data["input"]["description"] = desc
  data["input"]["thumbnail"] = thumb
  data["output"]["longURL"] = longLink
  data["output"]["shortURL"] = shortLink