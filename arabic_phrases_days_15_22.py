import argparse
import os
import time
import asyncio
import edge_tts

# Define phrases by day and category

# Day 15: Family Members
day15_phrases = {
    "Immediate Family": [
        {
            "ar": "أب",
            "transliteration": "ab",
            "en": "father"
        },
        {
            "ar": "أم",
            "transliteration": "umm",
            "en": "mother"
        },
        {
            "ar": "أخ كبير",
            "transliteration": "akh kabir",
            "en": "older brother"
        },
        {
            "ar": "أخت كبيرة",
            "transliteration": "ukht kabira",
            "en": "older sister"
        },
        {
            "ar": "أخ صغير",
            "transliteration": "akh saghir",
            "en": "younger brother"
        },
        {
            "ar": "أخت صغيرة",
            "transliteration": "ukht saghira",
            "en": "younger sister"
        },
        {
            "ar": "ابن",
            "transliteration": "ibn",
            "en": "son"
        },
        {
            "ar": "بنت",
            "transliteration": "bint",
            "en": "daughter"
        }
    ],
    "Extended Family": [
        {
            "ar": "جد",
            "transliteration": "jadd",
            "en": "grandfather"
        },
        {
            "ar": "جدة",
            "transliteration": "jadda",
            "en": "grandmother"
        },
        {
            "ar": "عم",
            "transliteration": "'amm",
            "en": "paternal uncle"
        },
        {
            "ar": "عمة",
            "transliteration": "'amma",
            "en": "paternal aunt"
        },
        {
            "ar": "خال",
            "transliteration": "khal",
            "en": "maternal uncle"
        },
        {
            "ar": "خالة",
            "transliteration": "khala",
            "en": "maternal aunt"
        },
        {
            "ar": "ابن العم",
            "transliteration": "ibn al-'amm",
            "en": "paternal cousin (male)"
        },
        {
            "ar": "ابن الخال",
            "transliteration": "ibn al-khal",
            "en": "maternal cousin (male)"
        }
    ]
}

# Day 16: Social Interactions
day16_phrases = {
    "Greetings and Farewells": [
        {
            "ar": "كيف حالك هذه الأيام؟",
            "transliteration": "kayfa haluk hadhihi al-ayyam?",
            "en": "How have you been lately?"
        },
        {
            "ar": "لم أرك منذ زمن",
            "transliteration": "lam arak mundhu zaman",
            "en": "Long time no see"
        },
        {
            "ar": "سعيد بلقائك",
            "transliteration": "sa'id biliqa'ik",
            "en": "Nice to meet you"
        },
        {
            "ar": "إلى اللقاء",
            "transliteration": "ila al-liqa'",
            "en": "See you later"
        },
        {
            "ar": "اعتني بنفسك",
            "transliteration": "i'tani binafsik",
            "en": "Take care"
        }
    ],
    "Social Phrases": [
        {
            "ar": "عذراً على الإزعاج",
            "transliteration": "'udhran 'ala al-iz'aj",
            "en": "Excuse me/Sorry to bother you"
        },
        {
            "ar": "لا مشكلة",
            "transliteration": "la mushkila",
            "en": "It's okay/No problem"
        },
        {
            "ar": "بالتوفيق",
            "transliteration": "bit-tawfiq",
            "en": "Good luck to you"
        },
        {
            "ar": "في صحتك",
            "transliteration": "fi sihhatik",
            "en": "Cheers (when drinking)"
        },
        {
            "ar": "كما تريد",
            "transliteration": "kama turid",
            "en": "Whatever/It doesn't matter"
        }
    ]
}

# Day 17: Arabic Etiquette
day17_phrases = {
    "Polite Expressions": [
        {
            "ar": "من فضلك",
            "transliteration": "min fadlik",
            "en": "please"
        },
        {
            "ar": "شكراً",
            "transliteration": "shukran",
            "en": "thank you"
        },
        {
            "ar": "عفواً",
            "transliteration": "'afwan",
            "en": "you're welcome"
        },
        {
            "ar": "آسف",
            "transliteration": "asif",
            "en": "sorry"
        },
        {
            "ar": "لا بأس",
            "transliteration": "la ba's",
            "en": "it's okay"
        }
    ],
    "Cultural Etiquette": [
        {
            "ar": "على حسب عادات البلد",
            "transliteration": "'ala hasab 'adat al-balad",
            "en": "According to the country's customs"
        },
        {
            "ar": "تقديم القهوة",
            "transliteration": "taqdim al-qahwa",
            "en": "serving coffee (as a sign of hospitality)"
        },
        {
            "ar": "تقديم الهدايا",
            "transliteration": "taqdim al-hadaya",
            "en": "giving gifts"
        },
        {
            "ar": "احترام الكبير والعطف على الصغير",
            "transliteration": "ihtiram al-kabir wal-'atf 'ala al-saghir",
            "en": "respect the elderly and care for the young"
        },
        {
            "ar": "التواضع",
            "transliteration": "at-tawadu'",
            "en": "modesty/humility"
        }
    ]
}

# Day 18: Islamic and Arabic Festivals
day18_phrases = {
    "Major Festivals": [
        {
            "ar": "عيد الفطر",
            "transliteration": "'Eid al-Fitr",
            "en": "Eid al-Fitr"
        },
        {
            "ar": "عيد الأضحى",
            "transliteration": "'Eid al-Adha",
            "en": "Eid al-Adha"
        },
        {
            "ar": "رمضان",
            "transliteration": "Ramadan",
            "en": "Ramadan"
        },
        {
            "ar": "المولد النبوي",
            "transliteration": "Al-Mawlid an-Nabawi",
            "en": "Prophet's Birthday"
        },
        {
            "ar": "رأس السنة الهجرية",
            "transliteration": "Ra's as-Sana al-Hijriyya",
            "en": "Islamic New Year"
        }
    ],
    "Festival Traditions": [
        {
            "ar": "العيدية",
            "transliteration": "al-'idiyya",
            "en": "Eid money gift"
        },
        {
            "ar": "كعك العيد",
            "transliteration": "ka'k al-'id",
            "en": "Eid cookies"
        },
        {
            "ar": "صلاة العيد",
            "transliteration": "salat al-'id",
            "en": "Eid prayer"
        },
        {
            "ar": "إفطار رمضان",
            "transliteration": "iftar ramadan",
            "en": "Ramadan breakfast"
        },
        {
            "ar": "زكاة الفطر",
            "transliteration": "zakat al-fitr",
            "en": "Charity given before Eid al-Fitr"
        },
        {
            "ar": "تكبيرات العيد",
            "transliteration": "takbirat al-'id",
            "en": "Eid takbeer"
        }
    ]
}

# Day 19: Home and Living
day19_phrases = {
    "Rooms and Areas": [
        {
            "ar": "غرفة الجلوس",
            "transliteration": "ghurfat al-julus",
            "en": "living room"
        },
        {
            "ar": "غرفة النوم",
            "transliteration": "ghurfat an-nawm",
            "en": "bedroom"
        },
        {
            "ar": "مطبخ",
            "transliteration": "matbakh",
            "en": "kitchen"
        },
        {
            "ar": "حمام",
            "transliteration": "hammam",
            "en": "bathroom"
        },
        {
            "ar": "شرفة",
            "transliteration": "shurfa",
            "en": "balcony"
        },
        {
            "ar": "حديقة",
            "transliteration": "hadiqa",
            "en": "garden"
        }
    ],
    "Household Items": [
        {
            "ar": "طاولة",
            "transliteration": "tawila",
            "en": "table"
        },
        {
            "ar": "كرسي",
            "transliteration": "kursi",
            "en": "chair"
        },
        {
            "ar": "سرير",
            "transliteration": "sarir",
            "en": "bed"
        },
        {
            "ar": "أريكة",
            "transliteration": "arika",
            "en": "sofa"
        },
        {
            "ar": "تلفاز",
            "transliteration": "tilfaz",
            "en": "television"
        },
        {
            "ar": "ثلاجة",
            "transliteration": "thallaja",
            "en": "refrigerator"
        },
        {
            "ar": "مكيف",
            "transliteration": "mukayyif",
            "en": "air conditioner"
        }
    ]
}

# Day 20: Public Places
day20_phrases = {
    "Common Places": [
        {
            "ar": "مستشفى",
            "transliteration": "mustashfa",
            "en": "hospital"
        },
        {
            "ar": "مدرسة",
            "transliteration": "madrasa",
            "en": "school"
        },
        {
            "ar": "مكتبة",
            "transliteration": "maktaba",
            "en": "library"
        },
        {
            "ar": "حديقة عامة",
            "transliteration": "hadiqa 'amma",
            "en": "park"
        },
        {
            "ar": "بنك",
            "transliteration": "bank",
            "en": "bank"
        },
        {
            "ar": "مكتب البريد",
            "transliteration": "maktab al-barid",
            "en": "post office"
        },
        {
            "ar": "مطعم",
            "transliteration": "mat'am",
            "en": "restaurant"
        }
    ],
    "Public Communication": [
        {
            "ar": "هل يمكنني التقاط الصور هنا؟",
            "transliteration": "hal yumkinuni iltiqat as-suwar huna?",
            "en": "Can I take photos here?"
        },
        {
            "ar": "أين الحمام من فضلك؟",
            "transliteration": "ayna al-hammam min fadlik?",
            "en": "Where is the restroom?"
        },
        {
            "ar": "هل يوجد واي فاي هنا؟",
            "transliteration": "hal yujad wifi huna?",
            "en": "Is there WiFi here?"
        },
        {
            "ar": "ما هي ساعات العمل؟",
            "transliteration": "ma hiya sa'at al-'amal?",
            "en": "What are the business hours?"
        },
        {
            "ar": "أحتاج مساعدة",
            "transliteration": "ahtaj musa'ada",
            "en": "I need help"
        }
    ]
}

# Day 21: Arabic and Islamic Traditions
day21_phrases = {
    "Cultural Concepts": [
        {
            "ar": "الكرامة",
            "transliteration": "al-karama",
            "en": "dignity/honor"
        },
        {
            "ar": "الضيافة",
            "transliteration": "ad-diyafa",
            "en": "hospitality"
        },
        {
            "ar": "بر الوالدين",
            "transliteration": "birr al-walidayn",
            "en": "filial piety"
        },
        {
            "ar": "التسامح",
            "transliteration": "at-tasamuh",
            "en": "tolerance"
        },
        {
            "ar": "الوسطية",
            "transliteration": "al-wasatiyya",
            "en": "moderation"
        }
    ],
    "Traditional Arts": [
        {
            "ar": "الخط العربي",
            "transliteration": "al-khat al-'arabi",
            "en": "Arabic calligraphy"
        },
        {
            "ar": "الزخرفة الإسلامية",
            "transliteration": "az-zakhrafa al-islamiyya",
            "en": "Islamic decoration"
        },
        {
            "ar": "الموسيقى العربية",
            "transliteration": "al-musiqa al-'arabiyya",
            "en": "Arabic music"
        },
        {
            "ar": "الشعر العربي",
            "transliteration": "ash-shi'r al-'arabi",
            "en": "Arabic poetry"
        },
        {
            "ar": "النقش",
            "transliteration": "an-naqsh",
            "en": "engraving"
        },
        {
            "ar": "الطب العربي",
            "transliteration": "at-tibb al-'arabi",
            "en": "traditional Arabic medicine"
        }
    ]
}

# Day 22: Everyday Communication
day22_phrases = {
    "Daily Expressions": [
        {
            "ar": "صباح الخير",
            "transliteration": "sabah al-khayr",
            "en": "good morning"
        },
        {
            "ar": "تصبح على خير",
            "transliteration": "tusbih 'ala khayr",
            "en": "good night"
        },
        {
            "ar": "ما شاء الله",
            "transliteration": "ma sha' Allah",
            "en": "expression of appreciation"
        },
        {
            "ar": "في أمان الله",
            "transliteration": "fi aman Allah",
            "en": "goodbye (May God protect you)"
        },
        {
            "ar": "الحمد لله",
            "transliteration": "al-hamdu lillah",
            "en": "praise be to God"
        }
    ],
    "Common Phrases": [
        {
            "ar": "إن شاء الله",
            "transliteration": "in sha' Allah",
            "en": "God willing"
        },
        {
            "ar": "بارك الله فيك",
            "transliteration": "barak Allahu fik",
            "en": "may God bless you"
        },
        {
            "ar": "جزاك الله خيراً",
            "transliteration": "jazak Allahu khayran",
            "en": "may God reward you"
        },
        {
            "ar": "السلام عليكم",
            "transliteration": "as-salamu 'alaykum",
            "en": "peace be upon you"
        },
        {
            "ar": "وعليكم السلام",
            "transliteration": "wa 'alaykum as-salam",
            "en": "and peace be upon you too"
        }
    ]
}

# Dictionary mapping day numbers to phrase dictionaries
all_phrases = {
    15: day15_phrases,
    16: day16_phrases,
    17: day17_phrases,
    18: day18_phrases,
    19: day19_phrases,
    20: day20_phrases,
    21: day21_phrases,
    22: day22_phrases
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
    parser.add_argument("--day", "-d", type=int, choices=[15, 16, 17, 18, 19, 20, 21, 22], default=None,
                        help="Day number to generate (15-22). If not specified, generates all days.")
    parser.add_argument("--text-only", "-t", action="store_true",
                        help="Generate only text files (no audio)")
    parser.add_argument("--voice", "-v", type=str,
                        help="Voice to use for audio generation")
    parser.add_argument("--language", "-l", type=str, choices=["ar", "en", "both"], default="both",
                        help="Language to generate audio for (ar=Arabic, en=English, both=Both languages)")
    args = parser.parse_args()
    
    # Determine which days to process
    days_to_process = [args.day] if args.day else range(15, 23)
    
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
    print("  - Generate text files only: python arabic_phrases_days_15_22.py --text-only")
    print("  - Generate files for just Day 15: python arabic_phrases_days_15_22.py --day 15")
    print("  - Generate Arabic audio only: python arabic_phrases_days_15_22.py --language ar")
    print("  - Generate English audio only: python arabic_phrases_days_15_22.py --language en")
    print("  - Generate with different voice: python arabic_phrases_days_15_22.py --voice ar-EG-SalmaNeural")
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