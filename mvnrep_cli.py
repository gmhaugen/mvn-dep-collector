import requests
from bs4 import BeautifulSoup
import time

"""
Fetches dependencies from mvnrepository.com based on filename.jar.
"""

BASEURL = "https://mvnrepository.com/"
HEADERS = {"Accept": "application/json", "Request": "application/json"}
TIMEOUT = (1, 5)
SESSION = requests.Session()

def get_dependency_details(artifact_id, version, group_id=None):
    if group_id is None:
        group_id = artifact_id
    url = f"{BASEURL}artifact/{group_id}/{artifact_id}/{version}"
    response = SESSION.get(url=url, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        return [response.status_code, url, response]
    elif response.status_code == 404:
        group_id = artifact_id.split("-")[0]
        url = f"{BASEURL}artifact/{group_id}/{artifact_id}/{version}"
        response = SESSION.get(url=url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 200 or response.status_code == 404:
            return [response.status_code, url, response]
    else:
        return [response.status_code, url, response]

def filter_dependency(data):
    soup = BeautifulSoup(data, "html.parser")
    lines = str(soup.find(id="maven-a")).split("\n")[1:-1]
    dependency = ""
    for i in range(0, len(lines)):

        dependency += "\t\t" + lines[i]
        if i is not len(lines) - 1:
            dependency += "\n"
    return dependency.replace("&lt;", "<").replace("&gt;", ">")

path = "../.."
with open(f"{path}/libraries.lst", "r") as infile:
    with open(f"{path}/dependencies.xml", "w") as depfile:
        with open(f"{path}/deps_not_found.lst", "w") as nffile:
            for line in infile.readlines():
                print(line)
                dash_count = 0
                for i in range(0, len(line)):
                    if i == len(line) - 5:
                        break
                    if line[i] == '.':
                        break
                    if line[i] == '-':
                        dash_count += 1
                if dash_count == 0:
                    depfile.write(f"{line}\n")
                elif dash_count == 1:
                    group_id = line.split("-")[0]
                    version = line.split("-")[1][:-5]
                    response = get_dependency_details(group_id, version)
                    if response[0] == 200:
                        dependency = filter_dependency(response[2].text)
                        print("ok")
                        depfile.write(f"{dependency}\n")
                    else:
                        nffile.write(f"{line}\n")
                elif dash_count >= 2:
                    new_group_id = ""
                    group_id = line.split("-")[:len(line.split("-")) - 1]
                    version = line.split("-")[len(line.split("-")) - 1][:-5]
                    if len(version) == 1:
                        version = group_id[len(group_id) - 1] + "-" + version
                    for i in range(0, len(group_id)):
                        appended_dash = ""
                        if i is not len(group_id):
                            appended_dash = "-"
                        if version.startswith(group_id[i]):
                            del group_id[i]
                            group_id[i - 1] = group_id[i - 1][:len(group_id[i - 1]) - 1]
                            break
                        new_group_id += group_id[i] + appended_dash
                    if new_group_id.endswith('-'):
                        new_group_id = new_group_id[:-1]
                    response = get_dependency_details(new_group_id, version)
                    if response[0] == 200:
                        dependency = filter_dependency(response[2].text)
                        print("ok")
                        depfile.write(f"{dependency}\n")
                    else:
                        nffile.write(f"{line}\n")
                else:
                    print("e")

                time.sleep(10)
