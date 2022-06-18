import os
import logging
import discord
from dotenv import load_dotenv
from client import ChartizardClient

if __name__ == '__main__':
  # Initialize logging
  logging.basicConfig(level=logging.INFO)

  # Load token from env
  load_dotenv()
  if token := os.environ.get('DISCORD_TOKEN'):
    token = os.environ['DISCORD_TOKEN']
    logging.info("👍 Found discord token!")
  else:
    raise RuntimeError('👎 Expected environment variable "DISCORD_TOKEN"')

  # Create client intents
  intents = discord.Intents.default()
  intents.reactions = True
  
  # Create client
  client = ChartizardClient(intents=intents)
  client.run(token)
