#!/usr/bin/python3

from github import Github
import requests

# using username and password
g = Github()

repo_list = ["tpcp-project/tar",
             "tpcp-project/sqlite"]

for repo_id in repo_list:

    repo = g.get_repo(repo_id)

    #print(repo)

    rel = repo.get_latest_release()

    #print(rel)

    assets = rel.get_assets()

    #print(assets)

    #print(assets.totalCount)

    for asset in assets:
        #print(asset)
        #print(asset.name)
        #print(asset.browser_download_url)
        
        with open('TESTBED_EXECUTABLES/'+asset.name, 'wb') as f:
            f.write(requests.get(asset.browser_download_url).content)
