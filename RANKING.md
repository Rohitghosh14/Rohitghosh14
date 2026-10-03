# Sources and methodology

Everything on the profile card is public GitHub data, refreshed daily by `.github/workflows/profile.yml`.

- **World follower rank:** number of GitHub users with more followers than me, plus one (GitHub user search). Regional ranks add a `location:` filter. Location is free text, so users who write it differently are not counted. Treat regions as approximate.
- **Owned stars:** stars on my public, non-fork repositories.
- **Commits / PRs / Issues / Reviews (365 days):** GitHub GraphQL `contributionsCollection`.
- **Builder Index (custom score, 0-100):** the average of five axes, each capped at 100:
  - Creation = public repos / 40
  - Shipping = commits (365d) / 1000
  - Collaboration = (PRs + reviews, 365d) / 100
  - Maintenance = repos pushed in the last 90 days / 10
  - Community = (followers + stars) / 200
- **Top repositories:** the list `FEATURED` in `scripts/build_profile.py`.

The Builder Index is my own simple formula for tracking progress. It is not an official GitHub metric.
