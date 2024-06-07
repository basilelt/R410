# Commandes

## Insérer un nouvel album
```bash
curl -d @insert.json -H 'Content-Type: application/json' http://127.0.0.1:8000/albumapi/api/
```

## Récupérer l'album d'ID 2
```bash
curl http://127.0.0.1:8000/albumapi/api/2/ 
```

## Récupérer l'album dont le titre est "smells like teen spirit"
```bash
curl "http://127.0.0.1:8000/albumapi/api/?title=smells+like+teen+spirit"
```