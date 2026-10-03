# Sources and methodology

All numbers on the profile card come from the public GitHub API and are refreshed daily by `.github/workflows/profile.yml`.

- **Public repos, followers:** from `GET /users/{user}`.
- **Stars earned:** sum of stars on public, non-fork repositories I own.
- **Merged PRs (external):** pull requests I authored that were merged into repositories I do not own (GitHub search).
- **Follower rank:** the number of GitHub users with more followers than me, plus one, using GitHub user search. Regions use the free-text `location:` field, so users who write their location differently are not counted. Treat these as approximate.
- **Languages:** the primary language of each public repository I own.
- **Top repositories:** the projects listed in `FEATURED` inside `scripts/build_profile.py`.
