import json

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
    return '"' + text.replace('"', '""') + '"'


def split_cloze(text):
    """text: aaa {{bbb}} ccc"""
    pre, text = text.split("{{")
    blank, post = text.split("}}")
    return pre, blank, post


def generate_anki_card_set(collection_path, output_path, collection_name):
    with open(collection_path) as f:
        collection = json.load(f)["sents"]
    with open(output_path, "w") as f:
        print(HEADER, file=f)
        for cloze in collection:
            text, trans = cloze["text"], cloze["translation"]
            autio = cloze["ttsAudioUrl"]
            difficulty = cloze["difficulty"]

            pre, blank, post = split_cloze(text)
            audio = autio.rsplit("/")[-1]

            print(
                CardTemplate,
                collection_name,
                escape_text(pre),
                escape_text(blank),
                escape_text(post),
                escape_text(trans),
                "[sound:" + audio + "]",
                difficulty,
                sep="\t",
                file=f,
            )


if __name__ == "__main__":
    generate_anki_card_set(
        "./Cm-Ind-MC100/all.json", "./cm_indonesian_100.txt", "collection_name"
    )
