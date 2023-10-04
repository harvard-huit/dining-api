## Secrets

The only secret-secret this currently uses is the foodpro database password. However, the following environment variables will be needed. 

 - `DB_DRIVER`
 - `DB_HOST`
 - `DB_INSTANCE`
 - `DB_USER`
 - `DB_PWD`
 - `ECS_APIKEY`

## Database

There is only a prod instance of this database and the database used here is sqlserver, so gl with that. 

## Running Locally

In order to run locally, you'll need to be logged in to admints-dev vpc with `aws-saml-cli` and logged in to a VPN. 

```
gunicorn --certfile=ssl/cert.pem --keyfile=ssl/key.pem --reload -b 0.0.0.0:9022 app:app
```

## Deployments

### Actions

Usage of the actions is preferred for building and deploying the runtime as well as promoting the proxy code. 