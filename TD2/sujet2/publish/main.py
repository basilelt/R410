import asyncio
import nats
import json

async def selector_cb(msg, nc):
    data = msg.data.decode()
    if data == 'connected':
        channels = [
            'Sélectionner le salon :',
            '1. Général',
            '2. RT',
            '3. Annonces',
        ]
        await nc.publish(msg.reply, '\n'.join(channels).encode())

async def channel_cb(msg, nc):
    data = msg.data.decode()
    if data == '1':
        await nc.publish(msg.reply, b'general')
    elif data == '2':
        await nc.publish(msg.reply, b'rt')
    elif data == '3':
        await nc.publish(msg.reply, b'annonces')
    else:
        await nc.publish(msg.reply, b'unknown')

async def transfer_cb(msg, nc):
    data = json.loads(msg.data.decode())
    await nc.publish(data[1], data[0].encode())
        
async def server():
    nc = await nats.connect("nats://127.0.0.1:4222")
    await nc.subscribe('selector', cb=lambda msg: selector_cb(msg, nc))
    await nc.subscribe('channel', cb=lambda msg: channel_cb(msg, nc))
    await nc.subscribe('transfer', cb=lambda msg: transfer_cb(msg, nc))
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("AsyncIO is exiting...")
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(server())
    except KeyboardInterrupt:
        print("Program is exiting...")