---
license: cc-by-nc-nd-4.0
viewer: false
---

# Insecta Image Dataset
The "Insecta Image Dataset" is a high-quality, professionally standardized image collection comprising comprehensively desensitized JPG pictures covering multiple orders, families, genera, and species within the class Insecta. Each image is annotated with dual authoritative labels—a verified Chinese common name and its corresponding Latin scientific name, reviewed by entomology experts. Strictly adhering to data compliance and privacy protection principles, all background and metadata have been removed to focus solely on the morphological features of the insects. This dataset is designed to serve as a solid, reliable, and readily usable benchmark resource for training and evaluating computer vision models in tasks such as image classification, object detection, and fine-grained recognition, as well as for interdisciplinary applications including biodiversity research, digital specimen repository development, and intelligent identification system implementation.

## Supported classes
[List of insects with included images](https://kakamond-insects.ms.show/viewer.html)

## Usage
```python
from datasets import load_dataset

ds = load_dataset(
    "Genius-Society/insecta",
    name="default",
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