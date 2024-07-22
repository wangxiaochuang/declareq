# drequests

declare network request

- Works with requests
- Inspired by [uplink](https://github.com/prkumar/uplink)
- more simple and flixible

just like uplink did, use Github API v3 for example:

```python
from declareq.arguments import Path, Query, UrlPrefix
from declareq.builder import Consumer
from declareq.commands import get


class Github(Consumer):
    '''github v3 api'''

    def __init__(self, _: UrlPrefix):
        pass

    @get("/users/{user}/repos")
    def get_repos(self, user: Path, sort_by: Query("sort") = "created"):
        '''get github repos of user'''


github = Github("https://api.github.com")
github.get_repos("prkumar", sort_by="created")
```