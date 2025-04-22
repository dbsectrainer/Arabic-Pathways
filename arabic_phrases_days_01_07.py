import argparse
import os
import time
import asyncio
import edge_tts

# Define phrases by day and category

# Day 1: Basic Greetings & Common Phrases
day1_phrases = {
    "Basic Greetings & Common Phrases": [
        {
            "ar": "مرحبا",
            "transliteration": "Marhaba",
            "en": "Hello"
        },
        {
            "ar": "صباح الخير",
            "transliteration": "Sabah al-khayr",
            "en": "Good morning"
        },
        {
            "ar": "مساء الخير",
            "transliteration": "Masa' al-khayr",
            "en": "Good evening"
        },
        {
            "ar": "مع السلامة",
            "transliteration": "Ma'a as-salama",
            "en": "Goodbye"
        },
        {
            "ar": "شكرا",
            "transliteration": "Shukran",
            "en": "Thank you"
        }
    ],
    "Self Introduction": [
        {
            "ar": "اسمي...",
            "transliteration": "Ismi...",
            "en": "My name is..."
        },
        {
            "ar": "تشرفت بمعرفتك",
            "transliteration": "Tasharraftu bima'rifatik",
            "en": "Nice to meet you"
        },
        {
            "ar": "أنا أمريكي",
            "transliteration": "Ana amriki",
            "en": "I am American"
        },
        {
            "ar": "وأنت؟",
            "transliteration": "Wa anta?",
            "en": "And you?"
        }
    ],
    "Basic Questions": [
        {
            "ar": "كيف حالك؟",
            "transliteration": "Kayfa haluk?",
            "en": "How are you?"
        },
        {
            "ar": "من أي بلد أنت؟",
            "transliteration": "Min ayyi balad anta?",
            "en": "What is your nationality?"
        },
        {
            "ar": "هل تتكلم الإنجليزية؟",
            "transliteration": "Hal tatakallam al-injliziyya?",
            "en": "Do you speak English?"
        },
        {
            "ar": "هل تفهم العربية؟",
            "transliteration": "Hal tafham al-arabiyya?",
            "en": "Do you understand Arabic?"
        }
    ]
}

# Day 2: Numbers and Counting
day2_phrases = {
    "Numbers 0-10": [
        {
            "ar": "صفر",
            "transliteration": "sifr",
            "en": "zero"
        },
        {
            "ar": "واحد",
            "transliteration": "wahid",
            "en": "one"
        },
        {
            "ar": "اثنان",
            "transliteration": "ithnan",
            "en": "two"
        },
        {
            "ar": "ثلاثة",
            "transliteration": "thalatha",
            "en": "three"
        },
        {
            "ar": "أربعة",
            "transliteration": "arba'a",
            "en": "four"
        },
        {
            "ar": "خمسة",
            "transliteration": "khamsa",
            "en": "five"
        },
        {
            "ar": "ستة",
            "transliteration": "sitta",
            "en": "six"
        },
        {
            "ar": "سبعة",
            "transliteration": "sab'a",
            "en": "seven"
        },
        {
            "ar": "ثمانية",
            "transliteration": "thamaniya",
            "en": "eight"
        },
        {
            "ar": "تسعة",
            "transliteration": "tis'a",
            "en": "nine"
        },
        {
            "ar": "عشرة",
            "transliteration": "ashara",
            "en": "ten"
        }
    ],
    "Basic Counting Phrases": [
        {
            "ar": "كم؟",
            "transliteration": "kam?",
            "en": "How many/much?"
        },
        {
            "ar": "المجموع",
            "transliteration": "al-majmu'",
            "en": "in total"
        },
        {
            "ar": "الأول",
            "transliteration": "al-awwal",
            "en": "first"
        },
        {
            "ar": "الثاني",
            "transliteration": "al-thani",
            "en": "second"
        }
    ]
}

# Day 3: Time Expressions
day3_phrases = {
    "Time Words": [
        {
            "ar": "الآن",
            "transliteration": "al-an",
            "en": "now"
        },
        {
            "ar": "اليوم",
            "transliteration": "al-yawm",
            "en": "today"
        },
        {
            "ar": "غدا",
            "transliteration": "ghadan",
            "en": "tomorrow"
        },
        {
            "ar": "أمس",
            "transliteration": "ams",
            "en": "yesterday"
        },
        {
            "ar": "صباحا",
            "transliteration": "sabahan",
            "en": "morning"
        },
        {
            "ar": "مساء",
            "transliteration": "masa'an",
            "en": "evening"
        },
        {
            "ar": "ليلا",
            "transliteration": "laylan",
            "en": "night"
        }
    ],
    "Asking Time": [
        {
            "ar": "كم الساعة؟",
            "transliteration": "kam as-sa'a?",
            "en": "What time is it?"
        },
        {
            "ar": "الساعة الثالثة الآن",
            "transliteration": "as-sa'a al-thalitha al-an",
            "en": "It's 3 o'clock now"
        },
        {
            "ar": "متى؟",
            "transliteration": "mata?",
            "en": "When?"
        },
        {
            "ar": "أي يوم من الأسبوع؟",
            "transliteration": "ayyu yawm min al-usbu'?",
            "en": "What day of the week?"
        }
    ]
}

# Day 4: Basic Verbs and Actions
day4_phrases = {
    "Common Verbs": [
        {
            "ar": "يكون",
            "transliteration": "yakun",
            "en": "to be"
        },
        {
            "ar": "يملك",
            "transliteration": "yamlik",
            "en": "to have"
        },
        {
            "ar": "يريد",
            "transliteration": "yurid",
            "en": "to want"
        },
        {
            "ar": "يذهب",
            "transliteration": "yadhhab",
            "en": "to go"
        },
        {
            "ar": "يأتي",
            "transliteration": "ya'ti",
            "en": "to come"
        },
        {
            "ar": "يأكل",
            "transliteration": "ya'kul",
            "en": "to eat"
        },
        {
            "ar": "يشرب",
            "transliteration": "yashrab",
            "en": "to drink"
        },
        {
            "ar": "يتكلم",
            "transliteration": "yatakallam",
            "en": "to speak/to say"
        }
    ],
    "Simple Sentences": [
        {
            "ar": "أريد أن أذهب هناك",
            "transliteration": "urid an adhhab hunak",
            "en": "I want to go there"
        },
        {
            "ar": "هل لديك وقت؟",
            "transliteration": "hal ladayka waqt?",
            "en": "Do you have time?"
        },
        {
            "ar": "هيا نذهب لتناول الطعام",
            "transliteration": "hayya nadhhab litanawul at-ta'am",
            "en": "Let's go eat"
        },
        {
            "ar": "لا أعرف",
            "transliteration": "la a'rif",
            "en": "I don't know"
        }
    ]
}

# Day 5: Basic Adjectives
day5_phrases = {
    "Common Adjectives": [
        {
            "ar": "جيد",
            "transliteration": "jayyid",
            "en": "good"
        },
        {
            "ar": "سيء",
            "transliteration": "sayyi'",
            "en": "bad"
        },
        {
            "ar": "كبير",
            "transliteration": "kabir",
            "en": "big"
        },
        {
            "ar": "صغير",
            "transliteration": "saghir",
            "en": "small"
        },
        {
            "ar": "كثير",
            "transliteration": "kathir",
            "en": "many/much"
        },
        {
            "ar": "قليل",
            "transliteration": "qalil",
            "en": "few/little"
        },
        {
            "ar": "حار",
            "transliteration": "harr",
            "en": "hot"
        },
        {
            "ar": "بارد",
            "transliteration": "barid",
            "en": "cold"
        },
        {
            "ar": "جديد",
            "transliteration": "jadid",
            "en": "new"
        },
        {
            "ar": "قديم",
            "transliteration": "qadim",
            "en": "old (for objects)"
        }
    ],
    "Descriptive Phrases": [
        {
            "ar": "جيد جدا",
            "transliteration": "jayyid jiddan",
            "en": "very good"
        },
        {
            "ar": "غالي جدا",
            "transliteration": "ghali jiddan",
            "en": "too expensive"
        },
        {
            "ar": "جميل جدا",
            "transliteration": "jamil jiddan",
            "en": "very beautiful"
        },
        {
            "ar": "ليس بعيدا جدا",
            "transliteration": "laysa ba'idan jiddan",
            "en": "not too far"
        }
    ]
}

# Day 6: Question Words
day6_phrases = {
    "Question Words": [
        {
            "ar": "ماذا",
            "transliteration": "madha",
            "en": "what"
        },
        {
            "ar": "من",
            "transliteration": "man",
            "en": "who"
        },
        {
            "ar": "أين",
            "transliteration": "ayna",
            "en": "where"
        },
        {
            "ar": "لماذا",
            "transliteration": "limadha",
            "en": "why"
        },
        {
            "ar": "كيف",
            "transliteration": "kayfa",
            "en": "how"
        },
        {
            "ar": "كم",
            "transliteration": "kam",
            "en": "how many/how much"
        }
    ],
    "Common Questions": [
        {
            "ar": "ما هذا؟",
            "transliteration": "ma hadha?",
            "en": "What is this?"
        },
        {
            "ar": "من هذا؟",
            "transliteration": "man hadha?",
            "en": "Who is that?"
        },
        {
            "ar": "ما اسمك؟",
            "transliteration": "ma ismuk?",
            "en": "What is your name?"
        },
        {
            "ar": "كم سعر هذا؟",
            "transliteration": "kam si'r hadha?",
            "en": "How much is this?"
        },
        {
            "ar": "أين الحمام؟",
            "transliteration": "ayna al-hammam?",
            "en": "Where is the bathroom?"
        }
    ]
}

# Day 7: Arabic Alphabet and Pronunciation
day7_phrases = {
    "Arabic Alphabet (Part 1)": [
        {
            "ar": "ا",
            "transliteration": "alif",
            "en": "first letter of the alphabet"
        },
        {
            "ar": "ب",
            "transliteration": "ba",
            "en": "b sound"
        },
        {
            "ar": "ت",
            "transliteration": "ta",
            "en": "t sound"
        },
        {
            "ar": "ث",
            "transliteration": "tha",
            "en": "th sound (as in 'think')"
        },
        {
            "ar": "ج",
            "transliteration": "jim",
            "en": "j sound"
        },
        {
            "ar": "ح",
            "transliteration": "ha",
            "en": "heavy h sound"
        },
        {
            "ar": "خ",
            "transliteration": "kha",
            "en": "kh sound (like Scottish 'loch')"
        }
    ],
    "Arabic Alphabet (Part 2)": [
        {
            "ar": "د",
            "transliteration": "dal",
            "en": "d sound"
        },
        {
            "ar": "ذ",
            "transliteration": "dhal",
            "en": "th sound (as in 'this')"
        },
        {
            "ar": "ر",
            "transliteration": "ra",
            "en": "r sound (rolled)"
        },
        {
            "ar": "ز",
            "transliteration": "zay",
            "en": "z sound"
        },
        {
            "ar": "س",
            "transliteration": "sin",
            "en": "s sound"
        },
        {
            "ar": "ش",
            "transliteration": "shin",
            "en": "sh sound"
        },
        {
            "ar": "ص",
            "transliteration": "sad",
            "en": "emphatic s sound"
        }
    ],
    "Arabic Alphabet (Part 3)": [
        {
            "ar": "ض",
            "transliteration": "dad",
            "en": "emphatic d sound"
        },
        {
            "ar": "ط",
            "transliteration": "ta",
            "en": "emphatic t sound"
        },
        {
            "ar": "ظ",
            "transliteration": "dha",
            "en": "emphatic th sound"
        },
        {
            "ar": "ع",
            "transliteration": "ayn",
            "en": "voiced pharyngeal sound"
        },
        {
            "ar": "غ",
            "transliteration": "ghayn",
            "en": "gh sound (like French r)"
        },
        {
            "ar": "ف",
            "transliteration": "fa",
            "en": "f sound"
        },
        {
            "ar": "ق",
            "transliteration": "qaf",
            "en": "deep k sound"
        }
    ],
    "Arabic Alphabet (Part 4)": [
        {
            "ar": "ك",
            "transliteration": "kaf",
            "en": "k sound"
        },
        {
            "ar": "ل",
            "transliteration": "lam",
            "en": "l sound"
        },
        {
            "ar": "م",
            "transliteration": "mim",
            "en": "m sound"
        },
        {
            "ar": "ن",
            "transliteration": "nun",
            "en": "n sound"
        },
        {
            "ar": "ه",
            "transliteration": "ha",
            "en": "h sound"
        },
        {
            "ar": "و",
            "transliteration": "waw",
            "en": "w sound"
        },
        {
            "ar": "ي",
            "transliteration": "ya",
            "en": "y sound"
        }
    ]
}

# Dictionary mapping day numbers to phrase dictionaries
all_phrases = {
    1: day1_phrases,
    2: day2_phrases,
    3: day3_phrases,
    4: day4_phrases,
    5: day5_phrases,
    6: day6_phrases,
    7: day7_phrases
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
    parser.add_argument("--day", "-d", type=int, choices=[1, 2, 3, 4, 5, 6, 7], default=None,
                        help="Day number to generate (1-7). If not specified, generates all days.")
    parser.add_argument("--text-only", "-t", action="store_true", 
                        help="Generate only text files (no audio)")
    parser.add_argument("--voice", "-v", type=str,
                        help="Voice to use for audio generation")
    parser.add_argument("--language", "-l", type=str, choices=["ar", "en", "both"], default="both",
                        help="Language to generate audio for (ar=Arabic, en=English, both=Both languages)")
    args = parser.parse_args()
    
    # Determine which days to process
    days_to_process = [args.day] if args.day else [1, 2, 3, 4, 5, 6, 7]
    
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
    print("  - Generate text files only: python arabic_phrases_days_01_07.py --text-only")
    print("  - Generate files for just Day 1: python arabic_phrases_days_01_07.py --day 1")
    print("  - Generate Arabic audio only: python arabic_phrases_days_01_07.py --language ar")
    print("  - Generate English audio only: python arabic_phrases_days_01_07.py --language en")
    print("  - Generate with different voice: python arabic_phrases_days_01_07.py --voice en-US-JennyNeural")
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
