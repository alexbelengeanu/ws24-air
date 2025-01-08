# ws24-air

# Dataset

* Download [CelebA dataset from Google Drive](https://drive.google.com/file/d/0B7EVK8r0v71pZjFTYXZWM3FlRnM/view?usp=drive_link&resourcekey=0-dYn9z10tMJOBAkviAcfdyQ)
* Extract the dataset into `./data`
* The final directory structure should look like this: `./data/img_align_celeba`
* To populate the local database, run `python3 -m utils.populate_vector_database` from the `root` directory

# API

* `pymilvus` does not support Windows, so you might want to use WSL if you don't have MacOS/Ubuntu - [check here](https://stackoverflow.com/a/79286565)
* To launch the API install the requirements and then write `python3 -m src.api` in the terminal
* You can use Swagger to get details about the endpoints by accessing http://localhost:5000/api/v1/docs after the API was launched