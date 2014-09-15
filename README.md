This server-side module reads through an email address once an hour for new messages. It was created to accomodate a supervisor who wanted auto-generated reports from MySQL data by sending an email to my address with the relevant information in the body of the email.

The file included is the main file, the "commands" file was ommited as it contained sensitive information. Essentially, it made a MySQL query, generated a gnuplot text file based on the data it found, executed it to create a graph of the data, converted the image into base64, and attached it to a mime-formated email, which it then sent back. 

Fairly straightforward, and made my life a lot easier.
