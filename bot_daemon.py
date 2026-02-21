"""
Highrise Bot - 24/7 Daemon Service
Runs as background service even when laptop is closed or logged out
"""
from highrise.__main__ import *
import traceback
import time
import sys
import logging
from datetime import datetime
import os
import signal

# Setup logging to a persistent log file
log_dir = "bot_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"bot_daemon_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global variable for graceful shutdown
shutdown_requested = False

def signal_handler(signum, frame):
    global shutdown_requested
    logger.warning("Shutdown signal received")
    shutdown_requested = True

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def run_bot():
    """Main bot runner function"""
    logger.info("=" * 60)
    logger.info("HIGHRISE BOT DAEMON V1.0 STARTING")
    logger.info("=" * 60)
    
    # Bot configuration
    bot_configs = [
        ("party", "PARTY", "698841da4ff421fb4deed7bd", "e0392717b3c46932f8ac506941e2df7d7c92fb3cd5abe63eb2cdac969b2519e3")
    ]
    
    bots = []
    
    # Load bots
    for bot_file_name, bot_class_name, room_id, bot_token in bot_configs:
        try:
            bot_module = __import__(bot_file_name)
            bot_class = getattr(bot_module, bot_class_name)
            bot = BotDefinition(bot_class(), room_id, bot_token)
            bots.append(bot)
            logger.info(f"✓ Loaded bot: {bot_class_name} from {bot_file_name}")
        except Exception as e:
            logger.error(f"✗ Failed to load bot {bot_file_name}: {e}")
            traceback.print_exc()
    
    if not bots:
        logger.critical("ERROR: No bots loaded! Cannot start.")
        sys.exit(1)
    
    logger.info(f"Successfully loaded {len(bots)} bot(s)")
    logger.info("=" * 60)
    
    # Main loop with error handling
    restart_count = 0
    while not shutdown_requested:
        try:
            restart_count += 1
            logger.info(f"[ATTEMPT #{restart_count}] Starting {len(bots)} bot(s)...")
            logger.info(f"Bot actively connecting to Highrise...")
            arun(main(bots))
            logger.warning("Main connection loop ended unexpectedly")
        except KeyboardInterrupt:
            logger.warning("Bot stopped by user (Ctrl+C)")
            break
        except ConnectionError as e:
            logger.error(f"✗ Connection lost: {e}")
            if not shutdown_requested:
                logger.info("Attempting to reconnect in 10 seconds...")
                time.sleep(10)
        except Exception as e:
            logger.error(f"✗ Exception occurred: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            if not shutdown_requested:
                logger.info("Bot will restart in 10 seconds...")
                time.sleep(10)
    
    logger.info("=" * 60)
    logger.info("BOT DAEMON SHUTDOWN")
    logger.info("=" * 60)

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)
