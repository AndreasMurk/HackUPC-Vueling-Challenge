"use client";
import {FC, useRef, useState} from "react";

const FLASK_BASE_URL = "http://localhost:5000";
const AUDIO_FILE_NAME = "audio.webm";

const AudioRecorder: FC = () => {
    const [permission, setPermission] = useState(false);
    const mediaRecorder = useRef<MediaRecorder | null>(null); // Corrected type
    const [recordingStatus, setRecordingStatus] = useState("inactive");
    const [stream, setStream] = useState<MediaStream | null>(null); // Corrected type
    const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
    const [receivedAudioChunks, setReceivedAudioChunks] = useState<Blob[]>([]);
    const [audio, setAudio] = useState<string | null>(null); // You can adjust the type as needed
    const [text, setText] = useState<string | null>(null); // You can adjust the type as needed
    const mimeType = "audio/webm";

    const getMicrophonePermission = async () => {
        if ("MediaRecorder" in window) {
            try {
                const streamData = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: false,
                });
                setPermission(true);
                setStream(streamData);
            } catch (err: any) {
                alert(err.message);
            }
        } else {
            alert("The MediaRecorder API is not supported in your browser.");
        }
    };

    const startRecording = async () => {
        if (!stream) {
            console.error("Stream is not available");
            return;
        }

        setRecordingStatus("recording");

        const chunks: Blob[] = [];
        mediaRecorder.current = new MediaRecorder(stream, {mimeType});

        mediaRecorder.current.ondataavailable = (event) => {
            if (typeof event.data === "undefined") return;
            if (event.data.size > 0) {
                chunks.push(event.data);
            }
        };
        setReceivedAudioChunks([]);
        setAudioChunks(chunks);

        mediaRecorder.current.start();

        mediaRecorder.current.onstop = () => {
            const audioBlob = new Blob(chunks, {type: mimeType});
            const audioUrl = URL.createObjectURL(audioBlob);
            setAudio(audioUrl);
        };
    };

    const stopRecording = () => {
        setRecordingStatus("inactive");
        if (!mediaRecorder.current) return;
        mediaRecorder.current.stop();
        mediaRecorder.current.onstop = async () => {
            const audioBlob = new Blob(audioChunks, {type: mimeType});

            // Create a FormData object and append the audio file
            const formData = new FormData();
            formData.append('audio', audioBlob, AUDIO_FILE_NAME);

            // Send the audio file to the backend
            try {
                const response = await fetch(`${FLASK_BASE_URL}/upload`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error(`Failed to upload audio: ${response.status} - ${response.statusText}`);

                if (response.body === null) throw new Error("Response body is null");

                // Receive audio chunks directly from response body
                const reader = response.body.getReader();
                const chunks = [];
                while (true) {
                    const {done, value} = await reader.read();
                    if (done) break;
                    chunks.push(value);
                }

                const combinedChunks = new Uint8Array(
                    chunks.reduce((acc, chunk) => acc + chunk.length, 0)
                );

                let offset = 0;
                chunks.forEach(chunk => {
                    combinedChunks.set(chunk, offset);
                    offset += chunk.length;
                });

                const receivedBlob = new Blob([combinedChunks], {type: 'audio/webm'});
                setReceivedAudioChunks([receivedBlob]);
            } catch (error: any) {
                console.error('Error transcribing audio:', error.message);
            }
            setAudioChunks([]);
        };
    };

    return (
        <div>
            <h2>Audio Recorder</h2>
            <main>
                <div className="audio-controls">
                    {!permission ? (
                        <button onClick={getMicrophonePermission} type="button">
                            Get Microphone
                        </button>
                    ) : null}
                    {permission && recordingStatus === "inactive" ? (
                        <button onClick={startRecording} type="button">
                            Start Recording
                        </button>
                    ) : null}
                    {recordingStatus === "recording" ? (
                        <button onClick={stopRecording} type="button">
                            Stop Recording
                        </button>
                    ) : null}
                    {text && <p>{text}</p>}
                    {receivedAudioChunks.length > 0 && (
                        <audio autoPlay={true}>
                            <source src={URL.createObjectURL(receivedAudioChunks[0])} type="audio/mpeg"/>
                            Your browser does not support the audio element.
                        </audio>
                    )}
                </div>
            </main>
        </div>
    );
}

export default AudioRecorder;