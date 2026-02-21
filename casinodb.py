import json
import threading
import shutil
import os
import sys
import types
from datetime import datetime

# Configuration - JUST CHANGE THESE NUMBERS
NUMBER_OF_BOTS = 15
NUMBER_OF_CASINO_BOTS = 0
DB_DIR = "DB"
os.makedirs(DB_DIR, exist_ok=True)

# Template for casino data
def create_casino_data():
    return {
        'bonuses': {},
        'total_players': 0,
        'active_players': 0,
        'total_bets': 0,
        'current_bets': 0,
        'total_wins': 0,
        'games_played': 0,
        'recent_winners': [],
        'hourly_stats': {
            'players': [0] * 24,
            'bets': [0] * 24,
            'updated': datetime.now().isoformat()
        }
    }

# Template for regular bot data
def create_regular_bot_data(instance_num=""):
    return {
        f"vip_users{instance_num}": [],
        f"msg{instance_num}": [],
        f"promo{instance_num}": [],
        f"ownerz{instance_num}": [],
        f"welcome{instance_num}": [],
        f"vip_loc{instance_num}": {},
        f"locations{instance_num}": {},
        f"bot_location{instance_num}": {},
        f"ranges{instance_num}": {},
        f"nicknames{instance_num}": {},
        f"bad_words{instance_num}": [],
        f"partyid{instance_num}": [],
        f"lids{instance_num}": [],
        f"language{instance_num}": [],
        f"user_ticket{instance_num}": {},
        f"data{instance_num}" if instance_num else "data": {}
    }

# Template for casino bot data
def create_casino_bot_data(instance_num=""):
    data = {
        f"ids{instance_num}": [],
        f"urls{instance_num}": {},
        f"owners{instance_num}": [],
        f"bot_location{instance_num}": {},
        f"wallet{instance_num}": {},
        f"casinodata{instance_num}": create_casino_data()
    }
    # Add table state for persistence
    data[f"table{instance_num}"] = create_table_data()
    return data

# Template for table data persistence
def create_table_data():
    return {
        "active": False,
        "players": {},
        "bet_timer_active": False,
        "game_timer_active": False,
        "dealer_hand": [],
        "dealer_value": 0,
        "dealer_blackjack": False,
        "drawing": False,
        "deck_state": None
    }

# Build the complete data mappings automatically
data_mappings = {}

# Only create instances if count is at least 1
if NUMBER_OF_BOTS >= 1:
    data_mappings.update(create_regular_bot_data())    # Regular bot 1

if NUMBER_OF_CASINO_BOTS >= 1:
    data_mappings.update(create_casino_bot_data())     # Casino bot 1

# Add numbered instances dynamically based on the larger of both counts
max_bots = max(NUMBER_OF_BOTS, NUMBER_OF_CASINO_BOTS)
for i in range(2, max_bots + 1):
    if i <= NUMBER_OF_BOTS:
        data_mappings.update(create_regular_bot_data(str(i)))
    if i <= NUMBER_OF_CASINO_BOTS:
        data_mappings.update(create_casino_bot_data(str(i)))

# Initialize global variables (keeping your exact variable names)
for key, value in data_mappings.items():
    globals()[key] = value.copy() if hasattr(value, 'copy') else value

def get_folder_path(var_name):
    """Determine the folder path for a variable based on its name"""
    # Extract number from variable name
    def extract_number(name):
        # Find all digits at the end of the string
        digits = ''
        for char in reversed(name):
            if char.isdigit():
                digits = char + digits
            else:
                break
        return digits if digits else '1'

    number = extract_number(var_name)

    if var_name.startswith(('vip_users', 'msg', 'promo', 'ownerz', 'welcome', 
                          'vip_loc', 'locations', 'bot_location', 'ranges', 
                          'nicknames', 'bad_words', 'partyid', 'lids', 'language', 'user_ticket', 'data')):
        # Regular bot data
        folder_name = number
        return os.path.join(DB_DIR, folder_name)
    elif var_name.startswith(('ids', 'urls', 'owners', 'wallet', 'casinodata', 'table')):
        # Casino bot data
        folder_name = f"casino{number}"
        return os.path.join(DB_DIR, folder_name)
    else:
        return DB_DIR  # Fallback to main DB folder

def save_data():
    """Save all data to JSON files in separate folders with atomic writes."""
    try:
        try:
            total, used, free = shutil.disk_usage("/home/container")
            if free < 1024 * 1024:  # 1MB minimum free space
                print("Not enough disk space to save data.")
        except:
            pass

        for var_name in data_mappings.keys():
            folder_path = get_folder_path(var_name)
            os.makedirs(folder_path, exist_ok=True)
            filename = os.path.join(folder_path, f"{var_name}.json")
            temp_filename = filename + ".tmp"

            try:
                # Write to temporary file first
                with open(temp_filename, "w") as f:
                    json.dump(globals()[var_name], f, default=str, indent=2, ensure_ascii=False)
                # Atomic replace
                os.replace(temp_filename, filename)
            except Exception as e:
                print(f"Error saving {filename}: {e}")
                # Clean up temp file if it exists
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

    except Exception as e:
        print(f"Error in save_data: {e}")
    finally:
        threading.Timer(120, save_data).start()

def load_data():
    """Load all data from JSON files in separate folders with proper error handling."""
    for var_name, default_value in data_mappings.items():
        folder_path = get_folder_path(var_name)
        filename = os.path.join(folder_path, f"{var_name}.json")

        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    loaded_data = json.load(f)

                # Special handling for casinodata structures to ensure all keys exist
                if var_name.startswith("casinodata"):
                    merged_data = create_casino_data()
                    merged_data.update(loaded_data)
                    globals()[var_name] = merged_data
                # Special handling for table data
                elif var_name.startswith("table"):
                    merged_data = create_table_data()
                    merged_data.update(loaded_data)
                    globals()[var_name] = merged_data
                else:
                    globals()[var_name] = loaded_data

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"{filename} not found or corrupted, using default values: {e}")
            # Keep the existing default value, don't overwrite
        except Exception as e:
            print(f"Error loading {filename}: {e}, using default values")
            # Keep the existing default value, don't overwrite

# Direct reference functions for imports
def import_regular_bot_data(bot_number, global_namespace):
    """Import regular bot data into the global namespace using direct references"""
    if bot_number == 1:
        suffix = ""
    else:
        suffix = str(bot_number)

    variables_map = {
        'vip_users': f"vip_users{suffix}",
        'msg': f"msg{suffix}",
        'promo': f"promo{suffix}",
        'ownerz': f"ownerz{suffix}",
        'welcome': f"welcome{suffix}",
        'vip_loc': f"vip_loc{suffix}",
        'locations': f"locations{suffix}",
        'bot_location': f"bot_location{suffix}",
        'ranges': f"ranges{suffix}",
        'nicknames': f"nicknames{suffix}",
        'bad_words': f"bad_words{suffix}",
        'partyid': f"partyid{suffix}",
        'ids': f"lids{suffix}",
        'user_ticket': f"user_ticket{suffix}",
        'language': f"language{suffix}",
        'data': f"data{suffix}" if suffix else "data"
    }

    for local_name, global_name in variables_map.items():
        if global_name in globals():
            global_namespace[local_name] = globals()[global_name]

def import_casino_bot_data(bot_number, global_namespace):
    """Import casino bot data into the global namespace using direct references"""
    if bot_number == 1:
        suffix = ""
    else:
        suffix = str(bot_number)

    variables_map = {
        'ids': f"ids{suffix}",
        'urls': f"urls{suffix}",
        'owners': f"owners{suffix}",
        'bot_location': f"bot_location{suffix}",
        'wallet': f"wallet{suffix}",
        'casino': f"casinodata{suffix}",
        'table': f"table{suffix}"  # Add table to imports
    }

    for local_name, global_name in variables_map.items():
        if global_name in globals():
            global_namespace[local_name] = globals()[global_name]

# Create regular bot modules
def create_regular_bot_modules():
    """Create bot1, bot2, bot3, etc. modules for regular bots"""
    for bot_num in range(1, NUMBER_OF_BOTS + 1):
        module_name = f"casinodb.bot{bot_num}"
        bot_module = types.ModuleType(module_name)
        import_regular_bot_data(bot_num, bot_module.__dict__)
        sys.modules[module_name] = bot_module

# Create casino bot modules
def create_casino_bot_modules():
    """Create cbot1, cbot2, cbot3, etc. modules for casino bots"""
    for bot_num in range(1, NUMBER_OF_CASINO_BOTS + 1):
        module_name = f"casinodb.cbot{bot_num}"
        casino_bot_module = types.ModuleType(module_name)
        import_casino_bot_data(bot_num, casino_bot_module.__dict__)
        sys.modules[module_name] = casino_bot_module

# Initialize data first
load_data()

# Then create modules with the loaded data
create_regular_bot_modules()
create_casino_bot_modules()

# Start periodic saving
save_data()