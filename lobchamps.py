import discord
from discord import app_commands
import random

# All 171 League of Legends champions as of October 2025
CHAMPIONS = [
    "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Ambessa", "Amumu", "Anivia", "Annie", "Aphelios",
    "Ashe", "Aurelion Sol", "Aurora", "Azir", "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", "Briar",
    "Caitlyn", "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko",
    "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar",
    "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei", "Illaoi", "Irelia", "Ivern", "Janna",
    "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "K'Sante", "Kai'Sa", "Kalista", "Karma", "Karthus",
    "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc",
    "Lee Sin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai",
    "Master Yi", "Mel", "Milio", "Miss Fortune", "Mordekaiser", "Morgana", "Naafiri", "Nami", "Nasus", "Nautilus",
    "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu & Willump", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy",
    "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "Rek'Sai", "Rell", "Renata Glasc", "Renekton", "Rengar",
    "Riven", "Rumble", "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen",
    "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Smolder", "Sona", "Soraka", "Swain", "Sylas",
    "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere",
    "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex", "Vi",
    "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo",
    "Yone", "Yorick", "Yunara""Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"
]

ROLES = ["Top", "Jungle", "Mid", "ADC", "Support"]

# Role emojis for better visuals
ROLE_EMOJIS = {
    "Top": "⚔️",
    "Jungle": "🌲",
    "Mid": "🔮",
    "ADC": "🏹",
    "Support": "🛡️"
}

class LoLBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True  # Enable voice state tracking
        intents.guilds = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = LoLBot()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'Bot is ready in {len(client.guilds)} guilds')

@client.tree.command(name="bravery", description="Get a random League of Legends champion and role!")
async def bravery(interaction: discord.Interaction):
    """Single player gets a random champion and role."""
    champion = random.choice(CHAMPIONS)
    role = random.choice(ROLES)
    emoji = ROLE_EMOJIS[role]
    
    embed = discord.Embed(
        title="🎲 Ultimate Bravery!",
        description=f"**{interaction.user.mention}**, your destiny awaits!",
        color=discord.Color.gold()
    )
    embed.add_field(name="Champion", value=f"**{champion}**", inline=True)
    embed.add_field(name="Role", value=f"{emoji} **{role}**", inline=True)
    embed.set_footer(text="Good luck on the Rift!")
    
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="team", description="Generate a full team composition (5 unique roles)")
async def team(interaction: discord.Interaction):
    """Generate a balanced team with 5 unique roles."""
    champions = random.sample(CHAMPIONS, 5)
    roles = ROLES.copy()
    random.shuffle(roles)
    
    embed = discord.Embed(
        title="🎯 Team Composition",
        description="Here's your balanced team setup!",
        color=discord.Color.blue()
    )
    
    for champion, role in zip(champions, roles):
        emoji = ROLE_EMOJIS[role]
        embed.add_field(
            name=f"{emoji} {role}",
            value=f"**{champion}**",
            inline=False
        )
    
    embed.set_footer(text="May the odds be in your favor!")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="bravery_party", description="Get random champions for multiple players")
@app_commands.describe(
    players="Number of players (1-10). Leave empty to use voice channel members!",
    use_voice="Automatically use everyone in your voice channel (overrides players count)"
)
async def bravery_party(
    interaction: discord.Interaction, 
    players: int = None,
    use_voice: bool = False
):
    """Generate random picks for multiple players or voice channel members."""
    
    voice_members = []
    
    # Check if user wants to use voice channel or is in one
    if use_voice or players is None:
        # Check if user is in a voice channel
        if interaction.user.voice and interaction.user.voice.channel:
            voice_channel = interaction.user.voice.channel
            # Get all members in the voice channel (excluding bots)
            voice_members = [member for member in voice_channel.members if not member.bot]
            
            if not voice_members:
                await interaction.response.send_message(
                    "❌ No users found in your voice channel (excluding bots)!",
                    ephemeral=True
                )
                return
                
            num_players = len(voice_members)
        else:
            await interaction.response.send_message(
                "❌ You must be in a voice channel to use this feature, or specify the number of players!",
                ephemeral=True
            )
            return
    else:
        # Use the specified number of players
        num_players = players
        
    if num_players < 1 or num_players > 10:
        await interaction.response.send_message(
            "❌ Please choose between 1 and 10 players!",
            ephemeral=True
        )
        return
    
    if num_players > len(CHAMPIONS):
        await interaction.response.send_message(
            f"❌ Cannot generate {num_players} unique picks. Maximum is {len(CHAMPIONS)}.",
            ephemeral=True
        )
        return
    
    champions = random.sample(CHAMPIONS, num_players)
    roles = random.choices(ROLES, k=num_players)
    
    embed = discord.Embed(
        title=f"🎲 Bravery Party ({num_players} Players)",
        description="Random picks for the whole squad!" + 
                   (f"\n🔊 Voice Channel: **{voice_channel.name}**" if voice_members else ""),
        color=discord.Color.purple()
    )
    
    for i, (champion, role) in enumerate(zip(champions, roles)):
        emoji = ROLE_EMOJIS[role]
        
        # Use voice member name if available, otherwise generic "Player X"
        if voice_members and i < len(voice_members):
            player_name = voice_members[i].display_name
            embed.add_field(
                name=f"**{player_name}**",
                value=f"**{champion}** {emoji} {role}",
                inline=False
            )
        else:
            embed.add_field(
                name=f"Player {i + 1}",
                value=f"**{champion}** {emoji} {role}",
                inline=False
            )
    
    embed.set_footer(text="Time to show your skills!")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="random_champ", description="Get a random champion (no role assigned)")
async def random_champ(interaction: discord.Interaction):
    """Just get a random champion without a role."""
    champion = random.choice(CHAMPIONS)
    
    await interaction.response.send_message(
        f"🎲 **{interaction.user.mention}**, your random champion is: **{champion}**!"
    )

@client.tree.command(name="random_role", description="Get a random role")
async def random_role(interaction: discord.Interaction):
    """Just get a random role."""
    role = random.choice(ROLES)
    emoji = ROLE_EMOJIS[role]
    
    await interaction.response.send_message(
        f"{emoji} **{interaction.user.mention}**, your random role is: **{role}**!"
    )

@client.tree.command(name="lol_help", description="Show all available commands")
async def lol_help(interaction: discord.Interaction):
    """Display help information."""
    embed = discord.Embed(
        title="🎮 LoL Random Champion Bot - Help",
        description="Generate random League of Legends champions and roles!",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="/bravery",
        value="Get a random champion and role for yourself",
        inline=False
    )
    embed.add_field(
        name="/team",
        value="Generate a balanced team (5 champions, 5 unique roles)",
        inline=False
    )
    embed.add_field(
        name="/bravery_party [players] [use_voice]",
        value="Get random picks for multiple players. Use `use_voice: True` to automatically assign to everyone in your voice channel!",
        inline=False
    )
    embed.add_field(
        name="/random_champ",
        value="Get just a random champion (no role)",
        inline=False
    )
    embed.add_field(
        name="/random_role",
        value="Get just a random role",
        inline=False
    )
    
    embed.set_footer(text=f"Total Champions: {len(CHAMPIONS)} | Roles: {len(ROLES)}")
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    import os
    
    # Get token from environment variable or replace with your token
    TOKEN = 'YOURTOKENGOESHERE'


    if not TOKEN:
        print("ERROR: Please set DISCORD_BOT_TOKEN environment variable")
        print("\nTo run this bot:")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create a new application")
        print("3. Go to 'Bot' section and create a bot")
        print("4. Copy the token and set it as environment variable:")
        print("   export DISCORD_BOT_TOKEN='your-token-here'")
        print("5. Enable 'MESSAGE CONTENT INTENT' in Bot settings")
        print("6. Go to OAuth2 > URL Generator")
        print("7. Select 'bot' and 'applications.commands' scopes")
        print("8. Select 'Send Messages' permission")
        print("9. Use the generated URL to invite the bot to your server")
    else:

        client.run(TOKEN)
