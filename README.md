# Ripio Client for Python
###  ALPHA SOFTWARE


This is a lightweight library that works as a client to [Ripio](https://www.ripio.com) Services

## Usage example
```python
from ripio.trade.client import Client

# API key is required for user data endpoints
client = Client(api_key='<api_key>', api_secret='<api_secret>')

# Get balance information
print(client.get_user_balances())

```
