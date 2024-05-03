import React, {useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import AudioRecorder from "./components/AudioRecorder";

function App() {
  const handleMicrophonePermission = async () => {
    try {
      // Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      console.log('Microphone access granted');
      // You can now use the stream object to access audio data
    } catch (error) {
      console.error('Microphone access denied', error);
    }
  };

  useEffect(() => {
    // Request microphone permission when component mounts
    handleMicrophonePermission().then(r => console.log("Microphone permission requested"));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <AudioRecorder />
    </div>
  );
}

export default App;
