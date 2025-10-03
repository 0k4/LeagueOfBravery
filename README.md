#  LeagueOfBravery
## LoL Random Champion + Role Picker - Discord Bot - Selfhosted


## Available Commands

- **`/bravery`** - Get a random champion and role (just for you!)
- **`/team`** - Generate a balanced 5-person team with unique roles
- **`/bravery_party [players]`** - Get random picks for multiple players (1-10)
- **`/bravery_party use_voice: True`** - Get random picks for everyone in your voice channel
- **`/random_champ`** - Get just a random champion
- **`/random_role`** - Get just a random role
- **`/lol_help`** - Show all available commands

## Features

- Beautiful Discord embeds with role emojis (⚔️🌲🔮🏹🛡️)
- Slash commands (modern Discord UI)
- User mentions in responses (doesn't work for party voice detection)
- Error handling for invalid inputs

## Setup Instructions



1. ### Install Required discord Package
```bash
pip install discord.py
```
2. ### Create a Discord Bot:

- Go to https://discord.com/developers/applications
- Click "New Application"
- Go to "Bot" section and click "Add Bot"
- Get the access token by clicking reset
- Enable "MESSAGE CONTENT INTENT" and "SERVER CONTENT INTENT" in Bot settings

3. ### Set your bot token:

- Replace the placeholder on line 244 with your actual token.
- e.g: TOKEN = 'MTQyMzU4NDc0Mzc0...'

4. ### Invite the bot to your server:
- Go to OAuth2 > URL Generator
- Select scopes: bot and applications.commands
- Select permissions: Send Messages, Use Slash Commands
- Copy and open the generated URL in browser and accept bot on discord

5. ### Run the bot:

```bash
python lobchamps.py
