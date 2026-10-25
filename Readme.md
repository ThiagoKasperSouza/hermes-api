# Hermes api gateway

Projeto capaz de consumir a gateway do hermes por meio da compatibilidade com openai


## Config:
```bash
docker compose up -d
docker compose exec hermes-api bash
hermes auth add nous --type oauth --no-browser
hermes model
```

## Rodar
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install openai python-dotenv
python main.py
``