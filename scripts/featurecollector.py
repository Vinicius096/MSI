# parametros: url do repositorio
# passo 1: clonar um repositorio
# passo 2: extrair as seguintes caracteristicas
# A) linguagem
# B) numero de commits que alterem um arquivo da linguagem
# C) numero de devs que alteraram um arquivo da linguagem
# D) numero de arquivos da linguagem
# E) Truck Factor do repositório
# passo 3: excluir o repositorio

from git import Repo
import os, sys

def get_repo_name(url: str) -> str:
    
    last_slash = url.rfind("/")
    last_suffix = url.rfind(".git")
    
    if last_suffix < 0:
        last_suffix = len(url)

    if last_slash < 0 or last_suffix <= last_slash:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash + 1:last_suffix]


repositories = open('data/vue.txt', 'r')
repo_url = repositories.readline()
repo_name = get_repo_name(repo_url)
repo_path = "/home/brenner/MSI/repositories/" + repo_name
os.mkdir(repo_path)
Repo.clone_from(repo_url, repo_path)
