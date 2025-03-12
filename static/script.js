// TTS form
const ttsForm = document.getElementById('ttsForm');
const ttsAudio = document.getElementById('ttsAudio');

ttsForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(ttsForm);
  try {
    const response = await fetch('/tts', {
      method: 'POST',
      body: formData
    });
    if (!response.ok) {
      throw new Error('TTS request failed.');
    }
    // Convert response to Blob for audio playback
    const blob = await response.blob();
    const objectURL = URL.createObjectURL(blob);
    ttsAudio.src = objectURL;
    ttsAudio.play();
  } catch (error) {
    console.error(error);
    alert('Error generating audio.');
  }
});

// STT with microphone
let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const transcriptionOutput = document.getElementById('transcriptionOutput');

recordBtn.addEventListener('click', async () => {
  // Request audio from mic
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  
  mediaRecorder.start();
  recordBtn.disabled = true;
  stopBtn.disabled = false;
  
  audioChunks = [];
  
  mediaRecorder.addEventListener('dataavailable', (event) => {
    audioChunks.push(event.data);
  });
});

stopBtn.addEventListener('click', async () => {
  mediaRecorder.stop();
  recordBtn.disabled = false;
  stopBtn.disabled = true;
  
  mediaRecorder.addEventListener('stop', async () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    // Create a FormData to send to the server
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recorded.wav');
    
    // Send to /stt endpoint
    try {
      const response = await fetch('/stt', {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        throw new Error('STT request failed.');
      }
      const result = await response.json();
      if (result.error) {
        transcriptionOutput.innerText = "Error: " + result.error;
      } else {
        transcriptionOutput.innerText = result.transcription;
      }
    } catch (err) {
      transcriptionOutput.innerText = "Error calling STT endpoint";
      console.error(err);
    }
  });
});
