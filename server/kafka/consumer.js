const { Kafka } = require('kafkajs');
const connectDB = require('../config/db');
const Log = require('../models/logModel');

const kafka = new Kafka({
  clientId: 'frame-log-consumer',
  brokers: [process.env.KAFKA_BROKER || 'localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'frame-log-group' });

const startConsumer = async () => {
  await connectDB();
  await consumer.connect();
  await consumer.subscribe({ topic: 'frame-logs', fromBeginning: false });
  console.log('Kafka Consumer connected');

  await consumer.run({
    eachMessage: async ({ message }) => {
      const log = JSON.parse(message.value.toString());
      await Log.create(log);  // save to MongoDB
    },
  });
};

startConsumer().catch(console.error);
