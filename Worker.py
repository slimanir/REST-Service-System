from radon.metrics import mi_visit
from radon.complexity import cc_visit, cc_rank
from pygit2 import Repository, clone_repository
import requests, json


FLASK_SERVER_NAME = 'https://api.github.com/repos/slimanir/REST-Service-System'

def set_repo():
    try:
        repo = Repository('./repo')
    except:
        repo_url = 'FLASK_SERVER_NAME'
        repo_path = './repo'
        repo = clone_repository(repo_url, repo_path)
    return repo
##### Code complexity calculation ###
def compute_complexity(source):
    result =[]
    blocks = cc_visit(source)
    mi = mi_visit(source, True)

    for func in blocks:
        result.append(func.name+"- CC Rank:"+cc_rank(func.complexity))
    return result

##### Exctract files and store them in the list of files 

def extract_files(sources):
    files = []
    for source in sources:
        files.append(repo[source.id].data.decode("utf-8"))
    return files
    
##### Get the tasks/work from the master/server ###

def get_work(repo):
    response = requests.get('localhost:8000/work', params={'key': 'value'})
    response.encoding = 'utf-8'
    json_file = response.json()
    tree = repo.get(json_file['commit']).tree
    id = json_file['id']
    sources = get_data(tree, repo)
    files = extract_files(sources)
    return files, id

##### Calculate complexity for all files ####

def do_work(work):
    results = []
    for file in work:
        results.append(compute_complexity(file))
    return results
##### Post results
def send_results(result):
    result = {'Result' : result}
    post = requests.post('localhost:8000/results', json=result)

if __name__ == '__main__':    
        repo = set_repo()
        work, id = get_work(repo)
        result = do_work(work)
        send_results(result)
