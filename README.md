# EVE-Infra-Indy-Index-Bot
An EVE Online reporting tool for Industry and Reaction Cost indexes

This tool is designed to interface with slack webhooks for reporting.

When ran, index_checker will make repeated ESI pulls to establish indexes, and prepare the report.

Then it will POST the finalized report to the SLACK WEBHOOK.

## CONFIG ##

### Runs on PYTHON 3.10

To configure this script properly, two SYSTEM ENVIORNMENT VARIABLES are required

INDY_BOT_ALLIANCE_ID - Set to an integer value for the Alliance ID of the target Alliance

INDY_BOT_SLACK_WEBHOOK_URL - Set to the slack webhook URL


### Config File -

The default config file will track systems owned by BRAVE COLLECTIVE.

To add or modify the list of alliances, insert their alliances IDs into the config file.

The webhook values currently stored will allow the administrator to determine where the system will attempt to send the outputs.

Currently these settings are not utilized.

### PIP Libraries Required:

Requests

## Future Ideas ##

Multi-alliance tracking

Discord functionality

Config file for easy modification
