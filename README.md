# Azure Devops Status Sonar Analysis Hook

This tool will receive webhooks from successful sonar could analysis and pass them on as statuses to Azure Devops Repo PRs.

## Requirements

- Python 3+
- SonarCloud webhook with secret - https://sonarcloud.io/documentation/project-administration/webhooks/
- ADO personal access token
- mapping between sonar cloud project keys and ADO repo urls

## Install

```shell script
git clone git@github.com:izanbard/sonarhook.git
cd sonarhook
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements
deactivate
```

## Configure

Edit file `app.config.ini` and replace place holders with data

```json
{
  "application":{
    "bind_address": "0.0.0.0",
    "port": 9000,
    "health_check_secret": "[my_super_secret]"
  },
  "repos": {
    "[sonar_project_key_1]": {
      "org_url": "[ADO url for org of that project key]",
      "project_name": "[Project name for the project within the organisation]",
      "repo_name": "[name of the repo (same as the slug)]"
    },
    "[sonar_project_key_2]": {
      "org_url": "[ADO url for org of that project key]",
      "project_name": "[Project name for the project within the organisation]",
      "repo_name": "[name of the repo (same as the slug)]"
    }
  }
}
```

| Key                   | Description                                                                                             | Example                       | Notes                                                                                                                    |
|-----------------------|---------------------------------------------------------------------------------------------------------|-------------------------------|--------------------------------------------------------------------------------------------------------------------------|
|--`application`--|--|--|--|
| `bind_address`        | The network interface to listen on                                                                      | `0.0.0.0`                     | Default is all interfaces                                                                                                |
| `port`                | The network port to listen on                                                                           | `9000`                        |                                                                                                                          |
| `health_check_secret` | A secret key that you can pass to the health check to ensure the service i up and running               | `secret`                      | See Health Check section below                                                                                           |
|--`repos`--|--|--|--|
| `[sonar_project_key]` | The sonar project key that will come in the the sonar webhook.                                          | `front_end_key`               | Multiple entries can be defined, each webhook is evaluated and only web hooks with a matching project key are processed. |
| `org_url`             | The ADO organisation url.                                                                               | `https://dev.azure.com/MyOrg` |                                                                                                                          |
| `project_name`        | The ADO project name in the above organisation that the repo matching this `sonar_project_key` sits in. | `MyProject`                   |                                                                                                                          |
| `repo_name`           | The name of the repo that matches the `sonar_project_key`.                                              | `front_end_code`              | Matches the repo at url: `git@ssh.dev.azure.com:v3/MyOrg/MyProject/front_end_code`                                       |

## Run

```shell script
cd sonarhook
source venv/bin/activate
export ADO_PAT=[ADO Personal Access Token]
export SONAR_WEBHOOK_SECRET=[Sonar Web Hook Secret]
python -m sonarhook --config app.config.json
```

### Serving

It is recommended that you secure this service behind and Apache or Nginx web server acting as TLS endpoint.

## Contributing/Forking

Go for your life.

## To DO

- Logging
- Unit Tests
- Pipeline