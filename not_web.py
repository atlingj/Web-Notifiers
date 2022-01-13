import bs4, requests, smtplib, re, sys, hashlib

# email list--------------------------------------------------
toAddress = ['name@email.com']
# ------------------------------------------------------------

address = "https://krebsonsecurity.com/"

NEW = False
#  download page
getPage = requests.get(address)
getPage.raise_for_status()  # end if error

#  gets most recent article from website
soup = bs4.BeautifulSoup(getPage.text, 'html.parser')
print(soup)
first_article = soup.select('.entry-title')[0]
text = first_article.find('a', href=True)
link = text['href']

#  string to bytes
byte_article = first_article.encode(encoding='utf-8')
#  create unique hash
hash_object = hashlib.sha1(byte_article)
digest = hash_object.hexdigest()

#  open stored digest file
#  compare and overwrite
old_hashes = open("hash.txt", "r")
pos_1 = (old_hashes.readline())
if pos_1 != digest:
    NEW = True
    old_hashes.close()
    old_hashes = open("hash.txt", "w")
    old_hashes.write(digest)

if NEW == True:
    conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
    conn.ehlo()  # call this to start the connection
    conn.starttls()  # starts tls encryption. When we send our password it will be encrypted.
    conn.login('name@email.com', 'password')
    conn.sendmail('name@email.com', toAddress, 'Subject: Change Alert!\n\nNew Krebs article!' + str(link))
    conn.quit()
    print('Sent notification e-mails for the following recipients:\n')
    for i in range(len(toAddress)):
        print(toAddress[i])
    print('')
else:
    print('You have no new reading.')
