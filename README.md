# Transaction helper 
## Warnings
### It is highly advised that you not actually use this for any person information about yourself or a client at this time as there is not securty and all the data that it stores is all to easily accessed through some very simple means. 

### Description
Transaction helper is a Web based program serving as a centralized hub, empowering agents to efficiently coordinate and track various tasks, documents, and milestones involved in real estate transactions. It enables seamless collaboration between agents, clients, and other involved parties, ensuring smooth and transparent communication.

### How it works
This program uses the Flask framework to generate forms that can be used to make changes to the text of a document. It creates a folder on the server named after the client and then with some pregenerated text files or ones uploaded by the user, it will generate a list of all the placeholders in the template file, then usiung the form will replace the placeholder text. It will then generate a page with the text completed for copying into an email.

### usage
After the git pull and all prerequistes are downloaded, use `$ flask run` to start a local server on http://localhost:5000/

The main page will load and ask for 
