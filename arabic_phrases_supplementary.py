import argparse
import os
import time
import asyncio
import edge_tts

# Define supplementary phrases by category

# Education & Academic Life
education_phrases = {
    "School Subjects": [
        {
            "ar": "رياضيات",
            "transliteration": "riyadiyyat",
            "en": "mathematics"
        },
        {
            "ar": "فيزياء",
            "transliteration": "fizya'",
            "en": "physics"
        },
        {
            "ar": "كيمياء",
            "transliteration": "kimya'",
            "en": "chemistry"
        },
        {
            "ar": "أحياء",
            "transliteration": "ahya'",
            "en": "biology"
        },
        {
            "ar": "تاريخ",
            "transliteration": "tarikh",
            "en": "history"
        },
        {
            "ar": "جغرافيا",
            "transliteration": "jughrafya",
            "en": "geography"
        },
        {
            "ar": "أدب",
            "transliteration": "adab",
            "en": "literature"
        }
    ],
    "Classroom Phrases": [
        {
            "ar": "ارفع يدك",
            "transliteration": "irfa' yadak",
            "en": "raise your hand"
        },
        {
            "ar": "لا أفهم",
            "transliteration": "la afham",
            "en": "I don't understand"
        },
        {
            "ar": "هل يمكنك الشرح مرة أخرى؟",
            "transliteration": "hal yumkinuk ash-sharh marra ukhra?",
            "en": "Can you explain again?"
        },
        {
            "ar": "انتهى الدرس",
            "transliteration": "intaha ad-dars",
            "en": "class is over"
        },
        {
            "ar": "امتحان",
            "transliteration": "imtihan",
            "en": "exam"
        }
    ]
}

# Hobbies & Interests
hobbies_phrases = {
    "Sports": [
        {
            "ar": "كرة القدم",
            "transliteration": "kurat al-qadam",
            "en": "football/soccer"
        },
        {
            "ar": "كرة السلة",
            "transliteration": "kurat as-salla",
            "en": "basketball"
        },
        {
            "ar": "سباحة",
            "transliteration": "sibaha",
            "en": "swimming"
        },
        {
            "ar": "كرة المضرب",
            "transliteration": "kurat al-midrab",
            "en": "tennis"
        },
        {
            "ar": "جري",
            "transliteration": "jary",
            "en": "running"
        }
    ],
    "Arts & Entertainment": [
        {
            "ar": "مشاهدة الأفلام",
            "transliteration": "mushahadat al-aflam",
            "en": "watch movies"
        },
        {
            "ar": "الاستماع إلى الموسيقى",
            "transliteration": "al-istima' ila al-musiqa",
            "en": "listen to music"
        },
        {
            "ar": "رسم",
            "transliteration": "rasm",
            "en": "painting"
        },
        {
            "ar": "تصوير",
            "transliteration": "taswir",
            "en": "photography"
        },
        {
            "ar": "عزف البيانو",
            "transliteration": "'azf al-piano",
            "en": "play piano"
        }
    ],
    "Reading & Literature": [
        {
            "ar": "رواية",
            "transliteration": "riwaya",
            "en": "novel"
        },
        {
            "ar": "شعر",
            "transliteration": "shi'r",
            "en": "poetry"
        },
        {
            "ar": "مجلة",
            "transliteration": "majalla",
            "en": "magazine"
        },
        {
            "ar": "قصص مصورة",
            "transliteration": "qisas musawwara",
            "en": "comics"
        },
        {
            "ar": "خيال علمي",
            "transliteration": "khayal 'ilmi",
            "en": "science fiction"
        }
    ]
}

# Emotions & Feelings
emotions_phrases = {
    "Basic Emotions": [
        {
            "ar": "سعيد",
            "transliteration": "sa'id",
            "en": "happy"
        },
        {
            "ar": "حزين",
            "transliteration": "hazin",
            "en": "sad"
        },
        {
            "ar": "غاضب",
            "transliteration": "ghadib",
            "en": "angry"
        },
        {
            "ar": "خائف",
            "transliteration": "kha'if",
            "en": "afraid"
        },
        {
            "ar": "متوتر",
            "transliteration": "mutawattir",
            "en": "nervous"
        },
        {
            "ar": "متحمس",
            "transliteration": "mutahammis",
            "en": "excited"
        }
    ],
    "Complex Feelings": [
        {
            "ar": "محبط",
            "transliteration": "muhbat",
            "en": "disappointed"
        },
        {
            "ar": "فخور",
            "transliteration": "fakhur",
            "en": "proud"
        },
        {
            "ar": "متأثر",
            "transliteration": "muta'aththir",
            "en": "moved/touched"
        },
        {
            "ar": "محتار",
            "transliteration": "muhtar",
            "en": "confused"
        },
        {
            "ar": "قلق",
            "transliteration": "qaliq",
            "en": "worried"
        }
    ],
    "Expressing Feelings": [
        {
            "ar": "أشعر بـ...",
            "transliteration": "ash'ur bi...",
            "en": "I feel..."
        },
        {
            "ar": "يجعلني سعيداً",
            "transliteration": "yaj'aluni sa'idan",
            "en": "makes me happy"
        },
        {
            "ar": "أنا قليلاً...",
            "transliteration": "ana qalilan...",
            "en": "I'm a bit..."
        },
        {
            "ar": "مزاجي سيء",
            "transliteration": "mizaji sayyi'",
            "en": "in a bad mood"
        }
    ]
}

# Weather & Daily Life
daily_life_phrases = {
    "Weather Conditions": [
        {
            "ar": "مشمس",
            "transliteration": "mushmis",
            "en": "sunny"
        },
        {
            "ar": "ممطر",
            "transliteration": "mumtir",
            "en": "rainy"
        },
        {
            "ar": "غائم",
            "transliteration": "gha'im",
            "en": "cloudy"
        },
        {
            "ar": "عاصف",
            "transliteration": "'asif",
            "en": "windy"
        },
        {
            "ar": "حار",
            "transliteration": "harr",
            "en": "hot"
        },
        {
            "ar": "رطب",
            "transliteration": "ratib",
            "en": "humid"
        }
    ],
    "Daily Routines": [
        {
            "ar": "الاستيقاظ",
            "transliteration": "al-istiqadh",
            "en": "wake up"
        },
        {
            "ar": "تنظيف الأسنان",
            "transliteration": "tandhif al-asnan",
            "en": "brush teeth"
        },
        {
            "ar": "الاستحمام",
            "transliteration": "al-istihman",
            "en": "take a shower"
        },
        {
            "ar": "تناول الفطور",
            "transliteration": "tanawul al-futur",
            "en": "eat breakfast"
        },
        {
            "ar": "الذهاب إلى العمل",
            "transliteration": "adh-dhahab ila al-'amal",
            "en": "go to work"
        },
        {
            "ar": "العودة من العمل",
            "transliteration": "al-'awda min al-'amal",
            "en": "return from work"
        }
    ],
    "Shopping Types": [
        {
            "ar": "محل ملابس",
            "transliteration": "mahall malabis",
            "en": "clothing store"
        },
        {
            "ar": "مكتبة",
            "transliteration": "maktaba",
            "en": "bookstore"
        },
        {
            "ar": "صيدلية",
            "transliteration": "saydaliyya",
            "en": "pharmacy"
        },
        {
            "ar": "مخبز",
            "transliteration": "makhbaz",
            "en": "bakery"
        },
        {
            "ar": "محل فواكه",
            "transliteration": "mahall fawakih",
            "en": "fruit store"
        }
    ]
}

# Comparison Structures
comparison_phrases = {
    "Basic Comparisons": [
        {
            "ar": "أكثر من",
            "transliteration": "akthar min",
            "en": "more than"
        },
        {
            "ar": "ليس مثل",
            "transliteration": "laysa mithl",
            "en": "not like"
        },
        {
            "ar": "مثل",
            "transliteration": "mithl",
            "en": "same as"
        },
        {
            "ar": "الأكثر",
            "transliteration": "al-akthar",
            "en": "the most"
        }
    ],
    "Example Sentences": [
        {
            "ar": "هذا أغلى من ذاك",
            "transliteration": "hadha aghla min dhak",
            "en": "this is more expensive than that"
        },
        {
            "ar": "اليوم ليس حاراً مثل الأمس",
            "transliteration": "al-yawm laysa harran mithl al-ams",
            "en": "today is not as hot as yesterday"
        },
        {
            "ar": "الاثنان جيدان بنفس القدر",
            "transliteration": "al-ithnan jayyidan binafs al-qadr",
            "en": "both are equally good"
        },
        {
            "ar": "هذا هو الخيار الأفضل",
            "transliteration": "hadha huwa al-khiyar al-afdal",
            "en": "this is the best choice"
        }
    ]
}

# Dictionary mapping categories to phrase dictionaries
supplementary_phrases = {
    "education": education_phrases,
    "hobbies": hobbies_phrases,
    "emotions": emotions_phrases,
    "daily_life": daily_life_phrases,
    "comparisons": comparison_phrases
}

def generate_text_file(category, format_type):
    """Generate a text file with all phrases for a specific category"""
    print(f"Generating {category} {format_type} text file...")
    
    phrases_dict = supplementary_phrases[category]
    
    # Ensure the text_files directory exists
    os.makedirs("text_files/supplementary", exist_ok=True)
    
    with open(f"text_files/supplementary/{category}_{format_type}.txt", "w", encoding="utf-8") as f:
        for subcategory, phrase_list in phrases_dict.items():
            f.write(f"\n{subcategory}\n")
            f.write("-" * len(subcategory) + "\n")
            for phrase in phrase_list:
                if format_type in phrase:
                    f.write(f"{phrase[format_type]}\n")
    
    print(f"✓ Saved to text_files/supplementary/{category}_{format_type}.txt")

async def generate_audio(category, format_type="ar", voice=None):
    """Generate audio file for a specific category using edge-tts"""
    # Set default voice based on language
    if voice is None:
        voice = "ar-SA-ZariyahNeural"  # Default Arabic voice
    
    print(f"\nGenerating {category} {format_type} audio file...")
    start_time = time.time()
    
    phrases_dict = supplementary_phrases[category]
    
    # Generate text for phrases
    text = ""
    for subcategory, phrase_list in phrases_dict.items():
        for phrase in phrase_list:
            # Add appropriate punctuation based on language
            if format_type == "ar":
                text += phrase['ar'] + "."
            else:
                text += phrase['en'] + ". "
    
    # Ensure the audio_files directory exists
    os.makedirs("audio_files/supplementary", exist_ok=True)
    
    # Configure edge-tts
    communicate = edge_tts.Communicate(text, voice)
    
    # Generate audio
    await communicate.save(f"audio_files/supplementary/{category}_{format_type}.mp3")
    
    elapsed = time.time() - start_time
    print(f"✓ Saved to audio_files/supplementary/{category}_{format_type}.mp3 ({elapsed:.2f}s)")

async def main():
    parser = argparse.ArgumentParser(description="Generate supplementary Arabic and English learning files")
    parser.add_argument("--category", "-c", type=str, 
                        choices=["education", "hobbies", "emotions", "daily_life", "comparisons"],
                        default=None,
                        help="Category to generate. If not specified, generates all categories.")
    parser.add_argument("--text-only", "-t", action="store_true", 
                        help="Generate only text files (no audio)")
    parser.add_argument("--voice", "-v", type=str,
                        help="Voice to use for audio generation")
    parser.add_argument("--language", "-l", type=str, choices=["ar", "en", "both"], default="both",
                        help="Language to generate audio for (ar=Arabic, en=English, both=Both languages)")
    args = parser.parse_args()
    
    # Determine which categories to process
    categories_to_process = [args.category] if args.category else supplementary_phrases.keys()
    
    # Process each category
    for category in categories_to_process:
        print(f"\n=== Processing {category} ===")
        
        # Generate text files for Arabic, transliteration, and English
        generate_text_file(category, "ar")
        generate_text_file(category, "transliteration")
        generate_text_file(category, "en")
        
        # Generate audio files if not text-only mode
        if not args.text_only:
            if args.language in ["ar", "both"]:
                await generate_audio(category, "ar", args.voice)
            if args.language in ["en", "both"]:
                await generate_audio(category, "en", args.voice)
    
    print("\nAll supplementary files generated successfully!")
    print("\nUsage examples:")
    print("  - Generate text files only: python arabic_phrases_supplementary.py --text-only")
    print("  - Generate files for just education: python arabic_phrases_supplementary.py --category education")
    print("  - Generate Arabic audio only: python arabic_phrases_supplementary.py --language ar")
    print("  - Generate English audio only: python arabic_phrases_supplementary.py --language en")
    print("  - Generate with different voice: python arabic_phrases_supplementary.py --voice ar-SA-ZariyahNeural")
    print("\nAvailable voices:")
    print("Arabic voices:")
    print("  - ar-SA-ZariyahNeural (Default female)")
    print("  - ar-SA-HamedNeural (Male)")
    print("\nEnglish voices:")
    print("  - en-US-JennyNeural (Default female)")
    print("  - en-US-GuyNeural (Male)")
    print("  - en-US-AriaNeural (Female)")
    print("  - en-US-DavisNeural (Male)")

if __name__ == "__main__":
    asyncio.run(main())