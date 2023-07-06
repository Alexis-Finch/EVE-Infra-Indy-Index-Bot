# EVE Infra Indy Index Bot

The purpose of this program is to present a list of cost indexes for Manufacturing and Reactions for an alliance (or alliances) in EVE Online

The data can then be sent to Discord or Slack

Set it up on a CRON job or task scheduler to cycle regularly, and it'll keep you up to date on the cost indexes in your systems! 

When ran, index_checker will make ESI pulls to establish indexes, and prepare the report.

Then it will POST the finalized report to the SLACK or DISCORD WEBHOOK.

## CONFIG ##

### Runs on PYTHON 3.10

To configure this script properly, SYSTEM ENVIORNMENT VARIABLES are required

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

