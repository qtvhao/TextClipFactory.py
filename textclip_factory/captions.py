from .text_clip_factory import TextClipFactory

params = {
    "text": "Hello, World!",
    "fontsize": 50,
    "font": "NotoMono-Regular",
    "color": "white"
}

text_clip = TextClipFactory.create_text_clip(params)
text_clip.show()
