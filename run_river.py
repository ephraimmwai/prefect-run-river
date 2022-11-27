import requests
import json as json_r
from prefect import flow, task, get_run_logger
from prefect.filesystems import GitHub
from prefect.blocks.system import JSON,Secret

json_block = JSON.load("payload")
github_block = GitHub.load("github-rivery")
secret_block = Secret.load("api-token")

access_token =secret_block.value.get_secret_value()

payload = json_r.dumps(json_block.value)

headers = {
 'Content-Type': 'application/json',
 'Authorization': access_token.strip('"\'')
}


@task
def call_river_api(url):
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

# @task
# def display_it():
#     json_block = JSON.load("payload")
#     logger=get_run_logger()
#     logger.info(access_token)




@flow(name="run_river")
def run_river(url):
    results = call_river_api(url)
    logger=get_run_logger()
    logger.info(results)
   
    # display_it()

if __name__ == "__main__":
    run_river(url="https://console.rivery.io/api/run") 