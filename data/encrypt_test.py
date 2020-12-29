import pyAesCrypt
buffersize = 512 * 1024
password = 'oo3aiiis'

pyAesCrypt.encryptFile('data/database.db', 'data/database.db' + '.mk', password, buffersize)