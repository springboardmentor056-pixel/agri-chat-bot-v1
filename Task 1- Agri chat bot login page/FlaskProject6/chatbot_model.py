import random

# Agriculture chatbot responses (English + Tamil)
responses = dict(
    greeting=[
        "Hello! I'm your agriculture assistant. 🌱 How can I help you today?",
        "Hi there! Ask me anything about farming and crops. 🚜",
        "வணக்கம்! நான் உங்கள் வேளாண் உதவியாளர். 🌾 இன்று உங்களுக்கு என்ன உதவி வேண்டும்?",
        "ஹாய்! விவசாயம் மற்றும் பயிர்கள் குறித்து எதை வேண்டுமானாலும் கேளுங்கள். 🚜"
    ],
    fertilizer=[
        "For better yield, use organic compost and nitrogen-rich fertilizer like urea.",
        "Consider using phosphorus and potassium-based fertilizers for root growth.",
        "சிறந்த விளைச்சலுக்கு, இயற்கை உரம் மற்றும் யூரியா போன்ற நைட்ரஜன் நிறைந்த உரத்தை பயன்படுத்துங்கள்.",
        "வேர் வளர்ச்சிக்கு பாஸ்பரஸ் மற்றும் பொட்டாசியம் அடிப்படையிலான உரங்களை பயன்படுத்துங்கள்."
    ],
    pest=[
        "Neem oil spray is effective for many pests.",
        "Introduce natural predators like ladybugs to control pest population.",
        "வெப்பச்செடி எண்ணெய் தெளிப்பு பல பூச்சிகளுக்கு பயனுள்ளதாக இருக்கும்.",
        "லேடிபக்ஸ் போன்ற இயற்கை எதிரிகளை அறிமுகப்படுத்தி பூச்சிகளை கட்டுப்படுத்துங்கள்."
    ],
    weather=[
        "Please check the local forecast before sowing seeds.",
        "Avoid watering plants if heavy rain is predicted.",
        "விதைகள் விதைக்கும் முன் உள்ளூர் வானிலை முன்னறிவிப்பை சரிபார்க்கவும்.",
        "கனமழை எதிர்பார்க்கப்பட்டால் தாவரங்களுக்கு நீர் ஊற்றுவதை தவிர்க்கவும்."
    ],
    default=[
        "I'm not sure about that. Could you please rephrase?",
        "Sorry, I don't understand. Can you ask another question?",
        "அதைப் பற்றி எனக்கு உறுதி இல்லை. தயவு செய்து மீண்டும் விளக்கமாகக் கேளுங்கள்.",
        "மன்னிக்கவும், எனக்கு புரியவில்லை. வேறு கேள்வி கேளுங்கள்."
    ]
)


def get_response(user_input):
    user_input = user_input.lower()

    # English + Tamil keyword matching
    if "hello" in user_input or "hi" in user_input or "வணக்கம்" in user_input or "ஹாய்" in user_input:
        return random.choice(responses["greeting"])
    elif "fertilizer" in user_input or "உரம்" in user_input:
        return random.choice(responses["fertilizer"])
    elif "pest" in user_input or "பூச்சி" in user_input:
        return random.choice(responses["pest"])
    elif "weather" in user_input or "வானிலை" in user_input:
        return random.choice(responses["weather"])
    else:
        return random.choice(responses["default"])
