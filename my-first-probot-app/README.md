# my-first-probot-app

> A GitHub App built with [Probot](https://github.com/probot/probot) that a simple testing app

## Setup

```sh
# Install dependencies

#Node Modules
npm install
#octokit dependencies
npm install @octokit/rest

# Run the bot
npm start
```

## Docker

```sh
# 1. Build container
docker build -t my-first-probot-app .

# 2. Start container
docker run -e APP_ID=<app-id> -e PRIVATE_KEY=<pem-value> my-first-probot-app
```

## Contributing

If you have suggestions for how my-first-probot-app could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For more, check out the [Contributing Guide](CONTRIBUTING.md).

## License

[ISC](LICENSE) © 2022 SasikumarKalaichelvan <sasikumar6795@gmail.com>
