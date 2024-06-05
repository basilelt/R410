import asyncio
import nats

async def cb(msg):
    print(msg.data.decode())

async def mafonction():
    nc = await nats.connect("nats://127.0.0.1:4222")

    inbox = nc.new_inbox()
    await nc.subscribe(inbox, cb=cb)
    
    n = 0
    try:
        while True:
            if n % 2 == 0:
                await nc.publish('hotline', b'0', reply=inbox)
            else:
                await nc.publish('hotline', b'1', reply=inbox)
            n += 1
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        print("mafonction is exiting...")
        
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(mafonction())
    except KeyboardInterrupt:
        print("Program is exiting...")