# Watchtower:Flow on Docker
Docker image for Watchtower:Flow, built with Ubuntu 20.04.

The current version is intended for testing local image builds for demonstration and testing purposes.

Subsequent versions may be intended to be run from Docker Hub.

## Build a Local Image

Clone this repo and cd into repo directory.

```shell
git clone git@github.com:mjhillyer/Watchtower-Deploy.git
cd Watchtower-Deplow
```

Remove old image (if any), and build a new one.

Currently the Dockerfile retrieves GovReady's `main` (e.g., `master`) branch.  Subsequent versions will pull a specific release tag instead of `main`.

```shell
docker rmi watchtower-flow ; docker build --tag watchtower-flow .
```

## Run Watchtower:Flow

Run an ephemeral container with port forwarding, in interactive mode

Include the "demo" argument to start Watchtower:Flow in demo mode.

```shell
docker run --rm -p 8000:8000 watchtower-flow demo
```

You should see the following output (with the actual password, instead of RANDOM_PASSWORD_HERE:

```
This is Watchtower:Flow.
v0.9.1.49.1

running some checks...
... done running some checks.

initializing database...
... done initializing database.

setting up system and creating demo user...
... done setting up system and creating demo user.

Created administrator account (username: admin) with password: RANDOM_PASSWORD_HERE

starting Watchtower:Flow server...
Watchtower:Flow is running.
Visit http://localhost:8000/ with your browser.
Log in with the administrator credentials above.
Hit control-C to exit.
```

Hit control-C when you want to exit.

## Alternative Run Command

The Docker container will output some simple instructions if the user does not include the "demo" argument. The intention is that when started with a generic run command, that may not include port forwarding, the user will be instructed to try again, with the proper port forwarding.

To try this feature:

```shell
docker run watchtower-flow
```

Note that this command will create a container with a randomly-generated name; after you stop it, remember to remove the container.

Also note, the following portion of the message, which presages more versions of the demo experience, is currently aspirational, not actual.

> To see options for a richer demo experience, including sample data, persistent data, and production-oriented demos, visit [...]

## Motivations and Next Steps

*tbd*

