import cv2
import insightface


class FaceEmbeddings:
  def __init__(self, name="buffalo_s"):
    self.model = insightface.app.FaceAnalysis(name=name,providers=['CPUExecutionProvider'], allowed_modules=["detection", "recognition"])
    self.model.prepare(ctx_id=0)

  def get_embedding(self, path : str):
    img = cv2.imread(path)
    if img is None:
      raise ValueError(f"No Image found at {path}!")
    #img_resize = cv2.resize(img, (112,112))
    try:
      embedding = self.model.get(img)[0]
    except:
      print("Hello World")
      embedding= [0] * 512
    return embedding.normed_embedding