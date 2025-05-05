def analisar_rosto(imagem_bytes):
    from PIL import Image
    import random
    img = Image.open(imagem_bytes)
    return random.choice(["feliz", "triste"])
