import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import RealtimeMonitor from './RealTimeMonitor'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <RealtimeMonitor/>
    </>
  )
}

export default App
