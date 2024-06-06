import asyncio
import nats
import json

async def run(loop):
    nc = await nats.connect("nats://127.0.01:4222", loop=loop)

    while True:
        departement = input("Enter the department: ")
        data = {
            'departement': departement
        }

        message = json.dumps(data).encode()
        await nc.publish('gareapi', message)

        msg = await nc.request('gareapi', message)
        print("Received response: ", json.dumps(json.loads(msg.data.decode()), indent=4))
        
        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != 'y':
            break

    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()