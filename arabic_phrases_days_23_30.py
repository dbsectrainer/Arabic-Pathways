import argparse
import os
import time
import asyncio
import edge_tts

# Define phrases by day and category

# Day 23: Workplace Vocabulary
day23_phrases = {
    "Job Titles": [
        {
            "ar": "مدير",
            "transliteration": "mudir",
            "en": "manager"
        },
        {
            "ar": "رئيس",
            "transliteration": "ra'is",
            "en": "boss"
        },
        {
            "ar": "زميل",
            "transliteration": "zamil",
            "en": "colleague"
        },
        {
            "ar": "سكرتير",
            "transliteration": "sikritir",
            "en": "secretary"
        },
        {
            "ar": "مهندس",
            "transliteration": "muhandis",
            "en": "engineer"
        },
        {
            "ar": "مندوب مبيعات",
            "transliteration": "mandub mabi'at",
            "en": "sales representative"
        },
        {
            "ar": "الموارد البشرية",
            "transliteration": "al-mawarid al-bashariyya",
            "en": "human resources"
        }
    ],
    "Office Items": [
        {
            "ar": "حاسوب",
            "transliteration": "hasub",
            "en": "computer"
        },
        {
            "ar": "طابعة",
            "transliteration": "tabi'a",
            "en": "printer"
        },
        {
            "ar": "مستند",
            "transliteration": "mustanad",
            "en": "document"
        },
        {
            "ar": "قاعة اجتماعات",
            "transliteration": "qa'at ijtima'at",
            "en": "meeting room"
        },
        {
            "ar": "مكتب",
            "transliteration": "maktab",
            "en": "office"
        },
        {
            "ar": "بطاقة عمل",
            "transliteration": "bitaqat 'amal",
            "en": "business card"
        }
    ]
}

# Day 24: Business Etiquette
day24_phrases = {
    "Meeting Etiquette": [
        {
            "ar": "في الموعد",
            "transliteration": "fil-maw'id",
            "en": "on time"
        },
        {
            "ar": "تقديم النفس",
            "transliteration": "taqdim an-nafs",
            "en": "self-introduction"
        },
        {
            "ar": "مصافحة",
            "transliteration": "musafaha",
            "en": "handshake"
        },
        {
            "ar": "تبادل بطاقات العمل",
            "transliteration": "tabadol bitaqat al-'amal",
            "en": "exchange business cards"
        },
        {
            "ar": "احترام",
            "transliteration": "ihtiram",
            "en": "respect"
        }
    ],
    "Business Phrases": [
        {
            "ar": "تشرفت بلقائك",
            "transliteration": "tasharraftu biliqa'ik",
            "en": "It's an honor to meet you"
        },
        {
            "ar": "أرجو أن نتعاون",
            "transliteration": "arju an nata'awan",
            "en": "I hope we can cooperate"
        },
        {
            "ar": "نتمنى تعاوناً مثمراً",
            "transliteration": "natamanna ta'awunan muthmiran",
            "en": "We hope for fruitful cooperation"
        },
        {
            "ar": "أتطلع إلى لقائك مرة أخرى",
            "transliteration": "atattala' ila liqa'ik marra ukhra",
            "en": "Looking forward to seeing you again"
        },
        {
            "ar": "عذراً على الإزعاج",
            "transliteration": "'udhran 'ala al-iz'aj",
            "en": "Sorry to disturb you"
        }
    ]
}

# Day 25: Remote Work
day25_phrases = {
    "Remote Work Terms": [
        {
            "ar": "العمل عن بعد",
            "transliteration": "al-'amal 'an bu'd",
            "en": "remote work"
        },
        {
            "ar": "العمل من المنزل",
            "transliteration": "al-'amal min al-manzil",
            "en": "work from home"
        },
        {
            "ar": "ساعات عمل مرنة",
            "transliteration": "sa'at 'amal marina",
            "en": "flexible working hours"
        },
        {
            "ar": "اجتماع عبر الفيديو",
            "transliteration": "ijtima' 'abr al-fidyu",
            "en": "video conference"
        },
        {
            "ar": "اتصال بالإنترنت",
            "transliteration": "ittisal bil-internet",
            "en": "internet connection"
        }
    ],
    "Remote Work Phrases": [
        {
            "ar": "الميكروفون لا يعمل",
            "transliteration": "al-mikrofon la ya'mal",
            "en": "The microphone is not working"
        },
        {
            "ar": "هل تسمعني؟",
            "transliteration": "hal tasma'uni?",
            "en": "Can you hear me?"
        },
        {
            "ar": "الإنترنت غير مستقر",
            "transliteration": "al-internet ghayr mustaqir",
            "en": "The internet is not stable"
        },
        {
            "ar": "هل يمكننا أن نبدأ؟",
            "transliteration": "hal yumkinuna an nabda'?",
            "en": "Can we start?"
        },
        {
            "ar": "الرجاء مشاركة شاشتك",
            "transliteration": "ar-raja' musharakat shashatik",
            "en": "Please share your screen"
        }
    ]
}

# Day 26: Online Meetings
day26_phrases = {
    "Meeting Vocabulary": [
        {
            "ar": "جدول الأعمال",
            "transliteration": "jadwal al-a'mal",
            "en": "agenda"
        },
        {
            "ar": "محضر الاجتماع",
            "transliteration": "mahdar al-ijtima'",
            "en": "meeting minutes"
        },
        {
            "ar": "مناقشة",
            "transliteration": "munaqasha",
            "en": "discussion"
        },
        {
            "ar": "قرار",
            "transliteration": "qarar",
            "en": "decision"
        },
        {
            "ar": "مشارك",
            "transliteration": "musharik",
            "en": "participant"
        },
        {
            "ar": "مدير الجلسة",
            "transliteration": "mudir al-jalsa",
            "en": "host/moderator"
        }
    ],
    "Meeting Phrases": [
        {
            "ar": "دعونا نبدأ",
            "transliteration": "da'una nabda'",
            "en": "Let's begin"
        },
        {
            "ar": "هل هناك أي أسئلة؟",
            "transliteration": "hal hunaka ayy as'ila?",
            "en": "Are there any questions?"
        },
        {
            "ar": "لدي سؤال",
            "transliteration": "ladayya su'al",
            "en": "I have a question"
        },
        {
            "ar": "أنا موافق",
            "transliteration": "ana muwafiq",
            "en": "I agree"
        },
        {
            "ar": "أنا غير موافق",
            "transliteration": "ana ghayr muwafiq",
            "en": "I disagree"
        },
        {
            "ar": "متى الاجتماع القادم؟",
            "transliteration": "mata al-ijtima' al-qadim?",
            "en": "When is the next meeting?"
        }
    ]
}

# Day 27: Email Communication
day27_phrases = {
    "Email Vocabulary": [
        {
            "ar": "بريد إلكتروني",
            "transliteration": "barid elektroniy",
            "en": "email"
        },
        {
            "ar": "المستلم",
            "transliteration": "al-mustalim",
            "en": "recipient"
        },
        {
            "ar": "المرسل",
            "transliteration": "al-mursil",
            "en": "sender"
        },
        {
            "ar": "الموضوع",
            "transliteration": "al-mawdu'",
            "en": "subject"
        },
        {
            "ar": "مرفق",
            "transliteration": "murfaq",
            "en": "attachment"
        },
        {
            "ar": "نسخة كربونية",
            "transliteration": "nuskha karbuniyya",
            "en": "CC (carbon copy)"
        }
    ],
    "Email Phrases": [
        {
            "ar": "السيد/السيدة المحترم/ة",
            "transliteration": "as-sayyid/as-sayyida al-muhtaram/a",
            "en": "Dear Sir/Madam"
        },
        {
            "ar": "شكراً على رسالتك",
            "transliteration": "shukran 'ala risalatik",
            "en": "Thank you for your email"
        },
        {
            "ar": "يرجى الاطلاع على المرفق",
            "transliteration": "yurja al-ittila' 'ala al-murfaq",
            "en": "Please check the attachment"
        },
        {
            "ar": "في انتظار ردك",
            "transliteration": "fi intidhar raddik",
            "en": "Looking forward to your reply"
        },
        {
            "ar": "مع خالص التحية",
            "transliteration": "ma'a khalis at-tahiyya",
            "en": "Sincerely"
        },
        {
            "ar": "تحياتي",
            "transliteration": "tahiyyati",
            "en": "Regards"
        }
    ]
}

# Day 28: Presentations
day28_phrases = {
    "Presentation Vocabulary": [
        {
            "ar": "عرض تقديمي",
            "transliteration": "'ard taqdimi",
            "en": "presentation"
        },
        {
            "ar": "شرائح",
            "transliteration": "shara'ih",
            "en": "slides"
        },
        {
            "ar": "رسم بياني",
            "transliteration": "rasm bayani",
            "en": "chart"
        },
        {
            "ar": "بيانات",
            "transliteration": "bayanat",
            "en": "data"
        },
        {
            "ar": "خاتمة",
            "transliteration": "khatima",
            "en": "conclusion"
        },
        {
            "ar": "جلسة الأسئلة والأجوبة",
            "transliteration": "jalsat al-as'ila wal-ajwiba",
            "en": "Q&A session"
        }
    ],
    "Presentation Phrases": [
        {
            "ar": "سأتحدث اليوم عن...",
            "transliteration": "sa'atahadath al-yawm 'an...",
            "en": "Today I will talk about..."
        },
        {
            "ar": "أولاً",
            "transliteration": "awwalan",
            "en": "firstly"
        },
        {
            "ar": "ثانياً",
            "transliteration": "thaniyan",
            "en": "secondly"
        },
        {
            "ar": "أخيراً",
            "transliteration": "akhiran",
            "en": "finally"
        },
        {
            "ar": "للتلخيص",
            "transliteration": "lit-talkhis",
            "en": "to summarize"
        },
        {
            "ar": "هل لديكم أي أسئلة؟",
            "transliteration": "hal ladaykum ayy as'ila?",
            "en": "Are there any questions?"
        }
    ]
}

# Day 29: Technical Phrases
day29_phrases = {
    "Technical Vocabulary": [
        {
            "ar": "برمجيات",
            "transliteration": "barmajiyyat",
            "en": "software"
        },
        {
            "ar": "أجهزة",
            "transliteration": "ajhiza",
            "en": "hardware"
        },
        {
            "ar": "برنامج",
            "transliteration": "barnamaj",
            "en": "program"
        },
        {
            "ar": "قاعدة بيانات",
            "transliteration": "qa'idat bayanat",
            "en": "database"
        },
        {
            "ar": "شبكة",
            "transliteration": "shabaka",
            "en": "network"
        },
        {
            "ar": "الحوسبة السحابية",
            "transliteration": "al-hawsaba as-sahabiyya",
            "en": "cloud computing"
        },
        {
            "ar": "الذكاء الاصطناعي",
            "transliteration": "adh-dhaka' al-istina'i",
            "en": "artificial intelligence"
        }
    ],
    "Technical Phrases": [
        {
            "ar": "النظام تعطل",
            "transliteration": "an-nidham ta'attal",
            "en": "The system crashed"
        },
        {
            "ar": "يحتاج إلى تحديث",
            "transliteration": "yahtaj ila tahdith",
            "en": "Need to update"
        },
        {
            "ar": "نسخ احتياطي للبيانات",
            "transliteration": "naskh ihtiyati lil-bayanat",
            "en": "Backup data"
        },
        {
            "ar": "إعادة تشغيل الحاسوب",
            "transliteration": "i'adat tashghil al-hasub",
            "en": "Restart the computer"
        },
        {
            "ar": "تنزيل الملفات",
            "transliteration": "tanzil al-malaffat",
            "en": "Download files"
        },
        {
            "ar": "رفع الملفات",
            "transliteration": "raf' al-malaffat",
            "en": "Upload files"
        }
    ]
}

# Day 30: Business Negotiations
day30_phrases = {
    "Negotiation Terms": [
        {
            "ar": "مفاوضات",
            "transliteration": "mufawadat",
            "en": "negotiation"
        },
        {
            "ar": "عقد",
            "transliteration": "'aqd",
            "en": "contract"
        },
        {
            "ar": "شروط",
            "transliteration": "shurut",
            "en": "terms"
        },
        {
            "ar": "اتفاقية",
            "transliteration": "ittifaqiyya",
            "en": "agreement"
        },
        {
            "ar": "سعر",
            "transliteration": "si'r",
            "en": "price"
        },
        {
            "ar": "صفقة",
            "transliteration": "safqa",
            "en": "deal"
        }
    ],
    "Negotiation Phrases": [
        {
            "ar": "نود مناقشة الشروط",
            "transliteration": "nawaddu munaqashat ash-shurut",
            "en": "We would like to discuss the terms"
        },
        {
            "ar": "هل يمكن تخفيض السعر؟",
            "transliteration": "hal yumkin takhfid as-si'r?",
            "en": "Can the price be reduced?"
        },
        {
            "ar": "نحتاج وقتاً للدراسة",
            "transliteration": "nahtaj waqtan lid-dirasa",
            "en": "We need time to study"
        },
        {
            "ar": "نقبل العرض",
            "transliteration": "naqbal al-'ard",
            "en": "We accept the offer"
        },
        {
            "ar": "نرفض العرض",
            "transliteration": "narfud al-'ard",
            "en": "We decline the offer"
        }
    ]
}

# Dictionary mapping day numbers to phrase dictionaries
all_phrases = {
    23: day23_phrases,
    24: day24_phrases,
    25: day25_phrases,
    26: day26_phrases,
    27: day27_phrases,
    28: day28_phrases,
    29: day29_phrases,
    30: day30_phrases
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
    parser.add_argument("--day", "-d", type=int, choices=[23, 24, 25, 26, 27, 28, 29, 30], default=None,
                        help="Day number to generate (23-30). If not specified, generates all days.")
    parser.add_argument("--text-only", "-t", action="store_true",
                        help="Generate only text files (no audio)")
    parser.add_argument("--voice", "-v", type=str,
                        help="Voice to use for audio generation")
    parser.add_argument("--language", "-l", type=str, choices=["ar", "en", "both"], default="both",
                        help="Language to generate audio for (ar=Arabic, en=English, both=Both languages)")
    args = parser.parse_args()
    
    # Determine which days to process
    days_to_process = [args.day] if args.day else range(23, 31)
    
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
    print("  - Generate text files only: python arabic_phrases_days_23_30.py --text-only")
    print("  - Generate files for just Day 23: python arabic_phrases_days_23_30.py --day 23")
    print("  - Generate Arabic audio only: python arabic_phrases_days_23_30.py --language ar")
    print("  - Generate English audio only: python arabic_phrases_days_23_30.py --language en")
    print("  - Generate with different voice: python arabic_phrases_days_23_30.py --voice ar-EG-SalmaNeural")
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