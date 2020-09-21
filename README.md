# Tennis courts availability checker

Booking tennis courts ran by ClubSpark can prove to be a very daunting experience. The tennis courts closest to my place provide free booking slots before 7-9am and paid ones 9am-8pm. The free slots are usually booked within seconds (sometimes milliseconds), since they are released. I found that quite often people will cancel their free slots late in the day, and if you are not constantly checking the platform for slots during that time of the day the slots will be booked by somebody who does. Checking for cancellations is a very daunting operation, so I built a bot, that will send me notifications on Telegram, notifying me in close to real-time when a free court becomes available.

This bot was built in python using Selenium framework, that enables it to login into your account and check if there will appear free booking courts as soon as people cancel. I am running it on AWS EC2 instance (inside `tmux`), which is better than running it on a local machine, as it doesn't consume my machine's local resources and I don't have to keep it always turned on.

## How to run

1. Clone the repo: `git clone https://github.com/iurietarlev/free_tennis_court_bot.git`
2. Install required libraries: `pip install -r requirements.txt`
3. Insert clubspark and telegram bot identification into the `config.yml` file.
4. Run the script: `python3 main.py --cfg ./config.yml`
