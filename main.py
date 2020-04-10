import csv
from gmailAuth import generateService
from email.mime.text import MIMEText
import base64

DESTINATION_ADDRESS = 'willsmith203+kqychyoydzne7jfnjwqj@boards.trello.com'
SENDER_ADDRESS = 'willsmithte@gmail.com'

def boldStyler(text):
    return '**' + text + '**'

with open('epics.csv', 'r') as file:
    csvReader = csv.reader(file)
    headers = next(csvReader)
    for line in csvReader:
        title = line[0]
        full = line[1]
        words = full.split(' ')
        asA = ' '.join(words[0:2])
        iWant = ' '.join(words[3:5])
        description = ' '.join([boldStyler(asA), words[2], boldStyler(iWant), ' '.join(words[5:])])
        
        emailSubject = title + ' #Feature'
        emailBody = '## User Stories\n' + description

        message = MIMEText(emailBody)
        message['to'] = DESTINATION_ADDRESS
        message['from'] = SENDER_ADDRESS
        message['subject'] = emailSubject
        
        messageToSend = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        try:
            service = generateService()
            message = (service.users().messages().send(userId='me', body=messageToSend).execute())
        except Exception as error:
            print(error)