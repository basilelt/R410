# Client 1
import asyncio
import nats
import json
import uuid

client_id = str(uuid.uuid4())  # Generate a unique identifier for the client
subject = None
nc = None  # Make nc a global variable

async def selector_cb(msg):
    global subject
    data = msg.data.decode()
    print(data)
    user_input = await asyncio.get_event_loop().run_in_executor(None, input, "\nChoix: ")
    response = await asyncio.wait_for(nc.request('channel', user_input.encode()), timeout=10.0)
    subject = response.data.decode()
    await nc.subscribe(subject, cb=chat_cb)  # Subscribe to the selected channel
    await channel_cb(response)

async def chat_cb(msg):
    global nc, subject
    data = json.loads(msg.data.decode())
    if data['id'] != client_id:  # Only display the message if it's not from this client
        print(data['message'])
        user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Do you want to respond to this message? (yes/no/transfer/exit): ")
        if user_input.lower() == 'yes':
            response_subject = await asyncio.get_event_loop().run_in_executor(None, input, "Enter the subject to respond on (leave blank for the same subject): ")
            if not response_subject:
                response_subject = msg.subject
            response_message = await asyncio.get_event_loop().run_in_executor(None, input, "Enter your response: ")
            message = json.dumps({'id': client_id, 'message': response_message})
            await nc.publish(response_subject, message.encode())
        elif user_input.lower() == 'transfer':
            new_subject = await asyncio.get_event_loop().run_in_executor(None, input, "Enter the new subject to transfer to: ")
            await nc.unsubscribe(subject)
            subject = new_subject
            await nc.subscribe(subject, cb=chat_cb)
        elif user_input.lower() == 'exit':
            await nc.unsubscribe(subject)

async def channel_cb(msg):
    global subject
    data = msg.data.decode()
    if data == 'unknown':
        print("Unknown channel")

async def client():
    global nc
    nc = await nats.connect("nats://127.0.0.1:4222")
    response = await asyncio.wait_for(nc.request('selector', b'connected'), timeout=10.0)
    await selector_cb(response)
    
    try:
        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, input)
            if user_input:
                message = json.dumps({'id': client_id, 'message': user_input})  # Include the client ID in the message
                await nc.publish(subject, message.encode())
    except asyncio.CancelledError:
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(client())
    except KeyboardInterrupt:
        print("Program is exiting...")