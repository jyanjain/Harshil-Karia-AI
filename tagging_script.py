import json
import re

STYLE_KEYWORDS = {
    "storytelling": [
        "story", "journey", "experience", "moment", "incident", "episode", " i remember",
        "when i was", "years ago", "remember", "lesson", "chapter", "phase", "example"
    ],
    "empathy": [
        "understand", "grateful", "challenging", "respect", "love", "valued",
        "respected", "friendship", "support", "care", "connect", "relationship", "gratitude", 'friends'
    ],
    "actionable": [
        "steps", "framework", "approach", "strategy", "plan", "roadmap", "lessons", "learned",
        "here’s what", "how to", "what works", "method", "process", "key takeaways", "challenge", "challenges"
    ],
    "reflective": [
        "spiritual", "life", "purpose", "meaning", "inner", "mindfulness",
        "meditation", "introspection", "values", "philosophy", "ethics"
    ],
    "analytical": [
        "metrics", "data", "ROI", "performance", "results", "analysis",
        "impact", "growth rate", "output", "conversion", "cost", "revenue", "marketing"
    ],
    "motivational": [
        "believe", "inspire", "drive", "focus", "discipline", "consistency", "fit", "workout"
        "resilience", "perseverance", "hustle", "ambition", "vision", "answer to"
    ]
}


CONTEXT_KEYWORDS = {
    "brand_strategy": [
        "brand", "marketing", "campaign", "consumer", "shopper", "storytelling", "creative direction", "branding", "creativity",
        "content", "advertising", "Cadbury", "Kinder Joy", "Maybelline", "L’Oreal", "clients", "global brands", "schbang"
    ],
    "startup_advice": [
        "startup", "entrepreneur", "risk", "opportunity", "bootstrap", "founder", "early stage", "growth hacking", "supermind", "running",
        "investment", "scaling", "pivot", "MVP", "product-market fit", "hustle", "perseverance", "schbang", "foxymoron", "answer to"
    ],
    "ai_in_advertising": [
        "AI", "Adobe Firefly", "creative analytics", "Advize", "automation","machine learning", "technology", 
        "second brain", "production", "AI-driven", "generative", "prompts", "tools", "innovation"
    ],
    "meditation_spirituality": [
        "meditation", "spiritual", "mindfulness", "reflection", "level supermind","peace", "calm", "breathing"
        ,"self-awareness", "mental clarity", "journaling", "affirmations", "purpose", "soul"
    ],
    "leadership": [
        "team", "talent", "culture", "leadership", "mentorship", "creative teams", "collaboration", "vision", 
        "hiring", "workplace", "management", "agency life"
    ],
    "business_growth": [
        "scaling", "growth", "expansion", "revenue", "contracts","profitability", "strategy", "operations", 
        "clients", "retainers", "deals", "partnerships", "network", "money"
    ],
    "content_marketing": [
        "social media", "content", "videos", "posts", "linkedin", "instagram", "audience", "distribution", 
        "reach", "virality", "influencers", "engagement", "community"
    ],
    "learning_journey": [
        "lessons", "mistakes", "what I learned", "what I realized", "key takeaway", "insight", "perspective", 
        "mentor", "education", "college", "school", "books", "podcasts", "decision"
    ]
}


def find_tags(text, keyword_map):
    tags = []
    lower_text = text.lower()
    for tag, keywords in keyword_map.items():
        for k in keywords:
            if re.search(r"\b" + re.escape(k.lower()) + r"\b", lower_text):
                tags.append(tag)
                break 
    return tags

data = []

with open("merged_harshil_data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line.strip())
            
            text_to_analyze = ""
            for m in obj.get("messages", []):
                if m["role"] == "assistant":
                    text_to_analyze += m["content"] + " "
            
            obj["style_markers"] = find_tags(text_to_analyze, STYLE_KEYWORDS)
            obj["context_tags"] = find_tags(text_to_analyze, CONTEXT_KEYWORDS)
            
            if obj["style_markers"] or obj["context_tags"]:
                data.append(obj)
                
        except Exception as e:
            print("Skipping invalid line:", e)

with open("final_data.jsonl", "w", encoding="utf-8") as f:
    for obj in data:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
