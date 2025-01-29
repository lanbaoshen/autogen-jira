from pathlib import Path


def load_template(file_name: str) -> str:
    file = Path(__file__).parents[1] / 'static/templates' / file_name
    if file.exists():
        with open(file, 'r') as f:
            return f.read()
    raise FileNotFoundError(f'Template file {file} not found')
