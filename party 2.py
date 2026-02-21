import sys
import math
import os
import time
from datetime import datetime, timedelta
import asyncio
from highrise import BaseBot, __main__
from highrise.models import User, SessionMetadata, Position
from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
import random
from datetime import datetime

# Import bot data - this will be populated by casinodb at runtime
try:
    from casinodb.bot1 import *
except (ImportError, ModuleNotFoundError):
    # Fallback if dynamic import fails - these will be initialized on_start
    vip_users = []
    msg = []
    promo = []
    ownerz = ["skybluoo","kar4n"]
    welcome = []
    vip_loc = {}
    locations = {}
    bot_location = {}
    ranges = {}
    nicknames = {}
    bad_words = []
    partyid = ["698841da4ff421fb4deed7bd"]  # ← YOUR ROOM ID
    ids = []
    user_ticket = {}
    language = []
    data = {}

emote_dict = {
    '1': ('idle-loop-sitfloor', 22.321055),
    '2': ('idle-enthusiastic', 15.941537),
    '3': ('emote-yes', 2.565001),
    '4': ('emote-wave', 2.690873),
    '5': ('emote-tired', 4.61063),
    '6': ('emote-snowball', 5.230467),
    '7': ('emote-snowangel', 6.218627),
    '8': ('emote-shy', 4.477567),
    '9': ('emote-sad', 5.411073),
    '10': ('emote-no', 2.703034),
    '11': ('emote-model', 6.490173),
    '12': ('emote-laughing', 2.69161),
    '13': ('emote-kiss', 2.387175),
    '14': ('emote-hot', 4.353037),
    '15': ('emote-hello', 2.734844),
    '16': ('emote-greedy', 4.639828),
    '17': ('emote-curtsy', 2.425714),
    '18': ('emote-confused', 8.578827),
    '19': ('emote-charging', 8.025079),
    '20': ('emote-bow', 3.344036),
    '21': ('emoji-thumbsup', 2.702369),
    '22': ('emoji-gagging', 5.500202),
    '23': ('emoji-flex', 2.099351),
    '24': ('emoji-celebrate', 3.412258),
    '25': ('emoji-angry', 5.760023),
    '26': ('dance-tiktok8', 11),
    '27': ('dance-tiktok2', 10.392353),
    '28': ('dance-shoppingcart', 4.316035),
    '29': ('dance-russian', 10.252905),
    '30': ('dance-pennywise', 4.214349),
    '31': ('dance-macarena', 12.214141),
    '32': ('dance-blackpink', 7.150958),
    '33': ('emote-hyped', 7.492423),
    '34': ('dance-jinglebell', 10.958832),
    '35': ('idle-nervous', 21.714221),
    '36': ('idle-toilet', 32.174447),
    '37': ('idle-floating', 27.791175),
    '38': ('dance-zombie', 12.922772),
    '39': ('emote-astronaut', 13.791175),
    '40': ('emote-swordfight', 5.914365),
    '41': ('emote-timejump', 4.007305),
    '42': ('emote-snake', 5.262578),
    '43': ('emote-float', 8.995302),
    '44': ('emote-telekinesis', 10.492032),
    '45': ('dance-pinguin', 11.58291),
    '46': ('dance-creepypuppet', 6.416121),
    '47': ('emote-sleigh', 11.333165),
    '48': ('emote-maniac', 4.906886),
    '49': ('emote-energyball', 7.575354),
    '50': ('emote-superpose', 4.530791),
    '51': ('emote-cute', 6.170464),
    '52': ('idle_singing', 13.791175),
    '53': ('emote-frog', 14.55257),
    '54': ('dance-tiktok9', 11.892918),
    '55': ('dance-weird', 21.556237),
    '56': ('dance-tiktok10', 8.225648),
    '57': ('emote-pose7', 4.655283),
    '58': ('emote-pose8', 4.808806),
    '59': ('idle-dance-casual', 9.079756),
    '60': ('emote-pose1', 2.825795),
    '61': ('emote-pose3', 5.10562),
    '62': ('emote-pose5', 4.621532),
    '63': ('emote-cutey', 3.26032),
    '64': ('emote-punkguitar', 9.365807),
    '65': ('emote-fashionista', 5.606485),
    '66': ('emote-gravity', 8.955966),
    '67': ('dance-icecream', 14.769573),
    '68': ('dance-wrong', 12.422389),
    '69': ('idle-uwu', 24.761968),
    '70': ('idle-dance-tiktok4', 15.500708),
    '71': ('emote-shy2', 4.989278),
    '72': ('dance-anime', 8.46671),
    '73': ('dance-kawai', 10.290789),
    '74': ('idle-wild', 26.422824),
    '75': ('emote-iceskating', 7.299156),
    '76': ('emote-pose6', 5.375124),
    '77': ('emote-celebrationstep', 3.353703),
    '78': ('emote-creepycute', 7.902453),
    '79': ('emote-pose10', 3.989871),
    '80': ('emote-boxer', 5.555702),
    '81': ('emote-headblowup', 11.667537),
    '82': ('emote-pose9', 4.583117),
    '83': ('emote-teleporting', 11.7676),
    '84': ('dance-touch', 11.7),
    '85': ('idle-guitar', 13.229398),
    '86': ('emote-gift', 5.8),
    '87': ('dance-employee', 8),
    '88': ('emote-looping', 8),
    '89': ('emote-kissing-bound', 10),
    '90': ('emote-zombierun', 9.182984),
    '91': ('emote-frustrated', 5.584622),
    '92': ('emote-slap', 2.724945),
    '93': ('emote-shrink', 8.738784),
    '94': ('dance-voguehands', 9.150634),
    '95': ('dance-smoothwalk', 6.690023),
    '96': ('dance-singleladies', 21.191372),
    '97': ('dance-orangejustice', 6.475263),
    '98': ('dance-metal', 15.076377),
    '99': ('dance-handsup', 22.283413),
    '100': ('dance-duckwalk', 11.748784),
    '101': ('dance-aerobics', 8.796402),
    '102': ('dance-sexy', 12.30883),
    '103': ('idle-dance-tiktok7', 12.956484),
    '104': ('sit-relaxed', 29.889858),
    '105': ('sit-open', 26.025963),
    '106': ('emoji-there', 2.059095),
    '107': ('emoji-sneeze', 2.996694),
    '108': ('emoji-smirking', 4.823158),
    '109': ('emoji-sick', 5.070367),
    '110': ('emoji-scared', 3.008487),
    '111': ('emoji-punch', 1.755783),
    '112': ('emoji-pray', 4.503179),
    '113': ('emoji-poop', 4.795735),
    '114': ('emoji-naughty', 4.277602),
    '115': ('emoji-mind-blown', 2.397167),
    '116': ('emoji-lying', 6.313748),
    '117': ('emoji-halo', 5.837754),
    '118': ('emoji-hadoken', 2.723709),
    '119': ('emoji-give-up', 5.407888),
    '120': ('emoji-dizzy', 4.053049),
    '121': ('emoji-crying', 3.696499),
    '122': ('emoji-clapping', 2.161757),
    '123': ('emoji-arrogance', 6.869441),
    '124': ('emoji-ghost', 3.472759),
    '125': ('emoji-eyeroll', 3.020264),
    '126': ('idle-fighter', 17.19123),
    '127': ('emote-wings', 13.134487),
    '128': ('emote-think', 3.691104),
    '129': ('emote-theatrical', 8.591869),
    '130': ('emote-tapdance', 11.057294),
    '131': ('emote-superrun', 6.273226),
    '132': ('emote-superpunch', 3.751054),
    '133': ('emote-sumo', 10.868834),
    '134': ('emote-suckthumb', 4.185944),
    '135': ('emote-splitsdrop', 4.46931),
    '136': ('emote-secrethandshake', 3.879024),
    '137': ('emote-ropepull', 8.769656),
    '138': ('emote-roll', 3.560517),
    '139': ('emote-rofl', 6.314731),
    '140': ('emote-robot', 7.607362),
    '141': ('emote-rainbow', 2.813373),
    '142': ('emote-proposing', 4.27888),
    '143': ('emote-peekaboo', 3.629867),
    '144': ('emote-peace', 5.755004),
    '145': ('emote-panic', 2.850966),
    '146': ('emote-ninjarun', 4.754721),
    '147': ('emote-nightfever', 5.488424),
    '148': ('emote-monster_fail', 4.632708),
    '149': ('emote-levelup', 6.0545),
    '150': ('emote-laughing2', 5.056641),
    '151': ('emote-kicking', 4.867992),
    '152': ('emote-jumpb', 3.584234),
    '153': ('emote-judochop', 2.427442),
    '154': ('emote-jetpack', 16.759457),
    '155': ('emote-hugyourself', 4.992751),
    '156': ('emote-harlemshake', 13.558597),
    '157': ('emote-happy', 3.483462),
    '158': ('emote-handstand', 4.015678),
    '159': ('emote-gordonshuffle', 8.052307),
    '160': ('emote-ghost-idle', 19.570492),
    '161': ('emote-gangnam', 7.275486),
    '162': ('emote-fainting', 18.423499),
    '163': ('emote-fail2', 6.475972),
    '164': ('emote-fail1', 5.617942),
    '165': ('emote-exasperatedb', 2.722748),
    '166': ('emote-exasperated', 2.367483),
    '167': ('emote-elbowbump', 3.799768),
    '168': ('emote-disco', 5.366973),
    '169': ('emote-disappear', 6.195985),
    '170': ('emote-deathdrop', 3.762728),
    '171': ('emote-death2', 4.855549),
    '172': ('emote-death', 6.615967),
    '173': ('emote-dab', 2.717871),
    '174': ('emote-cold', 3.664348),
    '175': ('emote-bunnyhop', 12.380685),
    '176': ('emote-boo', 4.501502),
    '177': ('emote-baseball', 7.254841),
    '178': ('emote-apart', 4.809542),
    '179': ('emote-attention', 4.401206),
    '180': ('emote-hearteyes', 4.034386),
    '181': ('emote-heartfingers', 4.001974),
    '182': ('emote-heartshape', 6.232394),
    '183': ('emote-hug', 3.503262),
    '184': ('emote-embarrassed', 7.414283),
    '185': ('emote-puppet', 16.325823),
    '186': ('idle_zombie', 28.754937),
    '187': ('idle_layingdown2', 21.546653),
    '188': ('idle_layingdown', 24.585168),
    '189': ('idle-sleep', 22.620446),
    '190': ('idle-sad', 24.377214),
    '191': ('idle-posh', 21.851256),
    '192': ('idle-loop-tired', 21.959007),
    '193': ('idle-loop-tapdance', 6.261593),
    '194': ('idle-loop-shy', 16.47449),
    '195': ('idle-loop-sad', 6.052999),
    '196': ('idle-loop-happy', 18.798322),
    '197': ('idle-loop-annoyed', 17.058522),
    '198': ('idle-loop-aerobics', 8.507535),
    '199': ('idle-lookup', 22.339865),
    '200': ('idle-hero', 21.877099),
    '201': ('idle-floorsleeping2', 17.253372),
    '202': ('idle-floorsleeping', 13.935264),
    '203': ('idle-dance-headbobbing', 25.367458),
    '204': ('idle-angry', 25.427848),
    '205': ('dance-hipshake', 12.8),
    '206': ('dance-tiktok11', 11.0),
    '207': ('emote-cutesalute', 3.0),
    '208': ('emote-salute', 3.0),
    '209': ('idle_tough', 18.0),
    '210': ('emote-fail3', 4.2),
    '211': ('emote-theatrical-test', 6.5),
    '212': ('emote-receive-happy', 3.5),
    '213': ('emote-confused2', 8.0),
    '214': ('dance-shuffle', 8.5),
    '215': ('idle-cold', 18.0),
    '216': ('mining-mine', 8.0),
    '217': ('mining-success', 3.5),
    '218': ('fishing-pull', 4.5),
    '219': ('fishing-idle', 15.0),
    '220': ('fishing-cast', 4.0),
    '221': ('fishing-pull-small', 5.0),
    '222': ('dance-fruity', 9.0),
    '223': ('dance-cheerleader', 8.5),
    '224': ('dance-tiktok14', 11.0),
    '225': ('emote-howl', 7.0),
    '226': ('idle-howl', 20.0),
    '227': ('emote-trampoline', 8.0),
    '228': ('emote-launch', 3.5),
    '229': ('emote-stargazer', 6.0),
    '230': ('dance-freshprince', 14.86),
    '231': ('idle-headless', 41.802306),
    '232': ('emote-gooey', 5.819651),
    '233': ('emote-electrified', 5.287880),
    'sit': ('idle-loop-sitfloor', 22.321055),
    'enthused': ('idle-enthusiastic', 15.941537),
    'yes': ('emote-yes', 2.565001),
    'wave': ('emote-wave', 2.690873),
    'tired': ('emote-tired', 4.61063),
    'snowball': ('emote-snowball', 5.230467),
    'snowangel': ('emote-snowangel', 6.218627),
    'shy': ('emote-shy', 4.477567),
    'sad': ('emote-sad', 5.411073),
    'no': ('emote-no', 2.703034),
    'model': ('emote-model', 6.490173),
    'lust': ('emote-lust', 4.655965),
    'laughing': ('emote-laughing', 2.69161),
    'kiss': ('emote-kiss', 2.387175),
    'hot': ('emote-hot', 4.353037),
    'hello': ('emote-hello', 2.734844),
    'greedy': ('emote-greedy', 4.639828),
    'curtsy': ('emote-curtsy', 2.425714),
    'confused': ('emote-confused', 8.578827),
    'charging': ('emote-charging', 8.025079),
    'bow': ('emote-bow', 3.344036),
    'thumb': ('emoji-thumbsup', 2.702369),
    'gagging': ('emoji-gagging', 5.500202),
    'flex': ('emoji-flex', 2.099351),
    'cursing': ('emoji-cursing', 2.382069),
    'celebrate': ('emoji-celebrate', 3.412258),
    'angry': ('emoji-angry', 5.760023),
    'tiktok8': ('dance-tiktok8', 11),
    'tiktok2': ('dance-tiktok2', 10.392353),
    'shoppingcart': ('dance-shoppingcart', 4.316035),
    'russian': ('dance-russian', 10.252905),
    'pennywise': ('dance-pennywise', 4.214349),
    'macarena': ('dance-macarena', 12.214141),
    'blackpink': ('dance-blackpink', 7.150958),
    'hyped': ('emote-hyped', 7.492423),
    'jinglebell': ('dance-jinglebell', 10.958832),
    'nervous': ('idle-nervous', 21.714221),
    'toilet': ('idle-toilet', 32.174447),
    'floating': ('idle-floating', 27.791175),
    'zombie': ('dance-zombie', 12.922772),
    'astronaut': ('emote-astronaut', 13.791175),
    'swordfight': ('emote-swordfight', 5.914365),
    'timejump': ('emote-timejump', 4.007305),
    'snake': ('emote-snake', 5.262578),
    'float': ('emote-float', 8.995302),
    'telekinesis': ('emote-telekinesis', 10.492032),
    'pinguin': ('dance-pinguin', 11.58291),
    'creepypuppet': ('dance-creepypuppet', 6.416121),
    'bike': ('emote-sleigh', 11.333165),
    'mani': ('emote-maniac', 4.906886),
    'energyball': ('emote-energyball', 7.575354),
    'superpose': ('emote-superpose', 4.530791),
    'cute': ('emote-cute', 6.170464),
    'tiktok9': ('dance-tiktok9', 11.892918),
    'weird': ('dance-weird', 21.556237),
    'tiktok10': ('dance-tiktok10', 8.225648),
    'pose7': ('emote-pose7', 4.655283),
    'pose8': ('emote-pose8', 4.808806),
    'dance-casual': ('idle-dance-casual', 9.079756),
    'pose1': ('emote-pose1', 2.825795),
    'pose3': ('emote-pose3', 5.10562),
    'pose5': ('emote-pose5', 4.621532),
    'cutey': ('emote-cutey', 3.26032),
    'punk': ('emote-punkguitar', 9.365807),
    'fashion': ('emote-fashionista', 5.606485),
    'gravity': ('emote-gravity', 8.955966),
    'icecream': ('dance-icecream', 14.769573),
    'wrong': ('dance-wrong', 12.422389),
    'uwu': ('idle-uwu', 24.761968),
    'sayso': ('idle-dance-tiktok4', 15.500708),
    'bashful': ('emote-shy2', 4.989278),
    'anime': ('dance-anime', 8.46671),
    'kawai': ('dance-kawai', 10.290789),
    'wild': ('idle-wild', 26.422824),
    'iceskating': ('emote-iceskating', 7.299156),
    'pose6': ('emote-pose6', 5.375124),
    'suii': ('emote-celebrationstep', 3.353703),
    'creepycute': ('emote-creepycute', 7.902453),
    'pose10': ('emote-pose10', 3.989871),
    'boxer': ('emote-boxer', 5.555702),
    'blow': ('emote-headblowup', 11.667537),
    'ditzy': ('emote-pose9', 4.583117),
    'teleporting': ('emote-teleporting', 11.7676),
    'touch': ('dance-touch', 11.7),
    'guitar': ('idle-guitar', 13.229398),
    'gift': ('emote-gift', 5.8),
    'employee': ('dance-employee', 8),
    'looping': ('emote-looping', 8),
    'smooch': ('emote-kissing-bound', 10),
    'camera': ('idle-phone-camera', 14.8),
    'phone': ('emote-phone', 9),
    'knock': ('knocking-screen', 7.5),
    'twerk': ('dance-twerk', 8.7),
    'singing': ('idle_singing', 13.791175),
    'frog': ('emote-frog', 14.55257),
    'zombierun': ('emote-zombierun', 9.182984),
    'frustrated': ('emote-frustrated', 5.584622),
    'slap': ('emote-slap', 2.724945),
    'kawaii': ('emote-kawaiigogo', 10.0),
    'shrink': ('emote-shrink', 8.738784),
    'vogue': ('dance-voguehands', 9.150634),
    'spiritual': ('dance-spiritual', 15.795092),
    'smoothwalk': ('dance-smoothwalk', 6.690023),
    'singleladies': ('dance-singleladies', 21.191372),
    'robotic': ('dance-robotic', 17.814959),
    'orange': ('dance-orangejustice', 6.475263),
    'metal': ('dance-metal', 15.076377),
    'handsup': ('dance-handsup', 22.283413),
    'floss': ('dance-floss', 21.329661),
    'duckwalk': ('dance-duckwalk', 11.748784),
    'breakdance': ('dance-breakdance', 17.623849),
    'aerobics': ('dance-aerobics', 8.796402),
    'sexy': ('dance-sexy', 12.30883),
    'tiktok7': ('idle-dance-tiktok7', 12.956484),
    'repose': ('sit-relaxed', 29.889858),
    'laidback': ('sit-open', 26.025963),
    'poke': ('emoji-there', 2.059095),
    'sneeze': ('emoji-sneeze', 2.996694),
    'smirking': ('emoji-smirking', 4.823158),
    'sick': ('emoji-sick', 5.070367),
    'scared': ('emoji-scared', 3.008487),
    'punch': ('emoji-punch', 1.755783),
    'pray': ('emoji-pray', 4.503179),
    'stinky': ('emoji-poop', 4.795735),
    'naughty': ('emoji-naughty', 4.277602),
    'mind-blown': ('emoji-mind-blown', 2.397167),
    'lying': ('emoji-lying', 6.313748),
    'halo': ('emoji-halo', 5.837754),
    'hadoken': ('emoji-hadoken', 2.723709),
    'give-up': ('emoji-give-up', 5.407888),
    'dizzy': ('emoji-dizzy', 4.053049),
    'crying': ('emoji-crying', 3.696499),
    'clapping': ('emoji-clapping', 2.161757),
    'arrogance': ('emoji-arrogance', 6.869441),
    'ghost': ('emoji-ghost', 3.472759),
    'eyeroll': ('emoji-eyeroll', 3.020264),
    'fighter': ('idle-fighter', 17.19123),
    'wings': ('emote-wings', 13.134487),
    'think': ('emote-think', 3.691104),
    'theatrical': ('emote-theatrical', 8.591869),
    'tapdance': ('emote-tapdance', 11.057294),
    'run': ('emote-superrun', 6.273226),
    'superpunch': ('emote-superpunch', 3.751054),
    'sumo': ('emote-sumo', 10.868834),
    'suckthumb': ('emote-suckthumb', 4.185944),
    'split': ('emote-splitsdrop', 4.46931),
    'handshake': ('emote-secrethandshake', 3.879024),
    'ropepull': ('emote-ropepull', 8.769656),
    'roll': ('emote-roll', 3.560517),
    'rofl': ('emote-rofl', 6.314731),
    'robot': ('emote-robot', 7.607362),
    'rainbow': ('emote-rainbow', 2.813373),
    'proposing': ('emote-proposing', 4.27888),
    'peekaboo': ('emote-peekaboo', 3.629867),
    'peace': ('emote-peace', 5.755004),
    'panic': ('emote-panic', 2.850966),
    'ninja': ('emote-ninjarun', 4.754721),
    'nightfever': ('emote-nightfever', 5.488424),
    'monster_fail': ('emote-monster_fail', 4.632708),
    'levelup': ('emote-levelup', 6.0545),
    'laugh': ('emote-laughing2', 5.056641),
    'kick': ('emote-kicking', 4.867992),
    'jumpb': ('emote-jumpb', 3.584234),
    'judochop': ('emote-judochop', 2.427442),
    'jetpack': ('emote-jetpack', 16.759457),
    'hugyourself': ('emote-hugyourself', 4.992751),
    'hero': ('idle-hero', 21.877099),
    'headball': ('emote-headball', 10.073119),
    'harlem': ('emote-harlemshake', 13.558597),
    'happy': ('emote-happy', 3.483462),
    'handstand': ('emote-handstand', 4.015678),
    'graceful': ('emote-graceful', 3.7498),
    'moonwalk': ('emote-gordonshuffle', 8.052307),
    'ghost float': ('emote-ghost-idle', 19.570492),
    'gangnam': ('emote-gangnam', 7.275486),
    'frollicking': ('emote-frollicking', 3.700665),
    'faint': ('emote-fainting', 18.423499),
    'fall': ('emote-fail2', 6.475972),
    'falling': ('emote-fail1', 5.617942),
    'exasperatedb': ('emote-exasperatedb', 2.722748),
    'exasperated': ('emote-exasperated', 2.367483),
    'elbowbump': ('emote-elbowbump', 3.799768),
    'disco': ('emote-disco', 5.366973),
    'disappear': ('emote-disappear', 6.195985),
    'deathdrop': ('emote-deathdrop', 3.762728),
    'death2': ('emote-death2', 4.855549),
    'death': ('emote-death', 6.615967),
    'dab': ('emote-dab', 2.717871),
    'cold': ('emote-cold', 3.664348),
    'bunny': ('emote-bunnyhop', 12.380685),
    'boo': ('emote-boo', 4.501502),
    'baseball': ('emote-baseball', 7.254841),
    'apart': ('emote-apart', 4.809542),
    'attention': ('emote-attention', 4.401206),
    'hearteyes': ('emote-hearteyes', 4.034386),
    'heartfingers': ('emote-heartfingers', 4.001974),
    'heartshape': ('emote-heartshape', 6.232394),
    'hug': ('emote-hug', 3.503262),
    'lagughing': ('emote-lagughing', 1.125537),
    'embarrassed': ('emote-embarrassed', 7.414283),
    'puppet': ('emote-puppet', 16.325823),
    'rest': ('sit-idle-cute', 17.062613),
    'zombie-idle': ('idle_zombie', 28.754937),
    'relax': ('idle_layingdown2', 21.546653),
    'attentive': ('idle_layingdown', 24.585168),
    'sleep': ('idle-sleep', 22.620446),
    'pouty': ('idle-sad', 24.377214),
    'posh': ('idle-posh', 21.851256),
    'tired-loop': ('idle-loop-tired', 21.959007),
    'shy-loop': ('idle-loop-shy', 16.47449),
    'sad-loop': ('idle-loop-sad', 6.052999),
    'chilling': ('idle-loop-happy', 18.798322),
    'annoyed': ('idle-loop-annoyed', 17.058522),
    'aerobics-loop': ('idle-loop-aerobics', 8.507535),
    'ponder': ('idle-lookup', 22.339865),
    'relaxing': ('idle-floorsleeping2', 17.253372),
    'cozy': ('idle-floorsleeping', 13.935264),
    'swinging': ('idle-dance-swinging', 13.198551),
    'dance-headbobbing': ('idle-dance-headbobbing', 25.367458),
    'angry-idle': ('idle-angry', 25.427848),
    'call': ('idle-phone-talking', 14.8),
    'phone-camera': ('idle-phone-camera', 14.8),
    'phone-emote': ('emote-phone', 9),
    'fresh': ('dance-freshprince', 14.86),
    'headless': ("idle-headless", 41.802306),
    'gooey': ("emote-gooey", 5.819651),
    'electrified': ("emote-electrified", 5.287880),
}

# Build reverse mapping for emote names (e.g., "frog" -> "53")
emote_name_to_key = {}
for key, (emote_name, _) in emote_dict.items():
    # Extract short name from emote-xxx or dance-xxx or idle-xxx format
    if '-' in emote_name:
        short_name = emote_name.split('-', 1)[1].lower()  # Get part after first dash
    else:
        short_name = emote_name.lower()
    emote_name_to_key[short_name] = key

# Get list of clean emote names for emotelist display
emote_names = sorted([emote_dict[key][0] for key in emote_dict.keys()])

# ===================== ADVANCED FEATURES DATA =====================

FACTS = [
    "🧠 Honey never spoils. Archaeologists found 3000-year-old honey that was still edible!",
    "🌍 Earth moves at 67,000 mph around the sun.",
    "🐝 Bees can recognize human faces.",
    "💎 A diamond is made of carbon, just like graphite pencil.",
    "🦑 Octopuses have three hearts.",
    "🌊 Sharks existed before dinosaurs.",
    "🦤 Dodos always flew in pairs - they were monogamous.",
    "🌙 The moon is moving 3.8cm away from Earth yearly.",
    "❄️ Antarctica is the largest desert on Earth.",
    "🦖 T-Rex had better vision than eagles.",
    "🌞 The sun's core is 27 million °F.",
    "🐘 Elephants have excellent memory and mourn their dead.",
    "🦋 Butterflies taste with their feet.",
    "🧬 Your DNA is 99.9% similar to any other human.",
    "👅 A giraffe's tongue is 20 inches long.",
    "🐠 Fish memory lasts 3 seconds (mostly).",
    "🌌 Light from distant stars took years to reach us.",
    "🦴 Your skeleton replaces itself every 10 years.",
    "🧠 Jellyfish are 95% water.",
    "🦁 Lions sleep 20 hours a day.",
    "🌻 Sunflowers track the sun's movement.",
    "🐢 Turtles can breathe through their butts.",
    "🦗 Crickets' ears are on their legs.",
    "🧬 Humans shed 30,000 skin cells per minute.",
    "🍌 Bananas are berries, but strawberries aren't.",
    "⚡ Lightning is 5x hotter than sun's surface.",
    "🌪️ Tornadoes can spin faster than Earth rotates.",
    "🐙 Octopuses are highly intelligent and use tools.",
    "🦀 Crabs walk sideways to move faster.",
    "🌺 Flowers bloom faster in music.",
    "🧲 Magnets get weaker when heated.",
    "🎸 Sound travels slower than light.",
    "🐛 Caterpillars have 2000+ muscles.",
    "🦋 Monarchs migrate 3000 miles annually.",
    "🌳 Trees communicate underground via fungi.",
    "🐝 Worker bees dance to show food location.",
    "🧟 Zombies don't exist, but fungus affects animal behavior.",
    "👁️ Your eyes are the same size since birth.",
    "🦴 Human bones are as strong as steel.",
    "💪 Your heart beats 100,000 times daily.",
    "🔥 Fire needs oxygen to burn but spreads faster in oxygen.",
    "🌊 Saltwater freezes at lower temperature than freshwater.",
    "🪶 Feathers are stronger than bones relative to weight.",
    "⚚ A single cloud can weigh as much as 100 elephants.",
    "🐌 Snails can sleep for up to 3 years.",
    "🪡 Spiders have blue blood.",
    "🦂 Scorpions can survive radiation 1000x more than humans.",
    "🧊 Ice formed from saltwater melts faster than freshwater ice.",
]

ROASTS = [
    "You're so quiet, I thought you were a statue! 😂",
    "Your dance moves are... unique! Keep it up!",
    "If you were a vegetable, you'd be awesome-sauce!",
    "Your jokes are so bad, they're good!",
    "You light up the room... when you leave!",
    "You're cooler than ice cream! 🍦",
    "Your personality is 10/10, but your luck... not so much!",
    "If you were a pizza, you'd have extra cheese-appeal!",
    "You're like a human ray of sunshine!",
    "Your style is goals! Keep slaying!",
    "You're so fun, gravity can't pull you down!",
    "If laughter was currency, you'd be rich!",
    "You're a vibe! Stay vibey!",
    "Your energy is contagious! Spread it!",
    "You're like a walking meme - pure comedy!",
    "If jokes were fish, you'd catch them all!",
    "Your potential is unlimited! Use it!",
    "You're proof that awesome exists!",
    "Your humor is chef's kiss! 👨‍🍳",
    "If compliments were currency, you'd be famous!",
    "You're the reason emojis were invented!",
    "Your laugh is the best sound ever!",
    "You're a total legend in your own mind!",
    "Your moves are smoother than butter!",
    "If confidence was a crime, you'd be guilty! 😎",
    "You're like a rare Pokémon - one of a kind!",
    "Your presence makes everyone smile!",
    "You're basically a human emoji!",
    "If you were a superhero, you'd be amazing!",
    "Your vibe is immaculate! No notes!",
    "You're so talented, the internet might break!",
    "If coolness was a competition, you'd win!",
    "Your brain is huge! Big brain energy!",
    "You're living rent-free in everyone's heart!",
    "Your aura is golden! Never dim it!",
    "If you were a song, you'd be a banger!",
    "You're the main character energy personified!",
    "Your wit is sharper than a sword!",
    "If you were a holiday, you'd be favorite day!",
    "You're basically a national treasure!",
    "Your jokes land harder than gravity!",
    "You're so cool, ice would be jealous!",
    "If humor was an art, you're Picasso!",
    "You're the reason WiFi was invented!",
    "Your personality pops like confetti!",
    "You're a living, breathing highlight reel!",
    "If awesomeness was a size, you'd be XL!",
    "You're basically the plot twist we needed!",
    "Your energy levels are over 9000!",
    "You're the reason stars shine bright! ✨"
]

THOUGHTS = [
    "💭 Every expert was once a beginner.",
    "🌟 Your potential is limitless when you believe.",
    "🔥 The only impossible journey is the one you never begin.",
    "💪 You are stronger than you think.",
    "🎯 Focus on progress, not perfection.",
    "✨ Your uniqueness is your superpower.",
    "🚀 Dream big, start small, act now.",
    "💖 You deserve good things to happen to you.",
    "🌈 Every failure is a step toward success.",
    "🎭 Be the energy you want to attract.",
    "📚 Knowledge is power - keep learning.",
    "🏆 Champions keep going when it gets tough.",
    "🌸 Growth happens outside your comfort zone.",
    "⚡ You have unlimited potential inside you.",
    "🎵 Let your passion be your fuel.",
    "🌊 Ride the waves instead of running from storms.",
    "💎 Your value doesn't decrease by someone's opinion.",
    "🔮 The future is what you make of it.",
    "🎨 Create the life you want to live.",
    "🦅 Spread your wings and soar high.",
    "🌙 Even the darkest night yields to dawn.",
    "🌻 Bloom where you're planted.",
    "💡 Your ideas matter - speak them.",
    "🎪 Life is better when you're laughing.",
    "🏅 You already proved you're capable.",
    "🌍 Small actions create big changes.",
    "🎯 Your goals are valid and worth pursuing.",
    "🦋 Transformation is always possible.",
    "⭐ You are worthy exactly as you are.",
    "🎁 Every day is a chance to start over.",
    "🔥 Your determination will take you far.",
    "🌟 Believe in yourself like you believe in others.",
    "💝 Kindness always comes back to you.",
    "🚀 You are meant for great things.",
    "🎊 Celebrate your wins - all of them.",
    "🌺 Your presence makes a difference.",
    "💪 You've survived 100% of bad days.",
    "🎯 Focus on what you can control today.",
    "🌅 Every sunrise brings new opportunities.",
    "💫 You're exactly where you need to be.",
    "🏖️ Sometimes you need to rest - that's okay.",
    "🎸 Keep playing your own tune.",
    "🦁 Your inner lion is stronger than your fears.",
    "🪴 Plant your dreams and watch them grow.",
    "🎪 The show must go on - keep shining!",
    "💎 You're a rare gem in a world of rocks.",
    "🏔️ Climb your mountains at your own pace.",
    "🎨 Paint your life with your own colors.",
    "🌟 You are the hero of your own story.",
]

QUIZZES = [
    {
        "question": "🌍 What is the capital of France?",
        "answers": ["paris", "paris, france"]
    },
    {
        "question": "🐭 Who created Mickey Mouse?",
        "answers": ["walt disney", "disney"]
    },
    {
        "question": "📺 What year was the first iPhone released?",
        "answers": ["2007", "two thousand seven"]
    },
    {
        "question": "🎬 What is the highest-grossing movie of all time?",
        "answers": ["avatar", "avatar 2"]
    },
    {
        "question": "🏀 How many NBA championships did Michael Jordan win?",
        "answers": ["6", "six"]
    },
    {
        "question": "🎵 Who is known as the 'King of Pop'?",
        "answers": ["michael jackson", "jackson"]
    },
    {
        "question": "⚽ Which country won the FIFA World Cup 2022?",
        "answers": ["argentina", "argentina"]
    },
    {
        "question": "🧬 What does DNA stand for?",
        "answers": ["deoxyribonucleic acid"]
    },
    {
        "question": "🌙 What is the largest planet in our solar system?",
        "answers": ["jupiter"]
    },
    {
        "question": "👑 Who was the first President of the United States?",
        "answers": ["george washington", "washington"]
    },
    {
        "question": "📚 Who wrote Romeo and Juliet?",
        "answers": ["william shakespeare", "shakespeare"]
    },
    {
        "question": "🌙 What is the Earth's natural satellite called?",
        "answers": ["moon", "the moon"]
    },
    {
        "question": "❄️ What is the coldest place on Earth?",
        "answers": ["antarctica"]
    },
    {
        "question": "🐋 What is the largest animal in the world?",
        "answers": ["blue whale", "whale"]
    },
    {
        "question": "⚡ What gas makes up most of the atmosphere?",
        "answers": ["nitrogen"]
    },
]

class PARTY(BaseBot):
    def __init__(self):
        super().__init__()
        self.prefix = "-"
        self.username = None
        self.owner_id = None
        self.owner = None
        self.bot_id = None
        self.quiet = False
        self.emote_task = None
        self.promo_task = None
        self.dance_loop_task = None
        self.users_in_square = []
        self.freeze = {}
        self.active_sos_requests = {}
        self.dance_loop_running = False
        self.auto_tip_task = None
        self.auto_tip_loop = None  # New: actual tipping loop
        self.auto_tip_ammount = 1
        self.auto_tip_time = 600
        self.auto_invite_task = None
        self.auto_invite_loop = None
        self.auto_invite_time = 3600*3
        self.last_positions = {}
        # store previous positions for summon/clear
        self.previous_positions = {}
        # track active emote loops per user id
        self.active_emote_loops = {}
        
        # ========== ADVANCED FEATURES INITIALIZATION ==========
        # Coin economy
        self.coins = {}
        # Quiz system
        self.quiz_sessions = {}
        # Cooldown system (5 second per user)
        self.cooldowns = {}
        # Content
        self.facts = FACTS
        self.roasts = ROASTS
        self.thoughts = THOUGHTS
        self.quizzes = QUIZZES
        
        self.BARS_DICTIONARY = {
            10000: "gold_bar_10k",
            5000: "gold_bar_5000",
            1000: "gold_bar_1k",
            500: "gold_bar_500",
            100: "gold_bar_100",
            50: "gold_bar_50",
            10: "gold_bar_10",
            5: "gold_bar_5",
            1: "gold_bar_1"
        }
        self.FEES_DICTIONARY = {
            10000: 1000,
            5000: 500,
            1000: 100,
            500: 50,
            100: 10,
            50: 5,
            10: 1,
            5: 1,
            1: 1
        }

    async def promo(self):
        while True:
            try:
                for items in promo:
                    await self.highrise.chat(items)
                    await asyncio.sleep(100)
            except:
                pass
            await asyncio.sleep(300)

    async def _dance_loop(self):
        while self.dance_loop_running:
            try:
                await self.highrise.send_emote("dance-floss")
                await asyncio.sleep(21.329661 + 0.01)
            except Exception:
                break

    async def monitor_auto_tip(self):
        while True:
            if data["auto_tip"] and self.auto_tip_loop is None:
                self.auto_tip_loop = asyncio.create_task(self._run_auto_tip())
            elif not data["auto_tip"] and self.auto_tip_loop:
                self.auto_tip_loop.cancel()
                try:
                    await self.auto_tip_loop
                except asyncio.CancelledError:
                    pass
                self.auto_tip_loop = None
            await asyncio.sleep(1)

    async def _run_auto_tip(self):
        while data["auto_tip"]:
            try:
                amount = int(self.auto_tip_ammount)
                room_users = (await self.highrise.get_room_users()).content
                await self.process_tips(self.username, amount, room_users, is_bulk=True)
            except:
                pass
            await asyncio.sleep(self.auto_tip_time)

    async def monitor_auto_invite(self):
        while True:
            if data["auto_invite"] and self.auto_invite_loop is None:
                self.auto_invite_loop = asyncio.create_task(self._run_auto_invite())
            elif not data["auto_invite"] and self.auto_invite_loop:
                self.auto_tip_loop.cancel()
                try:
                    await self.auto_tip_loop
                except asyncio.CancelledError:
                    pass
                self.auto_tip_loop = None
            await asyncio.sleep(1)

    async def _run_auto_invite(self):
        while data["auto_invite"]:
            try:
                await self.invite_all(self.username)
            except:
                pass
            await asyncio.sleep(self.auto_invite_time)

    async def on_start(self, session_metadata: SessionMetadata):
        if "auto_tip" not in data:
            data["auto_tip"] = False
        if "auto_invite" not in data:
            data["auto_invite"] = False
        if "flashed" not in data:
            data["flashed"] = {}
        if "points" not in data:
            data["points"] = {}
        if "rmsg" not in data:
            data["rmsg"] = []
        await asyncio.sleep(5)
        
        # Send startup message
        try:
            startup_msg = (
                "✅ 🤖 BOT IS ONLINE! 🤖 ✅\n"
                "🎮 Try: -help, -quiz, -rps, -balance\n"
                "😂 Or: -fact, -roast, -emotelist\n"
                "💰 Play & earn coins! 🎉"
            )
            await self.highrise.chat(startup_msg)
        except:
            pass
        
        try:
            self.username = await self.get_username(session_metadata.user_id)
            self.bot_id = session_metadata.user_id
            self.owner_id = session_metadata.room_info.owner_id
            self.owner = await self.get_username(self.owner_id)
        except Exception as e:
            print("Error in get username, and bot id on start:", e)

        if self.username not in ownerz:
            ownerz.append(self.username)
        if self.owner and self.owner not in ownerz:
            ownerz.append(self.owner)

        async def safe_cancel(task):
            if task:
                task.cancel()
                try:
                    await task
                except (asyncio.CancelledError, Exception):
                    pass

        await safe_cancel(self.emote_task)
        self.emote_task = asyncio.create_task(self.send_same_random_emote_to_all_users())

        await safe_cancel(self.dance_loop_task)
        self.dance_loop_running = True
        self.dance_loop_task = asyncio.create_task(self._dance_loop())

        await safe_cancel(self.auto_tip_task)
        self.auto_tip_task = asyncio.create_task(self.monitor_auto_tip())
        await safe_cancel(self.auto_invite_task)
        self.auto_invite_task = asyncio.create_task(self.monitor_auto_invite())

        await safe_cancel(self.promo_task)
        self.promo_task = asyncio.create_task(self.promo())

        try:
            if bot_location:
                await self.highrise.teleport(session_metadata.user_id, Position(**bot_location))
            else:
                await self.highrise.teleport(session_metadata.user_id, Position(15.5, 0.25, 2.5, 'FrontRight'))
        except:
            pass

        print(f"{self.username} is alive.")

    async def send_same_random_emote_to_all_users(self):
        try:
            while True:
                try:
                    if self.users_in_square:
                        all_emote_names = [k for k in emote_dict.keys() if isinstance(k, str)]
                        if all_emote_names:
                            random_emote_name = random.choice(all_emote_names)
                            emote_id, emote_duration = emote_dict.get(random_emote_name, (None, None))

                            for user_id in self.users_in_square:
                                await self.highrise.send_emote(emote_id, user_id)  # Use only emote_id
                except:
                    continue
                await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")

    async def invite_all(self, username):
        if username not in ownerz:
            await self.highrise.chat(f"@{username} You cant use this command.")
            return
        try:
            for user_id in ids:
                message_id = f"1_on_1:{user_id}:{self.bot_id}"
                await self.highrise.send_message(
                message_id,
                message_type="invite",
                content="Join this room!", 
                room_id=partyid[0])
                await asyncio.sleep(0.5)
        except Exception as e:
            await self.highrise.chat(f"error: {e}")

    async def on_user_join(self, user: User, pos: Position) -> None:
        await asyncio.sleep(1)
        try:
            # Welcome message with username
            welcome_msg = f"✨ Welcome {user.username}! ✨\n💬 PM 'hy' to unlock commands! 🚀\n🎉 Let's vibe together! 🔥"
            await self.highrise.chat(welcome_msg)
        except:
            pass

    async def on_user_leave(self, user: User) -> None:
        await asyncio.sleep(1.5)
        try:
            # Goodbye message with username
            goodbye_msg = f"👋 See you soon, {user.username}! 👋\n💙 Thanks for the vibes! 🎶"
            await self.highrise.chat(goodbye_msg)
            
            if user.id in self.users_in_square:
                self.users_in_square.remove(user.id)
            if user.username in data["points"] and data["points"][user.username]["join"] is not None:
                join_time = data["points"][user.username]["join"]
                spent = time.time() - join_time
                data["points"][user.username]["total"] += spent
                data["points"][user.username]["join"] = None
        except:
            pass

    async def on_user_move(self, user: User, pos: Position) -> None:
        try:
            if user.username.lower() in self.freeze:
                await self.highrise.teleport(user.id, self.freeze[user.username.lower()])
                return
            if "x1" in ranges and "x2" in ranges and "y" in ranges and "z1" in ranges and "z2" in ranges:
                if ranges["x1"] <= pos.x <= ranges["x2"] and pos.y == ranges["y"] and ranges["z1"] <= pos.z <= ranges["z2"]:
                    if user.id not in self.users_in_square:
                        self.users_in_square.append(user.id)
                        await self.highrise.teleport(user.id, Position(pos.x, pos.y, pos.z))
                else:
                    if user.id in self.users_in_square:
                        self.users_in_square.remove(user.id)
            if not data['flashed'].get(user.username, False):
                return
            def distance(pos1, pos2):
                return math.sqrt((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2 + (pos1.z - pos2.z)**2)
            if user.id in self.last_positions:
                last_pos = self.last_positions[user.id]
                if distance(pos, last_pos) >= 7:
                    await self.highrise.teleport(user.id, pos)
            self.last_positions[user.id] = pos
        except:
            pass

    async def on_whisper(self, user: User, message: str) -> None:
        if message.lower().strip() == "hy":
            msg1 = f"💬 Hey {user.username}! 👋"
            msg2 = "✨ PM 'hy' to subscribe & unlock!"
            msg3 = "🎶 Enjoy songs, notifications & more! 🎉"
            msg4 = "🎯 Totally FREE – join now! 🚀"
            await self.highrise.send_whisper(user.id, msg1)
            await asyncio.sleep(0.5)
            await self.highrise.send_whisper(user.id, msg2)
            await asyncio.sleep(0.5)
            await self.highrise.send_whisper(user.id, msg3)
            await asyncio.sleep(0.5)
            await self.highrise.send_whisper(user.id, msg4)

    async def sos(self, user_id, reason: str):
        if user_id in self.active_sos_requests:
            conversation_id = f"1_on_1:{user_id}:{self.bot_id}"
            await self.highrise.send_message(conversation_id, "You already have an active SOS request.")
            return
        username = await self.get_username(user_id)
        self.active_sos_requests[user_id] = {
            "victim": username,
            "reason": reason,
            "task": asyncio.create_task(self._sos_loop(user_id, username, reason))
        }

    async def _sos_loop(self, victim_id: str, victim_name: str, reason: str):
        try:
            while victim_id in self.active_sos_requests:
                for helper_id in msg:
                    if helper_id == victim_id:
                        continue  # Don't message the victim

                    message_id = f"1_on_1:{helper_id}:{self.bot_id}"
                    try:
                        await self.highrise.send_message(
                            message_id,
                            f"🚨 EMERGENCY: @{victim_name} needs help!\n"
                            f"📝 Reason: {reason}\n"
                            f"✋ Reply '1' to stop alerts"
                        )
                    except Exception as e:
                        print(f"Failed to send SOS to {helper_id}: {e}")
                    await asyncio.sleep(3)  # Rate limiting between messages
                await asyncio.sleep(5)  # Interval between broadcast rounds
        except Exception as e:
            print(f"SOS loop error: {e}")
        finally:
            self.active_sos_requests.pop(victim_id, None)

    async def stop_sos(self, helper_id: str):
        # Find which SOS this helper is responding to
        for victim_id, data in list(self.active_sos_requests.items()):
            if helper_id in msg:
                data["task"].cancel()
                try:
                    await data["task"]
                except asyncio.CancelledError:
                    pass

                # Notify the helper
                await self.highrise.send_message(
                    f"1_on_1:{helper_id}:{self.bot_id}",
                    f"✅ SOS alerts stopped for @{data['victim']}"
                )

                # Notify the victim
                if victim_id in self.active_sos_requests:
                    del self.active_sos_requests[victim_id]
                    await self.highrise.send_message(
                        f"1_on_1:{victim_id}:{self.bot_id}",
                        "Your SOS alerts have been cancelled by a helper."
                    )
                break

    async def color(self: BaseBot, category: str, color_palette: int):
        outfit = (await self.highrise.get_my_outfit()).outfit
        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0]
            if item_category == category:
                try:
                    outfit_item.active_palette = color_palette
                except:
                    await self.highrise.chat(f"The bot isn't using any item from the category '{category}'.")
                    return
        await self.highrise.set_outfit(outfit)

    async def equip(self, item_name: str):
        items = (await self.webapi.get_items(item_name=item_name)).items
        if not items:
            await self.highrise.chat(f"Item '{item_name}' not found.")
            return

        item = items[0]
        item_id, category = item.item_id, item.category

        inventory = (await self.highrise.get_inventory()).items
        has_item = any(inv_item.id == item_id for inv_item in inventory)

        if not has_item:
            if item.rarity == Rarity.NONE:
                pass
            elif not item.is_purchasable:
                await self.highrise.chat(f"Item '{item_name}' can't be purchased.")
                return
            else:
                try:
                    response = await self.highrise.buy_item(item_id)
                    if response != "success":
                        await self.highrise.chat(f"Failed to purchase item '{item_name}'.")
                        return
                    await self.highrise.chat(f"Item '{item_name}' purchased.")
                except Exception as e:
                    await self.highrise.chat(f"Error purchasing '{item_name}': {e}")
                    return

        new_item = Item(
            type="clothing",
            amount=1,
            id=item_id,
            account_bound=False,
            active_palette=0,
        )

        outfit = (await self.highrise.get_my_outfit()).outfit
        outfit = [
            outfit_item
            for outfit_item in outfit
            if outfit_item.id.split("-")[0][0:4] != category[0:4]
        ]

        if category == "hair_front" and item.link_ids:
            hair_back_id = item.link_ids[0]
            hair_back = Item(
                type="clothing",
                amount=1,
                id=hair_back_id,
                account_bound=False,
                active_palette=0,
            )
            outfit.append(hair_back)
        outfit.append(new_item)
        await self.highrise.set_outfit(outfit)

    async def remove(self: BaseBot, category: str):
        outfit = (await self.highrise.get_my_outfit()).outfit

        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0][0:3]
            if item_category == category[0:3]:
                try:
                    outfit.remove(outfit_item)
                except Exception as e:
                     pass
                     return
            await self.highrise.set_outfit(outfit)

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        try:
            response = await self.highrise.get_messages(conversation_id)
            if isinstance(response, GetMessagesRequest.GetMessagesResponse):
                message = response.messages[0].content
                if message.startswith("/sos"):
                    reason = message[5:].strip()
                    if len(reason) >= 15:
                        await self.sos(user_id, reason)
                    else:
                        await self.highrise.send_message(conversation_id, "Reason must be at least 15 characters long.")
                if message.strip() == "1" and user_id in msg:
                    await self.stop_sos(user_id)
                if message != "/verify":
                    if user_id not in ids:
                        ids.append(user_id)
                    return
            username = await self.get_username(user_id)
            info = await self.webapi.get_user(user_id)
            joined_at = info.user.joined_at
            if isinstance(joined_at, datetime):
                one_month_ago = datetime.now(joined_at.tzinfo) - timedelta(days=90)
                if joined_at <= one_month_ago:
                    if not username in user_ticket:
                        user_ticket[username] = 3
                        await self.highrise.send_message(conversation_id, "Your account is verified.")
                        await self.highrise.send_message(conversation_id, "You got 3 free tickets")
                        if not user_id in ids:
                            ids.append(user_id)
                else:
                    await self.highrise.send_message(conversation_id, "Sorry, it looks like your account is less than 3 months old, so you cant verify just yet.")
                    await asyncio.sleep(3)
                    await self.highrise.send_message(conversation_id,"We're just trying to keep things fair and avoid alt accounts grabbing free tickets.\nThanks for understanding! ⏳️")
        except Exception as e:
            print(e)

    async def _loop_emote_on_target(self, target_id: str, emote_id: str, duration: float):
        """Loop emote on a specific target user"""
        try:
            while True:
                try:
                    await self.highrise.send_emote(emote_id, target_id)
                except Exception:
                    pass
                await asyncio.sleep(duration + 0.1)
        except asyncio.CancelledError:
            return
        except Exception:
            return

    async def loop_emote(self, user: User, emote_name: str) -> None:
        emote_id, emote_duration = self.get_emote_info(emote_name)
        if not emote_id:
            await self.highrise.send_whisper(user.id, "Invalid emote")
            return

        while True:
            room_users = (await self.highrise.get_room_users()).content
            user_in_room = any(room_user.id == user.id for room_user, pos in room_users)

            if not user_in_room:
                break

            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                pass

            await asyncio.sleep(emote_duration + 0.1)

    def get_emote_info(self, emote_name: str):
        """Get emote ID and duration from emote_dict"""
        # Try direct numeric key first
        if emote_name in emote_dict:
            return emote_dict[emote_name]
        
        # Try emote name mapping (e.g., "frog" -> key "53")
        if emote_name in emote_name_to_key:
            key = emote_name_to_key[emote_name]
            return emote_dict[key]
        
        # Try treating emote_name as animation name (e.g., "emote-frog")
        for key, (anim_name, duration) in emote_dict.items():
            if anim_name == emote_name or anim_name.endswith(f"-{emote_name}"):
                return anim_name, duration
        
        return None, None

    async def emote(self, user: User, emote_name: str) -> None:
        """Send single emote to user"""
        emote_id, _ = self.get_emote_info(emote_name)
        if emote_id:
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except Exception as e:
                print(f"Error sending emote: {e}")

    async def stop_emote_on_user(self, moderator: User, target_username: str):
        target = target_username.replace("@", "").strip()
        target_id = None
        try:
            room_users = (await self.highrise.get_room_users()).content
            for ru, pos in room_users:
                if ru.username.lower() == target.lower():
                    target_id = ru.id
                    break
        except Exception:
            pass

        if not target_id:
            await self.highrise.send_whisper(moderator.id, "Target user not found in room.")
            return

        # Permission: owner/vip/mod or target themself
        try:
            priv = await self.highrise.get_room_privilege(moderator.id)
            is_mod = getattr(priv, 'moderator', False)
        except Exception:
            is_mod = False
        if moderator.username not in ownerz and moderator.username not in vip_users and not is_mod and moderator.id != target_id:
            await self.highrise.send_whisper(moderator.id, "You don't have permission to stop others' emotes.")
            return

        task = self.active_emote_loops.get(target_id)
        if task:
            try:
                task.cancel()
            except Exception:
                pass
            self.active_emote_loops.pop(target_id, None)
            await self.highrise.chat(f"⏹️ Stopped emote loop on @{target}.")
        else:
            await self.highrise.send_whisper(moderator.id, "No active emote loop on that user.")

    async def get_username(self, user_id: str) -> str:
        """Get username from user ID"""
        try:
            user_info = await self.webapi.get_user(user_id)
            return user_info.user.username
        except:
            return "Unknown"

    async def teleporter(self, message: str) -> None:
        """Handle teleporting users"""
        try:
            parts = message.split()
            if len(parts) < 2:
                await self.highrise.chat("Invalid teleport command")
                return
            username = parts[1].replace("@", "")
            room_users = (await self.highrise.get_room_users()).content
            for user_info in room_users:
                if user_info[0].username.lower() == username.lower():
                    await self.highrise.teleport(user_info[0].id, Position(15.5, 0.25, 2.5))
                    return
            await self.highrise.chat(f"User @{username} not found")
        except Exception as e:
            print(f"Teleport error: {e}")

    async def process_tips(self, username: str, amount: int, room_users, is_bulk=False) -> None:
        """Process tipping users"""
        try:
            tipped = 0
            for user_obj, _ in room_users:
                if user_obj.username != username:
                    try:
                        await self.highrise.send_item(user_obj.id, "gold_bar_1", amount)
                        tipped += 1
                    except Exception as e:
                        print(f"Failed to tip {user_obj.username}: {e}")
                    await asyncio.sleep(0.1)
            if tipped > 0:
                await self.highrise.chat(f"Tipped {tipped} users!")
        except Exception as e:
            print(f"Tip processing error: {e}")

    async def show_help(self, user: User):
        """Show help message with available commands"""
        try:
            # Send multiple shorter help messages
            msg1 = "📋 BOT COMMANDS:\n🎭 -wave, -dance, -emotelist\n👥 -summon @user, -goto @user"
            msg2 = "🎯 -emoteall wave, -kick @user\n👊 -punch @user, -set bot spot\n🛑 -stop, -help"
            await self.highrise.send_whisper(user.id, msg1)
            await asyncio.sleep(1)
            await self.highrise.send_whisper(user.id, msg2)
        except Exception as e:
            print(f"Error in show_help: {e}")

    async def summon_all(self, user: User):
        # Permission: owners, vip_users or room moderators
        try:
            priv = await self.highrise.get_room_privilege(user.id)
            is_mod = getattr(priv, 'moderator', False)
        except Exception:
            is_mod = False
        if user.username not in ownerz and user.username not in vip_users and not is_mod:
            await self.highrise.send_whisper(user.id, "🔒 You don't have permission to use summon all.")
            return
        try:
            room_users = (await self.highrise.get_room_users()).content
            # find caller's pos
            caller_pos = None
            for ru, pos in room_users:
                if ru.id == user.id and isinstance(pos, Position):
                    caller_pos = pos
                    break
            if not caller_pos:
                await self.highrise.send_whisper(user.id, "Couldn't determine your position.")
                return

            for ru, pos in room_users:
                try:
                    if not isinstance(pos, Position):
                        continue
                    if ru.id == self.bot_id or ru.id == user.id:
                        continue
                    if ru.username in ownerz or ru.username in vip_users:
                        continue
                    try:
                        rpriv = await self.highrise.get_room_privilege(ru.id)
                        if getattr(rpriv, 'moderator', False):
                            continue
                    except Exception:
                        pass

                    self.previous_positions[ru.id] = (pos.x, pos.y, pos.z)
                    try:
                        await self.highrise.teleport(ru.id, Position(caller_pos.x, caller_pos.y, caller_pos.z))
                    except Exception:
                        pass
                except Exception:
                    continue
            await self.highrise.chat(f"🔁 @{user.username} summoned everyone to their location.")
        except Exception as e:
            await self.highrise.send_whisper(user.id, f"Error: {e}")

    async def clear_all(self, user: User):
        # Permission: owners, vip_users or room moderators
        try:
            priv = await self.highrise.get_room_privilege(user.id)
            is_mod = getattr(priv, 'moderator', False)
        except Exception:
            is_mod = False
        if user.username not in ownerz and user.username not in vip_users and not is_mod:
            await self.highrise.send_whisper(user.id, "🔒 You don't have permission to use clear all.")
            return
        try:
            for uid, coords in list(self.previous_positions.items()):
                try:
                    await self.highrise.teleport(uid, Position(*coords))
                except Exception:
                    pass
            self.previous_positions.clear()
            await self.highrise.chat(f"✅ @{user.username} restored everyone's previous positions.")
        except Exception as e:
            await self.highrise.send_whisper(user.id, f"Error: {e}")

    async def emote_all(self, moderator: User, emote_name: str):
        # Permission: owners, vip_users or room moderators
        try:
            priv = await self.highrise.get_room_privilege(moderator.id)
            is_mod = getattr(priv, 'moderator', False)
        except Exception:
            is_mod = False
        if moderator.username not in ownerz and moderator.username not in vip_users and not is_mod:
            await self.highrise.send_whisper(moderator.id, "You don't have permission to use emote-all.")
            return
        
        # Get emote info - try name mapping first
        if emote_name in emote_name_to_key:
            key = emote_name_to_key[emote_name]
            emote_id, duration = emote_dict[key]
        else:
            emote_id, duration = self.get_emote_info(emote_name)
        
        if not emote_id:
            await self.highrise.send_whisper(moderator.id, f"Unknown emote: {emote_name}")
            return
        try:
            room_users = (await self.highrise.get_room_users()).content
            for ru, pos in room_users:
                try:
                    if ru.id == self.bot_id or ru.id == moderator.id:
                        continue
                    if ru.username in ownerz or ru.username in vip_users:
                        continue
                    try:
                        rpriv = await self.highrise.get_room_privilege(ru.id)
                        if getattr(rpriv, 'moderator', False):
                            continue
                    except Exception:
                        pass

                    existing = self.active_emote_loops.get(ru.id)
                    if existing:
                        try:
                            existing.cancel()
                        except Exception:
                            pass
                    task = self.highrise.tg.create_task(self._loop_emote_on_target(ru.id, emote_id, duration))
                    task.set_name(f"emote_loop_{ru.id}")
                    self.active_emote_loops[ru.id] = task
                except Exception:
                    continue
            await self.highrise.chat(f"🔁 Started looping emote '{emote_name}' on all users.")
        except Exception as e:
            await self.highrise.send_whisper(moderator.id, f"Error: {e}")

    async def stop_emote_all(self, moderator: User):
        # Permission: owners, vip_users or room moderators
        try:
            priv = await self.highrise.get_room_privilege(moderator.id)
            is_mod = getattr(priv, 'moderator', False)
        except Exception:
            is_mod = False
        if moderator.username not in ownerz and moderator.username not in vip_users and not is_mod:
            await self.highrise.send_whisper(moderator.id, "You don't have permission to stop emotes for all.")
            return
        for uid, task in list(self.active_emote_loops.items()):
            try:
                task.cancel()
            except Exception:
                pass
            self.active_emote_loops.pop(uid, None)
        await self.highrise.chat(f"⏹️ Stopped emote loops on all users.")

    async def emote_user(self, moderator: User, target_username: str, emote_name: str):
        """Send a single emote to a specific user (by username)."""
        try:
            target = target_username.replace("@", "").strip()
            room_users = (await self.highrise.get_room_users()).content
            target_id = None
            for ru, pos in room_users:
                if ru.username.lower() == target.lower():
                    target_id = ru.id
                    break
            if not target_id:
                await self.highrise.send_whisper(moderator.id, "User not found in room.")
                return

            # permission check
            try:
                priv = await self.highrise.get_room_privilege(moderator.id)
                is_mod = getattr(priv, 'moderator', False)
            except Exception:
                is_mod = False
            if moderator.username not in ownerz and moderator.username not in vip_users and not is_mod:
                await self.highrise.send_whisper(moderator.id, "You don't have permission to emote others.")
                return

            emote_id, _ = self.get_emote_info(emote_name)
            if not emote_id:
                await self.highrise.send_whisper(moderator.id, f"Unknown emote: {emote_name}")
                return

            try:
                await self.highrise.send_emote(emote_id, target_id)
                await self.highrise.chat(f"✅ Sent emote '{emote_name}' to @{target}.")
            except Exception as e:
                await self.highrise.send_whisper(moderator.id, f"Failed to send emote: {e}")
        except Exception as e:
            await self.highrise.send_whisper(moderator.id, f"Error: {e}")

    async def goback_user(self, moderator: User, target_username: str):
        """Teleport a single user back to their previous saved position."""
        try:
            target = target_username.replace("@", "").strip()
            room_users = (await self.highrise.get_room_users()).content
            target_id = None
            for ru, pos in room_users:
                if ru.username.lower() == target.lower():
                    target_id = ru.id
                    break
            if not target_id:
                await self.highrise.send_whisper(moderator.id, "User not found in room.")
                return

            # permission check
            try:
                priv = await self.highrise.get_room_privilege(moderator.id)
                is_mod = getattr(priv, 'moderator', False)
            except Exception:
                is_mod = False
            if moderator.username not in ownerz and moderator.username not in vip_users and not is_mod:
                await self.highrise.send_whisper(moderator.id, "You don't have permission to goback others.")
                return

            coords = self.previous_positions.get(target_id)
            if not coords:
                await self.highrise.send_whisper(moderator.id, "No previous position stored for that user.")
                return

            try:
                await self.highrise.teleport(target_id, Position(*coords))
                # remove from previous_positions
                self.previous_positions.pop(target_id, None)
                await self.highrise.chat(f"✅ Restored @{target} to previous position.")
            except Exception as e:
                await self.highrise.send_whisper(moderator.id, f"Teleport failed: {e}")
        except Exception as e:
            await self.highrise.send_whisper(moderator.id, f"Error: {e}")

    async def clear_nearby(self, user: User, radius: float = 3.0, push_distance: float = 5.0):
        """Push users near the caller away by teleporting them a bit further.
        Stores previous positions so they can be restored with goback/clear all.
        """
        try:
            try:
                room_users = (await self.highrise.get_room_users()).content
            except Exception as e:
                await self.highrise.send_whisper(user.id, f"Could not fetch room users: {e}")
                return

            # find caller position
            caller_pos = None
            for ru, pos in room_users:
                if ru.id == user.id and isinstance(pos, Position):
                    caller_pos = pos
                    break
            if not caller_pos:
                await self.highrise.send_whisper(user.id, "Could not determine your position.")
                return

            moved = 0
            for ru, pos in room_users:
                try:
                    if not isinstance(pos, Position):
                        continue
                    if ru.id == self.bot_id or ru.id == user.id:
                        continue
                    # skip owners/mods/vips
                    try:
                        rpriv = await self.highrise.get_room_privilege(ru.id)
                        if getattr(rpriv, 'moderator', False):
                            continue
                    except Exception:
                        pass
                    # distance check
                    dx = pos.x - caller_pos.x
                    dy = pos.y - caller_pos.y
                    dz = pos.z - caller_pos.z
                    dist_sq = dx*dx + dy*dy + dz*dz
                    if dist_sq <= radius*radius:
                        # save previous
                        self.previous_positions[ru.id] = (pos.x, pos.y, pos.z)
                        # push away along x axis (safe simple approach)
                        new_x = pos.x + (push_distance if dx >= 0 else -push_distance)
                        try:
                            await self.highrise.teleport(ru.id, Position(new_x, pos.y, pos.z))
                            moved += 1
                        except Exception:
                            continue
                except Exception:
                    continue
            await self.highrise.chat(f"✅ Pushed {moved} nearby user(s) away from @{user.username}.")
        except Exception as e:
            await self.highrise.send_whisper(user.id, f"Error in clear: {e}")

    async def add_mod(self, user: User, target_username: str | None = None):
        """Add a bot mod (stored in `vip_users`). Only owners can add mods."""
        try:
            # Permission: only owners
            if user.username not in ownerz:
                await self.highrise.send_whisper(user.id, "You are not authorized to use /addmod.")
                return

            # determine target (default to caller)
            target = user.username if not target_username else target_username.replace("@", "").strip()
            if not target:
                await self.highrise.send_whisper(user.id, "Invalid target username.")
                return

            # verify user exists in room
            try:
                room_response = await self.highrise.get_room_users()
                if not room_response or not hasattr(room_response, 'content'):
                    await self.highrise.send_whisper(user.id, "Could not fetch room users.")
                    return
                room_users = room_response.content
            except Exception as e:
                print(f"Error fetching room users: {e}")
                await self.highrise.send_whisper(user.id, f"Error fetching room users: {e}")
                return

            found = False
            target_name = None  # Initialize to prevent UnboundLocalError
            for ru, pos in room_users:
                if ru.username.lower() == target.lower():
                    found = True
                    target_name = ru.username
                    break
            if not found:
                await self.highrise.send_whisper(user.id, f"User @{target} not found in room.")
                return

            if target_name in vip_users:
                await self.highrise.send_whisper(user.id, f"@{target_name} is already a bot mod.")
                return

            # Update in casinodb for persistence if available
            try:
                import casinodb
                if hasattr(casinodb, 'vip_users'):
                    if target_name not in casinodb.vip_users:
                        casinodb.vip_users.append(target_name)
                else:
                    # fallback: try vip_users1
                    if hasattr(casinodb, 'vip_users1'):
                        if target_name not in casinodb.vip_users1:
                            casinodb.vip_users1.append(target_name)
                # save
                try:
                    casinodb.save_data()
                except Exception as e:
                    print(f"Warning: could not persist mod to DB: {e}")
            except Exception as e:
                # If casinodb not present, update local list only
                print(f"Casinodb error: {e}")
                if target_name not in vip_users:
                    vip_users.append(target_name)

            # ensure local list is updated
            if target_name not in vip_users:
                vip_users.append(target_name)

            await self.highrise.chat(f"✅ @{target_name} added as bot mod.")
        except Exception as e:
            print(f"Exception in add_mod: {e}")
            try:
                await self.highrise.send_whisper(user.id, f"Error in /addmod: {e}")
            except:
                print(f"Could not send error whisper: {e}")

    async def remove_mod(self, user: User, target_username: str | None = None):
        """Remove a bot mod. Only owners can remove mods."""
        try:
            if user.username not in ownerz:
                await self.highrise.send_whisper(user.id, "You are not authorized to use /removemod.")
                return

            target = user.username if not target_username else target_username.replace("@", "").strip()

            # find exact case username in vip_users
            found_name = None
            for v in list(vip_users):
                if v.lower() == target.lower():
                    found_name = v
                    break
            if not found_name:
                await self.highrise.send_whisper(user.id, f"@{target} is not a bot mod.")
                return

            # Remove from casinodb if available
            try:
                import casinodb
                removed = False
                if hasattr(casinodb, 'vip_users') and found_name in casinodb.vip_users:
                    casinodb.vip_users.remove(found_name)
                    removed = True
                if hasattr(casinodb, 'vip_users1') and found_name in casinodb.vip_users1:
                    casinodb.vip_users1.remove(found_name)
                    removed = True
                try:
                    casinodb.save_data()
                except Exception as e:
                    await self.highrise.send_whisper(user.id, f"Warning: could not persist removal to DB: {e}")
            except Exception:
                removed = False

            # Always remove from local list if present
            try:
                if found_name in vip_users:
                    vip_users.remove(found_name)
                    removed = True
            except Exception:
                pass

            if removed:
                await self.highrise.chat(f"✅ Removed @{found_name} from bot mods.")
            else:
                await self.highrise.send_whisper(user.id, f"Could not remove @{found_name} (not found or error).")
        except Exception as e:
            await self.highrise.send_whisper(user.id, f"Error in /removemod: {e}")

    async def loop(self, user: User, emote_name: str) -> None:
        taskgroup = self.highrise.tg
        task_list: list[asyncio.Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                task.cancel()
        task = taskgroup.create_task(self.loop_emote(user, emote_name))
        task.set_name(user.username)

    async def stop(self, user: User, message: str) -> None:
        taskgroup = self.highrise.tg
        task_list: list[asyncio.Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                task.cancel()
                await self.highrise.send_whisper(user.id, "Emote loop stopped.")

    async def follow(self, user: User, message: str) -> None:
        if user.username not in ownerz:
            return

        target_username = None
        if message.startswith("/follow @"):
            target_username = message[9:].split()[0]  # Extract username correctly

        async def following_loop(self, user: User, target_user: User) -> None:
            while True:
                room_users = (await self.highrise.get_room_users()).content
                target_position = None

                for room_user, position in room_users:
                    if room_user.id == target_user.id:
                        target_position = position
                        break

                if target_position:
                    if not isinstance(target_position, AnchorPosition):
                        await self.highrise.walk_to(Position(target_position.x + 1, target_position.y, target_position.z))

                await asyncio.sleep(0.5)

        taskgroup = self.highrise.tg
        task_list = list(taskgroup._tasks)

        for task in task_list:
            if task.get_name() == "following_loop":
                await self.highrise.send_whisper(user.id, "Already following someone")
                return

        target_user = None
        if target_username:
            room_users = (await self.highrise.get_room_users()).content
            for room_user, _ in room_users:
                if room_user.username == target_username:
                    target_user = room_user
                    break
            else:
                await self.highrise.send_whisper(user.id, f"User @{target_username} not found in the room")
                return

        if target_user is None:
            await self.highrise.send_whisper(user.id, "Invalid username")
            return

        taskgroup.create_task(following_loop(self, user, target_user), name="following_loop")
        await self.highrise.chat(f"Following {target_user.username}")

    async def stopf(self, user: User, message: str) -> None:
        if user.username not in ownerz:
            await self.highrise.send_whisper(user.id, "You are not able to use this command")
            return

        taskgroup = self.highrise.tg
        task_list = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == "following_loop":
                task.cancel()
                await self.highrise.chat(f"Stopping following {user.username}")
                return
        await self.highrise.chat("Not following anyone")

    async def summon(self, user: User, message: str) -> None:
        try:
            command, username = message.split(" ")
        except ValueError:
            await self.highrise.send_whisper(user.id, f"Incorrect format, please use {self.prefix}summon @username")
            return

        username = username.replace("@", "")
        user_privileges = await self.highrise.get_room_privilege(user.id)
        summoner_is_privileged = user_privileges.moderator or user.username in ownerz
        if not summoner_is_privileged:
            await self.highrise.send_whisper(user.id, f"You are not authorized to use {self.prefix}summon")
            return
        try:
            room_users = (await self.highrise.get_room_users()).content

            for user_info in room_users:
                if user_info[0].username.lower() == username.lower():
                    target_user_id = user_info[0].id
                    break
            else:
                await self.highrise.send_whisper(user.id, "User not found, please specify a valid user")
                return

        except Exception as e:
            await self.highrise.chat(f"Error fetching room users: {e}")
            return
        try:
            response = await self.highrise.get_room_users()

            for content in response.content:
                if content[0].id == user.id:
                    if isinstance(content[1], Position):
                        your_pos = content[1]
                        break
            else:
                await self.highrise.send_whisper(user.id, f"@{user.username}, you do not have a valid position.")
                return

        except Exception as e:
            await self.highrise.chat(f"Error fetching user position: {e}")
            return
        try:
            await self.highrise.teleport(user_id=target_user_id, dest=your_pos)
        except Exception as e:
            await self.highrise.chat(f"Error teleporting user: {e}")
            return

    async def goto(self, user, message):
        try:
            command, username = message.split(" ")
        except ValueError:
            await self.highrise.chat(f"Incorrect format, please use {self.prefix}goto @username")
            return

        username = username.replace("@", "")

        user_privileges = await self.highrise.get_room_privilege(user.id)

        summoner_is_privileged = user_privileges.moderator or user.username in ownerz

        if not summoner_is_privileged:
            await self.highrise.send_whisper(user.id, f"You are not authorized to use {self.prefix}goto")
            return

        room_users = (await self.highrise.get_room_users()).content
        for user_info in room_users:
            if user_info[0].username.lower() == username.lower():
                target_user_id = user_info[0].id
                target_user_position = user_info[1]
                break
        else:
            await self.highrise.chat("User not found, please specify a valid user")
            return

        try:
            await self.highrise.teleport(user_id=user.id, dest=target_user_position)
        except Exception as e:
            await self.highrise.chat(f"Error: {str(e)}.")

    async def send_leaderboard(self):
        if "points" not in data or not data["points"]:
            message = "No data available yet."
            await self.highrise.chat(f"\n🏆 {message}")
            return

        sorted_points = sorted(
            data["points"].items(),
        key=lambda x: x[1]["total"] + (time.time() - x[1]["join"] if x[1]["join"] else 0),
        reverse=True
    )
        top_users = sorted_points[:10]

        leaderboard = "\n🏆 Top 10 Users :"
        for i, (uid, info) in enumerate(top_users, start=1):
            total_seconds = info["total"]
            if info["join"] is not None:
                total_seconds += time.time() - info["join"]

            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            formatted_time = f"{hours:02d}h {minutes:02d}m"

            leaderboard += f"\n{i}. @{uid}: {formatted_time}"

        await self.highrise.chat(leaderboard)

    def get_user_time(self, username: str) -> str:
        if username not in data["points"]:
            return "00:00"
        total = data["points"][username]["total"]
        if data["points"][username]["join"] is not None:
            total += time.time() - data["points"][username]["join"]

        hours = int(total // 3600)
        minutes = int((total % 3600) // 60)
        return f"{hours:02d}h {minutes:02d}m"

    async def send_emotelist(self, user):
        try:
            # Sort keys: numeric first, then alphabetic
            sorted_keys = []
            for key in emote_dict.keys():
                try:
                    sorted_keys.append((int(key), key))
                except ValueError:
                    sorted_keys.append((9999, key))  # Non-numeric at end
            
            sorted_keys.sort()
            
            total_emotes = len(sorted_keys)
            
            # Send header
            await self.highrise.send_whisper(user.id, f"🎭 EMOTE LIST ({total_emotes} Total)\n" + "="*40)
            await asyncio.sleep(0.5)
            
            # Send emotes in chunks of 8
            for i in range(0, total_emotes, 8):
                message_lines = []
                for j in range(8):
                    idx = i + j
                    if idx < len(sorted_keys):
                        _, key = sorted_keys[idx]
                        anim_name, _ = emote_dict[key]
                        
                        # Clean up animation name for display
                        if '-' in anim_name:
                            clean_name = anim_name.split('-', 1)[1].replace('-', ' ').title()
                        else:
                            clean_name = anim_name.replace('-', ' ').title()
                        
                        # Format: "1. Sit Floor" or "wave. Wave"
                        message_lines.append(f"  {key:>3}. {clean_name:<20}")
                
                if message_lines:
                    message = "\n".join(message_lines)
                    await self.highrise.send_whisper(user.id, message)
                    await asyncio.sleep(0.8)
            
            # Send footer with usage
            await self.highrise.send_whisper(user.id, "="*40 + "\n💡 Usage: /wave  or  /1  or  wave  or  1")

        except Exception as e:
            print(f"Error in send_emotelist: {e}")
            await self.highrise.send_whisper(user.id, f"Error sending emotelist: {str(e)}")

    async def send_gameslist(self, user):
        """Send available games list"""
        try:
            games_msg1 = "🎮 AVAILABLE GAMES:\n🎯 Freeze Game - -freeze @user\n🎪 Pose Game - -pose @user\n⚡ Chase Game - -chase @user"
            games_msg2 = "🎲 Luck Game - -luck\n🎤 Karaoke - -karaoke\n🎪 Band Play - Coming Soon!\n✨ More games added daily!"
            
            await self.highrise.send_whisper(user.id, games_msg1)
            await asyncio.sleep(1)
            await self.highrise.send_whisper(user.id, games_msg2)
        except Exception as e:
            print(f"Error in send_gameslist: {e}")
            await self.highrise.send_whisper(user.id, f"Error: {str(e)}")

    async def get_id(self, username):
        try:
            target_name = username.split()[1].replace("@", "").lower() if " " in username else username.replace("@", "").lower()

            response = await self.highrise.get_room_users()
            for user_obj in response.content:
                if user_obj[0].username.lower() == target_name:
                    return user_obj[0].id

            await self.highrise.chat(f"User @{target_name} not found.")

        except Exception as e:
            await self.highrise.send_whisper(user.id, f"Unexpected error: {e}")

    async def on_chat(self, user: User, message: str):
        if message.lower() in ["tele mod", "tele vip"]:
            coordinates = vip_loc.get("mod" if message.lower() == "tele mod" else "vip")
            if coordinates and ((message.lower() == "tele mod" and (await self.highrise.get_room_privilege(user.id)).moderator) 
            or user.username in ownerz 
            or (message.lower() == "tele vip" and user.username in vip_users)):
                await self.highrise.teleport(user.id, Position(*coordinates))

        if message.lower().lstrip() in locations:
            try:
                location = locations[message.lower().lstrip()]
                x, y, z = map(float, location.split(","))
                await self.highrise.teleport(user.id, Position(x, y, z))
            except ValueError:
                print(f"Error: Invalid coordinates for location '{message}'")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        if message.lower().lstrip().startswith("tele ") and user.username in ownerz: 
            if "@" in message:
                try: 
                    await self.teleporter(message)
                except:
                    pass
        if any(word.lower() in message.lower() for word in bad_words) and user.username not in ownerz:
            try:
                await self.highrise.moderate_room(user.id, "kick")
            except Exception as e:
                print(e)
        if message.lower().lstrip().startswith(( "stop", "0", "/stop")):
            await self.stop(user, message)
        
        # Check if message is an emote (by number or name, without prefix)
        msg_lower = message.strip().lower()
        emote_key = None
        if msg_lower in emote_dict:
            emote_key = msg_lower  # Numeric key like "53"
        elif msg_lower in emote_name_to_key:
            emote_key = emote_name_to_key[msg_lower]  # Emote name like "frog"
        
        if emote_key:
            try:
                await self.loop(user, emote_key)
            except:
                pass
        
        if message.startswith(self.prefix):
            normalized_message = '/' + message.lstrip('/-!').lstrip()
            await self.process_normalized_chat(user, normalized_message)

    async def process_normalized_chat(self, user: User, message: str):
        # ========== CHECK ADVANCED FEATURES COMMANDS FIRST ==========
        # Parse message prefix and command
        normalized = message.lstrip('/-!').strip()
        tokens = normalized.split()
        
        if tokens:
            cmd = tokens[0].lower()
            args = tokens[1:]
            
            # Check cooldown for advanced commands
            if cmd in ["help", "commands", "games", "emotelist", "info", "balance", "leaderboard", 
                       "fact", "roast", "thought", "quiz", "ans", "rps", "slots", "dice"]:
                
                if not await self.check_cooldown(user.username):
                    await self.highrise.send_whisper(
                        user.id,
                        "⏳ Please wait 5 seconds before next command!"
                    )
                    return
                
                # Route to handlers
                try:
                    if cmd == "help":
                        await self.cmd_help(user)
                        return
                    elif cmd == "commands":
                        await self.cmd_commands(user)
                        return
                    elif cmd == "games":
                        await self.cmd_games(user)
                        return
                    elif cmd == "emotelist":
                        await self.cmd_emotelist(user)
                        return
                    elif cmd == "info":
                        await self.cmd_info(user)
                        return
                    elif cmd == "balance":
                        await self.cmd_balance(user)
                        return
                    elif cmd == "leaderboard":
                        await self.cmd_leaderboard(user)
                        return
                    elif cmd == "fact":
                        await self.cmd_fact(user)
                        return
                    elif cmd == "roast":
                        await self.cmd_roast(user)
                        return
                    elif cmd == "thought":
                        await self.cmd_thought(user)
                        return
                    elif cmd == "quiz":
                        await self.cmd_quiz(user)
                        return
                    elif cmd == "ans":
                        await self.cmd_answer(user, args)
                        return
                    elif cmd == "rps":
                        await self.cmd_rps(user, args)
                        return
                    elif cmd == "slots":
                        await self.cmd_slots(user, args)
                        return
                    elif cmd == "dice":
                        await self.cmd_dice(user, args)
                        return
                except Exception as e:
                    print(f"Error in advanced command {cmd}: {e}")
                    await self.highrise.send_whisper(user.id, f"❌ Error: {str(e)}")
                    return
        
        # ========== EXISTING PARTY BOT COMMANDS ==========
        
        # Handle help command
        if message.strip() == "/help" or message.strip().lower() == "/help":
            await self.show_help(user)
            return

        # Handle emotelist command
        if message.strip() == "/emotelist" or message.strip().lower() == "/emotelist":
            await self.send_emotelist(user)
            return

        # Handle games list command
        if (message.strip().lower() in ["/gameslist", "/games list", "/games", "/game", "/gamelist"]):
            await self.send_gameslist(user)
            return
        
        # Handle -summon all command
        if message.strip().lower() == "/summon all":
            await self.summon_all(user)
            return
        
        # Handle -clear all command
        if message.strip().lower() == "/clear all":
            await self.clear_all(user)
            return

        # Handle individual summon: -summon @username
        if message.startswith("/summon ") and "@" in message:
            await self.summon(user, message)
            return

        # Handle goto command: -goto @username
        if message.startswith("/goto ") and "@" in message:
            await self.goto(user, message)
            return

        # Handle individual emote commands: -emote_name or -number
        tokens = message.split()
        if len(tokens) >= 1:
            cmd = tokens[0].lstrip("/").lower()
            
            # Check if it's a numeric key (1-229) or an emote name (wave, frog, etc)
            emote_key = None
            if cmd in emote_dict:
                emote_key = cmd  # Numeric key
            elif cmd in emote_name_to_key:
                emote_key = emote_name_to_key[cmd]  # Emote name like "frog", "wave"
            
            if emote_key:
                # -wave or -wave @username (emote on specific user)
                if len(tokens) >= 2 and tokens[1].startswith("@"):
                    target_username = tokens[1].replace("@", "")
                    try:
                        await self.emote_user(user, target_username, emote_key)
                        return
                    except Exception as e:
                        await self.highrise.send_whisper(user.id, f"Error sending emote to user: {e}")
                        return
                else:
                    # Just do the emote on self
                    try:
                        await self.emote(user, emote_key)
                        return
                    except:
                        pass

        # Group commands: summon all, clear all, emote all, stopemote
        if message.startswith("/summon all") or message.strip() == "/summon all":
            await self.summon_all(user)
            return

        if message.startswith("/clear all") or message.strip() == "/clear all":
            await self.clear_all(user)
            return

        # /goback all -> restore everyone's previous positions (alias for clear_all)
        if message.startswith("/goback all") or message.strip() == "/goback all":
            await self.clear_all(user)
            return

        # /goback @user -> restore single user
        if message.startswith("/goback ") and "@" in message:
            parts = message.split(None, 1)
            if len(parts) >= 2:
                await self.goback_user(user, parts[1].strip())
            return

        # /clear -> push nearby users away from caller
        if message.strip() == "/clear":
            await self.clear_nearby(user)
            return

        # /addmod [@username] -> add a bot mod (stores in vip_users)
        if message.startswith("/addmod"):
            parts = message.split(None, 1)
            target = None
            if len(parts) >= 2:
                target = parts[1].strip()
            await self.add_mod(user, target)
            return

        # /removemod [@username] -> remove a bot mod
        if message.startswith("/removemod"):
            parts = message.split(None, 1)
            target = None
            if len(parts) >= 2:
                target = parts[1].strip()
            await self.remove_mod(user, target)
            return

        if message.startswith("/emoteall "):
            parts = message.split(None, 1)
            if len(parts) >= 2:
                await self.emote_all(user, parts[1].strip())
            return

        if message.startswith("/"):
            # pattern: /<emote> all
            tokens = message.split()
            cmd = tokens[0].lstrip("/").lower()
            
            # Check both numeric and named emotes
            emote_key = None
            if cmd in emote_dict:
                emote_key = cmd
            elif cmd in emote_name_to_key:
                emote_key = emote_name_to_key[cmd]
            
            if emote_key and len(tokens) >= 2 and tokens[1].strip().lower() == "all":
                await self.emote_all(user, emote_key)
                return

        if message.startswith("/stopemote"):
            parts = message.split(None, 1)
            if len(parts) >= 2 and parts[1].strip().lower() == "all":
                await self.stop_emote_all(user)
                return
            elif len(parts) >= 2:
                await self.stop_emote_on_user(user, parts[1].strip())
                return

        if message.startswith("/kick @"):
            if user.username not in ownerz:
                if user.username not in vip_users:
                    return
            try:
                user_id = await self.get_id(message)
                await self.highrise.send_emote("emote-kicking", user.id)
                await self.highrise.send_emote("emote-death", user_id)
                await self.highrise.chat(f"{user.username} kicked {await self.get_username(user_id)} in room.")
            except Exception as e:
                print(e)

        if message.startswith("/removetel") or message.startswith("/removetel "):
            # Check if user is owner or moderator
            user_privileges = await self.highrise.get_room_privilege(user.id)
            is_moderator = user_privileges.moderator if hasattr(user_privileges, 'moderator') else False
            if user.username not in ownerz and not is_moderator:
                await self.highrise.send_whisper(user.id, "You are not authorized to use this command.")
                return
            
            # Check if locations dict exists and has data
            if not locations or not isinstance(locations, dict):
                await self.highrise.send_whisper(user.id, "No teleport locations exist yet.")
                return
            
            try:
                # Extract location name from message
                parts = message.split(None, 1)  # Split into max 2 parts
                if len(parts) < 2:
                    await self.highrise.send_whisper(user.id, "Please specify a location name. Usage: -removetele location_name")
                    return
                location_name = parts[1].strip().lower()
                
                # Check if location exists (case-insensitive search)
                location_found = None
                for loc_key in list(locations.keys()):
                    if loc_key.lower() == location_name:
                        location_found = loc_key
                        break
                
                if location_found:
                    del locations[location_found]
                    # Try to save to database if available
                    try:
                        from casinodb import save_data
                        save_data()
                    except Exception as save_err:
                        print(f"Could not save data: {save_err}")
                    await self.highrise.send_whisper(user.id, f"✅ Successfully removed teleport location: {location_found}")
                else:
                    # Show available locations
                    available = ", ".join(locations.keys()) if locations else "none"
                    await self.highrise.send_whisper(user.id, f"❌ Location '{location_name}' not found. Available: {available}")
            except Exception as e:
                print(f"Error in /removetele: {e}")
                await self.highrise.send_whisper(user.id, "An error occurred while removing the location.")

        if message.startswith("/set "):
            # Teleport bot to a SAVED LOCATION
            user_privileges = await self.highrise.get_room_privilege(user.id)
            is_moderator = user_privileges.moderator if hasattr(user_privileges, 'moderator') else False
            if user.username not in ownerz and not is_moderator:
                await self.highrise.send_whisper(user.id, "You are not authorized to use this command.")
                return
            
            try:
                # Parse location name
                parts = message.split(None, 1)
                if len(parts) < 2:
                    available = ", ".join(locations.keys()) if locations else "none"
                    await self.highrise.send_whisper(user.id, f"Usage: -set <location_name>\n📍 Saved locations: {available}")
                    return
                
                location_name = parts[1].strip().lower()
                
                # Find location (case-insensitive)
                location_found = None
                for loc_key in locations.keys():
                    if loc_key.lower() == location_name:
                        location_found = loc_key
                        break
                
                if not location_found:
                    available = ", ".join(locations.keys()) if locations else "none"
                    await self.highrise.send_whisper(user.id, f"❌ Location '{location_name}' not found.\n📍 Available: {available}")
                    return
                
                # Get saved coordinates
                coord_str = locations[location_found]
                x, y, z = map(float, coord_str.split(","))
                
                # Teleport bot to that location
                await self.highrise.teleport(self.bot_id, Position(x, y, z))
                await self.highrise.send_whisper(user.id, f"✅ Bot teleported to '{location_found}' at ({x}, {y}, {z})")
                print(f"Bot teleported to location {location_found}")
            except Exception as e:
                print(f"Error in /set: {e}")
                await self.highrise.send_whisper(user.id, f"❌ An error occurred: {str(e)}")

        if message.startswith("/settele "):
            # Set a teleport location with OWNER'S current position with a custom name
            user_privileges = await self.highrise.get_room_privilege(user.id)
            is_moderator = user_privileges.moderator if hasattr(user_privileges, 'moderator') else False
            if user.username not in ownerz and not is_moderator:
                await self.highrise.send_whisper(user.id, "You are not authorized to use this command.")
                return
            
            try:
                # Parse: /settele location_name
                parts = message.split(None, 1)
                if len(parts) < 2:
                    await self.highrise.send_whisper(user.id, "Usage: -settele <location_name>")
                    return
                
                location_name = parts[1].strip().lower()
                
                # Get OWNER's current position (not bot's)
                response = await self.highrise.get_room_users()
                owner_pos = None
                for room_user, position in response.content:
                    if room_user.id == user.id:  # ← Save OWNER's location, not bot's
                        owner_pos = position
                        break
                
                if owner_pos is None:
                    await self.highrise.send_whisper(user.id, "Could not find your position.")
                    return
                
                if hasattr(owner_pos, 'x') and hasattr(owner_pos, 'y') and hasattr(owner_pos, 'z'):
                    # Save OWNER's location to locations dict
                    locations[location_name] = f"{owner_pos.x},{owner_pos.y},{owner_pos.z}"
                    
                    try:
                        from casinodb import save_data
                        save_data()
                    except Exception as save_err:
                        print(f"Could not save data: {save_err}")
                    
                    await self.highrise.send_whisper(user.id, f"✅ Location '{location_name}' saved at your current position ({owner_pos.x}, {owner_pos.y}, {owner_pos.z})")
                else:
                    await self.highrise.send_whisper(user.id, "❌ You are at an anchor position.")
            except Exception as e:
                print(f"Error in /settele: {e}")
                await self.highrise.send_whisper(user.id, f"❌ An error occurred: {str(e)}")

        if message.startswith("/punch @"):
            if user.username not in ownerz:
                if user.username not in vip_users:
                    return
            try:
                user_id = await self.get_id(message)
                await self.highrise.send_emote("emote-superpunch", user.id)
                await self.highrise.send_emote("emote-death", user_id)
                await self.highrise.chat(f"💥 {user.username} punched {await self.get_username(user_id)}!")
            except Exception as e:
                print(e)

    # ===================== ADVANCED FEATURES - MESSAGE SPLITTING =====================
    
    async def send_split_message(self, message: str, is_whisper: bool = False, user_id: str = None):
        """
        Split long messages into 220 char chunks and send with delay.
        Highrise chat limit: 240 chars, using 220 for safety.
        """
        max_length = 220
        
        if len(message) <= max_length:
            # Message fits in one part
            if is_whisper and user_id:
                await self.highrise.send_whisper(user_id, message)
            else:
                await self.highrise.chat(message)
            return
        
        # Split into parts
        parts = []
        current = 0
        
        while current < len(message):
            end = min(current + max_length, len(message))
            # Try to split at space if possible
            if end < len(message):
                last_space = message.rfind(' ', current, end)
                if last_space > current:
                    end = last_space + 1
            
            parts.append(message[current:end].strip())
            current = end
        
        # Send all parts with delay
        for i, part in enumerate(parts):
            if is_whisper and user_id:
                await self.highrise.send_whisper(user_id, part)
            else:
                await self.highrise.chat(part)
            
            if i < len(parts) - 1:
                await asyncio.sleep(0.4)  # Delay between messages

    # ===================== ADVANCED FEATURES - COOLDOWN SYSTEM =====================
    
    async def check_cooldown(self, username: str) -> bool:
        """Check 5-second cooldown per user"""
        now = datetime.now()
        
        if username not in self.cooldowns:
            self.cooldowns[username] = now
            return True
        
        elapsed = (now - self.cooldowns[username]).total_seconds()
        
        if elapsed >= 5:
            self.cooldowns[username] = now
            return True
        
        return False

    # ===================== ADVANCED FEATURES - COIN SYSTEM =====================
    
    def add_coins(self, username: str, amount: int):
        """Safely add coins"""
        self.coins.setdefault(username, 0)
        self.coins[username] = max(0, self.coins[username] + amount)

    def deduct_coins(self, username: str, amount: int) -> bool:
        """Safely deduct coins (prevent negatives)"""
        self.coins.setdefault(username, 0)
        if self.coins[username] >= amount:
            self.coins[username] -= amount
            return True
        return False

    # ===================== ADVANCED FEATURES - GENERAL COMMANDS =====================
    
    async def cmd_help(self, user: User):
        """Show detailed help"""
        help_text = (
            "📖 BOT FEATURES:\n\n"
            "🎮 GAMES: -rps -slots -dice\n"
            "🧠 QUIZ: -quiz -ans\n"
            "😂 FUN: -fact -roast -thought\n"
            "💰 ECONOMY: -balance -leaderboard\n"
            "📜 INFO: -commands -emotelist -info\n"
            "🎭 EMOTES: Type just emote name like 'frog' 'wave' 'ghost'"
        )
        await self.send_split_message(help_text, is_whisper=True, user_id=user.id)

    async def cmd_commands(self, user: User):
        """Show all commands"""
        cmds = (
            "🎯 COMMANDS:\n"
            "-help -commands -games -emotelist -info\n"
            "-balance -leaderboard -fact -roast -thought\n"
            "-quiz -ans -rps -slots -dice"
        )
        await self.send_split_message(cmds, is_whisper=True, user_id=user.id)

    async def cmd_games(self, user: User):
        """Show games list"""
        games = (
            "🎮 GAMES:\n"
            "-rps rock/paper/scissors - Win 15 coins\n"
            "-slots <bet> - 1-1000 coins\n"
            "-dice <bet> <1-6> - 5x multiplier"
        )
        await self.send_split_message(games, is_whisper=True, user_id=user.id)

    async def cmd_emotelist(self, user: User):
        """Show available emotes - delegated to send_emotelist"""
        try:
            await self.send_emotelist(user)
        except Exception as e:
            print(f"Error in cmd_emotelist: {e}")
            await self.highrise.send_whisper(user.id, f"❌ Error loading emotelist: {str(e)}")

    async def cmd_info(self, user: User):
        """Show bot info"""
        info = (
            "ℹ️ BOT INFO:\n"
            "🤖 Advanced Party Bot v5.0\n"
            "✨ 15+ commands\n"
            "🎮 3 games + Quiz\n"
            "💰 Coin economy\n"
            "🏆 Leaderboard system"
        )
        await self.send_split_message(info, is_whisper=True, user_id=user.id)

    async def cmd_balance(self, user: User):
        """Show user coins"""
        self.coins.setdefault(user.username, 100)  # Give 100 starting coins on first query
        balance = f"💰 @{user.username}: {self.coins[user.username]} coins"
        await self.highrise.send_whisper(user.id, balance)

    async def cmd_leaderboard(self, user: User):
        """Show top 5 richest users"""
        if not self.coins:
            await self.highrise.send_whisper(user.id, "📊 No data yet!")
            return
        
        sorted_users = sorted(self.coins.items(), key=lambda x: x[1], reverse=True)[:5]
        
        leaderboard = "🏆 TOP 5 RICHEST:\n"
        for i, (username, coins) in enumerate(sorted_users, 1):
            leaderboard += f"{i}. @{username}: {coins}💰\n"
        
        await self.send_split_message(leaderboard, is_whisper=True, user_id=user.id)

    # ===================== ADVANCED FEATURES - FUN COMMANDS =====================
    
    async def cmd_fact(self, user: User):
        """Send random fact"""
        fact = random.choice(self.facts)
        await self.send_split_message(fact)

    async def cmd_roast(self, user: User):
        """Send random roast"""
        roast = f"🔥 @{user.username}: {random.choice(self.roasts)}"
        await self.send_split_message(roast)

    async def cmd_thought(self, user: User):
        """Send motivational thought"""
        thought = random.choice(self.thoughts)
        await self.send_split_message(thought)

    # ===================== ADVANCED FEATURES - QUIZ SYSTEM =====================
    
    async def cmd_quiz(self, user: User):
        """Start quiz question"""
        quiz = random.choice(self.quizzes)
        self.quiz_sessions[user.username] = {
            "question": quiz["question"],
            "answers": quiz["answers"],
            "attempts": 0
        }
        
        msg = f"🧠 QUIZ for @{user.username}:\n{quiz['question']}\n💡 Answer with: -ans <answer>"
        await self.send_split_message(msg)

    async def cmd_answer(self, user: User, args: list):
        """Submit quiz answer"""
        if not args:
            await self.highrise.send_whisper(
                user.id,
                "❌ Usage: -ans <answer>"
            )
            return
        
        if user.username not in self.quiz_sessions:
            await self.highrise.send_whisper(
                user.id,
                "❓ No active quiz! Type -quiz first."
            )
            return
        
        session = self.quiz_sessions[user.username]
        session["attempts"] += 1
        user_answer = " ".join(args).lower().strip()
        
        correct_answers = [a.lower().strip() for a in session["answers"]]
        
        if user_answer in correct_answers:
            reward = 20
            self.add_coins(user.username, reward)
            msg = f"✅ CORRECT @{user.username}! 🎉 +{reward} coins!"
            await self.send_split_message(msg)
            del self.quiz_sessions[user.username]
        elif session["attempts"] >= 3:
            msg = f"❌ Wrong! Max attempts reached. Correct: {session['answers'][0]}"
            await self.highrise.send_whisper(user.id, msg)
            del self.quiz_sessions[user.username]
        else:
            remaining = 3 - session["attempts"]
            await self.highrise.send_whisper(
                user.id,
                f"❌ Wrong! {remaining} attempts left."
            )

    # ===================== ADVANCED FEATURES - GAME SYSTEM =====================
    
    async def cmd_rps(self, user: User, args: list):
        """Rock Paper Scissors game"""
        choices = ["rock", "paper", "scissors"]
        
        if not args:
            msg = f"🎮 RPS started for @{user.username}!\n-rps rock/paper/scissors"
            await self.highrise.send_whisper(user.id, msg)
            return
        
        user_choice = args[0].lower()
        
        if user_choice not in choices:
            await self.highrise.send_whisper(
                user.id,
                "❌ Choose: rock, paper, or scissors"
            )
            return
        
        bot_choice = random.choice(choices)
        
        # Determine winner
        if user_choice == bot_choice:
            result = f"🤝 Tie! Both chose {bot_choice}"
        elif (user_choice == "rock" and bot_choice == "scissors" or
              user_choice == "paper" and bot_choice == "rock" or
              user_choice == "scissors" and bot_choice == "paper"):
            self.add_coins(user.username, 15)
            result = f"✅ YOU WIN! {user_choice} > {bot_choice} | +15 coins! 💰"
        else:
            result = f"❌ YOU LOSE! {bot_choice} > {user_choice}"
        
        await self.highrise.send_whisper(user.id, result)

    async def cmd_slots(self, user: User, args: list):
        """Slots casino game"""
        if not args:
            await self.highrise.send_whisper(
                user.id,
                "❌ Usage: -slots <bet 1-1000>"
            )
            return
        
        try:
            bet = int(args[0])
            if bet < 1 or bet > 1000:
                raise ValueError()
        except ValueError:
            await self.highrise.send_whisper(
                user.id,
                "❌ Bet must be 1-1000 coins"
            )
            return
        
        if not self.deduct_coins(user.username, bet):
            await self.highrise.send_whisper(
                user.id,
                f"❌ Insufficient coins! You have {self.coins.get(user.username, 0)}"
            )
            return
        
        # Spin
        symbols = ["🍎", "🍌", "🍇", "🎰", "💎", "👑"]
        spin = [random.choice(symbols) for _ in range(3)]
        
        winnings = 0
        if spin[0] == spin[1] == spin[2]:
            winnings = bet * 10
        elif len(set(spin)) == 2:
            winnings = bet * 3
        
        self.add_coins(user.username, bet + winnings)
        
        msg = f"🎰 Spin: {spin[0]} {spin[1]} {spin[2]}\n"
        if winnings > 0:
            msg += f"🎉 WIN! +{winnings} coins!"
        else:
            msg += f"😔 Lost {bet} coins"
        
        await self.highrise.send_whisper(user.id, msg)

    async def cmd_dice(self, user: User, args: list):
        """Dice game"""
        if len(args) < 2:
            await self.highrise.send_whisper(
                user.id,
                "❌ Usage: -dice <bet> <prediction 1-6>"
            )
            return
        
        try:
            bet = int(args[0])
            prediction = int(args[1])
            
            if bet < 1 or bet > 1000:
                raise ValueError("Bet out of range")
            if prediction < 1 or prediction > 6:
                raise ValueError("Prediction must be 1-6")
        except ValueError as e:
            await self.highrise.send_whisper(
                user.id,
                f"❌ Invalid input: {str(e)}"
            )
            return
        
        if not self.deduct_coins(user.username, bet):
            await self.highrise.send_whisper(
                user.id,
                f"❌ Insufficient coins!"
            )
            return
        
        roll = random.randint(1, 6)
        
        if roll == prediction:
            winnings = bet * 5
            self.add_coins(user.username, bet + winnings)
            msg = f"🎲 Rolled: {roll}\n✅ CORRECT! +{winnings} coins!"
        else:
            msg = f"🎲 Rolled: {roll}\n❌ Wrong! Lost {bet} coins"
        
        await self.highrise.send_whisper(user.id, msg)

if __name__ == "__main__":
    bot = PARTY()
    __main__.run_bot(bot)