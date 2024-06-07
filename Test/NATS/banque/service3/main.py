import asyncio
import nats
import json
import datetime

async def service3():
    nc = await nats.connect("nats://127.0.0.1:4222")
        
    async def cb(msg):
        subject_parts = msg.subject.split('.')
        test = False
        try:
            date = datetime.datetime.strptime(subject_parts[3], "%Y-%m-%d")
        except ValueError:
            return await nc.publish(msg.reply, json.dumps({"date": test}).encode())
        
        ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
        if date >= ten_days_ago:
            test = True
        return await nc.publish(msg.reply, json.dumps({"date": test}).encode())
    
    await nc.subscribe('argent.*.*.*', cb=cb)
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("\nservice3 is exiting...")
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(service3())
    except KeyboardInterrupt:
        print("\nProgram is exiting...")