package main

import (
	"fmt"
	"net/http"
	"time"

	sarama "github.com/Shopify/sarama"
)

// Handler posts a message to Kafka Topic
func Handler(w http.ResponseWriter, r *http.Request) {
	brokers := []string{"my-cluster-kafka-bootstrap.kafka:9092"}
	producerConfig := sarama.NewConfig()
	producerConfig.Producer.RequiredAcks = sarama.WaitForAll
	producerConfig.Producer.Retry.Max = 10
	producerConfig.Producer.Return.Successes = true
	producer, err := sarama.NewSyncProducer(brokers, producerConfig)
	if err != nil {
		panic(err)
	}
	t := time.Now()
	ts := t.Format(time.RFC3339)
	message := fmt.Sprintf("{\"name\": \"value %s \"}", ts)
	_, _, err = producer.SendMessage(&sarama.ProducerMessage{
		Topic: "my-topic",
		Value: sarama.StringEncoder(message),
	})

	if err != nil {
		w.Write([]byte(fmt.Sprintf("Failed to publish message to topic %s: %v", "my-topic", err)))
		return
	}
	w.Write([]byte("Successfully sent to my-topic"))
}
