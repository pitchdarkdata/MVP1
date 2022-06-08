"""
Module to perform reviewer addition action for a Pull Request
"""
import os
import sys
import json
import logging
import subprocess
from pydriller import Git

logging.basicConfig(filename="reviewer.log",
                    filemode="a",
                    format="%(levelname)s %(asctime)s - %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger()


class Reviewer:
    def __init__(self, gitdata, repo_clone_path=os.getcwd()):
        """

        :param gitdata: Input data dictionary from pull requests which includes repo url, repo name, commits
        :param repo_clone_path: The path in which the repo has to cloned in local,
                                default would be the current working directory
        """

        # To do: Check with the input format, remove if not required
        try:
            self.gitdata = json.loads(gitdata)
        except json.JSONDecodeError:
            logger.error("Json conversion not required !!")
        self.repo_path = repo_clone_path
        logger.info(f"Input Data from Pull Request : {self.gitdata}")

    def repo_setup(self):
        """
        :return: repo clone status.
        """
        status = True
        try:
            # Remove if the directory already exists.
            os.system(f"rm -rf {self.repo_path}/{self.gitdata['repo_name']}")
            response = subprocess.Popen(f"cd {self.repo_path}; git clone {self.gitdata['repo_url']}", shell=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = response.communicate()
            logger.info(f"Command Output : {out}\nError: {err}")
            assert response.returncode == 0, \
                f"Error cloning the repository {self.gitdata['repo_name']} in path {self.repo_path}"
            assert os.path.isdir(f"{self.repo_path}/{self.gitdata['repo_name']}"), \
                f"The repository {self.gitdata['repo_name']} doesn't exist in path {self.repo_path}."
            logger.info("Repository cloned successfully in local.")
        except AssertionError as error:
            status = False
            logger.error(error)
        return status

    def get_modified_files(self, commit_id):
        """

        :param commit_id: Commit SHA
        :return: list of modified files
        """
        git_repo = Git(f"{self.repo_path}/{self.gitdata['repo_name']}")
        commit = git_repo.get_commit(commit_id)
        modified_files = [file.filename for file in commit.modified_files]
        logger.info(f"Files modified by commit {commit} :  {modified_files}")
        return modified_files

    def get_reviewers(self):
        """
        :return: list of reviewers.
        """
        reviewers = set()
        try:
            assert self.repo_setup(), f"Unable to proceed as the repository cloning resulted in error !!."
            git_repo = Git(f"{self.repo_path}/{self.gitdata['repo_name']}")
            self.gitdata['commit'] = [self.gitdata['commit']] if isinstance(self.gitdata['commit'], str) \
                else self.gitdata['commit']
            for commit in self.gitdata['commit']:
                commit_hook = git_repo.get_commit(commit)
                last_commit_dict = git_repo.get_commits_last_modified_lines(commit_hook)
                assert len(last_commit_dict) != 0, f"Previous commits aren't retrieved for {commit}"
                logger.info(f"Last Commit Dictionary : {last_commit_dict}")
                for filename, commits in last_commit_dict.items():
                    for commit_id in list(commits):
                        c_hook = git_repo.get_commit(commit_id)
                        logger.info(f"Modified file : {filename}\nCommit id: {commit_id}\nMessage : {c_hook.msg}")
                        reviewers.add(c_hook.author.name)
        except KeyError as key_error:
            logger.error(f"The Expected key doesnt exist !!. Error Occurred : {str(key_error)} ")
        except AssertionError as error:
            logger.error(error)
        return list(reviewers)


if __name__ == "__main__":
    # Execute the get method with the input args.
    try:
        r_obj = Reviewer(sys.argv[1])
        print(r_obj.get_reviewers())
    except IndexError:
        logger.error("Please pass the gitdata as an input argument to the script.")
