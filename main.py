from typing import Optional
import os
import requests
from dotenv import load_dotenv
from custom_logger import logger

load_dotenv()

GITEA_URL = "GITEA_URL"
SECURITY_TOKEN = "SECURITY_TOKEN"


class GiteaServiceError(ConnectionError):
    def __init__(self, message: str, additional_info: Optional[str] = None, inner_exception: Optional[Exception] = None):
        super().__init__(0, message)
        self.message = message
        self.additional_info = additional_info
        self._inner_exception = inner_exception

    def __str__(self):
        return self.message


class GiteaProcessor:
    def __init__(self, gitea_url: str, security_token: str):
        self._url = gitea_url.rstrip("/")
        self._security_token = security_token
        self._create_repo_url = f"{self._url}/api/v1/user/repos"
        logger.info("Gitea processor created", url=gitea_url)

    def create_repo(
            self,
            name: str,
            auto_init: bool = False,
            default_branch: str = "master",
            description: str = "",
            gitignores: str = "",
            issue_labels: str = "",
            license: str = "",
            private: bool = True,
            readme: str = "",
            template: bool = False,
            trust_model: str = "default"
    ):
        params = {
            "access_token": self._security_token
        }

        payload = {
            "name": name,
            "auto_init": auto_init,
            "default_branch": default_branch,
            "description": description,
            "gitignores": gitignores,
            "issue_labels": issue_labels,
            "license": license,
            "private": private,
            "readme": readme,
            "template": template,
            "trust_model": trust_model
        }
        logger.debug("Creating a repo", **payload)

        try:
            result = requests.post(url=self._create_repo_url, params=params, json=payload)
        except Exception as exc:
            logger.error("The repository is not created", **payload, exception=exc)
            raise GiteaServiceError("Cannot create a repository", inner_exception=exc)

        if not result.ok:
            raise GiteaServiceError("Cannot create a repository", result.text)
        logger.debug("Repo created", name=name)


if __name__ == "__main__":
    gitea_url = os.environ.get(GITEA_URL)
    if not gitea_url:
        logger.error("The gitea url is not set")
        exit(1)
    gitea_token = os.environ.get(SECURITY_TOKEN)
    if not gitea_token:
        logger.error("The gitea token is not set")
        exit(1)

    gitea = GiteaProcessor(gitea_url=gitea_url, security_token=gitea_token)
    gitea.create_repo("test1")
