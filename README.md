\# AI Registration Assistant



An intelligent conversational chatbot that guides students through an internship registration process using Natural Language Processing (NLP), intent recognition, entity extraction, validation, dialog management, and JSON-based storage.



\## Project Overview



The AI Registration Assistant is designed to help students complete an internship registration through a conversational interface.



The assistant can:



\- Greet users

\- Start a registration

\- Collect student information

\- Extract entities from natural language

\- Validate registration information

\- Manage conversation state

\- Answer frequently asked questions

\- Detect duplicate email registrations

\- Confirm registration details

\- Store completed registrations in JSON

\- Generate a unique registration ID

\- Handle invalid input and cancellation



\## Technologies Used



\- Python

\- NLTK

\- spaCy

\- Scikit-learn

\- Flask

\- JSON

\- Regular Expressions

\- Object-Oriented Programming



\## Project Structure



```text

ai-registration-assistant/

│

├── app/

│   ├── \_\_init\_\_.py

│   ├── routes.py

│   └── templates/

│       └── index.html

│

├── dialog/

│   ├── \_\_init\_\_.py

│   ├── state\_machine.py

│   ├── responses.py

│   └── assistant.py

│

├── nlp/

│   ├── \_\_init\_\_.py

│   ├── preprocessing.py

│   ├── intent\_classifier.py

│   ├── entity\_extractor.py

│   ├── intents.json

│   ├── faq.json

│   └── faq\_handler.py

│

├── registration/

│   ├── \_\_init\_\_.py

│   ├── validator.py

│   └── store.py

│

├── data/

│   └── registrations.json

│

├── tests/

│   └── test\_assistant.py

│

├── main.py

├── requirements.txt

├── .gitignore

└── README.md

