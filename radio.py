import pretty_errors
from colorama import Fore, init
from core.config import get_config
from core.logger import get_logger
from core.streamthread import StreamThread

init(autoreset=True)
pretty_errors.activate()
print(f"{Fore.YELLOW}[*] Radio loading...")

config = get_config()
logger = get_logger(__name__)
logger.info("Configuration & logger loaded")

print(f"{Fore.YELLOW}[*] Streams loading...")
for stream_name, stream_config in config.streams.items():
    try:
        StreamThread(
            stream_index = stream_config.get("mountpoint"),
            music_directory = stream_config.get("directory"),
            station_url = stream_config.get("station_url"),
            genre = stream_config.get("genre"),
            name = stream_config.get("name"),
            description = stream_config.get("description"),
        ).start()
    except:
        logger.error("There was an error trying to start %s", stream_config.get("name"))
