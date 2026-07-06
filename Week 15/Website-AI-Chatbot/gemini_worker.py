#!/usr/bin/env python3
"""
Legacy subprocess worker for Gemini API.
Now replaced by multiprocessing in functions.py.
Kept for compatibility if needed.
"""

import json
import sys


def main():
    try:
        data = json.loads(sys.stdin.read())
        api_key = data.get("api_key", "")
        prompt = data.get("prompt", "")

        if not api_key or not prompt:
            print(json.dumps({"error": "Missing api_key or prompt"}), flush=True)
            sys.exit(1)

        from google import genai
        client = genai.Client(api_key=api_key)

        MODELS = [
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash",
        ]

        for model_name in MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                print(json.dumps({"reply": response.text}), flush=True)
                sys.exit(0)
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    continue
                if "timeout" in error_msg.lower():
                    continue
                continue

        print(json.dumps({"error": "All models failed"}), flush=True)
        sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e)}), flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
