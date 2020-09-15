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

def commit_log_script(repo_path):
    subprocess.check_call([
        "./commit_log_script.sh", repo_path
    ])
    num_lines = 0
    #num_lines = sum(1 for line in open(repo_path + '/commitinfo.log'))
    return num_lines

def linguist_script(repo_path):
    subprocess.check_call([
        "./linguist_script.sh", repo_path
    ])
    LOC = 0
    num_lines = 0
    #print ("Counting lines of code...")
    #for line in open(repo_path + '/linguistfiles.log'):
    #    LOC += get_LOC(repo_path, line)
    #    num_lines += 1
    
    return num_lines, LOC

def get_LOC(repo_path, line):
    line = line.rstrip("\n")
    first_semicolon = line.find(";")
    target = "/" + line[first_semicolon+1:]
    if target.find(' ') > 0:
        return 0
    else:
        subprocess.check_call([
        "./count_loc_script.sh", repo_path, target
        ])
        with open( repo_path + '/LOC.txt', 'r') as LOC_file:
            contents = LOC_file.read()
            if contents.find("1 text file.") > 0:
                if contents.find("1 file ignored.") > 0:
                    return 0

                else:
                    sum_index = contents.find("SUM:")
                    sum_text = contents[sum_index:]
                    sum_text = sum_text[:sum_text.find('\n')]
                    LOC = int(re.findall(r'\d+', sum_text)[-1])
                    
            else:
                return 0

    return LOC

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


def devs_log_script(repo_path):
    subprocess.check_call([
        "./devs_log_script.sh", repo_path
    ])
    num_lines = 0
    #num_lines = sum(1 for line in open(repo_path + '/devsinfo.log'))
    return num_lines

def clean_repo(path: str):
    shutil.rmtree(path)

with open('data/systems.txt', 'r') as repositories:
    features = open('data/features.txt', 'w')
    features.write("Repository, Number of commits, Number of Files, LOC, TF, Number of Devs" + '\n')
    for line in repositories:
        repo_url = line.rstrip("\n")
        repo_name, repo_fullname = Get_repo_name(repo_url)
        repo_path = "/home/brenner/MSI/repositories/" + repo_name
        repo = Clone_repo(repo_url, repo_path)
        num_commits = commit_log_script(repo_path)
        num_files, LOC = linguist_script(repo_path)
        TF = gittruckfactor(repo_path, repo_fullname)
        num_devs = devs_log_script(repo_path)
        features.write(repo_fullname + ', ' + str(num_commits) + ', ' + str(num_files) + ', ' + str(LOC) + ', ' + TF + ', ' + str(num_devs) +'\n')
        clean_repo(repo_path)
    features.close()