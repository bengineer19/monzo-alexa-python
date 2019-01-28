# Monzo-Alexa-Python
An Alexa skill for querying a Monzo account, written in Python.

Currently the skill supports:
* Asking for the current account balance
* Asking how much has been spent this month
* Whether a particular purchase is affordable in relation to a monthly budget.
(eg "Alexa, can I afford an echo dot")

## Configuring Alexa intents, utterances and slots
The `alexa_skill_config.json` contains the intents and utterances required.

## Configuring Monzo auth
### Via direct access token (not reccomended)
Set the environment variable `ACCESS_TOKEN` in AWS Lambda configuration.
This will directly provide query access to the Monzo API.

### Via Oauth
Coming soon...
