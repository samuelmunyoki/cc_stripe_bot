import random
import string

def generate_random_email(length=10, domain='gmail.com'):
    username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    email = f'{username}@{domain}'
    return email