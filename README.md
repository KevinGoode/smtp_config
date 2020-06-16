# SMTP Config

This directory contains some notes and links about how to deploy and configure the SMTP server: postfix on a raspberry pi. The SMTP server is configured to prevent relay of messages to external mail servers unless a local user logs in.  Sample python code illustrates the main 2 use cases:
 1. Send email to local domain (no login)   
 2. Relay email to external domain (login) 
 
 NOTE. Example files that are edited in the the following instructions are encrypted and provided in confs directory.
 
## Settings up Postfix and associated tools
 
 1. Install postfix. Note the installer brings up a '[ncurses](https://tldp.org/HOWTO/NCURSES-Programming-HOWTO/index.html)' type terminal ui to configure postfix. In this configuration ui select 'internet' then enter the domain name of the mail server . That should be all that is required. This will create the file:  /etc/postfix/main.cf
```console
sudo apt-get postfix
```
 2. Create any new users and add to sudoers,
```console
sudo adduser USER_NAME
sudo adduser USER_NAME sudo
```
3. Configure postfix to map local linux users to user emails (See [this ](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-on-ubuntu-16-04) link)
```console
sudo postconf -e 'home_mailbox= Maildir/'
sudo postconf -e 'virtual_alias_maps= hash:/etc/postfix/virtual'
sudo nano /etc/postfix/virtual
```

| /etc/postfix/virtual |
----|-----
| contact@example.com sammy |
|admin@example.com sammy
  |
```console
sudo postmap /etc/postfix/virtual
sudo systemctl restart postfix
```
4. Install and configure a simple mail client (s-nail) (Again see [this ](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-on-ubuntu-16-04) link for details)
```console
echo 'export MAIL=~/Maildir' | sudo tee -a /etc/bash.bashrc | sudo tee -a /etc/profile.d/mail.sh
source /etc/profile.d/mail.sh
sudo apt-get install s-nail
sudo nano /etc/s-nail.rc
```
| /etc/s-nail.rc |
----|-----
| set emptystart |
| set folder=Maildir|
| set record=+sent|
5. Initialise users email directory ~/Maildir by sending an email or manually by
```console
mkdir ~/Maildir/tmp
mkdir ~/Maildir/cur
mkdir ~/Maildir/new
```
6. Start sending emails eg from hotmail to username@domainname and should see them turn up in: /home/USERNAME/Maildir/new. Can also view email from s-nail. See s-nail documentation or just type s-nail to see current list of emails.
<![endif]-->

NOTE: Emails can be sent to anywhere BUT when sent from your new local domain hotmail anti spam might send email back. Other email providers might put email in Junk because your domain might be deemed to be suspicious.
7. Set relay restrictions in /etc/postfix/main.cf (See comments [here](https://serverfault.com/questions/540714/my-postfix-is-letting-me-send-emails-through-it-without-a-username-password-ho))
```console
smtpd_relay_restrictions = permit_sasl_authenticated, reject_unauth_destination
```
NOTE: To restrict emails only from this domain you could set
smtpd_relay_restrictions = permit_sasl_authenticated, reject

8. Install and configure dovecot to force login when using smtp as a relay. Follow the instructions [here](https://samhobbs.co.uk/2013/12/raspberry-pi-email-server-part-2-dovecot) carefully. Basically edit the following files and restart services:
```console
nano /etc/dovecot/dovecot.conf
nano /etc/dovecot/conf.d/10-mail.conf
nano /etc/postfix/main.cf
nano /etc/dovecot/conf.d/10-master.conf
nano /etc/dovecot/conf.d/10-auth.conf
sudo service postfix restart
sudo service dovecot restart
```


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

## FAQ

 1. Any errors inspect mail log /var/log/mail.log
 2. If get this error: 'postdrop: warning: unable to look up public/pickup: No such file or directory' then see [here](https://www.linode.com/community/questions/11614/unable-to-sendmail-via-postfix-on-ubuntu-server): 
 ```console
 sudo mkfifo /var/spool/postfix/public/pickup
 ```
 
