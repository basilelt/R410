import asyncio
import nats

async def mafonction():
    # connexion au serveur
    nc = await nats.connect("nats://127.0.0.1:4222")

    # souscription a un sujet ou publication
    inbox = nc.new_inbox()
    
    compteur = 0
    try:
        while True:
            await nc.publish('compteur', str(compteur).encode(), reply=inbox)
            compteur += 2
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("mafonction is exiting...")
        
        # fermeture de la connexion
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(mafonction())
    except KeyboardInterrupt:
        print("Program is exiting...")