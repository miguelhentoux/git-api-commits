"""Repo's endpoints
"""
import pandas as pd
import requests
from api.core.config import api_settings
from api.schemas.schemas import RepoResponse
from fastapi import APIRouter, HTTPException

api_router = APIRouter()


def _git_request(endpoint: str) -> dict:
    """Fetch data from github

    Args:
        endpoint (str): url to fetch data

    Raises:
        HTTPException: Timeout
        HTTPException: Not found

    Returns:
        dict: Response Json
    """
    try:
        response = requests.get(endpoint, timeout=30)
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408, detail="Connection with GitHub failed")

    if response.status_code != 200:
        raise HTTPException(
            status_code=404, detail="Not Found")

    return response.json()


@api_router.get("/commits", response_model=RepoResponse)
def repo_commits(owner: str, repo: str) -> dict:
    """Fetch commits per author and date from github repo
    """
    endpoint = api_settings.URL_GIT + f'repos/{owner}/{repo}/commits'
    r_json = _git_request(endpoint)

    list_commit = []
    for commit in r_json:
        list_commit.append({'sha': commit['sha'],
                            'author': commit['commit']['author']['name'],
                            'date': commit['commit']['author']['date'], })

    df = pd.DataFrame(list_commit)
    if df.empty:
        # No commits, return default reponse
        resp_data = {
            'authors': '',
            'dates': [],
            'rows': [],
            'n_rows': 0
        }
        return resp_data

    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].apply(lambda x: x.date())
    df_pivot = pd.pivot_table(
        df, index='author', columns='date', aggfunc='count', fill_value=0)['sha']

    rows = []
    for i, author in enumerate(df_pivot.index):
        dict_temp = {}
        dict_temp['key'] = i
        dict_temp['author'] = author
        df_author = df_pivot.loc[author]
        for date_commit in df_pivot.loc[author].index:
            dict_date = {}
            dict_date['amount'] = int(
                df_author.loc[date_commit])  # type: ignore
            if int(df_author.loc[date_commit]) == 0:  # type: ignore
                dict_date['commits'] = []
            else:
                commits = list(
                    set(df[(df['date'] == date_commit) & (df['author'] == author)]['sha']))
                dict_date['commits'] = commits
            dict_temp[str(date_commit)] = dict_date
        rows.append(dict_temp)

    resp_data = {
        'authors': list(df_pivot.index),
        'dates': [str(x) for x in df_pivot.columns],
        'rows': rows,
        'n_rows': len(rows)
    }
    return resp_data
