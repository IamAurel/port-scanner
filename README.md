# TCP Port Scanner

Un scanner de ports TCP en Python.  
Il supporte le multi-threading et peut récupérer les banners des services ouverts.

## Installation

```bash
git clone https://github.com/IamAurel/port-scanner
cd port-scanner
```

## Utilisation

```bash
python cli.py -t <target> -p <port>
```

## Options

- `-t`, `--target` : IP ou hostname
- `-p`, `--ports` : port ou range (ex: 22 ou 1-1024)
- `-w`, `--workers` : nombre de threads (défaut 50)
- `--banner` : active le banner grabbing (plus lent)
- `--json` : exporte les résultats en JSON

## Exemple

```bash
python cli.py -t scanme.nmap.org -p 1-100 --banner --json result.json
```

## Notes

- À utiliser uniquement sur des cibles autorisées.
- Le banner grabbing est basique et peut ne pas fonctionner sur tous les services.
