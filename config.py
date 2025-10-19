import os, json
import dotenv

dotenv.load_dotenv(".env", override=True)

prefix = os.getenv("PREFIX")
USER_ID = int(os.getenv("USER_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
countdown_dict = json.loads(os.getenv("COUNTDOWN_DATES"))
starting_time_channel_id = int(os.getenv("STARTING_TIME_CHANNEL_ID"))
countdown_channel_id = int(os.getenv("COUNTDOWN_CHANNEL_ID"))