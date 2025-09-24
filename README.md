# shopify-connector

## Docker Deployment

### Build the Docker Image

```bash
docker build -t shopify-connector .
```

### Run the Container

```bash
docker run --env-file .env shopify-connector
```

Or with environment variables:

```bash
docker run \
  -e SHOPIFY_SHOP_URL=your-shop.myshopify.com \
  -e SHOPIFY_API_KEY=your_shopify_access_token \
  shopify-connector
```

## Decisions
- A simple logger was added to each file to enable the output to be quickly associated with the file.
- Classes were created for each client to incorporate a Singleton Pattern and set up the APIs and connections.
- Conversion from Shopify JSON to Everstox JSON was not completed due to time constraints. The focus was on setting up the development environment, portability (Docker) and the maintainability of the code.
- 'uv' was used to simplify the management of modules and collaboration.