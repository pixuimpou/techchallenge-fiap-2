api_fetch_params = f"""
{{
    'headers': {{
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'domain-id': 'br'
    }},
    'referrer': 'https://br.investing.com/',
    'referrerPolicy': 'strict-origin-when-cross-origin',
    'body': null,
    'method': 'GET',
    'mode': 'cors',
    'credentials': 'omit'
}}
"""

print(api_fetch_params)
