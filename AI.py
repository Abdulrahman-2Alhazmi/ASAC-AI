import asyncio
import io
import re

import cohere
import edge_tts
import sounddevice as sd
import soundfile as sf
import arabic_reshaper
from bidi.algorithm import get_display

from RealtimeSTT import AudioToTextRecorder


# ==============================
# ضع مفتاح Cohere هنا
# ==============================
CAK = "55jJ5MENJymIlXYJQghwA6kozSSZ6Azwi6q3pNPw"

co = cohere.ClientV2(CAK)


def contains_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))


# تحسين عرض النص العربي في الكونسول
def format_text(text):
    if contains_arabic(text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text


def get_voice(text):
    if contains_arabic(text):
        return "ar-SA-HamedNeural"
    else:
        return "en-US-GuyNeural"


def ask_ai(question):
    if contains_arabic(question):
        system_message = (
            "أجب دائمًا باللغة العربية فقط. "
            "لا تستخدم الإنجليزية إلا إذا طلب المستخدم ذلك."
        )
    else:
        system_message = (
            "Always reply in English. "
            "Do not switch to Arabic unless the user explicitly asks."
        )

    response = co.chat(
        model="command-a-03-2025",
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.message.content[0].text


async def speak(text, voice):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    audio_bytes = b""

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]

    audio, sample_rate = sf.read(
        io.BytesIO(audio_bytes),
        dtype="float32"
    )

    sd.play(audio, sample_rate)
    sd.wait()


def main():
    print("=" * 50)
    print("      Voice Chatbot Started")
    print("=" * 50)

    recorder = AudioToTextRecorder(
        use_main_model_for_realtime=True
    )

    while True:
        try:
            print("\n🎤 Listening...")

            text = recorder.text()

            if not text:
                continue

            text = text.strip()

            if text.lower() in ["exit", "quit"] or text in ["خروج", "إيقاف"]:
                print("Goodbye!")
                break

            print(f"\n🧑 You: {format_text(text)}")

            print("🤖 Thinking...")

            reply = ask_ai(text)

            print(f"\n💬 AI: {format_text(reply)}")

            voice = get_voice(text)

            print(f"🔊 Voice: {voice}")

            print("🔊 Speaking...")

            asyncio.run(speak(reply, voice))

        except KeyboardInterrupt:
            print("\nProgram stopped.")
            break

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()