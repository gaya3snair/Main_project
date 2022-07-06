import hashlib

def get_digest(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

if __name__ == '__main__':
    import pyAesCrypt

    password = "please-use-a-long-and-random-password"
    # encrypt
    pyAesCrypt.encryptFile("D:\\workspace\\PycharmProjects\\SNGIST_MCA_CloudStorage\\project\\myapp\\static\\myapp\\media\\404.png",
                           "D:\\workspace\\PycharmProjects\\SNGIST_MCA_CloudStorage\\project\\myapp\\static\\myapp\\media\\404.png.aes", password)
    # decrypt
    pyAesCrypt.decryptFile("D:\\workspace\\PycharmProjects\\SNGIST_MCA_CloudStorage\\project\\myapp\\static\\myapp\\media\\404.png.aes", "D:\\workspace\\PycharmProjects\\SNGIST_MCA_CloudStorage\\project\\myapp\\static\\myapp\\media\\404_d.png", password)
