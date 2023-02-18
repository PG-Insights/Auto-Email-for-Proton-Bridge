# -*- coding: utf-8 -*-

import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging
from aiosmtpd.smtp import SMTP


async def handle_message(message):
    print('Message received:')
    print(message)


def run_smtp_server(message_func=handle_message, port_num=1025):
    smtp_server = SMTP(message_func)
    handler = Debugging()
    handler.smtp_server = smtp_server
    controller = Controller(handler, port=port_num)

    async def start_server():
        controller.start()

    async def stop_server():
        controller.stop()

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(start_server())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(stop_server())
        loop.close()
        

if __name__ == '__main__':
    run_smtp_server()
