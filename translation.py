fr = {
        "title": "Chatbot Élections 2024",
        "language": "Langue :",
        "select_model": "Choisissez un modèle d'intelligence artificielle",
        "welcome_message": "Bonjour, je suis une intelligence artificielle pour vous aider avec le processus des élections. Comment puis-je vous aider ?",
        "attention_message": "*Attention, les réponses peuvent être approximatives. Relancez la réponse si besoin.*",
        "button_save_message": "Sauver messages"
    }
nl= {
        "title": "Verkiezingen 2024 chatbot",
        "language": "Taal :",
        "select_model": "Kies een llm",
        "welcome_message": "Hallo, ik ben een kunstmatige intelligentie om u te helpen met het verkiessingsproces. Hoe kan ik u helpen?",
        "attention_message": "*Let op, de antwoorden kunnen benaderend zijn. Herhaal de vraag indien nodig.*",
        "button_save_message": "Berichts opslaan"
    }
eng= {
    "title": "Chatbot elections 2024",
    "language": "Language:",
    "select_model": "Select a language model",
    "welcome_message": "Hello, I am an artificial intelligence here to assist you with the election process. How can I help you?",
    "attention_message": "*Please note, the answers may be approximate. Repeat the question if necessary.*",
    "button_save_message": "Save messages"
}

def get_translation(lang):
    if lang == "Français":
        return fr
    elif lang == "Nederlands":
        return nl
    else:
        return eng