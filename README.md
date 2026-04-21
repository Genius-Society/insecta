# 昆虫鉴别器 WebUI
[![auto-sync](https://github.com/Genius-Society/insecta/actions/workflows/auto-sync.yml/badge.svg)](https://github.com/Genius-Society/insecta/actions/workflows/auto-sync.yml)
[![license](https://img.shields.io/badge/license-CC--BY--NC--ND-98c610.svg)](./LICENSE)
[![hf](https://img.shields.io/badge/huggingface-insecta-ffd21e.svg)](https://huggingface.co/collections/Genius-Society/insecta)
[![ms](https://img.shields.io/badge/modelscope-insecta-624aff.svg)](https://www.modelscope.cn/collections/Genius-Society/kunchongtujian)

支持 2037 类 (可能是目, 科, 属或种等) 昆虫或其他节肢动物；拖拽含有昆虫的图片进网页，点击提交即可识别；系统会自动定位并识别图像中的虫子, 也支持识别手工选择的虫子区域；图像文件格式支持 PNG, JPG, JPEG 和 BMP, 且文件大小不超过 10M；支持三种图像上传方式: 图像 URL; 本地图像拖曳上传; 本地图像对话框上传；系统返回可能性最高的物种, 结果包括其中文名, 学名和可信度。

## 致谢
- <https://www.gradio.app>
- <https://github.com/quarrying/quarrying-insect-id>