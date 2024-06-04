import asyncio
import nats

async def cb(msg):
    print(f"message recu {msg.data.decode()}")

async def mafonction():
    # connexion au serveur
    nc = await nats.connect("nats://127.0.0.1:4222")

    # souscription a un sujet synchrone
    await nc.subscribe('compteur', cb=cb)
    
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