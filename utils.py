import os

EN_US = os.getenv("LANG") != "zh_CN.UTF-8"

if EN_US:
    import huggingface_hub

    MODEL_DIR = huggingface_hub.snapshot_download(
        "Genius-Society/insecta",
        cache_dir="./__pycache__",
    )

else:
    import modelscope

    MODEL_DIR = modelscope.snapshot_download(
        "Genius-Society/insecta",
        cache_dir="./__pycache__",
    )

ZH2EN = {
    "上传昆虫照片": "Upload insect picture",
    "状态栏": "Status",
    "识别结果": "Recognition result",
    "最可能的物种": "Best match",
    "图像文件格式支持 PNG, JPG, JPEG 和 BMP, 且文件大小不超过 10M": "Image file format support PNG, JPG, JPEG and BMP, and the file size does not exceed 10M.",
    "未知": "Unknown",
}


def _L(zh_txt: str):
    return ZH2EN[zh_txt] if EN_US else zh_txt
