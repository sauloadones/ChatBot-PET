import os
from PIL import Image

def converter_todas_para_jpg(pasta_origem="imagens", pasta_destino="imagens_convertidas"):
    os.makedirs(pasta_destino, exist_ok=True)

    for nome_arquivo in os.listdir(pasta_origem):
        if nome_arquivo.lower().endswith(".png"):
            caminho_original = os.path.join(pasta_origem, nome_arquivo)
            nome_base = os.path.splitext(nome_arquivo)[0]
            caminho_destino = os.path.join(pasta_destino, f"{nome_base}.jpg")

            try:
                with Image.open(caminho_original) as img:
                    img = img.convert("RGB")  # Remove canal alfa
                    img.thumbnail((1280, 1280))  # Reduz resolução se necessário
                    img.save(caminho_destino, format="JPEG", quality=85)
                    print(f"✅ {nome_arquivo} convertido com sucesso.")
            except Exception as e:
                print(f"❌ Erro ao processar {nome_arquivo}: {e}")


    

if __name__ == "__main__":
    converter_todas_para_jpg()