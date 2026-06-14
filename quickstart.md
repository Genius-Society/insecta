## 数据集: Genius-Society/insecta

```python
from modelscope.msdatasets import MsDataset

ds = MsDataset.load(
    "Genius-Society/insecta",
    subset_name="default", # image / sound / video
    split="train",
    cache_dir="./__pycache__",
    trust_remote_code=True,
)
for i in ds:
    print(i)
```