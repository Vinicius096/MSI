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
import os, sys, shutil

def Get_repo_name(url: str) -> str:
    
    last_slash = url.rfind("/")
    last_suffix = url.rfind(".git")
    
    if last_suffix < 0:
        last_suffix = len(url)

    if last_slash < 0 or last_suffix <= last_slash:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash + 1:last_suffix]

def Clone_repo(url: str, path: str):
    os.mkdir(path)
    repo = Repo.clone_from(url, path)
    return repo

def clean_repo(path: str):
    shutil.rmtree(path)

def Git_logger(repo, repo_name: str, features):
    loc = count_LOC()
    devs = count_devs()
    files = count_files()
    commits = count_commits()
    return loc, devs, files, commits

def count_LOC():
    return 0

def count_devs():
    return 0

def count_files():
    return 0

def count_commits():
    return 0

with open('data/vue.txt', 'r') as repositories:
    features = open('data/features', 'w')
    for repo_url in repositories:
        repo_name = Get_repo_name(repo_url)
        repo_path = "/home/brenner/MSI/repositories/" + repo_name
        repo = Clone_repo(repo_url, repo_path)
        Git_logger(repo, repo_name, features)
        clean_repo(repo_path)
    features.close()