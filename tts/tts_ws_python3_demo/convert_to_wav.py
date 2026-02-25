# -*- coding: utf-8 -*-
# 将PCM转换为WAV文件（添加WAV头）

import wave
import os

pcm_file = 'demo.pcm'
wav_file = 'test_voice.wav'

# 音频参数
sample_rate = 16000  # 采样率
channels = 1         # 单声道
bit_depth = 16       # 16位

with open(pcm_file, 'rb') as pcm:
    pcm_data = pcm.read()

with wave.open(wav_file, 'wb') as wav:
    wav.setnchannels(channels)
    wav.setsampwidth(bit_depth // 8)
    wav.setframerate(sample_rate)
    wav.writeframes(pcm_data)

print(f"转换完成: {wav_file}")
print(f"文件大小: {os.path.getsize(wav_file) / 1024:.1f} KB")
