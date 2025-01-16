import json
import os
import ffmpeg
from typing import List, Dict, Any, Optional

# 対象のディレクトリのパスを指定
DIRECTORY_PATH = "/DIR/PATH"
OUTPUT_JSON = "metadata.json"

# 取得するファイルの拡張子を指定
SUPPORTED_EXTENSIONS = (".mp4", ".mkv", ".avi", ".mov", ".flv")


def list_files(directory_path: str) -> List[str]:
    """指定したディレクトリから指定した拡張子のファイル一覧を取得"""
    try:
        with os.scandir(directory_path) as entries:
            filtered_files = [
                entry.path
                for entry in entries
                if entry.is_file() and entry.name.lower().endswith(SUPPORTED_EXTENSIONS)
            ]

            # ファイル名でソートして返す
            return sorted(filtered_files, key=lambda x: os.path.basename(x).lower())

    except FileNotFoundError:
        print(f"ディレクトリ内にファイルがありません: {directory_path}")
    except PermissionError:
        print(f"アクセス権限がありません: {directory_path}")
    return []


def calculate_frame_rate(stream: Dict[str, Any]) -> Optional[float]:
    """動画のストリームからフレームレートを計算"""
    r_frame_rate = stream.get("r_frame_rate")
    if not r_frame_rate:
        return None
    try:
        numerator, denominator = map(int, r_frame_rate.split("/"))
        return numerator / denominator if denominator != 0 else None
    except (ValueError, ZeroDivisionError):
        return None


def format_duration(duration: Optional[float]) -> str:
    """再生時間を 時:分:秒 形式に整形"""
    if not duration:
        return "Unknown"
    total_seconds = int(duration)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}時間{minutes}分{seconds}秒"
    elif minutes > 0:
        return f"{minutes}分{seconds}秒"
    return f"{seconds}秒"


def extract_metadata(entry_file: str) -> Optional[Dict[str, Any]]:
    """動画ファイルからメタデータを抽出"""
    try:
        # ffmpegでファイルのメタデータを取得
        probe = ffmpeg.probe(entry_file)
        format_info = probe.get("format", {})
        streams = probe.get("streams", [])

        # 音声ストリームの有無を確認
        has_audio = any(stream["codec_type"] == "audio" for stream in streams)

        # フレームレートを動画ストリームから計算
        frame_rate = next(
            (
                calculate_frame_rate(stream)
                for stream in streams
                if stream.get("codec_type") == "video"
            ),
            None,
        )

        # 再生時間を取得（秒単位）
        try:
            duration = float(format_info.get("duration", 0.0))
        except (ValueError, TypeError):
            duration = None

        # メタデータを辞書で返す
        return {
            "file_name": os.path.basename(entry_file),
            "extension": os.path.splitext(entry_file)[1].lower(),
            "has_audio": has_audio,
            "frame_rate": frame_rate,
            "duration": format_duration(duration),
            "bit_rate": format_info.get("bit_rate", "Unknown"),
        }
    except ffmpeg.Error as e:
        print(f"ffmpegのエラーが発生しました {entry_file}: {e}")
    except Exception as e:
        print(f"予期しないエラーで失敗しました {entry_file}: {e}")
    return None


def get_metadata(directory_path: str) -> List[Dict[str, Any]]:
    """指定したディレクトリ内のすべてのファイルのメタデータを取得"""
    entry_files = list_files(directory_path)
    return [
        metadata
        for entry_file in entry_files
        if (metadata := extract_metadata(entry_file))
    ]


def save_to_json(file_path: str, data: List[Dict[str, Any]]) -> None:
    """メタデータをJSONファイルに保存"""
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"{file_path}を保存しました")
    except Exception as e:
        print(f"保存に失敗しました: {e}")


def main(directory_path: str, output_filename: str):
    """ディレクトリ内の動画ファイルからメタデータを取得して出力"""
    if not os.path.exists(directory_path):
        print("ディレクトリがありませんでした")
        return

    # メタデータの取得
    metadata_list = get_metadata(directory_path)

    # JSONファイルに保存
    save_to_json(output_filename, metadata_list)


if __name__ == "__main__":
    main(DIRECTORY_PATH, OUTPUT_JSON)
