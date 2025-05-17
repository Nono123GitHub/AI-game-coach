import base64
import requests
import json
import os

# Path to directory containing images
directory = r"C:\Users\nshei\Desktop\youtube code\Expert System\people_moments"

image_files = os.listdir(directory)
if not image_files:
    print("No images found in directory.")
    exit()

first_image_path = os.path.join(directory, image_files[index])

# Convert image to base64
with open(first_image_path, "rb") as img_file:
    b64_image = base64.b64encode(img_file.read()).decode('utf-8')

prompt_llava = """
name the answers for these variables, and in python format, write purely the options for the vars, nothing else. Give one of the options based on the images.
dont be lazy and give all the options CHOOSE ONE, always start with ```python and end with ```

ALWAYS GIVE SOLELY IN PYTHON FORMAT,NO EXPLANATIONS

shooting_bow_type = # CHOOSE ONE: "longbow" | "shortbow" | "crossbow" | "melee" ,this is based on what is in the users hand.
shooting_draw_strength = # CHOOSE ONE: "weak" | "medium" | "strong" ,how strong the user is drawing their bow
shooting_fire_mode = # CHOOSE ONE: "single_shot" | "rapid_fire" ,look at how many arrows in the bow
shooting_aim = # CHOOSE ONE: "hip_fire" | "aimed" | "zoomed_in"| "not aiming" ,look at if the players crosshair is centered on a player or not
movement_walking = # CHOOSE ONE: True/False 
movement_crouching = # CHOOSE ONE: True/False
movement_jumping = # CHOOSE ONE: True/False
combat_melee_attack = # CHOOSE ONE: True/False
combat_target_enemy = # CHOOSE ONE: "nearest" | "strongest" | "weakest" | "farthest" , for weakest or strongest look at if they are in a vulnerable position.
enemy_vulnerable = # CHOOSE ONE: True/False , for weakest or strongest look at if they are in a vulnerable position.
cover_height = # CHOOSE ONE: "low" | "medium" | "high"
cover_stance = # CHOOSE ONE: "standing" | "crouching" | "prone"
health_status = # CHOOSE ONE: "healthy" | "wounded" | "critical" , THIS IS ALL BASED ON THE HEALTH BAR ON THE TOP LEFT CORNER
environment_obstacles = # CHOOSE ONE: "none" | "moving" | "static"
risk_enemy_type = # CHOOSE ONE: "melee" | "bow"
cover_angle = # CHOOSE ONE: "none" | "partial" | "full" , full meaning that players entire vision is blocked while none for open spaces
key_position_controlled_area = # CHOOSE ONE: "high_ground" | "central_zone" | "peripheral_area"
holding_flag = # CHOOSE ONE: "True" | "False" , based on if the player has a flag in his  hand
"""

# Send request to local Ollama LLaVA
payload_llava = {
    "model": "llava",
    "prompt": prompt_llava,
    "images": [b64_image],
    "stream": True
}

response = requests.post("http://localhost:11434/api/generate", json=payload_llava, stream=True)

print(f"{first_image_path}:")
llava_output = ""
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end="", flush=True)
                llava_output += data["response"]
        except json.JSONDecodeError:
            pass

# Send to Mistral for analysis
payload_mistral = {
        "model": "mistral",
        "prompt": f"""
        Narrow One is a browser-based multiplayer archery game where players compete in 5v5 matches with the goal of capturing the enemy flag.
        The game emphasizes skillful archery, positioning, and team play.

    There are multiple game modes:

    Capture the Flag (main mode)

    Custom Matches (private games with custom rules)

    Event Modes (temporary, themed rounds)

    Below is gameplay data from a match. Each value represents the player's state or decision at a given moment:

    shooting_bow_type: "longbow" | "shortbow" | "crossbow" | "melee"

    shooting_draw_strength: "weak" | "medium" | "strong"

    shooting_fire_mode: "single_shot" | "rapid_fire"

    shooting_aim: "hip_fire" | "aimed" | "zoomed_in" | "not aiming"

    movement_walking: True/False

    movement_crouching: True/False

    movement_jumping: True/False

    combat_melee_attack: True/False

    combat_target_enemy: "nearest" | "strongest" | "weakest" | "farthest"

    enemy_vulnerable: True/False

    cover_height: "low" | "medium" | "high"

    cover_stance: "standing" | "crouching" | "prone"

    health_status: "healthy" | "wounded" | "critical"

    environment_obstacles: "none" | "moving" | "static"

    risk_enemy_type: "melee" | "bow"

    cover_angle: "none" | "partial" | "full"

    key_position_controlled_area: "high_ground" | "central_zone" | "peripheral_area"

    holding_flag: True/False

    Model answer:
    Strengths:
    1. You are using a variety of bow types (longbow, shortbow, crossbow), which shows good adaptability to different situations.
    2. You make use of both single-shot and rapid-fire modes effectively, depending on the situation.
    3. You aim your shots consistently, whether it's hip fire, aimed, or zoomed in, showing good accuracy.
    4. You engage in melee combat when necessary, demonstrating versatility in close-quarters combat.
    5. You often target enemies strategically, choosing either the nearest enemy, the strongest, or the weakest opponent, which indicates some level of tactical awareness.
    6. You are aware of your health status and avoid engaging in combat when wounded or critical, showing good self-preservation skills.
    7. You are mindful of environmental obstacles and cover positions, utilizing low, medium, and high cover as needed.
    8. You control key positions such as high ground, central zone, and peripheral areas, demonstrating an understanding of map control.

    Areas for Improvement:
    1. While you use different bow types, it might be beneficial to spend more time mastering each weapon type to improve accuracy and efficiency.
    2. Consider varying your movement strategies by incorporating crouching and jumping into your movements to avoid enemy fire and gain tactical advantages.
    3. Be more proactive in controlling the flag when your team is attacking the enemy base, as holding the flag is a crucial aspect of winning Capture the Flag matches.
    4. Improve your ability to identify enemy vulnerabilities by observing their movement patterns and health status, allowing you to capitalize on opportunities for successful attacks.
    5. Pay attention to the risk posed by melee enemies when engaging in combat with them, as they can quickly close the distance and pose a significant threat if not dealt with promptly.
    6. Monitor your cover angle more diligently to ensure that you are fully protected from enemy fire, especially during intense combat situations.
    7. Focus on improving your positioning in team fights to maximize efficiency and reduce exposure to enemy fire.

    
    Also it is really important to mention:
    cover/hiding
    finding optimal routes when under pressure such as bringing flag back to base
    never mention capture the flag unless image desc includes holding flag
    jumping off things
    desciding when to get into a fight or not especially when under pressure

    Only mention these when relevant.

    Here's a sample of my gameplay data:
    {llava_output}

    Please analyze my playing strategy based on this data. What am I doing well? What areas could I improve in?

    """,
        "images": [b64_image],
        "stream": True
    }

response = requests.post("http://localhost:11434/api/generate", json=payload_mistral, stream=True)

print("\n--- Strategy Analysis ---")
mistral_output = ""
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end="", flush=True)
                mistral_output += data["response"]
        except json.JSONDecodeError:
            pass
