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
import os, sys, shutil, subprocess

def Get_repo_name(url: str) -> str:
    
    last_slash = url.rfind("/")
    second_last_slash = url.rfind("/", 0, url.rfind("/"))
    last_suffix = url.rfind(".git")
    
    if last_suffix < 0:
        last_suffix = len(url)

    if last_slash < 0 or last_suffix <= last_slash:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash + 1:last_suffix], url[second_last_slash + 1:last_suffix]

def Clone_repo(url: str, path: str):
    os.mkdir(path)
    repo = Repo.clone_from(url, path)
    return repo

def commit_log_script(repo_path):
    subprocess.call([
        "./commit_log_script.sh", repo_path
    ])

def linguist_script(repo_path):
    subprocess.call([
        "./linguist_script.sh", repo_path
    ])

def gittruckfactor(repo_path, repo_fullname):
    subprocess.call([
        "java", "-jar", "gittruckfactor.jar", repo_path, repo_fullname
    ])

def clean_repo(path: str):
    shutil.rmtree(path)

with open('data/vue.txt', 'r') as repositories:
    features = open('data/features', 'w')
    for repo_url in repositories:
        repo_name, repo_fullname = Get_repo_name(repo_url)
        repo_path = "/home/brenner/MSI/repositories/" + repo_name
        repo = Clone_repo(repo_url, repo_path)
        commit_log_script(repo_path)
        linguist_script(repo_path)
        gittruckfactor(repo_path, repo_fullname)
        #clean_repo(repo_path)
    features.close()