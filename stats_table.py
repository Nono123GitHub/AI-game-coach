import base64
import requests
import json
import os
import ast  # Safer than eval

img_file = file_paths[1]

# Read image and convert to base64
with open(img_file, "rb") as file:
    b64_image = base64.b64encode(file.read()).decode("utf-8")

# LLaVA prompt
prompt_llava = """
Give me the stats in python dictionary format only.

if the key is not there in the image, skip it

Keys:
total, assists,kills,capture,headshot

No markdown, no explanations, no code blocks.
"""

# API call payload
payload_llava = {
    "model": "llava",
    "prompt": prompt_llava,
    "images": [b64_image],
    "stream": True
}

# Send request
response = requests.post("http://localhost:11434/api/generate", json=payload_llava, stream=True)

print(f"{img_file}:")
llava_output = ""

# Capture streamed response
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                llava_output += data["response"]
        except json.JSONDecodeError:
            pass

# Clean the output from LLaVA
def clean_llava_output(raw):
    raw = raw.strip()
    if raw.startswith("```") and raw.endswith("```"):
        raw = raw.strip("`")  # removes all backticks
        raw = raw.replace("python", "").strip()
    return raw

clean_output = clean_llava_output(llava_output)

# Safely parse the cleaned output
try:
    stats = ast.literal_eval(clean_output)

    # Ensure all expected keys are present
    required_keys = {"total", "kills", "assists", "headshot","capture"}
    if not required_keys.issubset(stats):
        raise ValueError(f"Missing keys: {required_keys - stats.keys()}")

    print("\nFinal output:\n", stats)

    # Calculations
    kill_contribution_percentage = (stats["kills"] / stats["total"]) * 100
    assist_contribution_percentage = (stats["assists"] / stats["total"]) * 100
    combat_focus_ratio = (stats["kills"] + stats["assists"]) / stats["total"]
    score_per_kill = stats["total"] / stats["kills"]
    score_per_assist = stats["total"] / stats["assists"]
    kill_accuracy = stats["kills"] / stats["headshot"]

    # Output results
    print(f"\nKill Contribution %: {kill_contribution_percentage}")
    print(f"Assist Contribution %: {assist_contribution_percentage}")
    print(f"Combat Focus Ratio: {combat_focus_ratio}")
    print(f"Score per Kill: {score_per_kill}")
    print(f"Score per Assist: {score_per_assist}")
    print(f"Kill accuracy: {kill_accuracy}")

    # Very positive scoring logic
    score = (
        (kill_contribution_percentage * 0.5) +
        (assist_contribution_percentage * 0.4) +
        (combat_focus_ratio * 5) +
        (score_per_kill * 0.7) +
        (score_per_assist * 0.6) +
        (kill_accuracy * 0.5)
    ) / 4  # Soft normalization for a friendlier range

    score = max(min(score, 10), 0)  # Clamp to 0–10

    print(f"\nPerformance Score: {score:.1f}/10 ")




except Exception as e:
    print("\nError parsing output:", e)
    print("\nRaw response:\n", llava_output)
