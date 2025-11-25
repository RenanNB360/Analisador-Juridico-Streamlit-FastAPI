def load_prompt(name: str):
    with open(f'backend/service/prompts/{name}.txt', 'r', encoding='utf-8') as f:
        return f.read()
