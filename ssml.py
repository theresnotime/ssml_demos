def get_ssml(type: str, word: str, ipa: str, lang: str) -> str | bool:
    """Return the SSML for the given engine"""
    try:
        # TODO: Add voice selection support
        voice = "en-US-JennyNeural"
        if type == "basic":
            ssml_element = f'<speak"><lang xml:lang="{lang}"><phoneme alphabet="ipa" ph="{ipa}">{word}</phoneme></lang></speak>'
        elif type == "microsoft":
            ssml_element = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang}">
            <voice name="{voice}"><phoneme alphabet="ipa" ph="{ipa}">{word}</phoneme></voice>
            </speak>"""
        elif type == "larynx":
            ssml_element = f"""<?xml version="1.0"?>
            <speak version="1.1"
                xmlns="http://www.w3.org/2001/10/synthesis"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.w3.org/2001/10/synthesis
                    http://www.w3.org/TR/speech-synthesis11/synthesis.xsd"
                xml:lang="en-US">
                <lexicon xml:id="ipaInput" alphabet="ipa">
                    <lexeme>
                        <grapheme>{word}</grapheme>
                        <phoneme>{ipa}</phoneme>
                    </lexeme>
                </lexicon>
                <lookup ref="ipaInput">
                    <w>{word}</w>
                </lookup>
            </speak>"""
        else:
            raise Exception("type not recognized")
        return ssml_element

    except Exception as e:
        print(f"Error: {e}")
        exit(1)
