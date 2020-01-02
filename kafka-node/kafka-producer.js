module.exports = function (context) {
    var kafka = require('kafka-node'),
        Producer = kafka.Producer,
        KeyedMessage = kafka.KeyedMessage,
        client = new kafka.KafkaClient({kafkaHost: 'my-cluster-kafka-bootstrap.kafka:9092'}),
        producer = new Producer(client),
        km = new KeyedMessage('key', 'message'),
        payloads = [
            { topic: 'my-topic', messages: '{"content": "Another Clean message from kafka producer again"}', partition: 0 }
        ];

    var success = 0;
    console.log("Entering inside the function")
    producer.on('ready', function () {
        producer.send(payloads, function (err, data) {
            console.log(data);
            console.log("inside function");
            success = 1;
        });
    });

    producer.on('error', function (err) {})

    return {
        status: 200,
        body: "The success is "+ success
    };
}
