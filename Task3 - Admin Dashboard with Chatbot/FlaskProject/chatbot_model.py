import os
import random
from dotenv import load_dotenv
from openai import OpenAI
from translator_util import translate_text, detect_language  # your translation module

# ------------------- Load environment -------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = None
if api_key:
    client = OpenAI(api_key=api_key)


# ------------------- Greetings & Farewells -------------------
greetings = {
    "en": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
    "ta": ["வணக்கம்", "ஹலோ"],
    "hi": ["नमस्ते", "हैलो"],
    "ml": ["ഹലോ", "നമസ്ക്കാരം"],
    "te": ["హలో", "నమస్తే"]
}

greeting_responses = {
    "en": ["Hello! How can I help you today?", "Hi there! Ask me anything about farming. 🌾"],
    "ta": ["வணக்கம்! இன்று உங்களுக்கு எவ்வாறு உதவலாம்?"],
    "hi": ["नमस्ते! खेती के बारे में मुझसे कुछ भी पूछें। 🌱"],
    "ml": ["ഹലോ! കൃഷിയെ കുറിച്ച് എന്തെങ്കിലും ചോദിക്കാം. 🌿"],
    "te": ["హలో! వ్యవసాయం గురించి ఏదైనా అడగండి. 🌱"]
}

farewells = {
    "en": ["bye", "goodbye", "see you", "thanks", "thank you"],
    "ta": ["பிரியாவிடை", "நன்றி"],
    "hi": ["अलविदा", "धन्यवाद"],
    "ml": ["വിട", "നന്ദി"],
    "te": ["వీడ్కోలు", "ధన్యవాదాలు"]
}

farewell_responses = {
    "en": ["Goodbye! Happy farming! 🌾", "You're welcome! 😊"],
    "ta": ["வாழ்த்துகள்! மகிழ்ச்சியான விவசாயம்! 🌾"],
    "hi": ["अलविदा! खेती में सफलता मिले! 🌱"],
    "ml": ["വിട! സന്തോഷകരമായ കൃഷി ചെയ്യുക! 🌿"],
    "te": ["వీడ్కోలు! సంతోషకరమైన వ్యవసాయం! 🌱"]
}


# ------------------- Offline Knowledge Base -------------------
queries = {
    "soil": {
        # Cereals
        "cotton": {
            "en": "Cotton grows best in deep, fertile, well-drained sandy loam soil with good moisture retention.",
            "ta": "பருத்தி ஆழமான, வளமான, நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
            "hi": "कपास गहरी, उपजाऊ, अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगती है।",
            "ml": "പഞ്ചു ആഴമുള്ള, വളമുള്ള, നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണൽ-ചെങ്കല്ല് മണ്ണിൽ വളരുന്നു.",
            "te": "పత్తి లోతైన, సారవంతమైన, బాగా డ్రైనేజీ ఉన్న ఇసుక లోమ్ మట్టిలో బాగా పెరుగుతుంది."
        },
        "rice": {
            "en": "Rice grows best in clayey loam soil with good water retention.",
            "ta": "அரிசி நல்ல நீர் தாங்கும் திறன் கொண்ட பஞ்சுப் பாங்கு மண்ணில் சிறப்பாக வளரும்.",
            "hi": "चावल चिकनी दोमट मिट्टी में सबसे अच्छा उगता है जिसमें पानी की अच्छी धारण क्षमता होती है।",
            "ml": "അരി നല്ല ജലധാരണമുള്ള മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
            "te": "బియ్యం మంచి నీరు నిల్వ చేసే మట్టిలో బాగా పెరుగుతుంది."
        },
        "wheat": {
            "en": "Wheat prefers loamy or alluvial soil with good drainage.",
            "ta": "கோதுமை நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "गेहूं अच्छे जल निकासी वाले दोमट या जलोढ़ मिट्टी में उगता है।",
            "ml": "ഗോതമ്പ് നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
            "te": "గోధుమలు మంచి డ్రైనేజీ ఉన్న లోమ్ మట్టిలో బాగా పెరుగుతాయి."
        },
        "maize": {
            "en": "Maize grows well in well-drained sandy loam or loamy soil rich in organic matter.",
            "ta": "சோளம் நன்கு வடிகாலமைப்பு கொண்ட, உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "मक्का अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
            "ml": "ചോളം ജൈവവസ്തുക്കളിൽ സമ്പന്നമായ മണ്ണിൽ വളരുന്നു.",
            "te": "మొక్కజొన్న సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతుంది."
        },

        # Vegetables
        "tomato": {
            "en": "Tomatoes grow best in well-drained, fertile sandy loam soil with pH 6.0–6.8.",
            "ta": "தக்காளி நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
            "hi": "टमाटर उपजाऊ बलुई दोमट मिट्टी में अच्छी तरह उगते हैं।",
            "ml": "തക്കാളി വളമുള്ള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
            "te": "టమాటాలు మంచి డ్రైనేజీ ఉన్న మట్టిలో బాగా పెరుగుతాయి."
        },
        "potato": {
            "en": "Potatoes prefer loose, well-drained loamy soil with good organic content.",
            "ta": "உருளைக்கிழங்கு உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "आलू उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
            "ml": "ഉരുളക്കിഴങ്ങ് നല്ല ജൈവവസ്തുക്കളുള്ള മണ്ണിൽ വളരുന്നു.",
            "te": "బంగాళదుంపలు సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతాయి."
        },
        "onion": {
            "en": "Onions require well-drained sandy loam soil with neutral to slightly alkaline pH.",
            "ta": "வெங்காயம் நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "प्याज बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
            "ml": "സവാള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
            "te": "ఉల్లిపాయలు లోమ్ మట్టిలో బాగా పెరుగుతాయి."
        },
        "carrot": {
            "en": "Carrots grow well in deep, sandy, loose soil to allow root development.",
            "ta": "காரட் ஆழமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
            "hi": "गाजर रेतीली मिट्टी में अच्छी तरह उगता है।",
            "ml": "കാരറ്റ് ആഴമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
            "te": "గాజర గడ్డి మట్టిలో బాగా పెరుగుతుంది."
        },

        # Fruits
        "mango": {
            "en": "Mangoes prefer deep, well-drained sandy loam soil rich in organic matter.",
            "ta": "மாம்பழம் நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "आम बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
            "ml": "മാമ്പഴം വളമുള്ള മണ്ണിൽ വളരുന്നു.",
            "te": "మామిడి లోమ్ మట్టిలో బాగా పెరుగుతుంది."
        },
        "banana": {
            "en": "Bananas grow best in rich, well-drained loamy soil with high moisture retention.",
            "ta": "வாழை உயர் ஈரப்பதம் கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "केला उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
            "ml": "വാഴപ്പഴം നല്ല ജലധാരണമുള്ള മണ്ണിൽ വളരുന്നു.",
            "te": "అరటిపండ్లు లోమ్ మట్టిలో బాగా పెరుగుతాయి."
        },
        "apple": {
            "en": "Apples require well-drained loamy soil with good fertility and slightly acidic pH.",
            "ta": "ஆப்பிள் நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "सेब अम्लीय जल निकासी वाली मिट्टी में अच्छी तरह उगते हैं।",
            "ml": "ആപ്പിൾ നല്ല മണ്ണിൽ വളരുന്നു.",
            "te": "ఆపిల్ లోమ్ మట్టిలో బాగా పెరుగుతుంది."
        },
        "orange": {
            "en": "Oranges grow best in deep, sandy loam soil with good drainage.",
            "ta": "ஆரஞ்சு நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "संतरा बलुई मिट्टी में अच्छी तरह उगता है।",
            "ml": "ഓറഞ്ച് നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
            "te": "నారింజలు ఇసుక మట్టిలో బాగా పెరుగుతాయి."
        },
        "grape": {
            "en": "Grapes prefer well-drained sandy loam soil with moderate fertility.",
            "ta": "திராட்சை மணற்பாங்கு மண்ணில் வளரும்.",
            "hi": "अंगूर बलुई दोमट मिट्टी में अच्छी तरह उगते हैं।",
            "ml": "മുന്തിരി നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
            "te": "ద్రాక్షలు ఇసుక మట్టిలో బాగా పెరుగుతాయి."
        }
    },

    "fertilizer": {
        "en": [
            "Use organic compost and nitrogen-rich fertilizer for better yield.",
            "Phosphorus and potassium fertilizers help root growth.",
            "Apply balanced NPK fertilizer according to soil test results."
        ],
        "ta": ["மேல்தரம் விளைச்சல் பெற உயிர்ச்சத்து நிறைந்த உரம் பயன்படுத்தவும்.", "வேர் வளர்ச்சிக்கு பாஸ்பரஸ் மற்றும் பொட்டாசியம் உரங்கள் உதவும்."],
        "hi": ["बेहतर उपज के लिए कार्बनिक खाद और नाइट्रोजन-समृद्ध उर्वरक का उपयोग करें।", "जड़ विकास के लिए फॉस्फोरस और पोटेशियम उर्वरक मदद करते हैं।"],
        "ml": ["മികച്ച വിളവിന് ജൈവ വളവും നൈട്രജൻ സമ്പന്ന വളവും ഉപയോഗിക്കുക."],
        "te": ["మంచి దిగుబడికి ఆర్గానిక్ కాంపోస్ట్ మరియు నిట్రోజన్-రిచ్ ఎరువులను ఉపయోగించండి."]
    },

    "pest": {
        "en": [
            "Neem oil is effective against many pests.",
            "Use natural pesticides like garlic or chili extracts for eco-friendly farming.",
            "Regular monitoring and crop rotation help reduce pest attacks."
        ],
        "ta": ["நீம் எண்ணெய் பல பூச்சிகளுக்கு விளைவுள்ளது."],
        "hi": ["नीम का तेल कई कीड़ों के खिलाफ प्रभावी है।"],
        "ml": ["നീം എണ്ണ പല കീടങ്ങൾക്ക് ഫലപ്രദമാണ്."],
        "te": ["నీమోయిల్ చాలా pests కు సమర్థవంతంగా పనిచేస్తుంది."]
    },

    "harvest": {
        "en": "Harvesting depends on the crop type. Ensure proper maturity before harvesting for best yield.",
        "ta": "பழங்கள் அறுவடை செய்யும் முன் சரியான வளர்ச்சி பெற்றிருப்பதை உறுதி செய்யுங்கள்.",
        "hi": "फसल की कटाई प्रकार पर निर्भर करती है। सर्वोत्तम उपज के लिए सही परिपक्वता सुनिश्चित करें।",
        "ml": "വളവു വിളവെടുപ്പ് വിളയുടെ തരത്തിൽ ആശ്രിതമാണ്. നല്ല വിളവിന് പൂർണമായ വളർച്ച ഉറപ്പാക്കുക.",
        "te": "ఫలితానికి సరైన పాకవయసు వచ్చి ఉన్నట్లు నిర్ధారించండి."
    }
}


# ------------------- Functions -------------------

def get_offline_response(user_input: str, lang="en"):
    user_input_lower = user_input.lower()
    # Greetings & Farewells handled in process_message
    # Soil
    for crop, translations in queries.get("soil", {}).items():
        if crop in user_input_lower:
            return translations.get(lang, translations.get("en"))
    # Other topics
    for topic in ["fertilizer", "pest", "harvest"]:
        if topic in user_input_lower:
            resp = queries.get(topic, {}).get(lang, queries.get(topic, {}).get("en"))
            return random.choice(resp) if isinstance(resp, list) else resp
    return None


def ask_openai(user_input: str):
    if not client:
        return None
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an agriculture assistant. Reply clearly and concisely."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return None


def process_message(user_input, dest_lang=None):
    """
    1. Detect user language
    2. Check for greetings/farewells
    3. Offline knowledge base first
    4. OpenAI fallback
    5. Offline default fallback
    """
    try:
        user_lang = detect_language(user_input)
    except:
        user_lang = "en"

    if not dest_lang:
        dest_lang = user_lang

    # --- Step 0: Greetings ---
    user_input_lower = user_input.lower()
    for lang, greet_list in greetings.items():
        if any(greet.lower() in user_input_lower for greet in greet_list):
            return random.choice(greeting_responses.get(lang, greeting_responses["en"]))

    # --- Step 0b: Farewells ---
    for lang, bye_list in farewells.items():
        if any(word.lower() in user_input_lower for word in bye_list):
            return random.choice(farewell_responses.get(lang, farewell_responses["en"]))

    # --- Step 1: Offline KB ---
    response = get_offline_response(user_input, lang=dest_lang)
    if response:
        return response

    # --- Step 2: OpenAI fallback ---
    response = ask_openai(user_input)
    if response:
        if dest_lang != "en":
            try:
                response = translate_text(response, dest=dest_lang)
            except:
                pass
        return response

    # --- Step 3: Offline default fallback ---
    defaults = {
        "en": "I couldn’t find an answer. Please ask about soil, fertilizer, pests, or harvesting.",
        "ta": "நான் பதிலை கண்டறிய முடியவில்லை. தயவுசெய்து மணல், உரம், பூச்சிகள் அல்லது அறுவடை பற்றி கேளுங்கள்.",
        "hi": "मैं उत्तर नहीं पा सका। कृपया मिट्टी, उर्वरक, कीट या कटाई के बारे में पूछें।",
        "ml": "ഞാൻ ഒരു ഉത്തരം കണ്ടെത്താനായില്ല. ദയവായി മണ്ണ്, വളം, കീടങ്ങൾ അല്ലെങ്കിൽ വിളവെടുപ്പ് ചോദിക്കുക.",
        "te": "నేను సమాధానం కనుగొనలేకపోయాను. దయచేసి మట్టీ, ఎరువు, కీటకాల లేదా ఫలితాల గురించి అడగండి."
    }
    return defaults.get(dest_lang, defaults["en"])
