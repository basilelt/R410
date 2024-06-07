import asyncio
import nats
import json

async def banque():
    nc = await nats.connect("nats://127.0.0.1:4222")
    
    inbox = nc.new_inbox()
    async def reply(msg):
        data = json.loads(msg.data.decode())
        
        if "montant" in data:
            if data["montant"] is False:
                print("Transaction over 10 000€")
            elif data["montant"] is True:
                print("Transaction under 10 000€")
            else:
                print("Amount entered is not a valid number")
        if "compte" in data:
            if data["compte"] is False:
                print("Account not in list")
            elif data["compte"] is True:
                print("Account in list")
            else:
                print("Account entered is not an account number")
        if "date" in data:
            if data["date"] is False:
                print("Date over 10 days ago")
            elif data["date"] is True:
                print("Date under 10 days ago")
            else:
                print("Date entered is not a date")
                
    await nc.subscribe(inbox, cb=reply)
    
    try:
        account_nb = input("Enter account number (8 numbers): ")
        amount = input("Enter amount: ")
        date = input("Enter date (YYYY-MM-DD): ")
        print()
        
        await nc.publish(f'argent.{account_nb}.{amount}.{date}', b'', reply=inbox)

        # Allows to wait for responses to be received
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("\nbanque is exiting...")
        await nc.close()
    
if __name__ == '__main__':
    try:
        asyncio.run(banque())
    except KeyboardInterrupt:
        print("\nProgram is exiting...")