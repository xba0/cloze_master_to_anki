import json
import os

# copied from the exported file, the template is based on cloze_master.anki.card
HEADER = """#separator:tab
#html:true
#notetype column:1
#deck column:2
#tags column:9
"""
# each card format: CardTemplate, CollectionName, pre, blank, post, translation, sound, difficulty
# ClozeMaster	ClozeMaster Indonesian::Fluent Fast	Tidak	masalah	.	It doesn't matter.	[sound:5b9c44eb-708e-40e7-b0b9-8d185e1fd387.mp3]	139.0

# replace with the template name in the exported file
CardTemplate = "ClozeMaster"


def escape_text(text: str):
    if text != "":
        return '"' + text.replace('"', '""') + '"'
    else:
        return " "


def split_cloze(text):
    """text: aaa {{bbb}} ccc"""
    pre, text = text.split("{{")
    blank, post = text.split("}}")
    return pre, blank, post


def generate_anki_card_set(collection_path, collection_name):
    with open(collection_path) as f:
        collection = json.load(f)["sents"]
    cards = []
    for cloze in collection:
        text, trans = cloze["text"], cloze["translation"]
        autio = cloze["ttsAudioUrl"]
        difficulty = cloze["difficulty"]

        try:
            pre, blank, post = split_cloze(text)
        except:
            print("error parsing: ", text)
            continue
        audio = autio.rsplit("/")[-1]

        card = "\t".join(
            [
                CardTemplate,
                collection_name,
                escape_text(pre),
                escape_text(blank),
                escape_text(post),
                escape_text(trans),
                "[sound:" + audio + "]",
                str(difficulty),
            ]
        )
        cards.append(card)
    return cards


def generate_anki_collections(out_file, cards):
    with open(out_file, "w") as f:
        print(HEADER, file=f)
        for card in cards:
            print(card, file=f)


if __name__ == "__main__":
    cards = []
    for dire in os.listdir("cm-en-zh"):
        base_name = "FastTrack" if dire[0] == "F" else "MostCommon"
        cards += generate_anki_card_set(
            "cm-en-zh/" + dire + "/all.json",
            "ClozeMasterChinese-English::" + base_name + "::" + dire,
        )
    generate_anki_collections("/mnt/c/Users/bao/Desktop/generated.txt", cards)
