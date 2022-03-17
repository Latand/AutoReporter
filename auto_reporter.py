import asyncio
import logging
import random
from os import listdir
from os.path import isfile, join

from colorama import Fore, init
from environs import Env

from functions import load_proxies, get_valid_channel_urls, load_channels
from telegram_api import get_client_from_session, report_channel, create_new_session


async def create_client(session_file, proxy, api_id, api_hash):
    client = await get_client_from_session(f'sessions/{session_file}', proxy=proxy, api_id=api_id, api_hash=api_hash)
    await client.connect()
    status = await client.is_user_authorized()
    logging.info(Fore.MAGENTA + f'{session_file} Connecting status: {status}')
    return client


async def start_reporting(api_id, api_hash):
    proxy_list = load_proxies()
    channels = get_valid_channel_urls(load_channels())
    sessions = [f for f in listdir('sessions') if (isfile(join('sessions', f)) and f.endswith('.session'))]
    logging.info(Fore.BLUE + f'Loaded {len(sessions)} sessions: {sessions}')

    for session_file in sessions:
        proxy = random.choice(proxy_list)
        client = await create_client(session_file, proxy, api_id, api_hash)
        for channel in channels:
            if await report_channel(client, channel):
                logging.info(Fore.GREEN + f'Channel {channel} is reported')
            else:
                logging.info(Fore.RED + f'Failed to report channel: {channel}')
            delay = random.randint(100, 548) / 100
            logging.info(Fore.BLUE + f'Sleeping for {delay}')
            await asyncio.sleep(delay)

        logging.info(Fore.BLUE + f'{session_file} Disconnecting')
        await client.disconnect()


async def report_init_session(api_id, api_hash, phone_number, password):
    client = await create_new_session(api_id, api_hash, phone_number, password)
    status = await client.is_user_authorized()
    logging.info(Fore.MAGENTA + f'Connecting status: {status}')


if __name__ == '__main__':
    init(autoreset=True)

    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format=Fore.YELLOW + u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting script")

    env = Env()
    env.read_env()

    API_ID = env.int('API_ID')
    API_HASH = env.str('API_HASH')

    asyncio.run(start_reporting(API_ID, API_HASH))
