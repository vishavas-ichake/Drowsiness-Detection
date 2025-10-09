const mongoose = require('mongoose');

const logSchema = new mongoose.Schema({
  frameId: String,
  activity: String,
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Log', logSchema);
