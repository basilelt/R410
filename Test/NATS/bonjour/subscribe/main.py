import asyncio
import nats

async def bonjour():
    nc = await nats.connect("nats://127.0.0.1:4222")
    
    async def cb(msg):
        data = msg.data.decode()
        print(data)
        
        # Automatically reply to the message if an inbox is provided, don't block the event loop with an input() call
        if msg.reply:
            await nc.publish(msg.reply, ("Received your message -> " + data).encode())
            
    async def cb_strasbourg_midi(msg):
        print(msg.data.decode())
    async def cb_colmar_matin(msg):
        print(msg.data.decode() + "\n")
    
    # await nc.subscribe('bonjour.*.matin', cb=cb)
    # await nc.subscribe('bonjour.*.midi', cb=cb)
    await nc.subscribe('bonjour.strasbourg.matin', cb=cb)
    await nc.subscribe('bonjour.strasbourg.midi', cb=cb_strasbourg_midi)
    await nc.subscribe('bonjour.colmar.matin', cb=cb_colmar_matin)
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("\nbonjour is exiting...")
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(bonjour())
    except KeyboardInterrupt:
        print("\nProgram is exiting...")