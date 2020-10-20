import git
from git import Repo
import os, sys, shutil, subprocess, re
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math

def Get_repo_name(url: str) -> str:
    
    last_slash = url.rfind("/")
    second_last_slash = url.rfind("/", 0, url.rfind("/"))
    last_suffix = url.rfind(".git")
    
    if last_suffix < 0:
        last_suffix = len(url)

    if last_slash < 0 or last_suffix <= last_slash:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash + 1:last_suffix], url[second_last_slash + 1:last_suffix]

def commit_log_script(repo_path):
    subprocess.check_call([
        "./commit_log_script.sh", repo_path
    ])

def linguist_script(repo_path):
    subprocess.check_call([
        "./linguist_script.sh", repo_path
    ])

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

def Get_hash():
    log = pd.read_csv("data/log.csv", names=["Hash","Unix"])
    indice = len(log) - 1
    log["Relative"] = log["Unix"] - log["Unix"][indice]
    idade = log["Relative"][0]
    decimo = math.floor(idade/10)
    var = decimo
    array = log["Relative"].to_numpy()
    array = array[::-1]
    lista = [log["Hash"][indice]]

    for x in range(9):
        res = next(y for y, val in enumerate(array) if val > var)
        res = indice - res
        var = var + decimo
        lista.append(log["Hash"][res])
    
    return lista
    

def gittruckfactor(repo_path, repo_fullname):
    out = open("data/TF.txt", "w")
    subprocess.check_call([
        "java", "-jar", "gittruckfactor.jar", repo_path, repo_fullname
    ], stdout=out)
    out.close
    with open("data/TF.txt", "r") as out:
        for line in out:
            if line.find("TF = ") > -1:
                print (line)
                TF_value = line[5:line.find(r"(")-1]
                return TF_value
        return 0

def checkout(repo_path, lista, repo_fullname):
    TF_list = []
    for elemt in lista:
        subprocess.check_call([
            "./commit_checkout_script.sh", repo_path, elemt
        ])
        commit_log_script(repo_path)
        linguist_script(repo_path)
        TF = gittruckfactor(repo_path, repo_fullname)
        TF_list.append(TF)

    return TF_list

def clean_repo(path: str):
    shutil.rmtree(path)

with open('data/teste.txt') as repositories:
    features = open('data/new_features.txt', 'w')
    for line in repositories:
        repo_url = line.rstrip("\n")
        repo_name, repo_fullname = Get_repo_name(repo_url)
        repo_path = "/home/brenner/MSI/repositories/" + repo_name
        repo = Clone_repo(repo_url, repo_path)
        commit_date_log_script(repo_path)
        lista = Get_hash()
        TF = checkout(repo_path, lista, repo_fullname)
        features.write(repo_fullname + ", " + "TF: ")
        for x in range(9):
            features.write(TF[x] + ", ")
        features.write(TF[9] + "\n")
        clean_repo(repo_path)
    features.close()