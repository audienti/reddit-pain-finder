# Apify Reddit Scraper Notes

Actor:

- `harshmaur/reddit-scraper`

Use this as the default Reddit search Actor for lower-risk conversation discovery.

## How to verify and run it

Prefer the Apify tool surface when the current run has it.

If the run does not have Apify tools but the local `apify` CLI is authenticated, use:

```bash
apify actors info harshmaur/reddit-scraper --input
apify call harshmaur/reddit-scraper --input-file input.json --silent --json
apify datasets get-items <datasetId>
```

The `apify call ... --json` response includes the run metadata you need to locate the default dataset.

## Important input fields

- `searchTerms`: array of search phrases
- `searchPosts`: include posts in keyword results
- `searchComments`: include comments in keyword results
- `searchCommunities`: include communities in keyword results
- `withinCommunity`: optional single subreddit filter like `r/sales`
- `searchSort`: `relevance`, `hot`, `top`, `new`, or `comments`
- `searchTime`: `all`, `hour`, `day`, `week`, `month`, or `year`
- `crawlCommentsPerPost`: scrape comments for each returned post
- `maxPostsCount`: hard cap for saved posts
- `maxCommentsCount`: hard cap for comment search results
- `maxCommentsPerPost`: hard cap for comment crawl per post

## Default first pass

Use a cheap discovery run first:

```json
{
  "searchTerms": [
    "cold emails getting no replies",
    "founder led sales not scaling",
    "too many sales tools not integrated"
  ],
  "searchPosts": true,
  "searchComments": false,
  "searchCommunities": false,
  "searchSort": "relevance",
  "searchTime": "month",
  "crawlCommentsPerPost": false,
  "includeNSFW": false,
  "maxPostsCount": 10,
  "proxy": {
    "useApifyProxy": true,
    "apifyProxyGroups": [
      "RESIDENTIAL"
    ]
  }
}
```

## Recommended second pass

After you find good language or strong subreddits:

- set `withinCommunity` to a winning subreddit
- reduce `searchTerms` to the best 2-5 phrases
- optionally enable `crawlCommentsPerPost=true`
- keep `maxCommentsPerPost` low at first

## Cost discipline

- Bound the first run with `callOptions.maxTotalChargeUsd`
- Keep `maxPostsCount` small on pass 1
- Avoid comment crawling until the initial search surfaces useful posts
