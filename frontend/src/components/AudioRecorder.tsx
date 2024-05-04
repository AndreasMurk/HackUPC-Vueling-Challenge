"use client";
import {FC, useRef, useState} from "react";

const AudioRecorder: FC = () => {
    const [permission, setPermission] = useState(false);
    const mediaRecorder = useRef<MediaRecorder | null>(null); // Corrected type
    const [recordingStatus, setRecordingStatus] = useState("inactive");
    const [stream, setStream] = useState<MediaStream | null>(null); // Corrected type
    const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
    const [audio, setAudio] = useState<string | null>(null); // You can adjust the type as needed
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
        //stops the recording instance
        if (!mediaRecorder.current) return;
        mediaRecorder.current.stop();
        mediaRecorder.current.onstop = () => {
            //creates a blob file from the audiochunks data
            const audioBlob = new Blob(audioChunks, {type: mimeType});
            //creates a playable URL from the blob file.
            const audioUrl = URL.createObjectURL(audioBlob);
            setAudio(audioUrl);
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
                </div>
                {audio ? (
                    <div className="audio-container">
                        <audio src={audio} controls></audio>
                        <a download href={audio}>
                            Download Recording
                        </a>
                    </div>
                ) : null}
            </main>
        </div>
    );
}

export default AudioRecorder;