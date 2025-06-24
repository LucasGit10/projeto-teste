import os
import subprocess
from jinja2 import Environment, FileSystemLoader
import argparse

def init_git_repo(app_name, branch="main", port=8080, docker_image=None):
    base_path = os.path.join("apps", app_name)
    os.makedirs(base_path, exist_ok=True)

    src_path = os.path.join(base_path, "src")
    os.makedirs(src_path, exist_ok=True)

    env = Environment(loader=FileSystemLoader("templates"))

    # Dockerfile
    dockerfile_content = env.get_template("Dockerfile.j2").render(app_name=app_name)
    with open(os.path.join(base_path, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # docker-compose.yml
    compose_content = env.get_template("docker-compose.yml.j2").render(app_name=app_name, port=port)
    with open(os.path.join(base_path, "docker-compose.yml"), "w") as f:
        f.write(compose_content)

    # README.md
    readme_text = f"# {app_name}\n\nAplicação gerada automaticamente pelo orquestrador.\n"
    with open(os.path.join(base_path, "README.md"), "w") as f:
        f.write(readme_text)

    # .gitignore
    gitignore_text = "__pycache__/\n*.pyc\n.env\n*.log\n"
    with open(os.path.join(base_path, ".gitignore"), "w") as f:
        f.write(gitignore_text)

    # workflow GitHub Actions
    workflow_content = env.get_template("github-actions.yml.j2").render(
        app_name=app_name,
        branch=branch,
        docker_image=docker_image or f"{app_name}/image",
        port=port
    )
    workflow_dir = os.path.join(base_path, ".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    with open(os.path.join(workflow_dir, "deploy.yml"), "w") as f:
        f.write(workflow_content)

    # Código exemplo simples
    exemplo_code = f"print('Aplicação {app_name} rodando')\n"
    with open(os.path.join(src_path, "main.py"), "w") as f:
        f.write(exemplo_code)

    # Inicializar git e commit
    subprocess.run(["git", "init"], cwd=base_path)
    subprocess.run(["git", "add", "."], cwd=base_path)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=base_path)

    print(f"✅ Repositório git criado em {base_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerar repositório git com pipeline CI/CD")
    parser.add_argument("app_name", help="Nome da aplicação")
    parser.add_argument("--branch", default="main", help="Branch padrão do git")
    parser.add_argument("--port", default=8080, type=int, help="Porta da aplicação")
    parser.add_argument("--docker-image", default=None, help="Nome da imagem docker")

    args = parser.parse_args()

    init_git_repo(args.app_name, branch=args.branch, port=args.port, docker_image=args.docker_image)
