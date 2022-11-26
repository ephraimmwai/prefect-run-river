import requests
import json
from prefect import flow, task
from prefect.filesystems import GitHub
from prefect.blocks.system import JSON
from prefect.blocks.system import Secret


json_block = JSON.load("payload")
github_block = GitHub.load("github-rivery")
secret_block = Secret.load("api-token")
access_token =secret_block.get()

payload = json.dumps(json_block)
headers = {
 'Content-Type': 'application/json',
 'Authorization': access_token
}


@task
def call_river_api(url):
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

@flow(name="run_river")
def run_river(url):
    results = call_river_api(url)
    return results

if __name__ == "__main__":
    run_river(url="https://console.rivery.io/api/run") 
