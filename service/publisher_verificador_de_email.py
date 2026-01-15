def publisher_verificador_de_email(email):
    import pika, uuid, json
    RABBITMQ_URL = "amqps://nbjzdqxe:DUM9T7ujn94iaOtiGbyII0IwfPqWdCNd@shark.rmq.cloudamqp.com/nbjzdqxe"

    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    corr_id = str(uuid.uuid4())
    response = None

    channel.queue_declare(queue='fila_de_email', durable=True)

    def on_response(ch, method, props, body):
        nonlocal response 
        if props.correlation_id == corr_id:
            response = json.loads(body.decode())

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True
    )

    channel.basic_publish(
        exchange='',
        routing_key='fila_de_email',
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id,
        ),
        body=email
    )

    print("Aguardando resposta...")

    while response is None:
        connection.process_data_events(time_limit=1)

    print("Resposta do worker:", response)
    connection.close()

    return response
