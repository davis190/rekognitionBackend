
# Prerequisites
- Need to have run the setup or replace all the values in this module manually

# Steps
1. Install `serverless-python-requirements` and python `requests` modules if not installed
```
sls plugin install -n serverless-python-requirements
pip install requests -t .
```

2. Deploy the backend
```
sls deploy
```