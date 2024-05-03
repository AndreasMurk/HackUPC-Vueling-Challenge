import React, {FC, useState} from 'react';

const AudioRecorder: FC = () => {
    const [recording, setRecording] = useState(false);
    const [audioChunks, setAudioChunks] = useState<any[]>([]);
    let mediaRecorder: any;
    let audioStream: MediaStream | null = null;

    const startRecording = async () => {
        try {
            // Request microphone permission
            audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(audioStream);

            // Event handler when data is available
            mediaRecorder.ondataavailable = (event: BlobEvent) => {
                setAudioChunks((prevChunks) => [...prevChunks, event.data]);
            };

            // Start recording
            mediaRecorder.start();
            setRecording(true);
        } catch (error) {
            console.error('Error starting recording:', error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorder && audioStream) {
            // Stop recording
            mediaRecorder.stop();
            audioStream.getTracks().forEach((track) => track.stop());
            setRecording(false);
        }
    };

    const downloadRecording = () => {
        if (audioChunks.length > 0) {
            // Concatenate audio chunks into a single Blob
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

            // Create a temporary URL for the Blob
            const url = window.URL.createObjectURL(audioBlob);

            // Create a temporary anchor element to trigger download
            const a = document.createElement('a');
            document.body.appendChild(a);
            a.style.display = 'none';
            a.href = url;
            a.download = 'recording.webm';

            // Trigger download
            a.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }
    };

    return (
        <div>
            <h2>Audio Recorder</h2>
            <button onClick={recording ? stopRecording : startRecording}>
                {recording ? 'Stop Recording' : 'Start Recording'}
            </button>
            {audioChunks.length > 0 && (
                <button onClick={downloadRecording}>Download Recording</button>
            )}
        </div>
    );
};

export default AudioRecorder;
