#Azure Devops Status Sonar Analysis Hook

This tool will receive webhooks from successful sonar could analysis and pass them on as statuses to Azure Devops Repo PRs.

##Requirements

- Python 3+
- SonarCloud webhook secret
- ADO personal access token
- mapping between sonar cloud project keys and ADO repo urls

##Install

```shell script
git clone git@github.com:izanbard/sonarhook.git
cd sonarhook
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements
deactivate
```

##Configure

Edit file `app.config.ini` and replace place holders with data

```json
{
  "repos": {
    "[sonar_project_key]": {
      "org_url": "[ADO url for org of that project key]",
      "project_id_or_name": "[Project name for the project within the organisation]",
      "repo_name": "[name od the repo (same as the slug)]"
    } 
  }
}
```

##Run

```shell script
cd sonarhook
source venv/bin/activate
export ADO_PAT=[ADO Personal Access Token]
export SONAR_WEBHOOK_SECRET=[Sonar Web Hook Secret]
python -m sonarhook --config app.config.json
```

##Contributing/Forking

Go for your life.

##To DO

- Dockerise