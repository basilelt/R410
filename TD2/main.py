import asyncio
import nats

async def mafonction():
    # connexion au serveur
    nc = await nats.connect("http ://127.0.0.1:4222")

    # souscription a un sujet ou publication

    # fermeture de la connexion
    await nc.close()
    
if __name__ == '__main__':
    asyncio.run(mafonction())