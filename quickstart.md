## 数据集: Genius-Society/insecta

```python
from modelscope.msdatasets import MsDataset

ds = MsDataset.load(
    "Genius-Society/insecta",
    subset_name="default",
    split="train",
    cache_dir="./__pycache__",
    trust_remote_code=True,
)
for i in ds:
    print(i)
```

### 打印结果示例
```txt
{'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1280x2773 at 0x1A9E10E2390>, 'label': '榆黄毛萤叶甲', 'latin': 'Pyrrhalta maculicollis'}
{'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1152x2048 at 0x1A9E10E2450>, 'label': '苍白优草螽', 'latin': 'Euconocephalus pallidus'}
...
{'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=4032x3024 at 0x1A9E10E2510>, 'label': '凹毛蚁', 'latin': 'Lasius emarginatus'}
```