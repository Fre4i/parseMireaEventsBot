# mirea-events-bot

<p>The bot sends a list of events for the current day every day. </p>

<p>This bot also can:</p>

+ /show_all_events - show all events
+ /show_this_day_events - show all today's events
+ /show_this_month_events - show this month's events
+ /enable_notifications - enable/disable event reminders at 8:30 am (now notifications are enabled)
+ /help - instructions for the bot

[Link to the bot](https://t.me/mirea_events_bot)

## Project build

1. Clone the repository
   ```Bash
   git clone https://github.com/Fre4i/parseMireaEventsBot.git
   ```
2. Install libraries from requirements.txt file
   ```Bash
   pip install -r requirements.txt
   ```
3. Create files: `.env` and and create variable `TELEGRAM_TOKEN=YOUR_TOKEN`

## Hosting
I use [heroku](https://www.heroku.com/) as hosting.
