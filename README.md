# Coffee Leaderboard

A coffee consumption leaderboard Slack integration. This was started as a fun
way for my Slack group to record our coffee consumption during the work day.

In Slack, when someone starts a message with the coffee emoji (`:coffee:`),
Slack sends the message on to the server which records the user. The records
are viewable via a leaderboard on the site's primary page.

**Warning!** _2.0 is a rewrite and has breaking changes, including the switch
to a different database (Postgres from MongoDB), ORM (switching to
Tortoise-ORM) and using a different framework (Starlette from Flask)._

## Installation

### Requirements

- Python 3.6+
- [Starlette ASGI framework](https://github.com/encode/starlette)
- [Tortoise-ORM](https://tortoise-orm.readthedocs.io/en/latest/index.html)
- Postgres or SQLite asyncio driver
  - asyncpg for Postrgres
  - aiosqlite for SQLite

### Slack Setup

_Coming Soon_

### Leaderboard Setup

_Coming Soon_

## Features Roadmap

The 2.0 rebuild is currently missing some of the features that existed with
the "+XP" version. These will be reintroduced as time allows.

-[x] Basic leaderboard tracking of coffee drinkage
-[ ] Installation documentation
-[ ] User profile pages
-[ ] User experience gain
-[ ] Leaderboard weekday averages chart
