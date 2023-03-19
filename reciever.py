import pika
import json
from analys import analitics as anal
from sender import responce

hostname = '89.108.70.10'  # Ip сервера
port = 5672  # Порт
ReciveQueue = "DownStream"  # Поток получения
ResponceQueue = "UpStream"  # Поток отправки


def parsing(data):
    print(data)
    paramArray = []  # Массив параметров
    IdArray = []  # Массив Id Пользователей
    for i in data:
        averageResault = []
        IdArray.append(i["Id"])
        averageResault.append(i['TeamMembers'])
        averageResault.append(i['DayAvTime'])
        averageResault.append(i['TaskAmount'])
        averageResault.append(i['NcomplitedTask'])
        averageResault.append(i['AvgMess'])
        averageResault.append(i['ProjectsAmount'])
        averageResault.append(i['StekAmount'])
        averageResault.append(i['SportPlayer'])
        paramArray.append(averageResault)

    return paramArray, IdArray


def reciever():
    credentials = pika.PlainCredentials(username='admin', password='admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=ReciveQueue)

    def callback(ch, method, properties, body):
        parsingResult, Id_Array = parsing(json.loads(body))
        resaultAnalytics = anal(parsingResult)
        ResponceData = []
        for i in range(len(Id_Array)):
            ResponceData.append({"Id": int(Id_Array[i]), "BurnoutPercent" : float(resaultAnalytics[i][1])})
            #ResponceData.append([int(Id_Array[i]), float(resaultAnalytics[i][1])])

            # ResponceData.append({int(Id_Array[i]): float(resaultAnalytics[i][1])})
            print(ResponceData)
        responce(ResponceData, hostname, ResponceQueue)

    channel.basic_consume(queue=ReciveQueue, on_message_callback=callback, auto_ack=True)

    print('Ожидание данных.')
    channel.start_consuming()

reciever()
