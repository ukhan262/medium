# github-actions-medium-post

Github action used to upload Markdown files to medium.com, any markdown file modified in `./articles` will be posted to medium.com

## Configuration

In order to authenticate with medium.com, you will need to create an integration token. This can be done by following the instructions [here](https://help.medium.com/hc/en-us/articles/213480868-Get-integration-token).

Once you have the integration token, you will need to add it as a secret to your repository. This can be done by navigating to the settings page of your repository and selecting the secrets tab. Once there, add a new secret with the name `MEDIUM_TOKEN` and the value of your integration token.

## Local development

To run the action locally, you will need to create a .env file with the following values:

```bash
MEDIUM_TOKEN=<your integration token>
```

Now install requirements from the requirements.txt file:

```bash
pip3 install -r src/requirements.txt
```


Once this is done, you can run the action with the following command:

```bash
python3 src/main.py
```
