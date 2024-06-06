import asyncio
import nats
import os
import signal
import aiohttp
import json

async def cb(msg):
    data = json.loads(msg.data.decode())
    departement = data.get('departement')

    if departement:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://web/gareapi/api/', params={'departement': departement}) as resp:
                res = await resp.text()
                await msg.respond(res.encode())
    else:
        await msg.respond('No departement provided'.encode())

async def bridge():
    nc = await nats.connect("nats://nats:4222")

    await nc.subscribe('gareapi', cb=cb)
    
    try:
        while True:
            await asyncio.sleep(1)
    except (asyncio.CancelledError, SystemExit):
        await nc.close()

def handle_exit(*args):
    raise SystemExit()

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handle_exit)
    try:
        asyncio.run(bridge())
    except (KeyboardInterrupt, SystemExit):
        print("Program is exiting...")