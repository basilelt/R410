import asyncio
import nats
import json

async def selector_cb(msg, nc):
    data = msg.data.decode()
    print(data)
    user_input = await asyncio.get_event_loop().run_in_executor(None, input, "\nChoix: ")
    await nc.request('channel', user_input.encode(), cb=channel_cb)

async def channel_cb(msg, nc):
    data = msg.data.decode()
    if data == 'unknown':
        print("Unknown channel")
    else:
        await nc.subscribe(data, cb=chat_cb)
        
        try:
            while True:
                user_input = await asyncio.get_event_loop().run_in_executor(None, input)
        except asyncio.CancelledError:
            await nc.close()

async def chat_cb(msg, nc):
    data = msg.data.decode()
    print(data + " " + "Répondre(1), Transférer(2), Quitter(3)")
    user_input = await asyncio.get_event_loop().run_in_executor(None, input, "\nChoix: ")
    if user_input == '1':
        reply = await asyncio.get_event_loop().run_in_executor(None, input)
        await nc.publish(msg.reply, reply.encode())
    elif user_input == '2':
        reply = await asyncio.get_event_loop().run_in_executor(None, input)
        reply = [reply, data]
        await nc.publish('transfer', json.dumps(reply).encode())
    elif user_input == '3':
        await nc.close()
        
async def client():
    nc = await nats.connect("nats://127.0.0.1:4222")
    await nc.request('selector', b'connected', cb=lambda msg: selector_cb(msg, nc))
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(client())
    except KeyboardInterrupt:
        print("Program is exiting...")