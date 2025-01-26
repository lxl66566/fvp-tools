import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from bin_archiver import extract, pack


def process_audio_files(folder: Path, speed: float):
    """处理文件夹中的所有文件"""
    for ogg_file in folder.rglob("*"):
        output_file = ogg_file.parent / f"temp_{ogg_file.name}"

        # 使用 ffmpeg 加速音频但不改变音高
        cmd = [
            "ffmpeg",
            "-i",
            str(ogg_file),
            "-filter:a",
            f"atempo={speed}",
            "-vn",
            str(output_file),
            "-y",  # 覆盖已存在的文件
        ]

        try:
            print(f"处理 {ogg_file}...")
            subprocess.run(cmd, check=True, capture_output=True)
            # 替换原文件
            output_file.replace(ogg_file)
        except subprocess.CalledProcessError as e:
            print(f"处理 {ogg_file} 时出错: {e}")
            output_file.unlink(missing_ok=True)


if __name__ == "__main__":
    binary_path = Path("Z:/xx.bin")
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        extract(binary_path, temp_dir)
        process_audio_files(temp_dir, 2.0)
        pack(temp_dir, binary_path)
