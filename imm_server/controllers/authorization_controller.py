from typing import List

import connexion
from connexion.exceptions import OAuthProblem

TOKEN_DB = {
    'prenosis123': {
        'uid': 100
    }
}

def check_api_key(api_key, required_scopes):
	info = TOKEN_DB.get(api_key, None)
	if not info:
		raise OAuthProblem("Invalid token")
	return info  
    

