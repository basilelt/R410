# Client 1
import asyncio
import nats
import json
import uuid
import threading

client_id = str(uuid.uuid4())  # Generate a unique identifier for the client
subject = None
nc = None  # Make nc a global variable
subscription = None  # Store the Subscription object
exit_flag = False  # Flag to indicate when to exit the program

async def selector_cb(msg):
    global subject, subscription
    data = msg.data.decode()
    print(data)
    user_input = await asyncio.get_event_loop().run_in_executor(None, input, "\nChoix: ")
    response = await asyncio.wait_for(nc.request('channel', user_input.encode()), timeout=10.0)
    subject = response.data.decode()
    subscription = await nc.subscribe(subject, cb=chat_cb)  # Store the Subscription object

async def chat_cb(msg):
    global nc, subject, subscription
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
            await subscription.unsubscribe()  # Unsubscribe using the Subscription object
            response = await asyncio.wait_for(nc.request('selector', b'connected'), timeout=10.0)
            await selector_cb(response)  # Show the channel list again
        elif user_input.lower() == 'exit':
            global exit_flag
            exit_flag = True
            await subscription.unsubscribe()  # Unsubscribe using the Subscription object

def input_thread(loop):
    global exit_flag
    while not exit_flag:
        user_input = input()
        if user_input:
            message = json.dumps({'id': client_id, 'message': user_input})  # Include the client ID in the message
            asyncio.run_coroutine_threadsafe(nc.publish(subject, message.encode()), loop)

async def client():
    global nc
    nc = await nats.connect("nats://127.0.0.1:4222")
    response = await asyncio.wait_for(nc.request('selector', b'connected'), timeout=10.0)
    await selector_cb(response)
    
    threading.Thread(target=input_thread, args=(asyncio.get_event_loop(),), daemon=True).start()  # Start the input thread
    
    try:
        while not exit_flag:
            await asyncio.sleep(1)  # Wait for the exit_flag to be set
    except asyncio.CancelledError:
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(client())
    except KeyboardInterrupt:
        print("Program is exiting...")