import os
import sys
import time
import socket
import configparser

dirname = os.path.dirname(__file__) # Путь папки проекта
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'server_conf.ini'))

class Client_machine:
    
    def __init__(self, cl_socket, cl_adress):
        self.conn = cl_socket   # Сокет клиента
        self.addr = cl_adress   # Адрес клиента
        self.name = 'Unknow'    # Имя клиента. До объявления по умолчанию Unknow


try:
    if(config['CONFIG']):
        pass
except:
    config['CONFIG'] = {
    'local': 'False',
    'port': '49999',
    'work': 'True'
    }

    with open(os.path.join(dirname, 'server_conf.ini'), 'w') as configfile:
        config.write(configfile)

def toBool(value):
    '''Принимает текстовое значение'''
    if (value == 'True'):
        return True
    else:
        return False

def myIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Настройки
server_PORT = int(config['CONFIG']['port'])     # Порт сервера
server_work = toBool(config['CONFIG']['work'])  # Переменная работы сервера
if (toBool(config['CONFIG']['local'])):
    server_IP = 'localhost'
else:
    server_IP = myIP()  

# Запуск сервера
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # AF_INET работа с IPv4, SOCK_STREAM работа с TCP
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)   # Указывает на то, что не надо отправлять собранные пакеты, а слать информацию сразу
main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)   # Если от клиента нет связи больше 1 секунды, то удаляем его из стека
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)  # Время простоя клиента после которого он будет удалён из стека
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1) # Время между проверками статуса клиента
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 2)   # Количество попыток проверки статуса клиента
main_socket.bind((server_IP, server_PORT)) # Завязка сокета с IP и портом
main_socket.setblocking(0) # Не останавливать выполнение программы пока получаем данные
main_socket.listen(5) # Включение прослушки порта. 5 говорит о количестве одновременно подключаемых клиентов. 5 не максимальное количество клиентов!

print(f'Сервер запущен по адресу {server_IP} на {server_PORT} порту\nCtrl + C для завершения работы сервера')

while server_work:
    try:
        time.sleep(1) # Задержка чтобы не положить порт

    except:
        server_work = False
        print('Остановка работы сервера')

main_socket.close()