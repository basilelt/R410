import asyncio
import nats

async def cb(msg):
    data = msg.data.decode()
    if data == '0':
        print(data + " " + "Even")
        await msg.respond(b'0')
    else:
        print(data + " " + "Odd")
        await msg.respond(b'1')
    

async def mafonction():
    # connexion au serveur
    nc = await nats.connect("nats://127.0.0.1:4222")

    # souscription a un sujet synchrone
    await nc.subscribe('hotline', cb=cb)
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # fermeture de la connexion
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(mafonction())
    except KeyboardInterrupt:
        print("Program is exiting...")