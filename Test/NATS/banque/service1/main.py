import asyncio
import nats
import json

async def service1():
    nc = await nats.connect("nats://127.0.0.1:4222")
    
    async def cb(msg):
        subject_parts = msg.subject.split('.')
        try:
            amount = int(subject_parts[2])
        except ValueError:
            return await nc.publish(msg.reply, json.dumps({"montant": "not a number"}).encode())
        if amount < 0:
            return await nc.publish(msg.reply, json.dumps({"montant": "negative"}).encode())
        test = True
        if amount > 10000:
            test = False
        return await nc.publish(msg.reply, json.dumps({"montant": test}).encode())
    
    await nc.subscribe('argent.*.*.*', cb=cb)
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("\nservice1 is exiting...")
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(service1())
    except KeyboardInterrupt:
        print("\nProgram is exiting...")