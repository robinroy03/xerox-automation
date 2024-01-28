# from labels
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# from draft (deleted duplicates)
import base64
from email.message import EmailMessage
import google.auth

from bs4 import BeautifulSoup 
import email
import lxml

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://mail.google.com/"]

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

# Save the credentials for the next run
with open("token.json", "w") as token:
    token.write(creds.to_json())

def gmail_create_draft():
  """Create and insert a draft email.
   Print the returned draft's message and id.
   Returns: Draft object, including draft id and message meta data.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
#   creds, _ = google.auth.default()

  try:
    # create gmail api client
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()

    message.set_content("meow?")

    message["To"] = "robin.roy2022@vitstudent.ac.in"
    message["From"] = "robin.roy2022@vitstudent.ac.in"
    message["Subject"] = "test"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}
    # pylint: disable=E1101
    draft = (
        service.users()
        .drafts()
        .create(userId="me", body=create_message)
        .execute()
    )

    print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    draft = None

  return draft

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmail_send_message():
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
#   creds, _ = google.auth.default()

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content("86")
    # print(service.users().messages().list(userId = 'me').execute())

    message["To"] = "robin.roy2022@vitstudent.ac.in"
    # message["From"] = "robin.roy2022@vitstudent.ac.in"
    message["Subject"] = "Heylo"
    # message["in-reply-to"] = "robin.roy2022@vitstudent.ac.in"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


def gmail_read_messages():
  try:
    service = build("gmail", "v1", credentials=creds)
    result = service.users().messages().list(userId = 'me').execute()

    messages = result.get('messages')

    for msg in messages:
      txt = service.users().messages().get(userId = 'me', id = msg['id']).execute()
      print(txt)
      try:       
        # Get value of 'payload' from dictionary 'txt' 
        payload = txt['payload'] 
        headers = payload['headers'] 

        # Look for Subject and Sender Email in the headers 
        for d in headers: 
            if d['name'] == 'Subject': 
                subject = d['value'] 
            if d['name'] == 'From': 
                sender = d['value'] 

        # The Body of the message is in Encrypted format. So, we have to decode it. 
        # Get the data and decode it with base 64 decoder. 
        parts = payload.get('parts')[0] 
        data = parts['body']['data'] 
        data = data.replace("-","+").replace("_","/") 
        decoded_data = base64.b64decode(data) 

        # Now, the data obtained is in lxml. So, we will parse  
        # it with BeautifulSoup library 
        soup = BeautifulSoup(decoded_data , "lxml") 
        body = soup.body() 

        # Printing the subject, sender's email and message 
        print("Subject: ", subject) 
        print("From: ", sender) 
        print("Message: ", body) 
        print('\n') 
      
      except Exception as e:
         print(e)
         pass
  
  except HttpError as error:
    print(f"An error occured {error}")



gmail_read_messages()
# gmail_send_message()
# gmail_create_draft()
