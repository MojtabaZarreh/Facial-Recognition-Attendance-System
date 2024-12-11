import bcrypt

def hash(password):
    return bcrypt.hashpw(
        password=password.encode('utf-8'),
        salt=bcrypt.gensalt()
    )

def check(password, hash_password):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hash_password
    )
    

# p1 = hash('zarmoj123!') 
# print(p1)
# p2 = 'zarmoj123!'

# if check(p2, p1):
#     print("Welcome to GeekPython.")
# else:
#     print("Invalid Credential.")