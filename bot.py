import disnake

from disnake.ext import commands
from disnake.ext.commands import Param
from disnake.utils import get

import os

# Environment Variables
from dotenv import load_dotenv

dotenvDir = "token_container/"
load_dotenv(os.path.join(dotenvDir, '.env'))

token = os.environ.get("token")

testEnv = [772518966777741372]

mediationClient = disnake.Client()
intents = disnake.Intents.default()
mediationBot = commands.Bot(command_prefix="!", help_command=None, sync_permissions = True, intents=intents, test_guilds=testEnv)

async def role_autocomp(inter: disnake.ApplicationCommandInteraction, user_input: str):
	VARIANTS = [inter.guild.get_role(780461582580056114).name, inter.guild.get_role(780461634396487701).name, inter.guild.get_role(933787975475658802).name]
	return [var for var in VARIANTS if user_input.lower() in var]

@mediationBot.slash_command(name="assign", description="Assign an administrator role via the mediator.")
async def assignRole(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, role: str = Param(description = "The role to assign.", autocomp=role_autocomp)):
	for guildRole in inter.guild.roles:
		if guildRole.name.lower() == role.lower():
			await member.add_roles(guildRole)
			break
	await inter.response.send_message(f"Added {member.mention} to {guildRole.mention}.")

@commands.guild_permissions(guild_id = 772518966777741372, role_ids = {933785995814502430 : True})
@mediationBot.slash_command(name="addmin", description="Adds a community admin to the community admin role via the mediatior.", default_permission=False)
async def addAdmin(inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
	communityAdminRole = inter.guild.get_role(933785995814502430)
	if communityAdminRole in inter.author.roles:
		await member.add_roles(communityAdminRole)
		await inter.response.send_message(f"Added {member.mention} to {communityAdminRole.mention}.")
	else:
		await inter.response.send_message(f"You do not have the required permissions to execute this command.")

@commands.guild_permissions(guild_id = 772518966777741372, role_ids = {933785995814502430 : True})
@mediationBot.slash_command(name="removeadmin", description="Remove yourself from the community admin role via the mediatior.", default_permission=False)
async def removeAdmin(inter: disnake.ApplicationCommandInteraction):
	communityAdminRole = inter.guild.get_role(933785995814502430)
	if communityAdminRole in inter.author.roles:
		await inter.author.remove_roles(communityAdminRole)
		await inter.response.send_message(f"Removed {inter.author.mention} from {communityAdminRole.mention}.")
	else:
		await inter.response.send_message(f"You do not have the required permissions to execute this command.")

mediationBot.run(token)