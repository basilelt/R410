# Résultat des tests
```bash
~/R410/Test/NATS/banque/publish main* 5m 56s
(.venv) .venv ❯ python main.py
Enter account number: 12345678
Enter amount: 5000
Enter date (YYYY-MM-DD): 2024-06-01

Transaction under 10 000€
Account in list
Date under 10 days ago
^C
banque is exiting...

~/R410/Test/NATS/banque/publish main* 23s
(.venv) .venv ❯ python main.py
Enter account number: 12345
Enter amount: 15000
Enter date (YYYY-MM-DD): 2024-05-01

Transaction over 10 000€
Date over 10 days ago
Account not in list
```