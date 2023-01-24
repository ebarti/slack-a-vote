# Slack-A-Vote

This is a poll/survey app that is built using the [next-gen developer platform](https://api.slack.com/future/intro) of Slack.


## Setup

Before getting started, make sure you have a development workspace where you
have permissions to install apps. If you don’t have one set up, go ahead and
[create one](https://slack.com/create). Also, please note that the workspace
requires any of [the Slack paid plans](https://slack.com/pricing).

### Install the Slack CLI

To use this sample, you first need to install and configure the Slack CLI.
Step-by-step instructions can be found in our
[Quickstart Guide](https://api.slack.com/future/quickstart).

### Clone the Sample App

Start by cloning this repository:

```zsh
# Clone this project onto your machine
$ slack create my-app -t slack-samples/bolt-python-starter-template -b future

# Change into this project directory
$ cd my-app

# Setup your python virtual environment
$ python3 -m venv .venv
$ source .venv/bin/activate

# Install the project dependencies
$ pip install -r requirements.txt
```

#### Linting

```zsh
# Run flake8 from root directory for linting
flake8 *.py && flake8 functions/

# Run black from root directory for code formatting
black .
```


## Running Your Project Locally

While building your app, you can see your changes propagated to your workspace
in real-time with `slack run`. In both the CLI and in Slack, you'll know an app
is the development version if the name has the string `(dev)` appended.

```zsh
# Run app locally
$ slack run

⚡️ Bolt app is running! ⚡️
```

Once running, click the
[previously created Shortcut URL](#create-a-link-trigger) associated with the
`(dev)` version of your app. This should start a workflow that opens a form used
to send a message to a certain channel!

To stop running locally, press `<CTRL> + C` to end the process.

## Deploying
Currently deploying to slack is not yet supported.

## Project Structure

### `manifest.json`

`manifest.json` is a configuration for Slack CLI apps in JSON. This file will
establish all basic configurations for your application, including app name
and description.

### `/triggers`

All trigger configuration files live in here - currently empty.

### `slack.json`

Used by the CLI to interact with the project's SDK dependencies. It contains
script hooks that are executed by the CLI and implemented by the SDK.


Env vars


BASE_WORKSPACE_URL

Notes - Company wide initiatives day