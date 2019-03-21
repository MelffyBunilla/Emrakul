![Stats](https://img.shields.io/badge/discord-177%20servers%2012271%20unique%20users-blue.svg)(https://discordapp.com/oauth2/authorize?client_id=245372541915365377&scope=bot&permissions=0)
![Docker Pulls](https://img.shields.io/docker/pulls/neosloth/bolasbot.svg)(https://hub.docker.com/r/neosloth/bolasbot)

[https://theneosloth.github.io/Bolas/](https://theneosloth.github.io/Bolas)

# Bolas

Bolas is a mtg card-fetcher discord bot that is heavily inspired by [yawgmoth](https://github.com/Lerker3/yawgmoth). I am using this project as a way to try out some new approaches to api wrappers and plugin systems, so the way some parts of the bot are implemented are a bit esoteric.

## Structure

The core of the bot is located in bot.py, all simple commands such as !pingme should go in commands.py. More advanced functionality such as the card fetcher should be developed in card_hooks.py. Those files contain the base class that the plugins should be derived from.

The plugins are loaded through a metaclass called PluginMount. Every class derived from PluginMount will be automatically loaded and added to either the self.chat_hook or self.commands variables.

The docstring for each one of the plugins are all concatenated together and can be displayed with the hardcoded “!help” command.

## How to run

Export BOLAS_SECRET_TOKEN. Execute run.py.

```sh
export $BOLAS_SECRET_TOKEN=THIS-IS-A-SECRET
python ./run.py

```

## Using docker

The arm64v8 and amd64 images are available at neosloth/bolasbot. For other architectures the image can be built using the included Dockerfile

### Building the image

``` sh
docker build --tag=bolasbot .
```

### Running Bolas

``` sh
docker run -e BOLAS_SECRET_TOKEN=THIS_IS_A_SECRET --name bolas --restart unless-stopped bolasbot

```

## Add Bolas to your Discord server

[Click here](https://discordapp.com/oauth2/authorize?client_id=245372541915365377&scope=bot&permissions=0)
