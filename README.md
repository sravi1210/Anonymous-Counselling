# Anonymous-Counselling
This is a annonymous counselling platform developed my us at Students web committee for a accesible counselling envirnment for institute students.

### Workflow of the portal:

* Home page has button for student to start talking to the counsellor which will redirect the user to a window. On clicking connect to counsellor, if any of the counsellor are active, student will be redirected to a new chat session and counsellor will be notified about the waiting student. 
* When a student will be redirect to chat session, a alert is shown to send "Hi" to start a conversation. 
* After that student will see a message showing to wait till counsellor joins the chat session.
* Once the counseller joins the chat session, both will see each others sent messages and anonymous user can talk with counsellor freely witohut any hesitation.
* Counsellors have the right to abort any chat session via abort option. So if they the student is misusing the platform or something inappropriate, they can close the chat session.
* When a chat of the user with counsellor will end, counsellor will abort the chat session and both counsellor and user will be redirected to their respective home. Aborting a chat session will delete all messages which were sent and received in that chat session.
* To improvise, we have added sessions to the chatrooms (that is why chat sessions). So if for 10 minutes, user isn't responding or there is no activity from user side, whenver user or counsellor will refresh the page, chat session will get deleted.
* To improvise further, if there are any chat sessions which remained unattended for more than 10 minutes by both counsellor and user, a automatic function running in background will make sure that the chat session is deleted. 
 
 
### To run the project on your machine:
```
$ git clone https://github.com/sravi1210/Anonymous-Counselling.git
$ cd Anonymous-Counselling
$ pip3 install -r requirements.txt
$ cd portal
$ python3 manage.py runserver
```
