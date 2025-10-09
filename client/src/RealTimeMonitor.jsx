// App.js
import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";
import "./App.css";

const socket = io("http://localhost:5000"); // unchanged

export default function RealTimeFeed() {
  const videoRef = useRef(null);
  const intervalRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [sending, setSending] = useState(false);
  const [fps, setFps] = useState(0);
  const fpsCounterRef = useRef({ count: 0, lastAt: Date.now() });

  // Only display these simplified user-facing fields
  const [activity, setActivity] = useState({
    eye_status: "unknown",
    yawning: "unknown",
    head_tilted: "unknown",
    phone_used: "unknown",
  });

  useEffect(() => {
    // Socket listeners for UI state and incoming predictions
    const onConnect = () => setConnected(true);
    const onDisconnect = () => setConnected(false);
    const onActivity = (data) => {
      // keep only user-facing, human-readable values
      setActivity({
        eye_status: data.eye_status ?? "unknown",
        yawning: data.yawning ?? "unknown",
        head_tilted: data.head_tilted ? "Yes" : "No",
        phone_used: data.phone_used ? "Yes" : "No",
      });
    };

    socket.on("connect", onConnect);
    socket.on("disconnect", onDisconnect);
    socket.on("activity", onActivity);

    // Obtain webcam stream
    let streamRef = null;
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        streamRef = stream;
        if (videoRef.current) videoRef.current.srcObject = stream;
      })
      .catch((err) => {
        console.error("Camera error:", err);
      });

    // Capture frames every 200ms (logic preserved)
    intervalRef.current = setInterval(() => {
      if (!videoRef.current || videoRef.current.readyState < 2) return;

      setSending(true);
      const canvas = document.createElement("canvas");
      canvas.width = 224;
      canvas.height = 224;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(videoRef.current, 0, 0, 224, 224);
      const base64Image = canvas.toDataURL("image/jpeg");

      socket.emit("frame", base64Image);

      // FPS counter (UI only)
      fpsCounterRef.current.count += 1;
      const now = Date.now();
      if (now - fpsCounterRef.current.lastAt >= 1000) {
        setFps(fpsCounterRef.current.count);
        fpsCounterRef.current.count = 0;
        fpsCounterRef.current.lastAt = now;
      }

      setTimeout(() => setSending(false), 120);
    }, 200);

    // cleanup
    return () => {
      clearInterval(intervalRef.current);
      if (streamRef) streamRef.getTracks().forEach((t) => t.stop());
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
      socket.off("activity", onActivity);
    };
  }, []);

  return (
    <div className="classic-root">
      <header className="classic-header">
        <div className="brand">
          <h1>Real‑Time Monitor</h1>
          <div className="sub">Live user activity</div>
        </div>

        <div className="status-wrap">
          <div className={`conn-dot ${connected ? "on" : "off"}`} />
          <div className="conn-text">{connected ? "Connected" : "Disconnected"}</div>
        </div>
      </header>

      <main className="classic-main">
        <section className="left-col">
          <div className="video-card">
            <video
              ref={videoRef}
              autoPlay
              muted
              playsInline
              className="video-el"
              width={640}
              height={480}
            />
            <div className="video-overlay">
              <div className="sending">
                <div className={`pulse-dot ${sending ? "active" : ""}`} />
                <div className="sending-text">{sending ? "Sending…" : "Idle"}</div>
              </div>

              <div className="fps-badge">FPS: {fps}</div>
            </div>
          </div>

          <div className="info-row">
            <div className="badge classic">Classic</div>
            <div className="hint">Capture: 224×224 • Interval: 200ms</div>
          </div>
        </section>

        <aside className="right-col">
          <div className="activity-box">
            <h2>Current Activity</h2>

            <div className="activity-grid">
              <div className="activity-item">
                <div className="label">Eyes</div>
                <div className={`value ${activity.eye_status === "closed_long" ? "alert" : "ok"}`}>
                  {activity.eye_status}
                </div>
              </div>

              <div className="activity-item">
                <div className="label">Yawning</div>
                <div className={`value ${activity.yawning === "yawning" ? "alert" : "ok"}`}>
                  {activity.yawning}
                </div>
              </div>

              <div className="activity-item">
                <div className="label">Head Tilt</div>
                <div className={`value ${activity.head_tilted === "Yes" ? "alert" : "ok"}`}>
                  {activity.head_tilted}
                </div>
              </div>

              <div className="activity-item">
                <div className="label">Phone</div>
                <div className={`value ${activity.phone_used === "Yes" ? "alert" : "ok"}`}>
                  {activity.phone_used}
                </div>
              </div>
            </div>
          </div>

          <div className="notes">
            <div>Video stream is local. Predictions are shown above.</div>
          </div>
        </aside>
      </main>

      <footer className="classic-footer">
        <div>© {new Date().getFullYear()} — keep it classic.</div>
      </footer>
    </div>
  );
}
