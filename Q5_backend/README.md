### Q5 - backend development
---
#### Enviorment steps:
1. Install python3
2. Install the packages in requirements.txt using pip

---
### Execution:
Execute the following in any shell:
> python main.py

This command starts the flask server running at http://127.0.0.1:5000/
To validate a user, send a POST request to the following endoint:
> http://127.0.0.1:5000/validate

The endpoint accepts html FORM based body inputs with `application/x-www-form-urlencoded` content type headers. 

Use the form key `login_id` to pass the username(which has the first 2 characters denoting the country code) and `login_passwd` to pass the password.

The end point returns a JSON response with a single field called `Status` that contains the result of the authentication process. There are 3 possible states for this:

- `Wrong country code` is returned is the country code in the login id is not present in the defined set of country codes
- `User not found` is returned if the user name is not present in the database
- `Incorrect Password` is returned if the entered password does not match the one present in the database
- `Authenticated` is returned if the login id and password passes all checks

Currently two entries are hard coded so the following parameters will generate a success:

- login_id=sggalvin; login_passwd=123456
- loginid=inrde; login_passwd=rdedev

---

### Architecture
The database used here is a file based SQlite database. The `cryptography` package is used for encrypting and decrypting the passwords. On startup, the program checks if either the database file or encryption file is present. if either one is missing, a fresh encryption key as well as a database is created. The newly created database is then filled with dummy data. When filling, all passwords are encrypted using the Fernet symmetric encryption.

Upon receiving a request, the country code is extracted from the login id and then checked against a list of hard coded country codes. These codes are obtained from the `ISO 3166-1 alpha-2` country code list.

A database query then checks for the presence of the given user name. If a valid user is present, the users encrypted password is retrieved, decrypted using the encryption key and checked for equality. 
