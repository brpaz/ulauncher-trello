# Ulauncher-Trello

> Open your Trello boards from Ulauncher
## Demo

![demo](demo.gif)

## Requirements

* [ulauncher](https://ulauncher.io/)
* Python >= 2.7
* Trello package ```pip install trello```

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```https://github.com/brpaz/ulauncher-trello```

## Usage

Before being able to use the Extension you must have a Trello API Key and token and set them in the plugin settings.

You can get both [here](https://trello.com/app-key). First generate your API key, and then below, you have the link to authorize your application and generate your API Token.

**Note: This app dont use Oauth. Please follow the instruction on Trello website to generate a token where it says: "If you are looking to build an application for yourself, or are doing local testing, you can manually generate a Token"**

## Development

1. Clone the repo.
2. From the root folder of the project, run ```make link```. This will create a symlink to the "ulauncher extensions" directory.

To see your changes, stop ulauncher and run it from the command line with: ```ulauncher -v```.

## Contributing

All contributions all welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for start.

## License

MIT
