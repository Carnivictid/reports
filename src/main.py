from O365 import Connection, FluentInbox
from client import Client
from time import sleep
import getpass
import soupy
import utils
import sys


JSONPATH = "config.json"
USERNAME = input("Enter your O365 email address: ")
PASSWORD = getpass.getpass("Enter the password: ")


def get_inbox():
    Connection.login(*(USERNAME, PASSWORD))
    return FluentInbox()

def main():
    # Get the contents of the config JSON
    jcontents = utils.open_json(JSONPATH)
    auth = (USERNAME, PASSWORD)
    
    # Make an empty array to store the client objects
    client_objects = []
    
    # Iterate through the JSON, and make an object for each client 
    for json_config in jcontents["technician"]["clients"]:
        new_client = Client(json_config)
        client_objects.append(new_client)
        
    # Connect to the Office 365 inbox, get a list of emails
    inbox = get_inbox()
    emails_list = inbox.from_folder('Monthly Reports').fetch_next(50) # magic
    
    # Download all the attachments locally
    # This needs a serious rework, it is very unoptimized!
    for client_obj in client_objects:
        for email in emails_list:
            for report_email in client_obj.client_emails:
                if email.getSubject() == report_email["subject"]:
                    email.fetchAttachments()
                    if email.attachments[0].save("./pdfs/"):
                        client_obj.downloaded_report_count += 1
                    else:
                        raise ValueError("File save error!")
                        
        if client_obj.report_count != client_obj.downloaded_report_count:
            raise ValueError("Missing File: {}".format(client_obj.client_name))
    
    # Parse each document and make a dict of scores
    for client in client_objects:
        sd, ns = soupy.get_score_dict("./pdfs/"+client.client_emails[0]["filename"])   
        client.set_scores_dict(sd)
        client.set_network_health_score(ns)
    
    # For each client, generate a report based on the scores.
    for count, client in enumerate(client_objects):
        #if count == 1: # Comment in and set break point for testing.
            #break
        if client.network_score == 0:
            print("NO MANAGED SERVICES FOR {}!".format(client.client_name))
        else:
            e_email = client.build_email()
            print("Sending email for: {}... Status: ".format(client.client_name), end="")
            print(client.send_email(e_email, auth))
            sleep(10)

    return 0


if __name__ == "__main__":
    sys.exit(main())
