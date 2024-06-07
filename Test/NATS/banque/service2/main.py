import asyncio
import nats
import json

async def service2():
    nc = await nats.connect("nats://127.0.0.1:4222")
    
    evange_list = ["12345678", "87654321", "98765432", "23456789"]
    
    async def cb(msg):
        subject_parts = msg.subject.split('.')
        account = subject_parts[1]
        if account.isdigit() is False or len(account) != 8:
            return await nc.publish(msg.reply, json.dumps({"compte": "not an account number"}).encode())
        test = False
        if account in evange_list:
            test = True
        return await nc.publish(msg.reply, json.dumps({"compte": test}).encode())
    
    await nc.subscribe('argent.*.*.*', cb=cb)
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("\nservice2 is exiting...")
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(service2())
    except KeyboardInterrupt:
        print("\nProgram is exiting...")