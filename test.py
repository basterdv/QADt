from datetime import datetime
import time  # Подписка на события по времени
import pandas as pd
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp


# qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK по портам по умолчанию

def changed_connection(data):
    """Пользовательский обработчик событий:
    - Соединение установлено
    - Соединение разорвано
    """
    # dpg.add_text(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}', parent='data_w')
    log_index = f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}'
    print(log_index)  # Печатаем полученные данные
    print(0, log_index)


def check_connect():
    # Проверяем соединение
    if qp_provider.IsConnected()["data"] == 1:
        print(0, f' Quik подключен')
    else:
        print(0, f' Quik не подключен')


def print_callback(data):
    """Пользовательский обработчик событий:
    - Изменение стакана котировок
    - Получение обезличенной сделки
    - Получение новой свечки
    """
    lst = data

    hour = str(lst['data']['datetime']['hour'])
    min = str(lst['data']['datetime']['min'])
    sec = str(lst['data']['datetime']['sec'])
    str_d = str(f'{hour}:{min}:{sec}')
    datetime_new = datetime.strptime(str_d, '%H:%M:%S').strftime('%X')

    lst['data']['datetime'] = datetime_new  # меняем значение в поле даты
    # Проверям напряление по номеру флага
    if lst['data']['flags'] == 1025:
        lst['data']['flags'] = 'продажа'
    elif lst['data']['flags'] == 1026:
        lst['data']['flags'] = 'купля'
        # tree.tag_configure(foreground='green')
    else:
        lst['data']['flags'] = '------'

    df = pd.DataFrame([lst['data']])  # тоже самое df = pd.DataFrame(lst2,index=[ 0 ])
    df = df.drop(columns=['exec_market', 'repoterm', 'reporate', 'exchange_code', 'yield', 'open_interest',
                          'repovalue', 'sec_code', 'tradenum', 'settlecode', 'repo2value', 'class_code', 'benchmark',

                          'accruedint', 'period'])
    df = df[['trade_num', 'datetime', 'seccode', 'price', 'qty', 'value', 'flags']]

    # filter_sec = ['SBER','VTBR', 'LKOH']
    # filter_sec = 'VTBR'

    df_row = df.to_numpy().tolist()

    if df_row[0][2] == secCode:
        print(df_row[0])
        if df_row [0][4] > 5000:
            print(f'{df_row[0][6]} {df_row[0][4]} лотов в {df_row[0][1]}')
            qp_provider.MessageWarning(f'{df_row[0][6]} {df_row[0][4]} лотов в {df_row[0][1]}')

    # new_filter = []
    # for i in open_config():
    #     new_filter.append(i[0])

    # for row in df_row:
    #     # фильтруем поток по выбранным инстментам
    #     for i in new_filter:
    #         if row[2] == i:
    #             tree.insert("", END, values=row)


def print_callback2(data):
    """Пользовательский обработчик событий:
    - Изменение стакана котировок
    - Получение обезличенной сделки
    - Получение новой свечки
    """
    print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data["data"]}')  # Печатаем полученные данные


def get_data():
    check_connect()
    class_code = 'TQBR'  # Класс тикера
    sec_code = 'SBER'  # Тикер
    # Обезличенные сделки. Чтобы получать, в QUIK открыть Таблицу обезличенных сделок, указать тикер

    qp_provider.OnAllTrade = print_callback  # Обработчик получения обезличенной сделки

    sleep_sec = 0, 5  # Кол-во секунд получения обезличенных сделок
    # print('Секунд обезличенных сделок:', sleep_sec)
    # time.sleep(sleep_sec)  # Ждем кол-во секунд получения обезличенных сделок

    qp_provider.OnConnected = changed_connection  # Нажимаем кнопку "Установить соединение" в QUIK
    qp_provider.OnDisconnected = changed_connection  # Нажимаем кнопку "Разорвать соединение" в QUIK


def get_all_accounts():
    """Получение всех торговых счетов"""
    futures_firm_id = 'SPBFUT'  # Фирма для фьючерсов. Измените, если требуется, на фирму, которую для фьючерсов поставил ваш брокер

    class_codes = qp_provider.GetClassesList()['data']  # Список классов
    class_codes_list = class_codes[:-1].split(',')  # Удаляем последнюю запятую, разбиваем значения по запятой
    trade_accounts = qp_provider.GetTradeAccounts()['data']  # Все торговые счета
    money_limits = qp_provider.GetMoneyLimits()['data']  # Все денежные лимиты (остатки на счетах)
    depo_limits = qp_provider.GetAllDepoLimits()['data']  # Все лимиты по бумагам (позиции по инструментам)
    orders = qp_provider.GetAllOrders()['data']  # Все заявки
    stop_orders = qp_provider.GetAllStopOrders()['data']  # Все стоп заявки

    # Коды клиента / Фирмы / Счета
    for trade_account in trade_accounts:  # Пробегаемся по всем счетам
        firm_id = trade_account['firmid']  # Фирма
        trade_account_id = trade_account['trdaccid']  # Счет
        distinct_client_code = list(set([moneyLimit['client_code'] for moneyLimit in money_limits if
                                         moneyLimit['firmid'] == firm_id]))  # Уникальные коды клиента по фирме
        print(
            f'Код клиента {distinct_client_code[0] if distinct_client_code else "не задан"}, Фирма {firm_id}, Счет {trade_account_id} ({trade_account["description"]})')
        trade_account_class_codes = trade_account['class_codes'][1:-1].split(
            '|')  # Классы торгового счета. Удаляем последнюю вертикальную черту, разбиваем значения по вертикальной черте
        intersection_class_codes = list(set(trade_account_class_codes).intersection(
            class_codes_list))  # Классы, которые есть и в списке и в торговом счете
        # Классы
        for class_code in intersection_class_codes:  # Пробегаемся по всем общим классам
            class_info = qp_provider.GetClassInfo(class_code)['data']  # Информация о классе
            print(f'- Класс {class_code} ({class_info["name"]}), Тикеров {class_info["nsecs"]}')
            # Инструменты. Если выводить на экран, то занимают много места. Поэтому, закомментировали
            # class_securities = qpProvider.GetClassSecurities(classCode)['data'][:-1].split(',')  # Список инструментов класса. Удаляем последнюю запятую, разбиваем значения по запятой
            # print(f'  - Тикеры ({class_securities})')
        if firm_id == futures_firm_id:  # Для фьючерсов свои расчеты
            # Лимиты
            print(
                f'- Фьючерсный лимит {qp_provider.GetFuturesLimit(firm_id, trade_account_id, 0, "SUR")["data"]["cbplimit"]} SUR')
            # Позиции
            futures_holdings = qp_provider.GetFuturesHoldings()['data']  # Все фьючерсные позиции
            active_futures_holdings = [futuresHolding for futuresHolding in futures_holdings if
                                       futuresHolding['totalnet'] != 0]  # Активные фьючерсные позиции
            for active_futures_holding in active_futures_holdings:
                print(
                    f'  - Фьючерсная позиция {active_futures_holding["sec_code"]} {active_futures_holding["totalnet"]} @ {active_futures_holding["cbplused"]}')
        else:  # Для остальных фирм
            # Лимиты
            firm_money_limits = [moneyLimit for moneyLimit in money_limits if
                                 moneyLimit['firmid'] == firm_id]  # Денежные лимиты по фирме
            for firm_money_limit in firm_money_limits:  # Пробегаемся по всем денежным лимитам
                limit_kind = firm_money_limit['limit_kind']  # День лимита
                print(
                    f'- Денежный лимит {firm_money_limit["tag"]} на T{limit_kind}: {firm_money_limit["currentbal"]} {firm_money_limit["currcode"]}')
                # Позиции
                firm_kind_depo_limits = [depoLimit for depoLimit in depo_limits if
                                         depoLimit['firmid'] == firm_id and depoLimit['limit_kind'] == limit_kind and
                                         depoLimit['currentbal'] != 0]  # Берем только открытые позиции по фирме и дню
                for firm_kind_depo_limit in firm_kind_depo_limits:  # Пробегаемся по всем позициям
                    sec_code = firm_kind_depo_limit["sec_code"]  # Код тикера
                    class_code = qp_provider.GetSecurityClass(class_codes, sec_code)['data']
                    entry_price = float(firm_kind_depo_limit["wa_position_price"])
                    last_price = float(qp_provider.GetParamEx(class_code, sec_code, 'LAST')['data'][
                                           'param_value'])  # Последняя цена сделки
                    if class_code == 'TQOB':  # Для рынка облигаций
                        last_price *= 10  # Умножаем на 10
                    print(
                        f'  - Позиция {class_code}.{sec_code} {firm_kind_depo_limit["currentbal"]} @ {entry_price:.2f}/{last_price:.2f}')
        # Заявки
        firm_orders = [order for order in orders if
                       order['firmid'] == firm_id and order['flags'] & 0b1 == 0b1]  # Активные заявки по фирме
        for firm_order in firm_orders:  # Пробегаемся по всем заявкам
            buy = firm_order['flags'] & 0b100 != 0b100  # Заявка на покупку
            print(
                f'- Заявка номер {firm_order["order_num"]} {"Покупка" if buy else "Продажа"} {firm_order["class_code"]}.{firm_order["sec_code"]} {firm_order["qty"]} @ {firm_order["price"]}')
        # Стоп заявки
        firm_stop_orders = [stopOrder for stopOrder in stop_orders if stopOrder['firmid'] == firm_id and stopOrder[
            'flags'] & 0b1 == 0b1]  # Активные стоп заявки по фирме
        for firm_stop_order in firm_stop_orders:  # Пробегаемся по всем стоп заявкам
            buy = firm_stop_order['flags'] & 0b100 != 0b100  # Заявка на покупку
            print(
                f'- Стоп заявка номер {firm_stop_order["order_num"]} {"Покупка" if buy else "Продажа"} {firm_stop_order["class_code"]}.{firm_stop_order["sec_code"]} {firm_stop_order["qty"]} @ {firm_stop_order["price"]}')


def get_ticker_info():
    # Данные тикера
    vtb = qp_provider.GetSecurityInfo(classCode, secCode)['data']  # Интерпретатор языка Lua, Таблица 4.21 Инструменты
    # print('Ответ от сервера:', vtb)

    print(f'Информация о тикере {classCode}.{secCode} ({vtb["short_name"]}):')  # Короткое наименование инструмента
    tradeAccount = qp_provider.GetTradeAccount(classCode)["data"]  # Торговый счет для класса тикера
    print('Торговый счет:', tradeAccount)
    lastPrice = float(
        qp_provider.GetParamEx(classCode, secCode, 'LAST')['data']['param_value'])  # Последняя цена сделки
    print('Последняя цена сделки:', lastPrice)
    print('Валюта:', vtb['face_unit'])  # Валюта номинала
    print('Лот:', vtb['lot_size'])  # Размер лота
    print('Цифр после запятой:', vtb['scale'])  # Точность (кол-во значащих цифр после запятой)
    print('Шаг цены:', vtb['min_price_step'])  # Минимальный шаг цены


def test():
    tes = qp_provider.GetNumCandles(tag)
    print(tes)
    # tesdel = qp_provider.DelAllLabels(tag)
    # testadd = qp_provider.AddLabel(price, cur_date, cur_time, qty, path, label_id, alignment, background)
    # print(testadd)


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK

    firmId = 'MC0063100000'  # Фирма
    classCode = 'TQBR'  # Класс тикера
    secCode = 'VTBR'  # Тикер

    # Получение информации по тикеру
    get_ticker_info()
    #  получения обезличенных сделок
    get_data()
    tag = 'VTBR_tag'

    price = '0,023131'
    cur_date = '2024.03.29'
    cur_time = '13.15.00'
    qty = 'hgjhggjjgjhjhgjhg'
    path = ''
    label_id = 'label_tag'
    alignment = 'LEFT'
    background = '1'


    # Запрос текущего стакана. Чтобы получать, в QUIK открыть Таблицу Котировки, указать тикер
    # print(f'Текущий стакан {classCode}.{secCode}:', qp_provider.GetQuoteLevel2(classCode, secCode)['data'])

    # Выход
    # qp_provider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy
