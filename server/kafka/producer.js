const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'frame-logger',
  brokers: [process.env.KAFKA_BROKER || 'localhost:9092']
});

const producer = kafka.producer();

const connectProducer = async () => {
  await producer.connect();
  console.log('Kafka Producer connected');
};

const sendLog = async (log) => {
  await producer.send({
    topic: 'frame-logs',
    messages: [
      { value: JSON.stringify(log) }
    ]
  });
};

module.exports = { connectProducer, sendLog };
