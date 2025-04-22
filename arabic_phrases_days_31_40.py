import argparse
import os
import time
import asyncio
import edge_tts

# Define phrases by day and category

# Day 31: Arabic Proverbs and Sayings
day31_phrases = {
    "Common Proverbs": [
        {
            "ar": "العقل السليم في الجسم السليم",
            "transliteration": "al-'aql as-salim fil-jism as-salim",
            "en": "a sound mind in a sound body"
        },
        {
            "ar": "على قدر أهل العزم تأتي العزائم",
            "transliteration": "'ala qadr ahl al-'azm ta'ti al-'aza'im",
            "en": "achievements come according to one's determination"
        },
        {
            "ar": "الوقاية خير من العلاج",
            "transliteration": "al-wiqaya khayr min al-'ilaj",
            "en": "prevention is better than cure"
        },
        {
            "ar": "من جد وجد",
            "transliteration": "man jadda wajada",
            "en": "whoever strives shall succeed"
        },
        {
            "ar": "الصديق وقت الضيق",
            "transliteration": "as-sadiq waqt ad-diq",
            "en": "a friend in need is a friend indeed"
        },
        {
            "ar": "رب ضارة نافعة",
            "transliteration": "rubba darrah nafi'ah",
            "en": "sometimes harm brings benefit"
        }
    ],
    "Using Proverbs": [
        {
            "ar": "كما يقول المثل العربي",
            "transliteration": "kama yaqul al-mathal al-'arabi",
            "en": "as the Arabic proverb says"
        },
        {
            "ar": "هذا يذكرني بالمثل القائل",
            "transliteration": "hadha yudhakkiruni bil-mathal al-qa'il",
            "en": "this reminds me of the saying"
        },
        {
            "ar": "صدق من قال",
            "transliteration": "sadaqa man qal",
            "en": "true are the words of who said"
        },
        {
            "ar": "وكما قال أجدادنا",
            "transliteration": "wa kama qal ajdaduna",
            "en": "and as our ancestors said"
        }
    ]
}

# Day 32: Modern Arabic Expressions
day32_phrases = {
    "Internet Expressions": [
        {
            "ar": "يا سلام",
            "transliteration": "ya salam",
            "en": "wow/amazing"
        },
        {
            "ar": "تحياتي",
            "transliteration": "tahiyyati",
            "en": "regards (common in messages)"
        },
        {
            "ar": "برو",
            "transliteration": "bro",
            "en": "brother (borrowed from English)"
        },
        {
            "ar": "لول",
            "transliteration": "lol",
            "en": "LOL (laugh out loud)"
        },
        {
            "ar": "يعطيك العافية",
            "transliteration": "ya'tik al-'afiya",
            "en": "well done/thank you"
        },
        {
            "ar": "ما شاء الله",
            "transliteration": "ma sha' Allah",
            "en": "expression of admiration"
        }
    ],
    "Youth Expressions": [
        {
            "ar": "يا خرابي",
            "transliteration": "ya kharabi",
            "en": "oh my goodness"
        },
        {
            "ar": "على راسي",
            "transliteration": "'ala rasi",
            "en": "sure thing/with pleasure"
        },
        {
            "ar": "تمام التمام",
            "transliteration": "tamam at-tamam",
            "en": "perfect/absolutely"
        },
        {
            "ar": "ولا يهمك",
            "transliteration": "wala yhimmak",
            "en": "don't worry about it"
        },
        {
            "ar": "مية مية",
            "transliteration": "miyya miyya",
            "en": "perfect/100%"
        },
        {
            "ar": "يا ريت",
            "transliteration": "ya rayt",
            "en": "I wish"
        }
    ]
}

# Day 33: Formal Expressions
day33_phrases = {
    "Formal Greetings": [
        {
            "ar": "سعادة",
            "transliteration": "sa'adat",
            "en": "his/her excellency"
        },
        {
            "ar": "حضرات السادة الكرام",
            "transliteration": "hadarat as-sada al-kiram",
            "en": "dear honorable gentlemen"
        },
        {
            "ar": "نشكر لكم حسن تعاونكم",
            "transliteration": "nashkur lakum husn ta'awunikum",
            "en": "we thank you for your kind cooperation"
        },
        {
            "ar": "تشرفنا بمعرفتكم",
            "transliteration": "tasharrafna bima'rifatikum",
            "en": "honored to meet you"
        },
        {
            "ar": "مع فائق الاحترام",
            "transliteration": "ma'a fa'iq al-ihtiram",
            "en": "with utmost respect"
        }
    ],
    "Formal Phrases": [
        {
            "ar": "العبد لله",
            "transliteration": "al-'abd lillah",
            "en": "I (humble)"
        },
        {
            "ar": "حضرتك",
            "transliteration": "hadratak",
            "en": "you (formal)"
        },
        {
            "ar": "شركتنا المتواضعة",
            "transliteration": "sharikatuna al-mutawadi'a",
            "en": "our humble company"
        },
        {
            "ar": "شركتكم الموقرة",
            "transliteration": "sharikatukum al-muwaqqara",
            "en": "your esteemed company"
        },
        {
            "ar": "نتطلع إلى ردكم الكريم",
            "transliteration": "natattalla' ila raddikum al-karim",
            "en": "looking forward to your kind reply"
        },
        {
            "ar": "جزيل الشكر",
            "transliteration": "jazil ash-shukr",
            "en": "many thanks"
        }
    ]
}

# Day 34: Debate and Discussion
day34_phrases = {
    "Discussion Terms": [
        {
            "ar": "وجهة نظر",
            "transliteration": "wijhat nadhar",
            "en": "viewpoint"
        },
        {
            "ar": "حجة",
            "transliteration": "hujja",
            "en": "argument/point"
        },
        {
            "ar": "دليل",
            "transliteration": "dalil",
            "en": "evidence"
        },
        {
            "ar": "رد",
            "transliteration": "radd",
            "en": "refute/rebut"
        },
        {
            "ar": "مناظرة",
            "transliteration": "munadhara",
            "en": "debate"
        },
        {
            "ar": "موقف",
            "transliteration": "mawqif",
            "en": "stance/position"
        }
    ],
    "Discussion Phrases": [
        {
            "ar": "في رأيي",
            "transliteration": "fi ra'yi",
            "en": "in my opinion"
        },
        {
            "ar": "من واقع تجربتي",
            "transliteration": "min waqi' tajribati",
            "en": "from my experience"
        },
        {
            "ar": "لا أتفق معك لأن",
            "transliteration": "la attafiq ma'ak li'anna",
            "en": "I disagree because"
        },
        {
            "ar": "أود أن أضيف نقطة",
            "transliteration": "awaddu an udif nuqta",
            "en": "I'd like to add a point"
        },
        {
            "ar": "دعنا ننظر من زاوية أخرى",
            "transliteration": "da'na nandhur min zawiya ukhra",
            "en": "let's look from another angle"
        },
        {
            "ar": "للتلخيص",
            "transliteration": "lit-talkhis",
            "en": "to summarize"
        }
    ]
}

# Day 35: Storytelling
day35_phrases = {
    "Narrative Elements": [
        {
            "ar": "قصة",
            "transliteration": "qissa",
            "en": "story"
        },
        {
            "ar": "شخصية",
            "transliteration": "shakhsiyya",
            "en": "character"
        },
        {
            "ar": "حبكة",
            "transliteration": "habka",
            "en": "plot"
        },
        {
            "ar": "خلفية",
            "transliteration": "khalfiyya",
            "en": "background/setting"
        },
        {
            "ar": "موضوع",
            "transliteration": "mawdu'",
            "en": "theme"
        },
        {
            "ar": "نهاية",
            "transliteration": "nihaya",
            "en": "ending"
        }
    ],
    "Storytelling Phrases": [
        {
            "ar": "كان يا ما كان",
            "transliteration": "kan ya ma kan",
            "en": "once upon a time"
        },
        {
            "ar": "في يوم من الأيام",
            "transliteration": "fi yawm min al-ayyam",
            "en": "one day"
        },
        {
            "ar": "فجأة",
            "transliteration": "faj'atan",
            "en": "suddenly"
        },
        {
            "ar": "بعد ذلك",
            "transliteration": "ba'd dhalik",
            "en": "after that"
        },
        {
            "ar": "وأخيراً",
            "transliteration": "wa akhiran",
            "en": "finally"
        },
        {
            "ar": "العبرة من القصة",
            "transliteration": "al-'ibra min al-qissa",
            "en": "the moral of the story"
        }
    ]
}

# Day 36: Persuasive Speech
day36_phrases = {
    "Persuasion Techniques": [
        {
            "ar": "إقناع",
            "transliteration": "iqna'",
            "en": "persuade"
        },
        {
            "ar": "تأثير",
            "transliteration": "ta'thir",
            "en": "influence"
        },
        {
            "ar": "جذب",
            "transliteration": "jadhb",
            "en": "attract"
        },
        {
            "ar": "تأكيد",
            "transliteration": "ta'kid",
            "en": "emphasize"
        },
        {
            "ar": "اقتراح",
            "transliteration": "iqtirah",
            "en": "suggest"
        },
        {
            "ar": "توضيح",
            "transliteration": "tawdih",
            "en": "explain"
        }
    ],
    "Persuasive Phrases": [
        {
            "ar": "أقترح بشدة",
            "transliteration": "aqtarih bishidda",
            "en": "I strongly suggest"
        },
        {
            "ar": "بلا شك",
            "transliteration": "bila shakk",
            "en": "without a doubt"
        },
        {
            "ar": "أرجو أن تفكر في",
            "transliteration": "arju an tufakkir fi",
            "en": "please consider"
        },
        {
            "ar": "الأهم من ذلك",
            "transliteration": "al-ahamm min dhalik",
            "en": "most importantly"
        },
        {
            "ar": "كما يعلم الجميع",
            "transliteration": "kama ya'lam al-jami'",
            "en": "as everyone knows"
        },
        {
            "ar": "تثبت الحقائق",
            "transliteration": "tuthbit al-haqa'iq",
            "en": "facts prove that"
        }
    ]
}

# Day 37: Practice Dialogue - Restaurant
day37_phrases = {
    "Restaurant Dialogue 1": [
        {
            "ar": "النادل: أهلاً وسهلاً، كم شخص؟",
            "transliteration": "an-nadil: ahlan wa sahlan, kam shakhs?",
            "en": "Waiter: Welcome, how many people?"
        },
        {
            "ar": "الزبون: شخصان، من فضلك",
            "transliteration": "az-zabun: shakhsan, min fadlik",
            "en": "Customer: Two people, please"
        },
        {
            "ar": "النادل: تفضلوا معي",
            "transliteration": "an-nadil: tafaddalu ma'i",
            "en": "Waiter: Please follow me"
        },
        {
            "ar": "الزبون: هل لديكم قائمة الطعام؟",
            "transliteration": "az-zabun: hal ladaykum qa'imat at-ta'am?",
            "en": "Customer: Do you have a menu?"
        },
        {
            "ar": "النادل: تفضل، خذ وقتك",
            "transliteration": "an-nadil: tafaddal, khudh waqtak",
            "en": "Waiter: Here you are, take your time"
        }
    ],
    "Restaurant Dialogue 2": [
        {
            "ar": "الزبون: أريد أن أطلب",
            "transliteration": "az-zabun: urid an atlub",
            "en": "Customer: I'd like to order"
        },
        {
            "ar": "النادل: ماذا تحب أن تطلب؟",
            "transliteration": "an-nadil: madha tuhibb an tatlub?",
            "en": "Waiter: What would you like to order?"
        },
        {
            "ar": "الزبون: أريد شاورما دجاج وسلطة",
            "transliteration": "az-zabun: urid shawarma dajaj wa salata",
            "en": "Customer: I want a chicken shawarma and salad"
        },
        {
            "ar": "النادل: حسناً، هل تريد شيئاً آخر؟",
            "transliteration": "an-nadil: hasanan, hal turid shay'an akhar?",
            "en": "Waiter: OK, anything else?"
        },
        {
            "ar": "الزبون: نعم، كوب عصير برتقال",
            "transliteration": "az-zabun: na'am, kub 'asir burtuqal",
            "en": "Customer: Yes, a glass of orange juice"
        }
    ]
}

# Day 38: Practice Dialogue - Shopping
day38_phrases = {
    "Shopping Dialogue 1": [
        {
            "ar": "الزبون: كم سعر هذا القميص؟",
            "transliteration": "az-zabun: kam si'r hadha al-qamis?",
            "en": "Customer: How much is this shirt?"
        },
        {
            "ar": "البائع: مئتان درهم",
            "transliteration": "al-ba'i': mi'atan dirham",
            "en": "Seller: 200 dirhams"
        },
        {
            "ar": "الزبون: غالي جداً، هل يمكن تخفيض السعر؟",
            "transliteration": "az-zabun: ghali jiddan, hal yumkin takhfid as-si'r?",
            "en": "Customer: That's too expensive. Can you reduce the price?"
        },
        {
            "ar": "البائع: حسناً، مئة وثمانون درهم",
            "transliteration": "al-ba'i': hasanan, mi'a wa thamanun dirham",
            "en": "Seller: OK, 180 dirhams"
        },
        {
            "ar": "الزبون: حسناً، سآخذه",
            "transliteration": "az-zabun: hasanan, sa'akhudhuhu",
            "en": "Customer: OK, I'll take it"
        }
    ],
    "Shopping Dialogue 2": [
        {
            "ar": "الزبون: أين غرفة القياس؟",
            "transliteration": "az-zabun: ayna ghurfat al-qiyas?",
            "en": "Customer: Where is the fitting room?"
        },
        {
            "ar": "البائع: هناك، على اليمين",
            "transliteration": "al-ba'i': hunak, 'ala al-yamin",
            "en": "Seller: There, on the right"
        },
        {
            "ar": "الزبون: هل لديكم مقاس أكبر؟",
            "transliteration": "az-zabun: hal ladaykum maqas akbar?",
            "en": "Customer: Do you have a larger size?"
        },
        {
            "ar": "البائع: دعني أتحقق. نعم، هذا مقاس XL",
            "transliteration": "al-ba'i': da'ni atahaqqaq. na'am, hadha maqas XL",
            "en": "Seller: Let me check. Yes, here's size XL"
        },
        {
            "ar": "الزبون: شكراً، سأجربه",
            "transliteration": "az-zabun: shukran, sa'ujarribuh",
            "en": "Customer: Thanks, I'll try it on"
        }
    ]
}

# Day 39: Practice Dialogue - Business Meeting
day39_phrases = {
    "Business Meeting Dialogue 1": [
        {
            "ar": "السيد أحمد: صباح الخير، شكراً لحضوركم اجتماع اليوم",
            "transliteration": "as-sayyid Ahmad: sabah al-khayr, shukran li-hudurikum ijtima' al-yawm",
            "en": "Mr. Ahmad: Good morning, thank you for attending today's meeting"
        },
        {
            "ar": "السيدة منى: ما موضوع النقاش اليوم؟",
            "transliteration": "as-sayyida Muna: ma mawdu' an-niqash al-yawm?",
            "en": "Ms. Muna: What are we discussing today?"
        },
        {
            "ar": "السيد أحمد: سنناقش تقدم المشروع الجديد",
            "transliteration": "as-sayyid Ahmad: sanunaaqish taqaddum al-mashru' al-jadid",
            "en": "Mr. Ahmad: We'll discuss the progress of the new project"
        },
        {
            "ar": "السيد محمد: لقد جهزت التقرير",
            "transliteration": "as-sayyid Muhammad: laqad jahhaztu at-taqrir",
            "en": "Mr. Muhammad: I have prepared the report"
        },
        {
            "ar": "السيد أحمد: ممتاز، تفضل بالبدء",
            "transliteration": "as-sayyid Ahmad: mumtaz, tafaddal bil-bad'",
            "en": "Mr. Ahmad: Excellent, please begin"
        }
    ],
    "Business Meeting Dialogue 2": [
        {
            "ar": "السيد محمد: حسب البيانات، ارتفعت مبيعاتنا بنسبة ٢٠٪",
            "transliteration": "as-sayyid Muhammad: hasab al-bayanat, irtafa'at mabi'atuna bi-nisbat 20%",
            "en": "Mr. Muhammad: According to the data, our sales have increased by 20%"
        },
        {
            "ar": "السيدة منى: هذا خبر جيد، لكن التكاليف ارتفعت أيضاً",
            "transliteration": "as-sayyida Muna: hadha khabar jayyid, lakin at-takalif irtafa'at aydan",
            "en": "Ms. Muna: That's good news, but costs have also increased"
        },
        {
            "ar": "السيد أحمد: نحتاج إلى إيجاد طرق لخفض التكاليف",
            "transliteration": "as-sayyid Ahmad: nahtaj ila ijad turuq li-khafd at-takalif",
            "en": "Mr. Ahmad: We need to find ways to reduce costs"
        },
        {
            "ar": "السيد محمد: لدي بعض المقترحات",
            "transliteration": "as-sayyid Muhammad: ladayya ba'd al-muqtarahat",
            "en": "Mr. Muhammad: I have some suggestions"
        },
        {
            "ar": "السيد أحمد: تفضل",
            "transliteration": "as-sayyid Ahmad: tafaddal",
            "en": "Mr. Ahmad: Go ahead"
        }
    ]
}

# Day 40: Practice Dialogue - Travel
day40_phrases = {
    "Travel Dialogue 1": [
        {
            "ar": "السائح: عفواً، كيف أصل إلى برج خليفة؟",
            "transliteration": "as-sa'ih: 'afwan, kayfa asil ila burj khalifa?",
            "en": "Tourist: Excuse me, how do I get to Burj Khalifa?"
        },
        {
            "ar": "المواطن: يمكنك استخدام المترو إلى محطة برج خليفة/دبي مول",
            "transliteration": "al-muwatin: yumkinuk istikhdam al-metro ila mahattat burj khalifa/dubai mall",
            "en": "Local: You can take the metro to Burj Khalifa/Dubai Mall station"
        },
        {
            "ar": "السائح: كم من الوقت يستغرق؟",
            "transliteration": "as-sa'ih: kam min al-waqt yastaghrik?",
            "en": "Tourist: How long does it take?"
        },
        {
            "ar": "المواطن: حوالي عشرين دقيقة",
            "transliteration": "al-muwatin: hawali 'ishrin daqiqa",
            "en": "Local: About twenty minutes"
        },
        {
            "ar": "السائح: شكراً جزيلاً على المساعدة",
            "transliteration": "as-sa'ih: shukran jazilan 'ala al-musa'ada",
            "en": "Tourist: Thank you very much for your help"
        }
    ],
    "Travel Dialogue 2": [
        {
            "ar": "السائح: متى يغلق المتحف؟",
            "transliteration": "as-sa'ih: mata yughlik al-mathaf?",
            "en": "Tourist: What time does the museum close?"
        },
        {
            "ar": "الموظف: نغلق في الساعة الثامنة مساءً",
            "transliteration": "al-muwadhdhaf: nughlik fi as-sa'a ath-thamina masa'an",
            "en": "Staff: We close at 8 PM"
        },
        {
            "ar": "السائح: كم رسوم الدخول؟",
            "transliteration": "as-sa'ih: kam rusum ad-dukhul?",
            "en": "Tourist: How much is the admission fee?"
        },
        {
            "ar": "الموظف: خمسون درهماً للكبار، وللطلاب النصف",
            "transliteration": "al-muwadhdhaf: khamsun dirhaman lil-kibar, wa lit-tullab an-nisf",
            "en": "Staff: 50 dirhams for adults, half price for students"
        },
        {
            "ar": "السائح: أنا طالب، هذه بطاقتي الجامعية",
            "transliteration": "as-sa'ih: ana talib, hadhihi bitaqati al-jami'iyya",
            "en": "Tourist: I'm a student, here's my university ID"
        }
    ]
}

# Dictionary mapping day numbers to phrase dictionaries
all_phrases = {
    31: day31_phrases,
    32: day32_phrases,
    33: day33_phrases,
    34: day34_phrases,
    35: day35_phrases,
    36: day36_phrases,
    37: day37_phrases,
    38: day38_phrases,
    39: day39_phrases,
    40: day40_phrases
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
    parser.add_argument("--day", "-d", type=int, choices=[31, 32, 33, 34, 35, 36, 37, 38, 39, 40], default=None,
                        help="Day number to generate (31-40). If not specified, generates all days.")
    parser.add_argument("--text-only", "-t", action="store_true",
                        help="Generate only text files (no audio)")
    parser.add_argument("--voice", "-v", type=str,
                        help="Voice to use for audio generation")
    parser.add_argument("--language", "-l", type=str, choices=["ar", "en", "both"], default="both",
                        help="Language to generate audio for (ar=Arabic, en=English, both=Both languages)")
    args = parser.parse_args()
    
    # Determine which days to process
    days_to_process = [args.day] if args.day else range(31, 41)
    
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
    print("  - Generate text files only: python arabic_phrases_days_31_40.py --text-only")
    print("  - Generate files for just Day 31: python arabic_phrases_days_31_40.py --day 31")
    print("  - Generate Arabic audio only: python arabic_phrases_days_31_40.py --language ar")
    print("  - Generate English audio only: python arabic_phrases_days_31_40.py --language en")
    print("  - Generate with different voice: python arabic_phrases_days_31_40.py --voice ar-EG-SalmaNeural")
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