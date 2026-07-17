import os
import time
import random
import shutil
import datasets
import requests
import subprocess
from PIL import Image
from tqdm import tqdm
from io import BytesIO

_HOME = f"https://www.modelscope.cn/datasets/Genius-Society/{os.path.basename(__file__)[:-3]}"

_URL = "https://master.dl.sourceforge.net/project/git-large-file-storage.mirror/v3.7.1/git-lfs-linux-amd64-v3.7.1.tar.gz"
# for sound
_ENDPOINT = "https://www.missevan.com"
# for video
_BVID = "BV14krgYJE4B"


class insecta(datasets.GeneratorBasedBuilder):
    def _chrome_ver(self):
        return requests.get(
            "https://www.modelscope.cn/models/Genius-Society/latest_mirrors/resolve/master/chrome/version"
        ).text.split(".")[0]

    def _header(self):
        return {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self._chrome_ver()}.0.0.0 Safari/537.36"
        }

    def _info(self):
        if self.config.name == "default":
            self.config.name = "image"

        if self.config.name == "image":
            features = {
                "image": datasets.Image(),
                "label": datasets.Value("string"),
                "latin": datasets.Value("string"),
            }

        elif self.config.name == "sound":
            features = {
                "audio": datasets.Value("string"),
                "image": datasets.Image(),
                "label": datasets.Value("string"),
                "latin": datasets.Value("string"),
            }

        elif self.config.name == "video":
            features = {
                "video": datasets.Value("string"),
                "image": datasets.Image(),
                "duration": datasets.Value("duration[s]"),
                "label": datasets.Value("string"),
                "latin": datasets.Value("string"),
            }

        else:
            raise NameError("Invalid subset name!")

        return datasets.DatasetInfo(
            features=datasets.Features(features),
            config_name=self.config.name,
            license="CC-BY-NC-ND",
            version="0.0.1",
            homepage=_HOME,
        )

    # for default
    def _git_lfs_installed(self):
        try:
            r = subprocess.run(
                ["git", "lfs", "version"],
                capture_output=True,
                text=True,
                shell=True,
            )
            return r.returncode == 0 and "git-lfs" in r.stdout

        except:
            return False

    def _download_and_extract(self, url: str):
        try:
            git_lfs_pkg = url.split("/")[-1]
            subprocess.run(["wget", "-O", f"./{git_lfs_pkg}", url], check=True)
            subprocess.run(["tar", "-xzf", git_lfs_pkg], check=True)
            ver = git_lfs_pkg.split("it-lfs-linux-amd64-v")[-1].split(".tar.g")[0]
            return f"./git-lfs-{ver}/git-lfs"

        except Exception as e:
            print(f"{e}, retrying...")
            return self._download_and_extract(url)

    def _fix_git_lfs(self, bin_dir="/usr/local/bin/"):
        if not self._git_lfs_installed():
            if "posix" == os.name:
                git_lfs = self._download_and_extract(_URL)
                if not os.path.exists(f"{bin_dir}git-lfs"):
                    subprocess.run(["chmod", "+x", git_lfs], check=True)
                    shutil.move(git_lfs, bin_dir)

            else:
                raise EnvironmentError("请安装 Git LFS!")

        subprocess.run(["git", "lfs", "install"], check=True)
        return f"{self._cache_downloaded_dir}/extracted/{os.path.basename(self._cache_dir)}"

    def _clone_repo(self, repo_dir: str, repo_url=f"{_HOME}.git"):
        try:
            shutil.rmtree(repo_dir, ignore_errors=True)
            os.makedirs(repo_dir, exist_ok=True)
            subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
            return f"{repo_dir}/已鉴定"

        except Exception as e:
            print(f"{e}, retrying...")
            return self._clone_repo(repo_dir)

    # for sound
    def _get_sounds(self, drama_id=73247, page_size=100):
        try:
            response = requests.get(
                f"{_ENDPOINT}/dramaapi/getdramaepisodedetails",
                params={"drama_id": drama_id, "p": 1, "page_size": page_size},
                headers=self._header(),
            )
            response.raise_for_status()
            return response.json()["info"]["Datas"]

        except Exception as e:
            print(f"{e}, retrying...")
            time.sleep(random.randint(3, 5))
            return self._get_sounds()

    def _dld_img(self, url: str):
        try:
            response = requests.get(url, headers=self._header())
            response.raise_for_status()
            return Image.open(BytesIO(response.content))

        except Exception as e:
            print(f"{e}, retrying...")
            return self._dld_img(url)

    # for video
    def _get_videos(self):
        try:
            response = requests.get(
                "https://api.bilibili.com/x/player/pagelist",
                params={"bvid": _BVID},
                headers=self._header(),
            )
            response.raise_for_status()
            return response.json()["data"]

        except Exception as e:
            print(f"{e}, retrying...")
            return self._get_videos()

    def _split_generators(self, dl_manager):
        dataset = []
        if self.config.name == "image":
            repo_dir = self._fix_git_lfs()
            data_dir = self._clone_repo(repo_dir)
            for fpath in dl_manager.iter_files([data_dir]):
                if fpath.lower().endswith(".jpg"):
                    dir_name: str = os.path.basename(os.path.dirname(fpath))
                    label, latin = dir_name.split(" ", 1)
                    dataset.append(
                        {
                            "image": fpath,
                            "label": label.strip(),
                            "latin": latin.strip(),
                        }
                    )

        elif self.config.name == "sound":
            files = self._get_sounds()
            for file in tqdm(files, desc="Parsing classes"):
                label, latin = str(file["soundstr"]).split(" ", 1)
                dataset.append(
                    {
                        "audio": f"{_ENDPOINT}/soundiframe/{file['id']}?type=small",
                        "image": self._dld_img(file["front_cover"]),
                        "label": label.strip(),
                        "latin": latin.strip(),
                    }
                )

        else:  # video
            files = self._get_videos()
            for file in tqdm(files, desc="Parsing classes"):
                label, latin = str(file["part"]).split(" ", 1)
                dataset.append(
                    {
                        "video": f"https://player.bilibili.com/player.html?bvid={_BVID}&p={file['page']}",
                        "image": self._dld_img(file["first_frame"]),
                        "duration": file["duration"],
                        "label": label.strip(),
                        "latin": latin.strip(),
                    }
                )

        random.shuffle(dataset)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"files": dataset},
            )
        ]

    def _generate_examples(self, files):
        for i, fpath in enumerate(files):
            yield i, fpath
