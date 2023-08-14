def Check_connect():
    if __name__ == '__main__':  # Точка входа при запуске этого скрипта

        # Проверяем соединение
        # print(f'Терминал QUIK подключен к серверу: {qp_provider.IsConnected()["data"] == 1}')
        dpg.add_text(f'Terminal QUIK connect to server:{qp_provider.IsConnected()["data"] == 1} ',
                     parent='logger')
        # Проверка работы скрипта QuikSharp. Должен вернуть Pong
        # print(f'Отклик QUIK на команду Ping: {qp_provider.Ping()["data"]}')
        dpg.add_text(f'Request QUIK from command Ping: {qp_provider.Ping()["data"]}', parent='logger')

        # Проверяем работу запрос/ответ
        trade_date = qp_provider.GetInfoParam('TRADEDATE')['data']  # Дата на сервере в виде строки dd.mm.yyyy
        server_time = qp_provider.GetInfoParam('SERVERTIME')['data']  # Время на сервере в виде строки hh:mi:ss
        # Переводим строки в дату и время
        dt = datetime.strptime(f'{trade_date} {server_time}', '%d.%m.%Y %H:%M:%S')
        # print(f'Дата и время на сервере: {dt}')
        dpg.add_text(f'Date and time on server: {dt}', parent='logger')
        # Проверка работы QUIK. Сообщение в QUIK должно показаться как информационное
        msg = 'Hello from Python!'
        # print(
        #    f'Отправка сообщения в QUIK: {msg}{qp_provider.MessageInfo(msg)["data"]}')
        dpg.add_text(f'Send test to в QUIK: {msg}{qp_provider.MessageInfo(msg)["data"]}', parent='logger')

        # Проверяем работу подписок
        qp_provider.OnConnected = lambda data: print(data)  # Нажимаем кнопку "Установить соединение" в QUIK
        qp_provider.OnDisconnected = lambda data: print(data)  # Нажимаем кнопку "Разорвать соединение" в QUIK


def print_callback(data):
    """Пользовательский обработчик событий:
    - Изменение стакана котировок
    - Получение обезличенной сделки
    - Получение новой свечки
    """

    lst = data
    #print(lst)
    # lst = datetime.now().strftime("%d.%m.%Y %H:%M:%S") - data["data"]
    # dpg.add_text(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data["data"]}', parent='data_w')
    # dpg.add_text(
    #     f'Номер сделки {lst["data"]["tradenum"]} Время {lst["data"]["datetime"]["hour"], lst["data"]["datetime"]["min"]}',
    #     parent='data_w')
    # print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data["data"]}')  # Печатаем полученные данные
    # hour = str(lst['data']['datetime']['hour'])
    # min = str(lst['data']['datetime']['hour'])
    # sec = str(lst['data']['datetime']['sec'])
    # datetime = f'{hour} : {min} : {sec}'

    # datetime = datetime.strftime("%H:%M:%S")

    # Проверям напряление по номеру флага
    if lst['data']['flags'] == 1025:
        flag = 'продажа'
    elif lst['data']['flags'] == 1026:
        flag = 'купля'
    else:
        flag = '------'
    # фильтруем поток по выбранным инстментам
    # filter_sec = ['SBER','VTBR', 'LKOH']
    filter_sec = ['SBER']

    for i in filter_sec:
        if lst['data']['seccode'] == i:
            # группируем по времени выбранный инстумент
            # count = count + int(lst['data']['qty'])
            sec = int(lst['data']['datetime']['sec'])
            #print(f'текущая секунда {sec}')
            # print('-----------------')
            count_sec(sec)

            # если есть нужный инструмент добавляем в таблицу
            with dpg.table_row(parent='data_table'):
                dpg.add_text(lst['data']['tradenum'])
                dpg.add_text(lst['data']['seccode'])
                dpg.add_text(lst['data']['price'])
                dpg.add_text(lst['data']['qty'])
                dpg.add_text(lst['data']['value'])
                dpg.add_text('date')
                #dpg.add_text(datetime)
                dpg.add_text(flag)
def count_sec(sec):
    pass
def Connect():
    try:
        qp_provider2 = qp_provider.OnConnected()  # Подключение к локальному запущенному терминалу QUIK по портам по умолчанию
        dpg.add_text('Подключение удалось', parent='logger')
    except:
        dpg.add_text('Подключить не удалось', parent='logger')

def Changed_connection(data):
    """Пользовательский обработчик событий:
    - Соединение установлено
    - Соединение разорвано
    """
    dpg.add_text(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}', parent='data_w')
    print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}')  # Печатаем полученные данные
def Close_connect():
    # try:
    qp_provider.CloseConnectionAndThread()
    # qp_provider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy
def Get_data():
    class_code = 'TQBR'  # Класс тикера
    sec_code = 'SBER'  # Тикер
    # Обезличенные сделки. Чтобы получать, в QUIK открыть Таблицу обезличенных сделок, указать тикер
    qp_provider.OnAllTrade = print_callback  # Обработчик получения обезличенной сделки

    qe = queue.Queue()
    t = threading.Thread(target=print_callback, args=[qe])
    t.start()

    while t.is_alive():  # пока функция выполняется
        n = qe.get()

        print(n)


    sleep_sec = 1  # Кол-во секунд получения обезличенных сделок
    # print('Секунд обезличенных сделок:', sleep_sec)
    # time.sleep(sleep_sec)  # Ждем кол-во секунд получения обезличенных сделок

    # qp_provider.OnAllTrade = qp_provider.DefaultHandler  # Возвращаем обработчик по умолчанию
    # qp_provider.OnConnected = changed_connection  # Нажимаем кнопку "Установить соединение" в QUIK
    # qp_provider.OnDisconnected = changed_connection  # Нажимаем кнопку "Разорвать соединение" в QUIK
def accaaunt_btn():
    trade_accounts = qp_provider.GetTradeAccounts()['data']  # Все торговые счета
    class_codes = qp_provider.GetClassesList()['data']  # Список классов
    class_codes_list = class_codes[:-1].split(',')  # Удаляем последнюю запятую, разбиваем значения по запятой
    money_limits = qp_provider.GetMoneyLimits()['data']  # Все денежные лимиты (остатки на счетах)
    # print(trade_accounts)
    # Пробегаемся по всем счетам
    for trade_account in trade_accounts:
        firm_id = trade_account['firmid']  # Фирма
        trade_account_id = trade_account['trdaccid']  # Счет
        distinct_client_code = list(set([moneyLimit['client_code'] for moneyLimit in money_limits if
                                         moneyLimit['firmid'] == firm_id]))  # Уникальные коды клиента по фирме
        dpg.add_text(f'Код клиента {distinct_client_code[0] if distinct_client_code else "не задан"},'
                     f' Фирма {firm_id}, Счет {trade_account_id} ({trade_account["description"]})', parent='data_w')
        trade_account_class_codes = trade_account['class_codes'][1:-1].split(
            '|')  # Классы торгового счета. Удаляем последнюю вертикальную черту, разбиваем значения по вертикальной черте
        intersection_class_codes = list(set(trade_account_class_codes).intersection(
            class_codes_list))  # Классы, которые есть и в списке и в торговом счете