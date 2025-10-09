const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const axios = require("axios"); // to call Python ML server
const dotenv = require('dotenv')
dotenv.config();
const port = process.env.PORT || 6969;

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });


io.on("connection", (socket) => {
  console.log("Client connected", socket.id);

  socket.on("frame", async (frame) => {
    try {
      // Send frame to Python ML server
      const response = await axios.post("http://localhost:8000/predict", { frame });
      const result = response.data; // e.g., { activity: "Yawning" }

      // Send back to client
      socket.emit("activity", result);
    } catch (err) {
      console.error(err);
    }
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected");
  });
});

server.listen(5000, () => console.log());
