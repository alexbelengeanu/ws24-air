import os

class Dataset():
    img_folder_path: str 
    img_identity_map_path: str

    def __init__(self, img_folder_path: str, img_identity_map_path: str):
        self.img_folder_path = img_folder_path
        self.img_identity_map_path = img_identity_map_path
        
    def images_by_identity(self) -> dict[str, list[str]]:
        images_by_identity = {}

        with open(self.img_identity_map_path, mode="r") as file:
            lines = file.readlines()
            for line in lines:
                img_path, face_id = os.path.join(self.img_folder_path, line.split(" ")[0]), int(line.split(" ")[1].removesuffix("\n"))
                if face_id in images_by_identity:
                    images_by_identity[face_id].append(img_path)
                else:
                    images_by_identity[face_id] = list([img_path])

        return images_by_identity


        