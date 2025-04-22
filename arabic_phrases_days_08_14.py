import argparse
import os
import time
import asyncio
import edge_tts

# Define phrases by day and category

# Day 8: Shopping Vocabulary
day8_phrases = {
    "Shopping Places": [
        {
            "ar": "متجر",
            "transliteration": "matjar",
            "en": "store"
        },
        {
            "ar": "سوبرماركت",
            "transliteration": "subermarket",
            "en": "supermarket"
        },
        {
            "ar": "سوق",
            "transliteration": "suq",
            "en": "market"
        },
        {
            "ar": "متجر كبير",
            "transliteration": "matjar kabir",
            "en": "department store"
        },
        {
            "ar": "مركز تسوق",
            "transliteration": "markaz tasawwuq",
            "en": "shopping mall"
        }
    ],
    "Shopping Phrases": [
        {
            "ar": "كم الثمن؟",
            "transliteration": "kam al-thaman?",
            "en": "How much money?"
        },
        {
            "ar": "غالي جداً",
            "transliteration": "ghali jiddan",
            "en": "Too expensive"
        },
        {
            "ar": "أرخص قليلاً",
            "transliteration": "arkhas qalilan",
            "en": "A little cheaper"
        },
        {
            "ar": "أريد هذا",
            "transliteration": "urid hadha",
            "en": "I want this one"
        },
        {
            "ar": "أنا فقط أنظر",
            "transliteration": "ana faqat andhur",
            "en": "I'm just looking"
        }
    ]
}

# Day 9: Transportation
day9_phrases = {
    "Transportation Types": [
        {
            "ar": "حافلة",
            "transliteration": "hafila",
            "en": "bus"
        },
        {
            "ar": "مترو",
            "transliteration": "metro",
            "en": "subway"
        },
        {
            "ar": "تاكسي",
            "transliteration": "taxi",
            "en": "taxi"
        },
        {
            "ar": "قطار",
            "transliteration": "qitar",
            "en": "train"
        },
        {
            "ar": "طائرة",
            "transliteration": "ta'ira",
            "en": "airplane"
        },
        {
            "ar": "دراجة",
            "transliteration": "darraja",
            "en": "bicycle"
        }
    ],
    "Transportation Phrases": [
        {
            "ar": "كيف أصل إلى المطار؟",
            "transliteration": "kayfa asil ila al-matar?",
            "en": "How do I get to the airport?"
        },
        {
            "ar": "أين موقف الحافلة؟",
            "transliteration": "ayna mawqif al-hafila?",
            "en": "Where is the bus stop?"
        },
        {
            "ar": "من فضلك خذني إلى هذا العنوان",
            "transliteration": "min fadlik khudhni ila hadha al-'unwan",
            "en": "Please take me to this address"
        },
        {
            "ar": "كم ثمن التذكرة؟",
            "transliteration": "kam thaman al-tadhkira?",
            "en": "How much is one ticket?"
        },
        {
            "ar": "متى تأتي الحافلة التالية؟",
            "transliteration": "mata ta'ti al-hafila al-taliya?",
            "en": "When does the next bus come?"
        }
    ]
}

# Day 10: Dining and Food
day10_phrases = {
    "Food Items": [
        {
            "ar": "أرز",
            "transliteration": "aruz",
            "en": "rice"
        },
        {
            "ar": "معكرونة",
            "transliteration": "ma'karona",
            "en": "noodles"
        },
        {
            "ar": "دجاج",
            "transliteration": "dajaj",
            "en": "chicken"
        },
        {
            "ar": "لحم بقر",
            "transliteration": "lahm baqar",
            "en": "beef"
        },
        {
            "ar": "لحم غنم",
            "transliteration": "lahm ghanam",
            "en": "lamb"
        },
        {
            "ar": "خضروات",
            "transliteration": "khudrawat",
            "en": "vegetables"
        },
        {
            "ar": "فواكه",
            "transliteration": "fawakih",
            "en": "fruit"
        }
    ],
    "Restaurant Phrases": [
        {
            "ar": "قائمة الطعام",
            "transliteration": "qa'imat al-ta'am",
            "en": "menu"
        },
        {
            "ar": "أريد أن أطلب",
            "transliteration": "urid an atlub",
            "en": "I'd like to order"
        },
        {
            "ar": "نادل",
            "transliteration": "nadil",
            "en": "waiter"
        },
        {
            "ar": "الحساب من فضلك",
            "transliteration": "al-hisab min fadlik",
            "en": "check please"
        },
        {
            "ar": "هل هذا لذيذ؟",
            "transliteration": "hal hadha ladhidh?",
            "en": "Is this delicious?"
        },
        {
            "ar": "أريد كأس ماء",
            "transliteration": "urid ka's ma'",
            "en": "I want a glass of water"
        }
    ]
}

# Day 11: Directions
day11_phrases = {
    "Direction Words": [
        {
            "ar": "يسار",
            "transliteration": "yasar",
            "en": "left side"
        },
        {
            "ar": "يمين",
            "transliteration": "yamin",
            "en": "right side"
        },
        {
            "ar": "أمام",
            "transliteration": "amam",
            "en": "in front"
        },
        {
            "ar": "خلف",
            "transliteration": "khalf",
            "en": "behind"
        },
        {
            "ar": "فوق",
            "transliteration": "fawq",
            "en": "above"
        },
        {
            "ar": "تحت",
            "transliteration": "taht",
            "en": "below"
        },
        {
            "ar": "داخل",
            "transliteration": "dakhil",
            "en": "inside"
        },
        {
            "ar": "خارج",
            "transliteration": "kharij",
            "en": "outside"
        }
    ],
    "Asking for Directions": [
        {
            "ar": "عفواً، أين البنك؟",
            "transliteration": "afwan, ayna al-bank?",
            "en": "Excuse me, where is the bank?"
        },
        {
            "ar": "كيف أصل إلى محطة القطار؟",
            "transliteration": "kayfa asil ila mahattat al-qitar?",
            "en": "How do I get to the train station?"
        },
        {
            "ar": "اذهب مباشرة",
            "transliteration": "idhhab mubashara",
            "en": "go straight"
        },
        {
            "ar": "انعطف يساراً",
            "transliteration": "in'atif yasaran",
            "en": "turn left"
        },
        {
            "ar": "انعطف يميناً",
            "transliteration": "in'atif yaminan",
            "en": "turn right"
        },
        {
            "ar": "كم المسافة مشياً؟",
            "transliteration": "kam al-masafa mashyan?",
            "en": "How far to walk?"
        }
    ]
}

# Day 12: Basic Sentence Patterns
day12_phrases = {
    "Subject-Verb-Object": [
        {
            "ar": "أنا آكل الأرز",
            "transliteration": "ana akul al-aruz",
            "en": "I eat rice"
        },
        {
            "ar": "هو يشرب الماء",
            "transliteration": "huwa yashrab al-ma'",
            "en": "He drinks water"
        },
        {
            "ar": "نحن نتعلم العربية",
            "transliteration": "nahnu nata'allam al-'arabiyya",
            "en": "We learn Arabic"
        },
        {
            "ar": "هي تقرأ كتاباً",
            "transliteration": "hiya taqra' kitaban",
            "en": "She reads a book"
        }
    ],
    "Question Patterns": [
        {
            "ar": "هل أنت طالب؟",
            "transliteration": "hal anta talib?",
            "en": "Are you a student?"
        },
        {
            "ar": "هل تحب الطعام العربي؟",
            "transliteration": "hal tuhibb al-ta'am al-'arabi?",
            "en": "Do you like Arabic food?"
        },
        {
            "ar": "هل تتكلم الإنجليزية؟",
            "transliteration": "hal tatakallam al-injliziyya?",
            "en": "Can you speak English?"
        },
        {
            "ar": "ما هذا؟",
            "transliteration": "ma hadha?",
            "en": "What is this?"
        }
    ],
    "Negation Patterns": [
        {
            "ar": "أنا لست عربياً",
            "transliteration": "ana lastu 'arabiyyan",
            "en": "I am not Arab"
        },
        {
            "ar": "ليس لديه وقت",
            "transliteration": "laysa ladayhi waqt",
            "en": "He doesn't have time"
        },
        {
            "ar": "لا أحب القهوة",
            "transliteration": "la uhibb al-qahwa",
            "en": "I don't like coffee"
        },
        {
            "ar": "هي لا تستطيع السباحة",
            "transliteration": "hiya la tastati' al-sibaha",
            "en": "She can't swim"
        }
    ]
}

# Day 13: Emergency and Travel Arabic
day13_phrases = {
    "Emergency Phrases": [
        {
            "ar": "النجدة!",
            "transliteration": "al-najda!",
            "en": "Help! (emergency)"
        },
        {
            "ar": "أحتاج مساعدة",
            "transliteration": "ahtaj musa'ada",
            "en": "I need help"
        },
        {
            "ar": "لقد ضللت الطريق",
            "transliteration": "laqad dalaltu al-tariq",
            "en": "I'm lost"
        },
        {
            "ar": "أنا مريض",
            "transliteration": "ana marid",
            "en": "I'm sick"
        },
        {
            "ar": "من فضلك اتصل بطبيب",
            "transliteration": "min fadlik ittasil bi-tabib",
            "en": "Please call a doctor"
        },
        {
            "ar": "من فضلك اتصل بالشرطة",
            "transliteration": "min fadlik ittasil bil-shurta",
            "en": "Please call the police"
        }
    ],
    "Hotel Phrases": [
        {
            "ar": "لدي حجز",
            "transliteration": "ladayya hajz",
            "en": "I have a reservation"
        },
        {
            "ar": "أريد غرفة",
            "transliteration": "urid ghurfa",
            "en": "I would like a room"
        },
        {
            "ar": "مفتاح الغرفة",
            "transliteration": "miftah al-ghurfa",
            "en": "room key"
        },
        {
            "ar": "تسجيل المغادرة",
            "transliteration": "tasjil al-mughadara",
            "en": "check out"
        },
        {
            "ar": "أمتعة",
            "transliteration": "amti'a",
            "en": "luggage"
        }
    ]
}

# Day 14: Travel Documents and Expressions
day14_phrases = {
    "Travel Documents": [
        {
            "ar": "جواز سفر",
            "transliteration": "jawaz safar",
            "en": "passport"
        },
        {
            "ar": "تأشيرة",
            "transliteration": "ta'shira",
            "en": "visa"
        },
        {
            "ar": "تذكرة طائرة",
            "transliteration": "tadhkirat ta'ira",
            "en": "airplane ticket"
        },
        {
            "ar": "بطاقة صعود",
            "transliteration": "bitaqat su'ud",
            "en": "boarding pass"
        },
        {
            "ar": "جمارك",
            "transliteration": "jumarik",
            "en": "customs"
        }
    ],
    "Useful Expressions": [
        {
            "ar": "لا أفهم",
            "transliteration": "la afham",
            "en": "I don't understand"
        },
        {
            "ar": "من فضلك أعد ما قلت",
            "transliteration": "min fadlik a'id ma qult",
            "en": "Please say it again"
        },
        {
            "ar": "تكلم ببطء من فضلك",
            "transliteration": "takallam bibot' min fadlik",
            "en": "Please speak more slowly"
        },
        {
            "ar": "هل تتكلم الإنجليزية؟",
            "transliteration": "hal tatakallam al-injliziyya?",
            "en": "Do you speak English?"
        },
        {
            "ar": "شكراً على مساعدتك",
            "transliteration": "shukran 'ala musa'adatik",
            "en": "Thank you for your help"
        },
        {
            "ar": "لا بأس",
            "transliteration": "la ba's",
            "en": "It doesn't matter/It's OK"
        }
    ]
}

# Dictionary mapping day numbers to phrase dictionaries
all_phrases = {
    8: day8_phrases,
    9: day9_phrases,
    10: day10_phrases,
    11: day11_phrases,
    12: day12_phrases,
    13: day13_phrases,
    14: day14_phrases
}

def generate_text_file(day, format_type):
    """Generate a text file with all phrases for a specific day"""
    print(f"Generating Day {day} {format_type} text file...")
    
    phrases_dict = all_phrases[day]
    
    # Ensure the text_files directory exists
    os.makedirs("text_files", exist_ok=True)
    
    with open(f"text_files/day{day}_{format_type}.txt", "w", encoding="utf-8") as f:
        for category, phrase_list in phrases_dict.items():
            f.write(f"\n{category}\n")
            f.write("-" * len(category) + "\n")
            for phrase in phrase_list:
                if format_type == "ar":
                    f.write(f"{phrase['ar']}\n")
                elif format_type == "transliteration":
                    f.write(f"{phrase['transliteration']}\n")
                else:  # English
                    f.write(f"{phrase['en']}\n")
    
    print(f"✓ Saved to text_files/day{day}_{format_type}.txt")

async def generate_audio(day, format_type="ar", voice=None):
    """Generate audio file for a specific day using edge-tts"""
    # Set default voice based on language
    if voice is None:
        voice = "ar-EG-SalmaNeural" if format_type == "ar" else "en-US-JennyNeural"
    
    print(f"\nGenerating Day {day} {format_type} audio file...")
    start_time = time.time()
    
    phrases_dict = all_phrases[day]
    
    # Generate text for phrases
    text = ""
    for category, phrase_list in phrases_dict.items():
        for phrase in phrase_list:
            # Add appropriate punctuation based on language
            if format_type == "ar":
                text += phrase['ar'] + "، "
            else:
                text += phrase['en'] + ". "
    
    # Ensure the audio_files directory exists
    os.makedirs("audio_files", exist_ok=True)
    
    # Configure edge-tts
    communicate = edge_tts.Communicate(text, voice)
    
    # Generate audio
    await communicate.save(f"audio_files/day{day}_{format_type}.mp3")
    
    elapsed = time.time() - start_time
    print(f"✓ Saved to audio_files/day{day}_{format_type}.mp3 ({elapsed:.2f}s)")

async def main():
    parser = argparse.ArgumentParser(description="Generate Arabic and English learning files")
    parser.add_argument("--day", "-d", type=int, choices=[8, 9, 10, 11, 12, 13, 14], default=None,
                        help="Day number to generate (8-14). If not specified, generates all days.")
    parser.add_argument("--text-only", "-t", action="store_true",
                        help="Generate only text files (no audio)")
    parser.add_argument("--voice", "-v", type=str,
                        help="Voice to use for audio generation")
    parser.add_argument("--language", "-l", type=str, choices=["ar", "en", "both"], default="both",
                        help="Language to generate audio for (ar=Arabic, en=English, both=Both languages)")
    args = parser.parse_args()
    
    # Determine which days to process
    days_to_process = [args.day] if args.day else range(8, 15)
    
    # Process each day
    for day in days_to_process:
        print(f"\n=== Processing Day {day} ===")
        
        # Generate text files for Arabic, Transliteration, and English
        generate_text_file(day, "ar")
        generate_text_file(day, "transliteration")
        generate_text_file(day, "en")
        
        # Generate audio files if not text-only mode
        if not args.text_only:
            if args.language in ["ar", "both"]:
                await generate_audio(day, "ar", args.voice)
            if args.language in ["en", "both"]:
                await generate_audio(day, "en", args.voice)
    
    print("\nAll files generated successfully!")
    print("\nUsage examples:")
    print("  - Generate text files only: python arabic_phrases_days_08_14.py --text-only")
    print("  - Generate files for just Day 8: python arabic_phrases_days_08_14.py --day 8")
    print("  - Generate Arabic audio only: python arabic_phrases_days_08_14.py --language ar")
    print("  - Generate English audio only: python arabic_phrases_days_08_14.py --language en")
    print("  - Generate with different voice: python arabic_phrases_days_08_14.py --voice ar-EG-SalmaNeural")
    print("\nAvailable voices:")
    print("Arabic voices:")
    print("  - ar-EG-SalmaNeural (Default female)")
    print("  - ar-EG-ShakirNeural (Male)")
    print("  - ar-SA-ZariyahNeural (Female)")
    print("  - ar-SA-HamedNeural (Male)")
    print("\nEnglish voices:")
    print("  - en-US-JennyNeural (Default female)")
    print("  - en-US-GuyNeural (Male)")
    print("  - en-US-AriaNeural (Female)")
    print("  - en-US-DavisNeural (Male)")

if __name__ == "__main__":
    asyncio.run(main())