Send emails with proton-bridge email client

You must have an instance of the Proton-Bridge client running
This uses a localhost loopback on 127.0.0.1 with port 1025
The Proton-Bridge client is responsible for sending the emails

The scripts expect that a .env file is located in the 
root directory with the format outlined below:

    UNAME = "proton-email@youraddress.com"
    PASS = "password-from-proton-bridge-not-account"

Once Proton-Bridge is configured, you will need the run the 
email_server.py script in a TMUX session and then 
can use the compose_email function to send Text and HTML through
email to any number of senders. You must use an email that
is registered with the Proton-Account as the "from" address

The "to-list" of emails must be one of the following:

    Python List
    Pandas Series
    Numpy Arrary


Currently the compose_email.py script will need to be
manually changed to alter the emails but this will
change with later iterations. 
