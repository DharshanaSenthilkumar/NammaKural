import re


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = text.lower().strip()

    # --------------------------------------------------------
    # Normalize common Tamil/Tanglish transaction words
    # --------------------------------------------------------

    replacements = {

        # Purchase / expense
        "வாங்கினேன்": " bought ",
        "வாங்கனேன்": " bought ",
        "வாங்கின": " bought ",
        "வாங்கினோம்": " bought ",
        "வாங்குனேன்": " bought ",
        "வாங்குனோம்": " bought ",

        "vanginen": " bought ",
        "vaanginen": " bought ",
        "vangunen": " bought ",
        "vaangunen": " bought ",

        # Sales / income
        "விற்றேன்": " sold ",
        "விற்றோம்": " sold ",
        "விற்றேன்": " sold ",

        "vitren": " sold ",
        "vittain": " sold ",

        # Rice variations
        "அரிசி": " rice ",
        "அருசி": " rice ",
        "அரசி": " rice ",
        "அயிரசி": " rice ",
        "அடிசி": " rice ",

        "arisi": " rice ",

        # Money words
        "ரூபாய்": " rupees ",
        "ரூபாய": " rupees ",
        "ரூபாய்க்கு": " rupees ",
        "ரூப்பாய்": " rupees ",
        "ரூப்பாய்க்கு": " rupees ",
        "ரூப்பியா": " rupees ",
        "ரூபியத்திற்கு": " rupees ",
        "ரூப்பியத்திற்கு": " rupees ",
        "ரூப்பிகள்க்கு": " rupees ",
        "ருப்பிஸ்க்குப்": " rupees ",
        "ருப்பிஸ்க்கு": " rupees ",
        "ரூபீஸ்": " rupees ",
        "ரூபீஸ்க்கு": " rupees ",

        "rupee": " rupees ",
        "rupees": " rupees ",
        "roobaikku": " rupees ",
        "roobakku": " rupees ",
        "rooba": " rupees "
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    # --------------------------------------------------------
    # Remove Tamil case endings from common money forms
    # --------------------------------------------------------

    text = re.sub(
        r'ருப்பிஸ\w*',
        ' rupees ',
        text
    )

    text = re.sub(
        r'ரூப்ப\w*',
        ' rupees ',
        text
    )

    text = re.sub(
        r'ரூப\w*',
        ' rupees ',
        text
    )

    # --------------------------------------------------------
    # Clean spaces
    # --------------------------------------------------------

    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    return text


# ============================================================
# PARSE TRANSACTION
# ============================================================

def parse_transaction(text):

    original_text = text

    normalized = normalize_text(text)

    # ========================================================
    # 1. TRANSACTION TYPE
    # ========================================================

    income_words = [
        "sold",
        "sale",
        "earned",
        "received",
        "income"
    ]

    expense_words = [
        "bought",
        "buy",
        "paid",
        "spent",
        "purchased"
    ]

    if any(word in normalized for word in income_words):

        transaction_type = "income"

    elif any(word in normalized for word in expense_words):

        transaction_type = "expense"

    else:

        transaction_type = "unknown"

    # ========================================================
    # 2. FIND ALL NUMBERS
    # ========================================================

    number_matches = list(
        re.finditer(
            r'\b\d+(?:\.\d+)?\b',
            normalized
        )
    )

    amount = None
    quantity = None
    unit = None

    # ========================================================
    # 3. DETECT QUANTITY + UNIT
    # ========================================================

    quantity_match = re.search(

        r'(\d+(?:\.\d+)?)\s*'
        r'(kg|kilogram|kilograms|'
        r'g|gram|grams|'
        r'litre|liter|litres|liters|'
        r'pieces|piece|pcs|'
        r'packet|packets|box|boxes)',

        normalized
    )

    if quantity_match:

        quantity = float(
            quantity_match.group(1)
        )

        unit = quantity_match.group(2)

    # ========================================================
    # 4. DETECT AMOUNT
    # ========================================================

    money_match = re.search(

        r'(\d+(?:\.\d+)?)\s*rupees',

        normalized
    )

    if money_match:

        amount = float(
            money_match.group(1)
        )

    # --------------------------------------------------------
    # FALLBACK:
    #
    # If Whisper didn't give us a recognizable money word,
    # use the number nearest the purchase/sale phrase.
    # --------------------------------------------------------

    if amount is None and number_matches:

        # If quantity exists, don't use quantity as amount
        if quantity_match:

            quantity_value = quantity_match.group(1)

            possible_numbers = [

                m for m in number_matches

                if m.group(0) != quantity_value
            ]

        else:

            possible_numbers = number_matches

        if possible_numbers:

            # Usually the remaining number is the amount
            amount = float(
                possible_numbers[-1].group(0)
            )

    # ========================================================
    # 5. FIND ITEM
    # ========================================================

    item = None

    # --------------------------------------------------------
    # Known business items
    # --------------------------------------------------------

    known_items = {

        "rice": "rice",
        "milk": "milk",
        "பால்": "milk",
        "பால்": "milk",

        "vegetables": "vegetables",
        "vegetable": "vegetables",
        "காய்கறி": "vegetables",

        "oil": "oil",
        "எண்ணெய்": "oil",

        "sugar": "sugar",
        "சர்க்கரை": "sugar",

        "flour": "flour",
        "மாவு": "flour",

        "tea": "tea",
        "தேநீர்": "tea"
    }

    # First check original text
    for word, standard_name in known_items.items():

        if word in text.lower():

            item = standard_name

            break

    # Then check normalized text
    if item is None:

        for word, standard_name in known_items.items():

            if word in normalized:

                item = standard_name

                break

    # ========================================================
    # 6. GENERIC ITEM EXTRACTION
    # ========================================================

    if item is None:

        # Find the part between amount and transaction verb
        if amount is not None:

            amount_match_for_item = re.search(
                str(int(amount)),
                normalized
            )

            if amount_match_for_item:

                start = (
                    amount_match_for_item.end()
                )

                remaining = normalized[start:]

                # Remove money word
                remaining = remaining.replace(
                    "rupees",
                    " "
                )

                # Remove transaction words
                for word in [
                    "bought",
                    "buy",
                    "paid",
                    "spent",
                    "purchased",
                    "sold"
                ]:

                    remaining = remaining.replace(
                        word,
                        " "
                    )

                remaining = re.sub(
                    r'\s+',
                    ' ',
                    remaining
                ).strip()

                if remaining:

                    words = remaining.split()

                    if words:

                        item = words[0]

    # ========================================================
    # 7. RETURN TRANSACTION
    # ========================================================

    return {

        "type": transaction_type,

        "item": item,

        "quantity": quantity,

        "unit": unit,

        "amount": amount,

        "text": original_text
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_cases = [

        "I bought rice for 250 rupees",

        "Today I bought 5 kg rice for 250 rupees",

        "இன்றைக்கு 250 rupeesக்கு அரசி வாங்கினேன்",

        "Innaiku 250 roobaikku arisi vanginen",

        "இம்மைக்கு 250 ரூப்பியத்திற்கு அடிசி வாங்கனேன்",

        "இன்னேக்கு 250 ரூப்பிகள்க்கு அயிரசி வாங்கனேன்",

        "இன்று 250 ருப்பிஸ்க்குப் பால் வாங்கனேன்"
    ]

    for text in test_cases:

        print("\n" + "=" * 60)

        print("INPUT:")

        print(text)

        print("\nPARSED:")

        print(parse_transaction(text))