# medDesk
This is a flask based web platform for user queries related to medical precautions, symptoms and nearby hospital. This uses gmaps API to plot the directions of recommended hospital from the user's current location. The user's current location is collected by first taking consent from the user and then setting it in the session variable to be furthar used by the module responsible for finding nearest hospital present in the data set in /hospital_data folder which has been preprocessed using the IPython notebook present in the same directory.
The registration process has a two factor authentication as it uses OTP validation to verify email id provided by users. The mail service uses Gmail API to send emails.
intents.json file contains some data which is used to train our chatbot and contemplate the user queries. Basically there are tags associated to each intent which has some set of responses which is selected randomly. The database file is present in the root directory of this repository "meddesk.sql".

