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

INDY_BOT_DISCORD_WEBHOOK_URL - Set to the discord webhook URL


### Config File -

The default config file will track systems owned by BRAVE COLLECTIVE.

To add or modify the list of alliances, insert their alliances IDs into the config file.

Slack and Discord integration are both supported.

The slack + discord boolean values in config.json will control which service(s) the system will attempt to send the output to.

### PIP Libraries Required:

Requests

## Future Ideas ##

Discord functionality
