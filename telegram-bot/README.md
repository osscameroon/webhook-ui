# WebHook-TelegramBot

Trigger your webhook from a telegram bot.

## Requirements
- virtualenv
- python (3.x is required)

## How to install

```bash
# To set your python environment
make set-env
# To install requirements inside your env
make install
```

## How to launch

- Copy `example.config.txt` to `config.txt` and set the appropriate parameters
- (optional) You can format or lint the project code
```bash
# To python format the code
make format
# To check the linter of the python code
make lint
```
- Start the telegram bot
```bash
# To start the telegram bot
make start
```
