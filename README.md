# EVE-Infra-Indy-Index-Bot
An EVE Online reporting tool for Industry and Reaction Cost indexes

This tool is designed to interface with slack webhooks for reporting.

When ran, index_checker will make repeated ESI pulls to establish indexes, and prepare the report.

Then it will POST the finalized report to the SLACK WEBHOOK.

## CONFIG ##

### Runs on PYTHON 3.9

To configure this script properly, two SYSTEM ENVIORNMENT VARIABLES are required

INDY_BOT_ALLIANCE_ID - Set to an integer value for the Alliance ID of the target Alliance

INDY_BOT_WEBHOOK_URL - Set to the slack webhook URL


### PIP Libraries Required:

Requests

## Future Ideas ##

Multi-alliance tracking

Discord functionality

Config file for easy modification
