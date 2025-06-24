import click
import os
import yaml
import subprocess
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "templates"
CONFIG_DIR = "config"
ANSIBLE_HOSTS = "ansible/hosts.ini"

@click.command()
@click.option("--app-name", prompt="Nome da aplicação")
@click.option("--environment", type=click.Choice(['homolog', 'producao']), prompt="Ambiente")
@click.option("--cloud", type=click.Choice(['aws', 'gcp', 'azure', 'local']), prompt="Cloud (aws, gcp, azure, local)")
@click.option("--port", prompt="Porta da aplicação", default="8080")
@click.option("--repository", prompt="URL do repositório Git")
@click.option("--ssh-key", prompt="Nome da chave SSH na sua máquina")
def orquestrar(app_name, environment, cloud, port, repository, ssh_key):
    # 1. Gerar settings.yaml
    config = {
        'app_name': app_name,
        'environment': environment,
        'cloud': cloud,
        'port': port,
        'repository': repository,
        'ssh_key': ssh_key
    }

    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(f"{CONFIG_DIR}/settings.yaml", "w") as f:
        yaml.dump(config, f)
    click.echo("✅ settings.yaml gerado")

    # 2. Gerar Dockerfile e docker-compose.yml
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    dockerfile = env.get_template("Dockerfile.j2").render(app_name=app_name)
    compose = env.get_template("docker-compose.yml.j2").render(app_name=app_name, port=port)

    with open("Dockerfile", "w") as f:
        f.write(dockerfile)

    with open("docker-compose.yml", "w") as f:
        f.write(compose)

    click.echo("✅ Dockerfile e docker-compose.yml gerados")

    # 3. Executar Terraform na cloud escolhida
    terraform_dir = f"terraform/{cloud}"

    if cloud == "aws":
        terraform_cmd = [
            "terraform", "apply", "-auto-approve",
            f"-var=ssh_key_name={ssh_key}",
            f"-var=app_port={port}"
        ]
    elif cloud == "gcp":
        terraform_cmd = [
            "terraform", "apply", "-auto-approve",
            f"-var=credentials_file=~/.gcp/credentials.json",
            f"-var=project=seu-projeto",
            f"-var=public_key_path=~/.ssh/{ssh_key}.pub"
        ]
    elif cloud == "azure":
        terraform_cmd = [
            "terraform", "apply", "-auto-approve",
            f"-var=ssh_public_key=~/.ssh/{ssh_key}.pub"
        ]
    elif cloud == "local":
        terraform_cmd = ["terraform", "apply", "-auto-approve"]

    subprocess.run(terraform_cmd, cwd=terraform_dir)
    click.echo("✅ Infraestrutura provisionada")

    # 4. Ler IP do output do Terraform
    output = subprocess.check_output(["terraform", "output", "-raw", "instance_ip"], cwd=terraform_dir)
    instance_ip = output.decode().strip()
    click.echo(f"🌐 IP da instância: {instance_ip}")

    # 5. Criar ansible/hosts.ini
    with open(ANSIBLE_HOSTS, "w") as f:
        f.write(f"[app]\n{instance_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/{ssh_key}.pem\n")

    # 6. Rodar playbooks Ansible
    subprocess.run(["ansible-playbook", "-i", ANSIBLE_HOSTS, "install_docker.yml"], cwd="ansible")
    subprocess.run(["ansible-playbook", "-i", ANSIBLE_HOSTS, "deploy_app.yml"], cwd="ansible")
    subprocess.run(["ansible-playbook", "-i", ANSIBLE_HOSTS, "setup_monitoring.yml"], cwd="ansible")
    click.echo("✅ Aplicação provisionada com observabilidade")

    # 7. Gerar CI/CD pipeline
    subprocess.run(["python", "scripts/generate_pipeline.py"])
    click.echo("✅ Pipeline GitHub Actions gerado")

    click.echo("🎉 Orquestração finalizada com sucesso!")

if __name__ == "__main__":
    orquestrar()