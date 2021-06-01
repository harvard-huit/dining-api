## Running Locally

In order to run locally, you'll need to be logged in to admints-dev vpc with `aws-saml-cli` and logged in to a VPN. 

```
gunicorn --certfile=ssl/cert.pem --keyfile=ssl/key.pem --reload -b 0.0.0.0:9022 app:app
```

## Deployments

### Dev
```
./build-api.yml --extra-vars "target_app_name='dining-api' target_port='9022' aais_stack='dev'"

./deploy-api.yml --extra-vars "target_app_name='dining-api' target_app_context='/ats/dining' target_port='9022' aais_stack='dev'"
```
