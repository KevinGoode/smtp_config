# SMTP Config

This directory contains some notes and links about how to deploy and configure the SMTP server: postfix on a raspberry pi. The SMTP server is configured to prevent relay of messages to external mail servers unless a local user logs in.  Sample python code illustrates the main 2 use cases:
1.) Send email to local domain (no login)
2.) Relay email to external domain (login)
  
## Settings up Postfix and associated tools


## Running example code

To generate code for a new database :

1.) Run: python3 smtp.py to see env variables to set
```console
[goode@localhost smtp]$ python3 smtp.py
Required Env variable 'SMTP_DOMAIN_NAME' is missing.
Must set all of the following env variables to proceed:
['SMTP_DOMAIN_NAME', 'SMTP_USER', 'SMTP_PASS', 'SMTP_FROM_EMAIL_IN_ORG', 'SMTP_TO_EMAIL_IN_ORG', 'SMTP_TO_EMAIL_OUTSIDE_ORG']
```

2.) Set env variables: eg export SMTP_DOMAIN_NAME=some.domain.name or edit set_env file and execute:
```console
source set_env
```
3.)  Run: python3 smtp.py

```console
[goode@localhost smtp]$ python3 smtp.py
2020-06-16 11:19:08,576 [INFO] SMTP Connecting...
2020-06-16 11:19:09,707 [INFO] SMTP Connected
2020-06-16 11:19:10,007 [INFO] SMTP Logged in
2020-06-16 11:19:10,156 [INFO] SMTP Sent email successfully.
2020-06-16 11:19:10,195 [INFO] SMTP Connecting...
2020-06-16 11:19:10,578 [INFO] SMTP Connected
2020-06-16 11:19:10,837 [INFO] SMTP Sent email successfully.
```
NOTE: An encrypted file example.gpg contains a real world example configuration. To unencrypt and use these variables
```console
gpg -d example.gpg > example
source example
python3 smtp.py
```

