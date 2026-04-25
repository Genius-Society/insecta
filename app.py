import cv2
import khandy
import numpy as np
import gradio as gr
from PIL import Image
from insectid import InsectDetector, InsectIdentifier
from utils import _L, MODEL_DIR, EN_US


def infer(filename: str):
    status = "Success"
    result = outxt = None
    try:
        if not filename:
            raise ValueError("请上传图片")

        detector = InsectDetector()
        identifier = InsectIdentifier()
        image = khandy.imread(filename)
        if image is None:
            raise ValueError("图片读取失败")

        if max(image.shape[:2]) > 1280:
            image = khandy.resize_image_long(image, 1280)

        image_for_draw = image.copy()
        image_height, image_width = image.shape[:2]
        boxes, confs, classes = detector.detect(image)
        text = _L("未知")
        for box, _, _ in zip(boxes, confs, classes):
            box = box.astype(np.int32)
            box_width = box[2] - box[0] + 1
            box_height = box[3] - box[1] + 1
            if box_width < 30 or box_height < 30:
                continue

            cropped = khandy.crop_or_pad(image, box[0], box[1], box[2], box[3])
            results = identifier.identify(cropped)
            print(results[0])
            prob = results[0]["probability"]
            if prob >= 0.10:
                text = (
                    "{}: {:.2f}%".format(
                        results[0]["latin_name"],
                        100.0 * results[0]["probability"],
                    )
                    if EN_US
                    else "{} {}: {:.2f}%".format(
                        results[0]["chinese_name"],
                        results[0]["latin_name"],
                        100.0 * results[0]["probability"],
                    )
                )

            position = [box[0] + 2, box[1] - 20]
            position[0] = min(max(position[0], 0), image_width)
            position[1] = min(max(position[1], 0), image_height)
            cv2.rectangle(
                image_for_draw,
                (box[0], box[1]),
                (box[2], box[3]),
                (0, 255, 0),
                2,
            )
            image_for_draw = khandy.draw_text(
                image_for_draw,
                text,
                position,
                font=None if EN_US else f"{MODEL_DIR}/simsun.ttc",
                font_size=15,
            )

        outxt = text.split(":")[0] if ":" in text else text
        result = Image.fromarray(image_for_draw[:, :, ::-1], mode="RGB")

    except Exception as e:
        status = f"{e}"

    return status, result, outxt


if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Interface(
            fn=infer,
            inputs=gr.Image(label=_L("上传昆虫照片"), type="filepath"),
            outputs=[
                gr.Textbox(label=_L("状态栏"), buttons=["copy"]),
                gr.Image(label=_L("识别结果"), buttons=["download", "fullscreen"]),
                gr.Textbox(label=_L("最可能的物种"), buttons=["copy"]),
            ],
            title=_L("图像文件格式支持 PNG, JPG, JPEG 和 BMP, 且文件大小不超过 10M"),
            examples=[
                f"{MODEL_DIR}/examples/butterfly.jpg",
                f"{MODEL_DIR}/examples/beetle.jpg",
            ],
            flagging_mode="never",
            cache_examples=False,
        )

        gr.HTML(
            """
            <iframe src="//player.bilibili.com/player.html?bvid=BV14krgYJE4B&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="100%" style="aspect-ratio: 16 / 9;"></iframe>
            """
        )

    demo.launch(css="#gradio-share-link-button-0 { display: none; }", ssr_mode=False)
