import click
import os
import yaml
import subprocess
from jinja2 import Environment, FileSystemLoader

CONFIG_DIR = "config"
TEMPLATES_DIR = "templates"

@click.command()
@click.option("--app-name", prompt="Nome da aplicação")
@click.option("--environment", type=click.Choice(['homolog', 'producao']), prompt="Ambiente")
@click.option("--cloud", type=click.Choice(['aws', 'gcp', 'azure', 'local']), prompt="Cloud Provider")
@click.option("--port", prompt="Porta da aplicação", default="8080")
@click.option("--repository", prompt="URL do repositório Git")
def gerar_configuracao(app_name, environment, cloud, port, repository):
    """
    Gera arquivos de configuração da aplicação: Docker, Compose, CI/CD e settings.
    Também gera a estrutura do repositório git com pipeline CI/CD dentro de apps/<app_name>/
    """
    print("🔧 Gerando configurações...")

    # Salvar configurações YAML
    config_data = {
        'app_name': app_name,
        'environment': environment,
        'cloud': cloud,
        'port': port,
        'repository': repository
    }

    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(os.path.join(CONFIG_DIR, "settings.yaml"), "w") as f:
        yaml.dump(config_data, f)
    print("✅ settings.yaml gerado")

    # Renderizar templates Dockerfile e docker-compose na raiz (opcional)
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    dockerfile_template = env.get_template("Dockerfile.j2")
    compose_template = env.get_template("docker-compose.yml.j2")

    with open("Dockerfile", "w") as f:
        f.write(dockerfile_template.render(app_name=app_name))

    with open("docker-compose.yml", "w") as f:
        f.write(compose_template.render(app_name=app_name, port=port))

    print("✅ Dockerfile e docker-compose.yml gerados com sucesso!")

    # === Etapa 8: gerar repositório git completo com pipeline no apps/<app_name>/ ===
    print(f"🚀 Gerando repositório git e pipeline CI/CD para {app_name} em apps/{app_name}/ ...")

    # Chama script init_git_repo.py via subprocess
    script_path = os.path.join("scripts", "init_git_repo.py")
    cmd = ["python3", script_path, app_name, "--port", str(port)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Repositório git criado com sucesso:\n{result.stdout}")
    else:
        print(f"❌ Erro ao criar repositório git:\n{result.stderr}")

if __name__ == "__main__":
    gerar_configuracao()
