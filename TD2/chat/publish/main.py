import asyncio
import nats
import json

class Server:
    def __init__(self):
        self.nc = None

    async def selector_cb(self, msg):
        data = msg.data.decode()
        if data == 'connected':
            channels = [
                'Sélectionner le salon :',
                '1. Général',
                '2. RT',
                '3. Annonces',
            ]
            await self.nc.publish(msg.reply, '\n'.join(channels).encode())

    async def channel_cb(self, msg):
        data = msg.data.decode()
        if data == '1':
            await self.nc.publish(msg.reply, b'general')
        elif data == '2':
            await self.nc.publish(msg.reply, b'rt')
        elif data == '3':
            await self.nc.publish(msg.reply, b'annonces')
        else:
            await self.nc.publish(msg.reply, b'unknown')

    async def transfer_cb(self, msg):
        data = json.loads(msg.data.decode())
        await self.nc.publish(data[1], data[0].encode())

    async def selector_wrapper(self, msg):
        await self.selector_cb(msg)

    async def channel_wrapper(self, msg):
        await self.channel_cb(msg)

    async def transfer_wrapper(self, msg):
        await self.transfer_cb(msg)

    async def run(self):
        self.nc = await nats.connect("nats://127.0.0.1:4222")
        await self.nc.subscribe('selector', cb=self.selector_wrapper)
        await self.nc.subscribe('channel', cb=self.channel_wrapper)
        await self.nc.subscribe('transfer', cb=self.transfer_wrapper)
        
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("AsyncIO is exiting...")
            await self.nc.close()

if __name__ == '__main__':
    server = Server()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("Program is exiting...")