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

client_list = [] # Список клиентов по умолчанию пустой

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
        try:
                client_socket, client_addr = main_socket.accept() # Получаем новое подключение. Сокет и адрес клиента.
                client_socket.setblocking(0)
                
                new_client = Client_machine(client_socket, client_addr) # Создаём нового клиента
                client_list.append(new_client) # Записываем клиента в список

        except Exception as e:
            pass

        # Чтение сообщений от клиентов
        for cl in client_list:
            try:
                # Парсинг сообщений на блоки
                # Из mes:1;mes:2;mes:3; получаем [['mes', '1'], ['mes', '2'], ['mes', '3']]
                data = cl.conn.recv(2**20).decode() # Получение сообщений
                data = data.split(';')
                for d in data:
                    data = d.split(':')

                    # Первым сообщением передаётся имя клиента
                    if data[0] == 'name':
                        cl.name = data[1]
            except:
                pass

        for cl in client_list:
                try:

                    # way - Where are you (Где ты?) должен вернуть imh
                    cl.conn.send('mes:way;'.encode())
                    
                    # Если есть команда, то отправить её
                    if command:
                        cl.conn.send(command_text.encode())
                        command_text = ''  
                        command = False                      
                    
                # Если не удалось отправить, то значит клиент оффлайн
                except:
                    client_list.remove(cl)
                    cl.conn.close()
                
                    print(f'{cl.name} > отключился')

    except:
        server_work = False
        print('Остановка работы сервера')

main_socket.close()