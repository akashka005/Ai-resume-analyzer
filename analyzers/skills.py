import re

HARD_SKILLS = {
    "programming": ["python","java","javascript","c++","c","c#","php","ruby","swift","kotlin","go","rust","typescript","matlab","r","sql","nosql","scala","perl","dart"],
    "web": ["html","css","react","angular","vue.js","svelte","next.js","tailwind","bootstrap","node.js","express","django","flask","laravel","spring boot","asp.net"],
    "data": ["mysql","postgresql","mongodb","redis","cassandra","firebase","dynamo","oracle","bigquery","snowflake","elasticsearch"],
    "cloud": ["aws","azure","google cloud","docker","kubernetes","jenkins","terraform","ansible"],
    "ml": ["tensorflow","pytorch","keras","scikit-learn","pandas","numpy","opencv","nlp","spacy","nltk","hugging face"],
    "security": ["penetration testing","kali","burp suite","owasp","nmap","wireshark","metasploit"],
    "mobile": ["flutter","react native","swiftui","android sdk"],
    "blockchain": ["ethereum","solidity","web3.js","hardhat"],
    "design": ["figma","adobe xd","sketch","photoshop","illustrator"]
}

SOFT_SKILLS = ["leadership","teamwork","communication","problem-solving","time management","adaptability","creativity","collaboration","negotiation","decision-making","mentoring","presentation","analytical"]

LANGUAGES = ["english","spanish","french","german","mandarin","hindi","arabic","japanese","korean","portuguese","russian","italian","dutch","turkish"]

def normalize_word(w):
    return re.sub(r'[^a-z0-9\.\-]','', w.lower())

def extract_and_categorize_skills(text):
    t = text.lower()
    found = {"technical":[], "soft":[], "languages":[], "categories":{}, "missing_skills_short":[]}
    for cat, skills in HARD_SKILLS.items():
        found['categories'][cat] = []
        for s in skills:
            if s in t:
                found['categories'][cat].append(s)
                found['technical'].append(s)
    for s in SOFT_SKILLS:
        if s in t:
            found['soft'].append(s)
    for s in LANGUAGES:
        if s in t:
            found['languages'].append(s)
    found['technical'] = sorted(list(set(found['technical'])))
    popular = ['python','flask','django','sql','aws','docker','kubernetes','react','tensorflow']
    missing = [p for p in popular if p not in found['technical']]
    found['missing_skills_short'] = missing[:6]
    return found