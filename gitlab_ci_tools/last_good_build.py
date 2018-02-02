# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
from types import SimpleNamespace
from urllib.parse import urlparse

from gitlab import Gitlab, GitlabAuthenticationError, GitlabGetError


def last_good_pipeline(client, project_name, branch):
    pipelines = client.projects.get(project_name).pipelines.list(as_list=False)
    # Pipelines are returned in reverse chronological order.
    return next(p for p in pipelines
                if p.status == 'success' and p.ref == branch)


def args_from_cli():
    parser = argparse.ArgumentParser(
        description='Print the Git hash of the last commit to a project '
                    'on a given branch for which a pipeline successful.',
    )
    parser.add_argument('project', help='fully qualified project name')
    parser.add_argument('branch', help='')
    parser.add_argument('--token', help='Gitlab private token for API access.')
    parser.add_argument('--gitlab', default='https://gitlab.com')
    return parser.parse_args()


def args_from_env():
    env = os.environ
    # spltting on '@' is necessary because CI specifies repository URL
    # as 'gitlab-ci-token:xxxx@<gitlab host>'
    *_, gitlab_host = urlparse(env['CI_REPOSITORY_URL']).netloc.split('@')
    gitlab_url = 'https://' + gitlab_host

    return SimpleNamespace(
        project=env['CI_PROJECT_PATH'],
        branch=env['CI_COMMIT_REF_NAME'],
        token=env.get('GITLAB_API_TOKEN'),
        gitlab=gitlab_url,
    )


def am_ci_job():
    return 'GITLAB_CI' in os.environ


def main():
    args = args_from_env() if am_ci_job() else args_from_cli()
    client = Gitlab(args.gitlab, args.token, api_version=4)
    try:
        if args.token:
            client.auth()
        print(last_good_pipeline(client, args.project, args.branch).sha)
    except GitlabAuthenticationError:
        print('Authentication error: did you provide a valid token?',
              file=sys.stderr)
        exit(1)
    except GitlabGetError as err:
        response = json.loads(err.response_body.decode())
        print('Problem contacting Gitlab: {}'
              .format(response['message']),
              file=sys.stderr)
        exit(1)
    except StopIteration:
        print('No successful pipelines for branch {}'.format(args.branch),
              file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
