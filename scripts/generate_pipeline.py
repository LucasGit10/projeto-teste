import yaml
from jinja2 import Environment, FileSystemLoader
import os

def gerar_github_actions(settings_path="config/settings.yaml"):
    with open(settings_path, "r") as f:
        config = yaml.safe_load(f)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("github-actions.yml.j2")

    rendered = template.render(
        environment=config["environment"],
        branch="main" if config["environment"] == "producao" else "staging",
        docker_image=f'{config["app_name"]}/image'
    )

    output_path = f'.github/workflows/deploy.yml'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(rendered)

    print(f"✅ Pipeline GitHub Actions gerado em: {output_path}")

if __name__ == "__main__":
    gerar_github_actions()
