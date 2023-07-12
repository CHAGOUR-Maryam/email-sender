"""
This code allows you to send emails with personalized attachments.
    EMAIL_SUBJECT : subject of email
    EMAIL_CONTENT : content of email
    ATTACHEMENT_FILE_DIRECTORY : the directory of all attached files
    EMAILS_TO : list of all emails reacivers
"""
import ssl
import smtplib
import streamlit as st
from email.message import EmailMessage
from common import common_pages_menu as cf
from common import common_alert_messages as cam
from streamlit_quill import st_quill
import os.path
import shutil




#EMAIL SENDER INTERFACE
st.markdown("""
      #  **:blue[Send Emails]**
""")

with st.expander("**:blue[STEPS TO DO BEFORE SENDING AN EMAIL]**"):
    st.markdown("""
        You should get the password from the 2 step verification 
        
        Here are the steps you should follow : 
        https://www.arysontechnologies.com/gmail-backup-software/turn-on-two-step-verification.html
    """)

st.markdown("**Sender email:  :red[*]** ")
EMAIL_ADDRESS = st.text_input("sender email", label_visibility="collapsed")

st.markdown("**Password:  :red[*]**")
PASSWORD = st.text_input("password", label_visibility="collapsed")

st.divider()

st.markdown("**Receiver emails:** (Enter the Emails seperated by a **LIGNE**)  **:red[*]**")
EMAILS_TO = st.text_area("receiver email", label_visibility="collapsed")


st.markdown("**Subject:  :red[*]**")
SUBJECT = st.text_input("subject", label_visibility="collapsed")

st.markdown("**Body:  :red[*]**")
EMAIL_CONTENT=st.text_area("body", label_visibility="collapsed")

st.markdown("**Attached file:**")
ATTACHEMENT_FILES = st.file_uploader("body", label_visibility="collapsed",accept_multiple_files=True)




#GET ALL THE EMAILS_TO IN A LIST
EMAILS_TO = EMAILS_TO.splitlines()



if st.button('SEND'):
    directory = "/send_emails"

    parent_dir = os.path.expanduser("~/")

    path = os.path.join(parent_dir, directory)

    if os.path.exists(path):
        print("folder already exists")
    else:
        os.mkdir(path)

    for email_to in EMAILS_TO:
        try:
            #email_to = email_to.strip() #removing white space in the start and at the end
            msg = EmailMessage()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email_to
            msg['Subject'] = SUBJECT
            msg.set_content(EMAIL_CONTENT)
            emails_to_cc = [email_to]

            for attachement_file in ATTACHEMENT_FILES:
                ATTACHEMENT_FILE_DIRECTORY=os.path.join(path, attachement_file.name)
                with open(ATTACHEMENT_FILE_DIRECTORY, "wb") as f:
                    f.write(attachement_file.getbuffer())
                filename = ATTACHEMENT_FILE_DIRECTORY

                with open(filename, 'rb') as f:
                    msg.add_attachment(f.read(), maintype='application', subtype='octet-stream',filename=attachement_file.name)


            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(EMAIL_ADDRESS, PASSWORD)

                smtp.sendmail(EMAIL_ADDRESS, emails_to_cc, msg.as_string())



        except(FileNotFoundError):
            print("--- ERROR  file not found: ")
            st.warning(" ERROR  file not found:")

        except(smtplib.SMTPRecipientsRefused):
            print("--- ERROR Email not correct for : ")
            st.warning(" ERROR  Email not correct for :")

        except():
            print("--- ERROR Other error for : ")
            st.warning(" ERROR Other error:")


    cam.alert_success()
    shutil.rmtree(path)
