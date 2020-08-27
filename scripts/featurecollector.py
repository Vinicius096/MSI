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
    num_lines = sum(1 for line in open(repo_path + '/commitinfo.log'))
    return num_lines


def linguist_script(repo_path):
    subprocess.call([
        "./linguist_script.sh", repo_path
    ])
    num_lines = sum(1 for line in open(repo_path + '/linguistfiles.log'))
    return num_lines

def gittruckfactor(repo_path, repo_fullname):
    out = open("data/TF.txt", "w+")
    subprocess.call([
        "java", "-jar", "gittruckfactor.jar", repo_path, repo_fullname
    ], stdout=out)
    return 0

def clean_repo(path: str):
    shutil.rmtree(path)

with open('data/vue.txt', 'r') as repositories:
    features = open('data/features.txt', 'w')
    features.write("Repository, Number of commits, Number of Files, TF" + '\n')
    for repo_url in repositories:
        repo_name, repo_fullname = Get_repo_name(repo_url)
        repo_path = "/home/brenner/MSI/repositories/" + repo_name
        repo = Clone_repo(repo_url, repo_path)
        num_commits = commit_log_script(repo_path)
        num_files = linguist_script(repo_path)
        TF = gittruckfactor(repo_path, repo_fullname)
        features.write(repo_fullname + ', ' + str(num_commits) + ', ' + str(num_files) + ', ' + str(TF) + '\n')
        clean_repo(repo_path)
        features.close()