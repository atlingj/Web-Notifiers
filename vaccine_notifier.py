import bs4, requests, smtplib, re, sys

# email list--------------------------------------------------
toAddress = ['name@email.com']
# ------------------------------------------------------------

address = "https://www.boots.ie/health/covid-19/covid-vaccination"
quote = "Due to large demand we currently have no further appointments available for the Janssen COVID-19 single dose vaccine."

NEW = False
#  download page
getPage = requests.get(address)
getPage.raise_for_status()  # end if error

#  get text from Boots' vaccination webpage
soup = bs4.BeautifulSoup(getPage.text, 'html.parser')
#  Checks for non-availability
Vacc_status = soup.find_all(string=re.compile(quote))
print(Vacc_status)
#  print("vac status =", Vacc_status[1])
if Vacc_status == None:
    sys.exit()

conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
conn.ehlo()  # call this to start the connection
conn.starttls()  # starts tls encryption. When we send our password it will be encrypted.
conn.login('name@email.com', 'password')
conn.sendmail('name@email.com', toAddress, 'Subject: Change Alert!\n\nBoots vaccine registration!!!' + address + '\n\nChange Notifier V1.0')
conn.quit()
print('Sent notification e-mails for the following recipients:\n')
for i in range(len(toAddress)):
    print(toAddress[i])
    print('')
