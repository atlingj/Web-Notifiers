import requests, smtplib, csv, re, os, sys
from bs4 import BeautifulSoup as bs

# email list--------------------------------------------------
toAddress = ['recipient@email.com']
# ------------------------------------------------------------
masterList = ['54447/characters','54447/locations','54447/maps','54447/organisations','54447/families','54447/calendars','54447/timelines','54447/races','54447/quests',
'54447/journals','54447/items','54447/events','54447/abilities','54447/notes']
# ------------------------------------------------------------
NEW = False

def listToString(new):
    string = ''
    for ele in new:
        string += ele
    return string

def get(endpoint):
    response = s.get('https://kanka.io/api/1.0/campaigns/' + endpoint)
    #  30 requests per minute with kanka API: uncomment this if adding multiple campaigns
    #  time.sleep(2)
    return response

def email(content, recipient):
    conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
    conn.ehlo()  # call this to start the connection
    conn.starttls()  # starts tls encryption. When we send our password it will be encrypted.
    conn.login('name@email.com', 'password')
    conn.sendmail('name@email.com', recipient,
                  'Subject: Change Alert!\n\nUpdate on kanka!\n' + content + "\nFrom RaspberryPi")
    conn.quit()
    print('Sent notification e-mails for the following recipients:\n')
    for i in range(len(toAddress)):
        print(toAddress[i])
    print('')

for token in open("kanka_token.txt"):
    token = token.rstrip('\r\n')
headers = {'Authorization': 'Bearer ' + token}

#  beautiful soup exceeds python's recursion limit
sys.setrecursionlimit(5000)

#  open session
s = requests.Session()
s.headers.update(headers)

#  create temp file to write unchanged and new values to
with open("temp.txt", 'w') as temp:
    temp.write('endpoint,updated\n')
    #  get request for each page
    #  open stored endpoints with "last updated"
    soup_string = ''
    for i in range(len(masterList)):
        endpoint = masterList[i]
        #  print("endpoint ", endpoint)
        #  get webpage
        response = get(endpoint)
        #  print(response.status_code)
        #  print(response)
        response.raise_for_status()  # end if error
        #  beautiful soup object to string
        #  Parse the html content
        try:
            soup_string = str(bs(response.text, 'html5lib'))
            print ("success" + endpoint)
        except:
            email("An error has occurred in kanka updater", "johnatling@gmail.com")
        #  print(soup_string)
        #  finds ID number for each linked page
        id_num = re.findall(r'(?<="id":)\d+', soup_string)
        #  print(id_num)
        #  finds time after last updated for above
        updated = re.findall(r'(?<="updated_at":")\d\d\d\d\W\d\d\W\d\d\w\d\d\W\d\d\W\d\d', soup_string)
        #  print(updated)
        #  writes all endpoints and last update to temp
        for x in range(len(id_num)):
            temp.write(masterList[i] + '/' + id_num[x] + ',' + updated[x] + '\n')

with open("temp.txt", 'r') as f1, open("checklist.txt", 'r') as f2:
    new = csv.DictReader(f1, delimiter=',')
    old = csv.DictReader(f2, delimiter=',')
    line_count = 1
    new_updated = "New pages for reading: "
    #  for row in csv_reader:
    for new_row in new:
        found = False
        for old_row in old:
            if new_row["endpoint"] == old_row["endpoint"]:
                found = True
                if new_row["updated"] != old_row["updated"]:
                    found = True
                    #  add to list of new pages
                    new_updated += ('https://kanka.io/en-US/campaign/' + new_row["endpoint"] + '\n')
                break
        if found == False:
            new_updated += ('https://kanka.io/en-US/campaign/' + new_row["endpoint"] + '\n')
            NEW = True

#  rename temp file as checklist.txt
os.rename(r'/path/to/file/temp.txt',r'/path/to/file/checklist.txt')

if NEW == True:
    print('Subject: Change Alert!\n\nUpdate on kanka!\n' + new_updated + "\nFrom RaspberryPi")
    #  email(new_updated, toAddress)