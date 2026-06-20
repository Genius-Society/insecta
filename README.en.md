---
license: cc-by-nc-nd-4.0
viewer: false
---

# Insecta Image Dataset
[viewer](https://www.modelscope.cn/datasets/Genius-Society/insecta/dataPeview)

## Intro
The "Insecta Image Dataset" is a high-quality, professionally standardized image collection comprising comprehensively desensitized JPG pictures covering multiple orders, families, genera, and species within the class Insecta. Each image is annotated with dual authoritative labels—a verified Chinese common name and its corresponding Latin scientific name, reviewed by entomology experts. Strictly adhering to data compliance and privacy protection principles, all background and metadata have been removed to focus solely on the morphological features of the insects. This dataset is designed to serve as a solid, reliable, and readily usable benchmark resource for training and evaluating computer vision models in tasks such as image classification, object detection, and fine-grained recognition, as well as for interdisciplinary applications including biodiversity research, digital specimen repository development, and intelligent identification system implementation.

The Insecta Audio Dataset is an acoustic sample library designed for intelligent recognition and ecological monitoring, featuring high-definition field recordings of common insect species and genera from across China, encompassing various behavioral acoustic characteristics such as wing vibrations, courtship calls, and alarm sounds from singing insects including cicadas, crickets, katydids, and bees. Each audio clip is accompanied by metadata including insect images, Chinese common names, and Latin scientific names, supporting tasks such as voiceprint recognition, species identification, behavioral analysis, environmental acoustic monitoring, and cross-modal joint retrieval. It is applicable to mobile insect sound identification application development, biodiversity acoustic research, and nature education scenarios, facilitating intelligent ecological cognition experiences of "identifying insects by sound and perceiving soundscapes."

The Insecta Video Dataset is a multimodal video library designed for intelligent recognition and ecological research, featuring high-definition field-captured footage of common insect species and genera from across China. Each video clip is annotated with both Chinese common names and Latin scientific names, supporting tasks such as object detection, behavioral analysis, fine-grained classification, and cross-modal retrieval. It is applicable to mobile insect identification application development, biodiversity monitoring, and science education scenarios, facilitating dynamic and intelligent insect cognition experiences.

## Supported classes
[List of insects with included images](https://kakamond-insects.ms.show/viewer.html)

## Environment
```bash
pip install datasets==3.6
```

## Usage
```python
from datasets import load_dataset

ds = load_dataset(
    "Genius-Society/insecta",
    name="default", # default / sound / video
    split="train",
    cache_dir="./__pycache__",
    trust_remote_code=True,
)
for i in ds:
    print(i)
```

## Maintenance
```bash
git clone git@hf.co:datasets/Genius-Society/insecta
cd insecta
```

## Mirror
<https://www.modelscope.cn/datasets/Genius-Society/insecta>