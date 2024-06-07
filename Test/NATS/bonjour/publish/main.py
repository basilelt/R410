import asyncio
import nats

async def bonjour():
    nc = await nats.connect("nats://127.0.0.1:4222")
    
    inbox = nc.new_inbox()
    async def reply(msg):
        print(f"Received reply: {msg.data.decode()}")
    await nc.subscribe(inbox, cb=reply)

    try:
        for i in range(10):
            # Strasbourg matin is the only one with an inbox
            await nc.publish('bonjour.strasbourg.matin', ("Strasbourg matin: " + str(i)).encode(), reply=inbox)
            await nc.publish('bonjour.strasbourg.midi', ("Strasbourg midi: " + str(i)).encode())
            await nc.publish('bonjour.colmar.matin', ("Colmar matin: " + str(i)).encode())
            await asyncio.sleep(1)
        # Allows to wait for responses to be received
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