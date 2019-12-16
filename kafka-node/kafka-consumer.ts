var kafka = require('kafka-node');
var Consumer = kafka.Consumer;
var Offset = kafka.Offset;
var Client = kafka.KafkaClient;
var topic = 'windowsSucks';

var client = new Client(process.env.ZOOKEEPER_PEERS);
client.on('ready',function() {
  console.log('client is ready');
  console.log(client);
});

var topics = [
    {topic: topic, partition: 0,offset:0},
];
var options = { autoCommit: false, fetchMaxWaitMs: 1000,fetchMinBytes: 1, fetchMaxBytes: 1024 * 1024 , fromOffset:true};

var consumer = new Consumer(client, topics, options);
var offset = new Offset(client);

consumer.on('message', function (message) {
  console.log(message);
});

consumer.on('error', function (err) {
  console.log('error', err);
});


consumer.on('offsetOutOfRange', function (topic) {
  topic.maxNum = 2;
  offset.fetch([topic], function (err, offsets) {
    if (err) {
      return console.error(err);
    }
    var min = Math.min(offsets[topic.topic][topic.partition]);
    consumer.setOffset(topic.topic, topic.partition, min);
  });
});