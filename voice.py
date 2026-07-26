import asyncio
import edge_tts
import sounddevice as sd
import soundfile as sf
import io

TEXT = "السلام عليكم، هذا اختبار للصوت المباشر."

async def main():
    communicate = edge_tts.Communicate(
        TEXT,
        voice="ar-SA-HamedNeural"
    )

    audio_data = b""

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]

    data, samplerate = sf.read(io.BytesIO(audio_data), dtype="float32")

    sd.play(data, samplerate)
    sd.wait()

asyncio.run(main())