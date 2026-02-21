from highrise.__main__ import *
import traceback
import time
import sys
import logging
from datetime import datetime

# Setup logging
log_file = f"bot_logs_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("Bot starting up...")

# Bot configuration - Using fixed party 2 bot
# Format: (python_file_name, bot_class_name, room_id, bot_token)
bot_configs = [
    ("party 2", "PARTY", "698841da4ff421fb4deed7bd", "e0392717b3c46932f8ac506941e2df7d7c92fb3cd5abe63eb2cdac969b2519e3")
]

bots = []

for bot_file_name, bot_class_name, room_id, bot_token in bot_configs:
    try:
        bot_module = __import__(bot_file_name)
        bot_class = getattr(bot_module, bot_class_name)
        bot = BotDefinition(bot_class(), room_id, bot_token)
        bots.append(bot)
        logger.info(f"Loaded bot: {bot_class_name} from {bot_file_name}")
    except Exception as e:
        logger.error(f"Failed to load bot {bot_file_name}: {e}")
        traceback.print_exc()

if not bots:
    logger.critical("ERROR: No bots loaded! Cannot start.")
    sys.exit(1)

# Main loop with error handling
while True:
    try:
        logger.info(f"Starting {len(bots)} bot(s)...")
        arun(main(bots))
    except KeyboardInterrupt:
        logger.warning("Bot stopped by user (Ctrl+C)")
        break
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        traceback.print_exc()
        logger.info("Restarting in 10 seconds...")
        time.sleep(10)