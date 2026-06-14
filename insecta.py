import os
import random
import shutil
import datasets
import subprocess

_HOME = f"https://www.modelscope.cn/datasets/Genius-Society/{os.path.basename(__file__)[:-3]}"

_URL = "https://master.dl.sourceforge.net/project/git-large-file-storage.mirror/v3.7.1/git-lfs-linux-amd64-v3.7.1.tar.gz"


class insecta(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.Value("string"),
                    "latin": datasets.Value("string"),
                }
            ),
            supervised_keys=("image", "latin"),
            license="CC-BY-NC-ND",
            version="0.0.1",
            homepage=_HOME,
        )

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

    def _clone_repo(self, repo_dir: str, repo_url: str = f"{_HOME}.git"):
        try:
            shutil.rmtree(repo_dir, ignore_errors=True)
            os.makedirs(repo_dir)
            subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
            return f"{repo_dir}/已鉴定"

        except Exception as e:
            print(f"{e}, retrying...")
            self._clone_repo(repo_dir)

    def _split_generators(self, dl_manager):
        dataset = []
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
