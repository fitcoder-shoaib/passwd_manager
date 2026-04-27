import secrets,string

def pass_gen(leng):
    letters = string.ascii_letters
    digits = string.digits
    symbols = "-_.," 
    
    alphabet = letters + digits + symbols
    
    while True:
        pasw = ''.join(secrets.choice(alphabet) for _ in range(leng))
        
        if (any(c.islower() for c in pasw)  
                and any(c.isupper() for c in pasw)
                and any(c.isdigit() for c in pasw)):
            return pasw
