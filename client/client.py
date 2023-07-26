import os
import time
import socket
import configparser

dirname = os.path.dirname(__file__)

# Инициализация файла конфигурации
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'client_config.ini'))
try:
    if(config['CONFIG']):
        pass
except:
    config['CONFIG'] = {
        'config' : 'config' ,
        'server_ip':'localhost',
        'server_port':'49999',
        'running':'False',
        'recon':'5'
    }

    with open(os.path.join(dirname, 'client_config.ini'), 'w') as configfile:
        config.write(configfile)

def toBool(value):
    '''Принимает текстовое значение'''
    if (value == 'True'):
        return True
    else:
        return False

# Настройки
server_IP = config['CONFIG']['server_ip']           # Адрес сервера
server_PORT = int(config['CONFIG']['server_port'])  # Порт сервера

recon = int(config['CONFIG']['recon'])              # Количество попыток переподключения к серверу
running = toBool(config['CONFIG']['running'])       # Переменная для запуска цикла
start_one = True                                    # Переменная для отправки первого сообщения
myname = socket.gethostname()                       # Имя клиента (имя компьютера)
need_recon = False                                  # Переменная запуска процедуры переподключения к серверу

# Подключение к серверу
i = 1
while i <= recon:
    print(f'{i} попытка подключения к {server_IP}:{server_PORT}')
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        server.connect((server_IP, server_PORT))

        running = True
        print('Соединение установленно!')
        break
    except:
        pass

    time.sleep(.5)
    i += 1

if (running == False):
    print('Подключение к серверу отсутствует')
    time.sleep(5)

while running:
    if start_one:
        start_message = 'name:' + myname + ';'
        server.send(start_message.encode())
        start_one = False

    try:
        # Получение данных с сервера
        data = server.recv(2**20).decode()
        data = data.split(';')
        for d in data:
            data = d.split(':')
            if data[0] == 'mes':
                if data[1] == 'way':
                    message = 'mes:imh;'
                    server.send(message.encode())
                    print(data[1])
    except:
        pass