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

##Run

```shell script
cd sonarhook
source venv/bin/activate
python -m sonarhook --config ./app.config.ini
```

##Contributing/Forking

Go for your life.

##To DO

- Dockerise