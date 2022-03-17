import socks
from telethon import functions, types, TelegramClient
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError

from functions import get_random_language


async def report_channel(client, channel_url: str):
    channel_info_by_url = await client.get_entity(channel_url)

    result = await client(functions.messages.ReportRequest(
        peer=channel_info_by_url,
        id=[1],
        reason=types.InputReportReasonOther(),
        message='Неправдива інформація про війну Росії з Україною\n'
                'Неправдивая информация о войне России с Украиной\n'
                'False information about Russia\'s war with Ukraine\n'
                'Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainians and Ukrainian soldiers.\n'
                'Пропаганда війни в Україні. Пропаганда вбивства українців та українських солдат.'))
    return result


async def get_client_from_session(session_path, proxy, api_hash, api_id):
    lang_code = get_random_language()
    while True:
        # host, port = proxy.strip().split(':')
        # proxy = (socks.SOCKS5, host, int(port))
        proxy = None
        try:
            client = TelegramClient(session=session_path,
                                    api_hash=api_hash,
                                    api_id=api_id,
                                    proxy=proxy,
                                    lang_code=lang_code,
                                    system_lang_code=lang_code)
            return client

        except (socks.ProxyConnectionError, socks.GeneralProxyError):
            return await get_client_from_session(session_path, proxy, api_hash, api_id)


async def create_new_session(api_id: int, api_hash: str, phone_number, password=None):
    client = TelegramClient(f'sessions/{phone_number}',
                            api_hash=api_hash,
                            api_id=api_id)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input('Enter the code sent to you in the Telegram: '))
        except SessionPasswordNeededError:
            await client.sign_in(phone_number, password=password)

    return client
