import git
from git import Repo
import os, sys, shutil, subprocess, re

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
    print ("Cloning repository " + url + " to " + path)
    os.mkdir(path)
    repo = Repo.clone_from(url, path)
    print ("Repository cloned")
    return repo

def commit_date_log_script(repo_path):
    subprocess.check_call([
        "./commit_date_log_script.sh", repo_path
    ])

def clean_repo(path: str):
    shutil.rmtree(path)

with open('data/teste.txt') as repositories:
    #features = open('data/new_features.txt', 'w')
    for line in repositories:
        repo_url = line.rstrip("\n")
        repo_name, repo_fullname = Get_repo_name(repo_url)
        repo_path = "/home/brenner/MSI/repositories/" + repo_name
        repo = Clone_repo(repo_url, repo_path)
        commit_date_log_script(repo_path)
        clean_repo(repo_path)
    #features.close()