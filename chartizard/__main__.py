import os
import logging
from dotenv import load_dotenv

from client import ChartizardClient

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load token from env
load_dotenv()
if token := os.environ.get('DISCORD_TOKEN'):
  token = os.environ['DISCORD_TOKEN']
  logging.info("👍 Found discord token!")
else:
  raise RuntimeError('👎 Expected environment variable "DISCORD_TOKEN"')


if __name__ == '__main__':
  client = ChartizardClient()
  client.run(token)
