import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
import matplotlib.pyplot as plt

# 이미지 로드 및 전처리 함수
def load_and_process_image(path):
    img = keras_image.load_img(path, target_size=(512, 512))
    img = keras_image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.vgg19.preprocess_input(img)
    return img

# 이미지 디스플레이 함수
def display_image(img, title=None):
    img = img.squeeze()  # 배치 차원 제거
    img = img.astype('uint8')
    plt.imshow(img)
    if title:
        plt.title(title)
    plt.axis('off')
    plt.show()

# 스타일 전이 모델 로드
def load_model():
    vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
    vgg.trainable = False

    # 사용하려는 레이어 선택
    content_layers = ['block5_conv2']  # 내용 이미지에서 사용
    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']  # 스타일 이미지에서 사용

    return vgg, content_layers, style_layers

# 스타일 전이 수행
def style_transfer(content_path, style_path, num_iterations=1000, content_weight=1e3, style_weight=1e-2):
    content_image = load_and_process_image(content_path)
    style_image = load_and_process_image(style_path)

    # 모델 및 레이어 정의
    vgg, content_layers, style_layers = load_model()
    outputs = [vgg.get_layer(name).output for name in (content_layers + style_layers)]
    model = models.Model(inputs=vgg.input, outputs=outputs)

    # 스타일 전이 입력 이미지
    generated_image = tf.Variable(tf.image.convert_image_dtype(content_image, dtype=tf.float32))

    # 손실 계산 함수 정의
    def compute_loss():
        model_outputs = model(generated_image)
        content_output = model_outputs[:len(content_layers)]
        style_output = model_outputs[len(content_layers):]

        # 내용 손실
        content_loss = tf.reduce_mean((content_output[0] - model(content_image)[0]) ** 2)

        # 스타일 손실
        style_loss = 0
        for style, generated in zip(style_output, style_output):
            style_loss += tf.reduce_mean((style - generated) ** 2)
        style_loss /= len(style_layers)

        return content_weight * content_loss + style_weight * style_loss

    # 옵티마이저 설정
    optimizer = tf.optimizers.Adam(learning_rate=0.02)

    # 최적화 루프
    for i in range(num_iterations):
        with tf.GradientTape() as tape:
            loss = compute_loss()
        gradients = tape.gradient(loss, generated_image)
        optimizer.apply_gradients([(gradients, generated_image)])
        if i % 100 == 0:
            print(f"Iteration {i}: loss={loss.numpy()}")
            display_image(generated_image.numpy(), title='Generated Image')

    return generated_image

# 사용 예시
content_image_path = './image/pk.png'  # 내용 이미지 경로
style_image_path = './image/cat.png'      # 스타일 이미지 경로
result = style_transfer(content_image_path, style_image_path)