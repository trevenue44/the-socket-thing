import os

from receive import start_receiving
from send import start_sending

choice = input("Enter 'send' or 'receive': ").strip()

if choice.lower() == 'send':
    file_path = os.path.abspath('./test_file.txt')
    start_sending(file_path)
elif choice.lower() == 'receive':
    start_receiving()
else:
    print('Invalid Input')