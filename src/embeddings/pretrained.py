import cv2
import insightface


class FaceEmbeddings:
  def __init__(self, name="buffalo_s"):
    self.model = insightface.app.FaceAnalysis(
      name=name,
      providers=['CPUExecutionProvider'],
      allowed_modules=["detection", "recognition"]
    )
    self.model.prepare(ctx_id=0)

  def get_embedding(self, path : str):
    img = cv2.imread(path)
    if img is None:
      raise ValueError(f"No image found at {path}!")
    else:
      #img = cv2.resize(img, (178, 218)) # Resize the image to the required dimensions
      faces = self.model.get(img)
      if not faces:
        # No faces detected in the image
        return -1
      elif len(faces) > 1:
        # Multiple faces detected in the image - only one face is allowed
        return -2
      else:
        # Return the embedding of the detected face
        return faces[0].normed_embedding