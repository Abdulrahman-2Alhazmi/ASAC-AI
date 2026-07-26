from RealtimeSTT import AudioToTextRecorder

def main():
    print("Initializing recorder...")

    # يكتشف اللغة تلقائيًا (عربي أو إنجليزي)
    recorder = AudioToTextRecorder(
    use_main_model_for_realtime=True
)
    
    print("Speak into the microphone...")

    while True:
        text = recorder.text()

        if text:
            print(repr(text))

if __name__ == "__main__":
    main()