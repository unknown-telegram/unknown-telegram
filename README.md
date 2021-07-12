<p align="center">
  <a href="https://github.com/unknown-telegram/unknown-telegram">
    <img src="logo.png" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">unknown-telegram</h3>

  <p align="center">
    A very simple Telegram userbot
    <br />
    <a href="https://github.com/unknown-telegram/modules">Modules</a>
    ·
    <a href="https://github.com/unknown-telegram/unknown-telegram/issues">Report Bug</a>
    ·
    <a href="https://github.com/unknown-telegram/unknown-telegram/issues">Request Feature</a>
    <br />
    <br />
    <a href="https://github.com/unknown-telegram/unknown-telegram/blob/main/LICENSE"><img src="https://img.shields.io/github/license/unknown-telegram/unknown-telegram" alt="GitHub license"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></img></a>
    <a href="https://www.codefactor.io/repository/github/unknown-telegram/unknown-telegram/overview/main"><img src="https://www.codefactor.io/repository/github/unknown-telegram/unknown-telegram/badge/main" alt="CodeFactor" /></a>
    <a href="https://wakatime.com/badge/github/unknown-telegram/unknown-telegram"><img src="https://wakatime.com/badge/github/unknown-telegram/unknown-telegram.svg" alt="Wakatime"></img></a>
  </p>
</p>

## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

_Example for Ubuntu. Advanced users can install this themselves._
* git
  ```sh
  $ apt install -y git
  ```

* python3
  ```sh
  $ apt install -y python3
  ```

* python3-pip
  ```sh
  $ apt install -y python3-pip
  ```

### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/unknown-telegram/unknown-telegram.git
   ```
2. Install pip packages
   ```sh
   $ python3 -m pip install -r requirements.txt
   ```

## Usage

1. Add a Telegram account
    ```sh
    $ python3 -m unknown-telegram -add
    ```
    The bot will ask for a phone number and code. This is necessary for the authorization procedure in Telegram.<br/>
    **Your data will sent only to the Telegram server.**
2. Run the bot
    ```sh
    $ python3 -m unknown-telegram
    ```
    Also, you can use a convenient way to launch a bot, for example: _screen, service, pm2_.

_Maybe, i'll write a wiki someday._

## Roadmap

See the [open issues](https://github.com/unknown-telegram/unknown-telegram/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU GPL v3.0 License. See `LICENSE` for more information.

<br />
<a href="https://github.com/othneildrew/Best-README-Template">I want the same README!</a>
